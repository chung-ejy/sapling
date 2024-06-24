import pandas as pd

class Processor(object):

    @classmethod
    def column_date_processing(self,data):
        data["date"] = pd.to_datetime(data["date"],utc=True)
        data["year"] = [x.year for x in data["date"]]
        data["quarter"] = [x.quarter for x in data["date"]]
        data["month"] = [x.month for x in data["date"]]
        data["week"] = [x.week for x in data["date"]]
        data["weekday"] = [x.weekday() for x in data["date"]]
        for col in data.columns:
            data.rename(columns={col:col.lower()},inplace=True)
        return data
        
    @classmethod
    def merge(self,d1,d2,on):
        new = d1.merge(d2,on=on,how="left",suffixes=("","_y"))
        drop_cols = [x for x in new.columns if "_y" in x]
        return new.drop(drop_cols,axis=1)