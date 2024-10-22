from database.adatabase import ADatabase
import pandas as pd

db = ADatabase("fred")

db.connect()
predictions = db.retrieve("sp500_projections")
db.disconnect()
print(predictions.tail())