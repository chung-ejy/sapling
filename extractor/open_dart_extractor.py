import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("OPENDARTKEY")
import requests as r
import zipfile
import io
class OpenDartExtractor(object):

    @classmethod
    def corporate_codes(self):
        unique_number_url = "https://opendart.fss.or.kr/api/corpCode.xml"
        params = {
            "crtfc_key": os.getenv("OPENDARTKEY"),
        }

        # Make the request and get the zip file content
        response = r.get(unique_number_url, params=params)

        # Ensure the response is OK
        if response.status_code == 200:
            # Create a ZipFile object from the response content
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))

            # Extract all files to a specified directory
            extract_dir = "./unique_numbers"  # Define your output directory
            zip_file.extractall(extract_dir)
            print(f"Files extracted to {extract_dir}")

            # Optionally, list the extracted files
            extracted_files = zip_file.namelist()
            print(f"Extracted files: {extracted_files}")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
            
    @classmethod
    def company_information(self,corporate_code):
        unique_number_url = "https://opendart.fss.or.kr/api/company.json"
        params = {
            "crtfc_key": os.getenv("OPENDARTKEY"),
            "corp_code":corporate_code
        }
        # Make the request and get the zip file content
        response = r.get(unique_number_url, params=params)
        return response.json()
    
    @classmethod
    def filing(self,corporate_code,year):
        unique_number_url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
        params = {
            "crtfc_key": os.getenv("OPENDARTKEY"),
            "corp_code":corporate_code,
            "bsns_year":year,
            "reprt_code":11011
        }
        # Make the request and get the zip file content
        response = r.get(unique_number_url, params=params)
        return response.json()