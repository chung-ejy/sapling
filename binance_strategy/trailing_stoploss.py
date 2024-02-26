import pandas as pd
from datetime import datetime
from binance_parameter_creator.binance_parameter_creator import BinanceParameterCreator as bpc
from time import sleep
from binance_strategy.abinance_strategy import ABinanceStrategy
class TrailingStopLoss(ABinanceStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)

    def logic(self,umf):

        account = umf.account()
        umf.change_leverage(self.ticker,self.leverage)
        balances = pd.DataFrame(umf.balance())
        usdt_balance = balances[balances["asset"]=="USDT"]
        positions = pd.DataFrame(account["positions"])
        xrp_positions = positions[positions["symbol"]==self.ticker]

        columns = ["start","open","high","low","close","volumne","end","volume","trades","buy_volumne","base_volume","ignore"]
        df = pd.DataFrame(data=umf.klines(self.ticker,interval="1m"),columns=columns)
        df["date"] = [datetime.utcfromtimestamp(int(x/1000)) for x in df["start"]]
        df.sort_values("date",inplace=True)
        df["close"] = [float(x) for x in df["close"]]
        df["rolling"] = df["close"].rolling(self.band).mean()
        df["signal"] = df["rolling"] > df["close"]
        df["signal"] = [1 if x == True else -1 for x in df["signal"]]
        
        current_market = df.iloc[-1]
        orders = pd.DataFrame(umf.get_all_orders("XRPUSDT"))
        new_orders = orders[orders["status"]=="NEW"]
        cash = float(usdt_balance["balance"].item())
        signal = current_market["signal"].item()
        price = float(current_market["close"].item())
        quantity = round(float(cash*0.98/price)) * self.leverage
        pv = float(xrp_positions["notional"].item())
        starting_amount = round(float(xrp_positions["positionAmt"].item()))
        pnl = float(xrp_positions["unrealizedProfit"].item())
        breakeven_price = float(xrp_positions["breakEvenPrice"].item())
        returns = pnl / self.leverage /cash

        if cash != 0 and pv == 0:
            umf.cancel_open_orders(self.ticker)
            umf.change_leverage(self.ticker,self.leverage)
            if signal == 1:
                umf.change_leverage(self.ticker,self.leverage)
                umf.new_order(**bpc.long_market_open(self.ticker,quantity))
                breakeven_price = 0
                while breakeven_price == 0:
                    account = umf.account()
                    positions = pd.DataFrame(account["positions"])
                    xrp_positions = positions[positions["symbol"]==self.ticker]
                    breakeven_price = float(xrp_positions["breakEvenPrice"].item())
                    starting_amount = float(xrp_positions["positionAmt"].item())
                    sleep(1)
                umf.change_leverage(self.ticker,self.leverage)
                umf.new_order(**bpc.long_trailing_stop(self.ticker,starting_amount,breakeven_price,self.profittake,self.callback))
            elif signal == -1:
                umf.change_leverage(self.ticker,self.leverage)
                umf.new_order(**bpc.short_market_open(self.ticker,quantity))
                breakeven_price = 0
                while breakeven_price == 0:
                    account = umf.account()
                    positions = pd.DataFrame(account["positions"])
                    xrp_positions = positions[positions["symbol"]==self.ticker]
                    breakeven_price = float(xrp_positions["breakEvenPrice"].item())
                    starting_amount = float(xrp_positions["positionAmt"].item())
                    sleep(1)
                umf.change_leverage(self.ticker,self.leverage)
                umf.new_order(**bpc.short_trailing_stop(self.ticker,starting_amount,breakeven_price,self.profittake,self.callback))
        else:
            if new_orders.index.size < 2:
                if returns > -self.deadpoint and returns < -self.stoploss:
                    if float(starting_amount) > 0:
                        try:
                            umf.change_leverage(self.ticker,self.leverage)
                            umf.new_order(**bpc.long_stop_loss(self.ticker,starting_amount,price,breakeven_price))
                        except:
                            umf.change_leverage(self.ticker,self.leverage)
                            umf.new_order(**bpc.long_stop_loss(self.ticker,starting_amount,price,breakeven_price*(1-self.stoploss)))
                    else:
                        try:
                            umf.change_leverage(self.ticker,self.leverage)
                            umf.new_order(**bpc.short_stop_loss(self.ticker,starting_amount,price,breakeven_price))
                        except:
                            umf.change_leverage(self.ticker,self.leverage)
                            umf.new_order(**bpc.long_stop_loss(self.ticker,starting_amount,price,breakeven_price*(1+self.stoploss)))
                elif returns < -self.deadpoint:
                    if float(starting_amount) > 0:
                        umf.change_leverage(self.ticker,self.leverage)
                        umf.new_order(**bpc.long_market_close(self.ticker,starting_amount))
                    else:
                        umf.change_leverage(self.ticker,self.leverage)
                        umf.new_order(**bpc.short_market_close(self.ticker,starting_amount))