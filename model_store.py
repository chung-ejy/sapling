from database.adatabase import ADatabase
import pandas as pd
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
from processor.processor import Processor as processor
from tqdm import tqdm
import warnings
warnings.simplefilter(action="ignore")
import pickle

## database init
db = ADatabase("algo")

filename = 'xgboost_model.pkl'

db.connect()
db.drop("model")
with open(filename, 'rb') as file:
    model = pickle.load(file)
    pickled = pickle.dumps(model)
    db.store("model",pd.DataFrame([{"model":pickled}]))
db.disconnect()