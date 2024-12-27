from strategy.anaistrategy import AnAIStrategy
import pandas as  pd
from processor.processor import Processor as processor
from tqdm import tqdm
from equations.capm import CAPM
from asset.exposure import Exposure
import warnings
warnings.simplefilter(action="ignore")

class FinancialStatementQuarterly(AnAIStrategy):
    
    def __init__(self):
        super().__init__("financial_statement_quarterly","sp500",["assets","liabilities","reference_price"])
        self.metric = "excess_return"
        self.growth = False
        self.start_year = 2013
        self.end_year = 2020

    def sell_clause(self,stock,market_data):
        current_quarter = (market_data.date.month - 1) // 3 + 1
        purchase_quarter = (stock.purchase_date.month - 1) // 3 + 1
        return (current_quarter != purchase_quarter)
    
    def load_factors(self):       
        self.market.connect()
        self.sec.connect()  
        factors_df = []
        for row in tqdm(self.index.iterrows()):
            try:
                ticker = row[1]["ticker"]
                cik = int(row[1]["CIK"])
                price = processor.column_date_processing(self.market.query("prices",{"ticker":ticker}))
                price["year"] = [x.year for x in price["date"]]
                price["quarter"] = [x.quarter for x in price["date"]]
                filings = processor.column_date_processing(self.sec.query("filings",{"cik":cik}))
                filings["year"] = [x.year if x.quarter < 4 else x.year + 1 for x in filings["date"]]
                filings["quarter"] = [x.quarter + 1 if x.quarter < 4 else 1 for x in filings["date"]]
                price = price.drop(["date","ticker"],axis=1).merge(filings.drop(["date","cik"],axis=1),on=["year","quarter"],how="left").groupby(["year","quarter"]).mean().reset_index()
                price["ticker"] = ticker
                price["y"] = price["adjclose"].shift(-1)
                price["reference_price"] = price["adjclose"].shift(1)
                factors_df.append(price[["year","quarter","ticker","y"]+self.factors])
            except Exception as e:
                print(ticker,str(e))
                continue
        self.sec.disconnect()
        self.market.disconnect()
        factors_df = pd.concat(factors_df).sort_values(["year","quarter"])
        return factors_df.dropna()

    def factor_load(self,standard_df):
        
        factors_df = self.load_factors()
        training_data = factors_df[(factors_df["year"]>self.start_year) & (factors_df["year"]<self.end_year)].dropna()
        sim = factors_df[(factors_df["year"]>=self.end_year-1)].drop("y",axis=1).dropna(subset=self.factors)
        sim = self.model(training_data,sim).dropna(subset=self.factors)
        prices = []
        self.market.connect()
        for ticker in tqdm(self.index["ticker"].unique()):
            try:
                price = standard_df[standard_df["ticker"]==ticker].sort_values("date")
                price.sort_values("date",inplace=True)
                price["year"] = [x.year for x in price["date"]]
                price["quarter"] = [x.quarter for x in price["date"]]
                price.sort_values("date",inplace=True)
                price = price.merge(sim[["year","quarter","ticker","prediction"]],on=["year","quarter","ticker"],how="left")
                price["factor"] = price["prediction"] / price["adjclose"] - 1
                prices.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
        self.market.disconnect()

        sim = pd.concat(prices).reset_index(drop=True)
        sim = CAPM.apply(sim)
        return sim.dropna(subset=["factor"])
    
    def signal(self,sim:pd.DataFrame):
        tickers = list(sim["ticker"].unique())
        sim["rank"] = sim.groupby("date",group_keys=False)["factor"].rank(method="dense", ascending=False).astype(int)
        sim["exposure"] = [Exposure.LONG if x < len(tickers) * 0.1 else Exposure.SHORT if x > len(tickers) * 0.9 else Exposure.NONE for x in sim["rank"]]
        return sim.drop("rank",axis=1)