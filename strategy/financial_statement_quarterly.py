from strategy.astrategy import AStrategy
from database.adatabase import ADatabase
import pandas as  pd
from processor.processor import Processor as processor
from tqdm import tqdm
import numpy as np
import warnings
from xgboost import XGBRegressor

warnings.simplefilter(action="ignore")

class FinancialStatementQuarterly(AStrategy):
    
    def __init__(self):
        super().__init__("financial_statement_quarterly")
        self.metric = "excess_return"
        self.growth = False

    def sell_clause(self,date,stock):
        return date.quarter != stock.buy_date.quarter
    
    def load_dataset(self):
        russell1000 = pd.read_html("https://en.wikipedia.org/wiki/Russell_1000_Index")[2].rename(columns={"Symbol":"ticker"})
        market_yield, spy = self.load_macro()
    
        self.market.connect()
        self.sec.connect()
        factors_df = []
        for ticker in tqdm(russell1000["ticker"].unique()):
            try:
                price = processor.column_date_processing(self.market.query("prices",{"ticker":ticker}))
                price["year"] = [x.year for x in price["date"]]
                price["quarter"] = [x.quarter for x in price["date"]]
                filings = processor.column_date_processing(self.sec.query("financials",{"ticker":ticker})).drop(["gsector","gicdesc"],axis=1)
                filings["year"] = [x.year for x in filings["date"]]
                filings["quarter"] = [x.quarter for x in filings["date"]]
                filings["quarter"] = filings["quarter"].shift(1)
                price = price.drop(["date","ticker"],axis=1).merge(filings.drop(["date","ticker"],axis=1),on=["year","quarter"],how="left").groupby(["year","quarter"]).mean().reset_index()
                price["ticker"] = ticker
                price["y"] = price["adjclose"].shift(-4)
                factors_df.append(price)
            except Exception as e:
                # print(ticker,str(e))
                continue
        self.sec.disconnect()
        self.market.disconnect()

        factors_df = pd.concat(factors_df)
        for column in factors_df:
            if column in factors_df[column]:
                factors_df.drop(column,axis=1,inplace=True)
        factors_df = factors_df.fillna(0)
        start_year = 2022
        end_year = 2023
        sim_end_year = 2025

        model = XGBRegressor()
        factors = ["ptb","roa","mktcap","bm","short_debt","divyield","adjclose"]
        factors_df.sort_values(["year","quarter"],inplace=True)
        training_data = factors_df[(factors_df["year"]>start_year) & (factors_df["year"]<end_year)].dropna()
        sim = factors_df[(factors_df["year"]>=end_year-1) & (factors_df["year"]<sim_end_year)].drop("y",axis=1).dropna()
        model.fit(training_data[factors],training_data["y"])
        sim["prediction"] = model.predict(sim[factors])

        prices = []
        self.market.connect()
        for ticker in tqdm(russell1000["ticker"].unique()):
            try:
                price = processor.column_date_processing(self.market.query("historical_prices",{"ticker":ticker}))
                price["year"] = [x.year for x in price["date"]]
                price["quarter"] = [x.quarter for x in price["date"]]
                price.sort_values("date",inplace=True)
                price = price.merge(russell1000[["ticker","GICS Sector"]],on="ticker",how="left")
                price = price.merge(sim[["year","quarter","ticker","prediction"]],on=["year","quarter","ticker"],how="left")
                price = price.merge(spy[["date","spy"]],on="date",how="left")
                price = price.merge(market_yield[["date","rf"]],on="date",how="left")
                price = self.index_factor_load(price)
                price["sigma"] = price["adjclose"].rolling(262).std()
                prices.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
        self.market.disconnect()

        sim = pd.concat(prices)
        self.save_sim(sim)

    def get_sim(self):
        self.db.connect()
        sim = processor.column_date_processing(self.db.retrieve("sim")).sort_values("date")
        self.db.disconnect()
        return sim