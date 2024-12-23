import pandas as pd
class DateColumns(object):

    @staticmethod
    def apply(df:pd.DataFrame):
        df["year"] = [x.year for x in df["date"]]
        df["quarter"] = [x.quarter for x in df["date"]]
        df["month"] = [x.month for x in df["date"]]
        df["week"] = [x.week for x in df["date"]]
        return df