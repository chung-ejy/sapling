import requests as r
import zipfile
import io
import os
from dotenv import load_dotenv
import pandas as pd
from extractor.open_dart_extractor import OpenDartExtractor
from database.adatabase import ADatabase

OpenDartExtractor.corporate_codes()
corporate_codes = pd.read_xml("./unique_numbers/CORPCODE.xml")
db = ADatabase("open_dart")
db.connect()
db.store("companies",corporate_codes)
db.disconnect()