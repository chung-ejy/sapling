from strategy.anaistrategy import AnAIStrategy
from database.adatabase import ADatabase
import pandas as  pd
from processor.processor import Processor as processor
from tqdm import tqdm
import warnings
warnings.simplefilter(action="ignore")
import math
class KRFinancialStatementYearly(AnAIStrategy):
    
    def __init__(self):
        super().__init__("kr_financial_statement_yearly",[
                                                            '부채총계',
                                                            '유동부채', 
                                                            '유동자산', 
                                                            '이익잉여금', 
                                                            '자산총계', 'adjclose'])
        self.metric = "excess_return"
        self.dart = ADatabase("open_dart")
        self.growth = False
        self.start_year = 2015
        self.end_year = 2022
        self.sim_end_year = 2025

    def sell_clause(self,date,stock):
        return date.quarter != stock.buy_date.quarter
    
    def load_factors(self):
        self.dart.connect()    
        kospi = self.dart.retrieve("kospi")
        self.dart.disconnect()
        self.market.connect()
        self.dart.connect()
        factors_df = []
        for ticker in tqdm(list(kospi["ticker"].unique())):
            try:
                trimed_ticker = str(int(ticker))
                price = processor.column_date_processing(self.market.query("kr_prices",{"ticker":trimed_ticker}).rename(columns={"Date":"date","Close":"adjclose"}))
                price["ticker"] = ticker
                price["year"] = [x.year for x in price["date"]]
                price["adjclose"] = [float(x) for x in price["adjclose"]]
                filings = self.dart.query("filings",{"ticker":str(ticker)})
                price = price.drop(["date","ticker"],axis=1).merge(filings.drop(["ticker"],axis=1),on=["year"],how="left")
                for column in self.factors:
                    try:
                        price[column] = [float(x) for x in price[column]]
                    except:
                        continue
                price = price[self.factors + ["year"]].groupby(["year"]).mean().reset_index()
                price["ticker"] = ticker
                price["y"] = price["adjclose"].shift(-1)
                factors_df.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
        self.dart.disconnect()
        self.market.disconnect()
        factors_df = pd.concat(factors_df)
        factors_df = factors_df.fillna(0)
        factors_df.sort_values(["year"],inplace=True)
        return factors_df

    def load_dataset(self):
        
        self.dart.connect()    
        kospi = self.dart.retrieve("kospi")
        self.dart.disconnect()
        kospi["GICS Sector"] = [round(math.log10(x)) for x in kospi["Total market cap."]]
        market_yield, spy = self.load_macro()
        factors_df = self.load_factors()
        training_data = factors_df[(factors_df["year"]>self.start_year) & (factors_df["year"]<self.end_year)].dropna()
        sim = factors_df[(factors_df["year"]>=self.end_year-1) & (factors_df["year"]<self.sim_end_year)].drop("y",axis=1).dropna()
        sim = self.model(training_data,sim)

        prices = []
        self.market.connect()
        for ticker in tqdm(kospi["ticker"].unique()):
            try:
                trimed_ticker = str(int(ticker))
                price = processor.column_date_processing(self.market.query("kr_prices",{"ticker":trimed_ticker}).rename(columns={"Date":"date","Close":"adjclose"}))
                price["ticker"] = ticker
                price["year"] = [x.year for x in price["date"]]
                price["adjclose"] = [float(x) for x in price["adjclose"]]
                price.sort_values("date",inplace=True)
                price = price.merge(sim[["year","ticker","prediction"]],on=["year","ticker"],how="left")
                price = self.index_factor_load(price,kospi,spy,market_yield)
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