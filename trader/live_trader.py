import pandas as pd
from trading_client.atradingclient import ATradingClient
from strategy.astrategy import AStrategy
from time import sleep

class LiveTrader(object):

    def __init__(self,trading_client: ATradingClient,strategy: AStrategy):
        self.trading_client = trading_client
        self.strategy = strategy
    
    def trade(self,recommendations: pd.DataFrame):
        recommendations.sort_values(self.strategy.ranker,ascending=self.strategy.ascending,inplace=True)
        account = self.trading_client.account()
        orders = self.trading_client.orders()
        cash = float(account["cash"])
        pv = float(account["portfolio_value"])
        positions = self.trading_client.positions()
        notional = round(float(pv/self.strategy.parameters.number_of_positions),2)
        if positions.index.size < self.strategy.parameters.number_of_positions:
            for i in range(self.strategy.parameters.number_of_positions):
                try:
                    recommendation, recommendation_order, position = self.strategy.buy_position_filter(i,recommendations,orders,positions)
                    if cash > 1 and cash >= notional and recommendation_order.index.size < 1 \
                                    and position.index.size < 1 and self.strategy.buy_clause(position,recommendation):
                        ticker = recommendation["ticker"]
                        self.trading_client.buy(ticker,notional)  
                        account = self.trading_client.account()
                        cash = float(account["cash"]) 
                    else:
                         continue
                except Exception as e:
                     print(str(e))
        else:
            positions = self.strategy.position_merge(positions,recommendations)          
            try:
                for i in range(self.strategy.parameters.number_of_positions):
                    try:
                        recommendation, recommendation_order, position = self.strategy.sell_position_filter(i,recommendations,orders,positions)
                        ticker = position["ticker"]
                        if self.strategy.sell_clause(position,recommendation):
                            self.trading_client.close()
                            sleep(60)
                            ticker = recommendation["ticker"]
                            self.trading_client.buy(ticker,notional)
                    except Exception as e:
                        print(str(e))
            except Exception as e:
                print(str(e))
            sleep(1)
                