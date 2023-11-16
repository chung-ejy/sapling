from database.adatabase import ADatabase
import pandas as pd
from processor.processor import Processor as p
from xgboost import XGBRegressor
fed = ADatabase("fed")

fed.connect()
us_macro = p.column_date_processing(fed.retrieve("us_macro"))
sp500 = p.column_date_processing(fed.retrieve("sp500")).rename(columns={"value":"sp500"})
fed.disconnect()

factors = [x for x in us_macro.columns if x not in ["year","date"]]
model_data = p.merge(sp500,us_macro,on="date").dropna()
model_data = model_data.drop("date",axis=1).groupby(["year","quarter"]).mean().reset_index()
model_data.sort_values(["year","quarter"],inplace=True)
model_data["y"] = model_data["sp500"].shift(-4)
model = XGBRegressor(booster="dart",learning_rate=0.5)
training_data = model_data[model_data["year"]<2021].dropna().copy().reset_index()
recommendation_data = model_data[model_data["year"]>=2021].copy().reset_index()

model.fit(training_data[factors],training_data["y"])
recommendation_data["prediction"] = model.predict(recommendation_data[factors])
fed.connect()
fed.drop("sp500_projections")
fed.store("sp500_projections",recommendation_data[["year","quarter","prediction"]])
fed.disconnect()