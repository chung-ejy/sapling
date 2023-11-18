from database.adatabase import ADatabase
import pandas as pd
from processor.processor import Processor as p
from xgboost import XGBRegressor

## run this code on a monthly basis
fed = ADatabase("fed")

fed.connect()
cpi = p.column_date_processing(fed.retrieve("cpi").rename(columns={"value":"cpi"}))
exports = p.column_date_processing(fed.retrieve("exports").rename(columns={"value":"exports"}))
gdp = p.column_date_processing(fed.retrieve("gdp").rename(columns={"value":"gdp"}))
unrate = p.column_date_processing(fed.retrieve("unrate").rename(columns={"value":"unrate"}))
treasury_yields = p.column_date_processing(fed.retrieve("treasury_yields").rename(columns={"value":"treasury_yields"}))
oil = p.column_date_processing(fed.retrieve("oil").rename(columns={"value":"oil"}))
sp500 = p.column_date_processing(fed.retrieve("sp500").rename(columns={"value":"sp500"}))
fed.disconnect()
factor_sets = [cpi,exports,gdp,unrate,oil,treasury_yields]
base = sp500
for factor_set in factor_sets:
    base = p.merge(base,factor_set,on="date")
base = base.ffill().bfill().dropna()
print(base.columns)
factors = ["cpi","exports","gdp","unrate","oil","sp500"]
base.to_csv("us_macro.csv")
model_data = p.merge(sp500,base,on="date").dropna()
model_data = model_data.drop(["date","realtime_start","realtime_end"],axis=1).groupby(["year","quarter"]).first().reset_index()
model_data = model_data.apply(pd.to_numeric)
model_data.sort_values(["year","quarter"],inplace=True)
model_data["y"] = model_data["sp500"].shift(-4)
model = XGBRegressor(booster="dart",learning_rate=0.5)

training_data = model_data[model_data["year"]<2021].dropna().copy().reset_index()
recommendation_data = model_data[model_data["year"]>=2021].copy().reset_index()

model.fit(training_data[factors],training_data["y"])
recommendation_data["prediction"] = model.predict(recommendation_data[factors])

## note the format of this db is year quarter prediction
fed.connect()
fed.drop("sp500_v2_projections")
fed.store("sp500_v2_projections",recommendation_data[["year","quarter","prediction"]])
fed.disconnect()