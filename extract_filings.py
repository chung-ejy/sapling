import requests
import zipfile

for year in range(2009,2024):
    for quarter in range(1,5):
        print(year,quarter)
        url = f"https://www.sec.gov/files/dera/data/financial-statement-data-sets/{year}q{quarter}.zip"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Open a file in write binary ('wb') mode
            with open(f'./sec/{year}q{quarter}.zip', 'wb') as file:
                # Write the file's content to the specified file
                file.write(response.content)

            # Open the downloaded zip file
            with zipfile.ZipFile(f'./sec/{year}q{quarter}.zip', 'r') as zip_ref:
                # Extract all the files in the zip file
                zip_ref.extractall(f'./sec/{year}q{quarter}')

            print("File downloaded and unzipped successfully.")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
            print(response)