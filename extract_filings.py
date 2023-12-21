import zipfile
from time import sleep
for year in range(2021,2024):
    for quarter in range(1,5):
        # Open the downloaded zip file
        with zipfile.ZipFile(f'./sec/{year}q{quarter}.zip', 'r') as zip_ref:
            # Extract all the files in the zip file
            zip_ref.extractall(f'./sec/{year}q{quarter}')
        print("File downloaded and unzipped successfully.")