import pandas as pd

class Processor(object):

    @classmethod
    def column_date_processing(self,data):
        data["date"] = [str(x) for x in pd.to_datetime(data["date"],utc=True).dt.date]
        data["date"] = pd.to_datetime(data["date"])
        for col in data.columns:
            data.rename(columns={col:col.lower()},inplace=True)
        return data