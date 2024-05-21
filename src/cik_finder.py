import requests
from bs4 import BeautifulSoup
import pandas as pd


# Function to get CIK code from SEC EDGAR
def get_cik(company_name):
    search_url = f"https://www.sec.gov/cgi-bin/browse-edgar?company={company_name}&owner=exclude&action=getcompany"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        cik = \
        soup.find('div', {'class': 'companyInfo'}).find('span', {'class': 'companyName'}).text.split('CIK#')[1].split(
            ' ')[0]
        return cik
    except Exception as e:
        return None


# Load the companies file
file_path = 'inputs/Companies.csv'
companies_df = pd.read_csv(file_path)

# Extract company names
company_names = companies_df['Company Name'].tolist()

# Retrieve CIK codes
cik_codes = []
for name in company_names:
    cik = get_cik(name)
    cik_codes.append(cik)

# Add retrieved CIK codes to the dataframe
companies_df['Retrieved CIK'] = cik_codes

# Compare the CIK codes
companies_df['CIK Match'] = companies_df['CIK'] == companies_df['Retrieved CIK']

# Save the updated dataframe to a new CSV file
output_file_path = 'path/to/your/updated_ttt.csv'
companies_df.to_csv(output_file_path, index=False)

print("CIK codes have been retrieved and compared. The updated file is saved as updated_ttt.csv.")
