from pandas_datareader.naver import NaverDailyReader

class PandasExtractor(object):

    @classmethod
    def prices(self,ticker,start,end):
        ndr = NaverDailyReader(symbols=ticker, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"), adjust_price=True, adjust_dividends=False)
        df = ndr.read().reset_index()
        return df