import pandas as pd
from binance_parameter_creator.binance_parameter_creator import BinanceParameterCreator as bpc
from time import sleep
from binance_strategy.abinance_strategy import ABinanceStrategy

class MarketMarket(ABinanceStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)

    def logic(self):

        account = self.umf.account()
        self.umf.change_leverage(self.ticker,self.leverage)
        balances = pd.DataFrame(self.umf.balance())
        usdt_balance = balances[balances["asset"]=="USDT"]
        positions = pd.DataFrame(account["positions"])
        xrp_positions = positions[positions["symbol"]==self.ticker]
        current_market = self.overhead()

        cash = float(usdt_balance["balance"].item())
        signal = current_market["signal"].item()
        price = float(current_market["close"].item())
        quantity = round(float(cash*0.95/price)) * self.leverage
        pv = float(xrp_positions["notional"].item())
        starting_amount = round(float(xrp_positions["positionAmt"].item()))
        pnl = float(xrp_positions["unrealizedProfit"].item())
        returns = pnl / self.leverage /cash
        
        if cash != 0 and pv == 0:
            self.umf.cancel_open_orders(self.ticker)
            if signal == 1:
                self.umf.change_leverage(self.ticker,self.leverage)
                self.umf.new_order(**bpc.long_market_open(self.ticker,quantity))
            elif signal == -1:
                self.umf.change_leverage(self.ticker,self.leverage)
                self.umf.new_order(**bpc.short_market_open(self.ticker,quantity))
        else:
            if returns < -self.deadpoint or returns > self.profittake:
                if float(starting_amount) > 0:
                    self.umf.change_leverage(self.ticker,self.leverage)
                    self.umf.new_order(**bpc.long_market_close(self.ticker,starting_amount))
                else:
                    self.umf.change_leverage(self.ticker,self.leverage)
                    self.umf.new_order(**bpc.short_market_close(self.ticker,starting_amount))