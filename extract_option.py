from database.adatabase import ADatabase
from extractor.alp_client_extractor import ALPClientExtractor
from extractor.tiingo_extractor import TiingoExtractor
from processor.processor import Processor as processor
from datetime import datetime, timedelta
from tqdm import tqdm 
from dotenv import load_dotenv
load_dotenv()
import os

oc = ALPClientExtractor(os.getenv("APCAKEY"),os.getenv("APCASECRET")).option_chains("AAPL")
print(oc)