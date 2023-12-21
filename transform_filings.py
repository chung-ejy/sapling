from database.adatabase import ADatabase
import pandas as pd
from processor.processor import Processor as processor
from tqdm import tqdm
market = ADatabase("market")
market.connect()
ciks = [int(x) for x in market.retrieve("sp500")["CIK"].values]
market.disconnect()
market.connect()
market.drop("filings")
for year in tqdm(range(2009,2024)):
    for quarter in range(1,4):
        try:
            num = pd.read_csv(f'./sec/{year}q{quarter}/num.txt', delimiter='\t')
            sub = pd.read_csv(f'./sec/{year}q{quarter}/sub.txt', delimiter='\t')[["adsh","cik","filed"]]
            num = processor.merge(num,sub,on="adsh")
            num["tag"] = [str(x).replace(".","").lower().replace("1","") for x in num["tag"]]
            num["cik"] = [int(x) for x in num["cik"]]
            for cik in ciks:
                try:
                    filings = num[num["cik"]==cik].pivot_table(columns="tag",index="adsh",values="value")
                    if filings.index.size > 0:
                        market.store("filings",filings)
                except:
                    continue
        except Exception as e:
            print(year,quarter,str(e))
            break
market.create_index("filings","cik")
market.disconnect()