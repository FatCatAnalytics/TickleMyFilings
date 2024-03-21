import requests
import xmltodict
import pandas as pd

class EdgarScraper:
    HEADER = {'User-Agent': 'Aksel Etingu aetingu@gmail.com'}
    BASE_URL = 'https://www.sec.gov/Archives/edgar/data/'
    SUBMISSION_URL_TEMPLATE = 'https://data.sec.gov/submissions/CIK{}.json'

    def fetch_data(self, url):
        response = requests.get(url, headers=self.HEADER)
        return response.json() if url.endswith('.json') else xmltodict.parse(response.content)

    def get_submission_df(self, cik, form='10-K'):
        url = self.SUBMISSION_URL_TEMPLATE.format(str(cik).zfill(10))
        data = self.fetch_data(url)
        submissions = pd.DataFrame(data['filings']['recent'])
        filtered_submissions = submissions[submissions['form'] == form].copy()
        filtered_submissions.loc[:, 'cik'] = data['cik']
        if filtered_submissions.empty:
            print(f"No {form} filings found for CIK {cik}.")
            return pd.DataFrame()
        filtered_submissions.loc[:, 'reporting_url'] = filtered_submissions.apply(self.build_reporting_url, axis=1)
        return filtered_submissions

    def build_reporting_url(self, row):
        accession_no = row['accessionNumber'].replace('-', '')
        cik_no = row['cik'].lstrip('0')
        report = row['primaryDocument'].replace('.htm', '_htm.xml')
        return f"{self.BASE_URL}{cik_no}/{accession_no}/{report}"

    def fetch_and_parse_xml(self, urls):
        return [self.fetch_data(url) for url in urls]
