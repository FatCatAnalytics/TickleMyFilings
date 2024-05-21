import requests
import xmltodict
import pandas as pd
from xml.parsers.expat import ExpatError
import logging


class EdgarFiling:
    HEADER = {'User-Agent': 'FIRSTNAME LASTNAME EMAIL'}
    BASE_URL = 'https://www.sec.gov/Archives/edgar/data/'
    SUBMISSION_URL_TEMPLATE = 'https://data.sec.gov/submissions/CIK{}.json'

    def fetch_data(self, url):
        try:
            response = requests.get(url, headers=self.HEADER)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            if url.endswith('.json'):
                return response.json()
            else:
                try:
                    return xmltodict.parse(response.content)
                except ExpatError as e:
                    print(f"XML parsing error for URL {url}: {e}")
                    return None
        except requests.exceptions.RequestException as e:
            print(f"Request error for URL {url}: {e}")
            return None

    def get_submission_df(self, cik, form='10-K'):
        url = self.SUBMISSION_URL_TEMPLATE.format(str(cik).zfill(10))
        data = self.fetch_data(url)
        if not data:
            return pd.DataFrame()

        submissions = pd.DataFrame(data['filings']['recent'])
        filtered_submissions = submissions[submissions['form'] == form].copy()

        if filtered_submissions.empty:
            print(f"No {form} filings found for CIK {cik}.")
            return pd.DataFrame()

        filtered_submissions.reset_index(drop=True, inplace=True)  # Ensure a proper index
        filtered_submissions.loc[:, 'cik'] = data['cik']
        filtered_submissions.loc[:, 'reporting_url'] = filtered_submissions.apply(self.build_reporting_url, axis=1)

        return filtered_submissions.head(1)

    def build_reporting_url(self, row):
        accession_no = row['accessionNumber'].replace('-', '')
        cik_no = row['cik'].lstrip('0')
        report = row['primaryDocument'].replace('.htm', '_htm.xml')
        return f"{self.BASE_URL}{cik_no}/{accession_no}/{report}"

    def fetch_and_parse_xml(self, urls):
        return [self.fetch_data(url) for url in urls]
