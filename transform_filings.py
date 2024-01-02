from database.adatabase import ADatabase
import pandas as pd
from processor.processor import Processor as processor
from tqdm import tqdm
relevant_tags = ["assets","liabilities","stockholdersequity","earningspersharebasic"]
market = ADatabase("market")
market.connect()
ciks = [int(x) for x in market.retrieve("sp500")["CIK"].values]
market.disconnect()
market.connect()
market.drop("filings")
for year in tqdm(range(2009,2024)):
    for quarter in tqdm(range(1,5)):
        try:
            sub = pd.read_csv(f'./sec/{year}q{quarter}/sub.txt',engine="python",sep=None
                              ,parse_dates=True,encoding="us-ascii",encoding_errors="replace",skipinitialspace=True,quoting=3)[["filed","adsh","cik"]]
            num = pd.read_csv(f'./sec/{year}q{quarter}/num.txt',engine="python",sep=None
                              ,parse_dates=True,encoding="us-ascii",encoding_errors="replace",skipinitialspace=True,quoting=3)
            num = processor.merge(num,sub,on="adsh").dropna()
            num["cik"] = [int(x) for x in num["cik"]]
            num["tag"] = [str(x).replace(".","").lower().replace("1","") for x in num["tag"]]
            num = num[num["tag"].isin(relevant_tags)]
            market.store("filings",num)
        except Exception as e:
            print(year,quarter,str(e))
            continue
market.create_index("filings","cik")
market.disconnect()