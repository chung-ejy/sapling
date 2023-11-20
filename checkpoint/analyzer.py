import matplotlib.pyplot as plt

class Analyzer(object):

    @classmethod
    def checkpoint(self,product):
        trades = product.retrieve_trades()
        plt.scatter(trades["abs"],trades["return"])
        plt.show()
        portfolio = trades[["date","return"]].groupby("date").sum().reset_index()
        portfolio["return"] = portfolio["return"] + 1
        portfolio["cr"] = portfolio["return"].cumprod()
        plt.plot(portfolio["date"].values,portfolio["cr"].values)
        plt.show()
        product.drop_portfolio()
        product.store_portfolio(portfolio)