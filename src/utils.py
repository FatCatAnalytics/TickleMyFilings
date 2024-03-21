import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import xmltodict


def setup_logging(level=logging.INFO):
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=level)

def make_request(url, headers=None, max_retries=3):
    session = requests.Session()
    retry_strategy = Retry(
        total=max_retries,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    response = session.get(url, headers=headers)
    response.raise_for_status()
    return response

def xml_to_dict(xml_data):
    try:
        return xmltodict.parse(xml_data)
    except Exception as e:
        logging.error("Error parsing XML to dictionary: %s", e)
        raise
