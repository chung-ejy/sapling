import pandas as pd
from datetime import datetime
from binance_parameter_creator.binance_parameter_creator import BinanceParameterCreator as bpc
from time import sleep
from binance_strategy.abinance_strategy import ABinanceStrategy

class TrailingBE(ABinanceStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)

    def logic(self):
        account = self.umf.account()
        balances = pd.DataFrame(self.umf.balance())
        usdt_balance = balances[balances["asset"]=="USDT"]
        positions = pd.DataFrame(account["positions"])
        xrp_positions = positions[positions["symbol"]==self.ticker]
        current_market = self.overhead()
        orders = pd.DataFrame(self.umf.get_all_orders("XRPUSDT"))
        new_orders = orders[orders["status"]=="NEW"]
        cash = float(usdt_balance["balance"].item())
        signal = current_market["signal"].item()
        
        price = float(current_market["close"].item())
        quantity = round(float(cash*0.90/price)) * self.leverage
        pv = float(xrp_positions["notional"].item())
        starting_amount = round(float(xrp_positions["positionAmt"].item()))
        pnl = float(xrp_positions["unrealizedProfit"].item())
        breakeven_price = float(xrp_positions["breakEvenPrice"].item())
        returns = pnl / self.leverage /cash
        if cash != 0 and pv == 0:
            self.umf.cancel_open_orders(self.ticker)
            if signal == 1:
                self.umf.change_leverage(self.ticker,self.leverage)
                self.umf.new_order(**bpc.long_market_open(self.ticker,quantity))
                breakeven_price = 0
                while breakeven_price == 0:
                    account = self.umf.account()
                    positions = pd.DataFrame(account["positions"])
                    xrp_positions = positions[positions["symbol"]==self.ticker]
                    breakeven_price = float(xrp_positions["breakEvenPrice"].item())
                    starting_amount = float(xrp_positions["positionAmt"].item())
                    sleep(1)
                self.umf.change_leverage(self.ticker,self.leverage)
                self.umf.new_order(**bpc.long_trailing_stop(self.ticker,starting_amount,breakeven_price,self.profittake,self.callback))
            elif signal == -1:
                self.umf.change_leverage(self.ticker,self.leverage)
                self.umf.new_order(**bpc.short_market_open(self.ticker,quantity))
                breakeven_price = 0
                while breakeven_price == 0:
                    account = self.umf.account()
                    positions = pd.DataFrame(account["positions"])
                    xrp_positions = positions[positions["symbol"]==self.ticker]
                    breakeven_price = float(xrp_positions["breakEvenPrice"].item())
                    starting_amount = float(xrp_positions["positionAmt"].item())
                    sleep(1)
                self.umf.change_leverage(self.ticker,self.leverage)
                self.umf.new_order(**bpc.short_trailing_stop(self.ticker,starting_amount,breakeven_price,self.profittake,self.callback))
        else:
            if new_orders.index.size < 2:
                if returns > -self.deadpoint and returns < -self.stoploss:
                    if float(starting_amount) > 0:
                        self.umf.change_leverage(self.ticker,self.leverage)
                        self.umf.new_order(**bpc.long_limit_close(self.ticker,starting_amount,breakeven_price))
                    else:
                        self.umf.change_leverage(self.ticker,self.leverage)
                        self.umf.new_order(**bpc.short_limit_close(self.ticker,starting_amount,breakeven_price))
            else:
                if returns < -self.deadpoint:
                    self.umf.cancel_open_orders(self.ticker)
                    if float(starting_amount) > 0:
                        self.umf.change_leverage(self.ticker,self.leverage)
                        self.umf.new_order(**bpc.long_limit_close(self.ticker,starting_amount,breakeven_price*(1-self.deadpoint+.001)))
                    else:
                        self.umf.change_leverage(self.ticker,self.leverage)
                        self.umf.new_order(**bpc.short_limit_close(self.ticker,starting_amount,breakeven_price*(1+self.deadpoint-.001)))