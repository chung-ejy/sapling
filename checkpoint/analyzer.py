import matplotlib.pyplot as plt

class Analyzer(object):

    @classmethod
    def checkpoint(self,product):
        product.fed.connect()
        bench = product.processor.column_date_processing(product.fed.retrieve("sp500"))
        product.fed.disconnect()
        trades = product.processor.column_date_processing(product.retrieve_trades())
        plt.scatter(trades["abs"],trades["return"])
        plt.show()
        portfolio = trades[["date","return"]].groupby("date").sum().reset_index()
        portfolio = product.processor.merge(portfolio,bench,on="date").dropna()
        portfolio["bcr"] = (portfolio["value"] - portfolio["value"].iloc[0]) / portfolio["value"].iloc[0] + 1
        portfolio["return"] = portfolio["return"] + 1
        portfolio["cr"] = portfolio["return"].cumprod()
        plt.plot(portfolio["date"].values,portfolio["cr"].values)
        plt.plot(portfolio["date"].values,portfolio["bcr"].values)
        plt.show()
        product.drop_portfolio()
        product.store_portfolio(portfolio)