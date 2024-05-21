import logging
from src.data_fetching import EdgarFiling
from src.output_processing import OutputProcessor
from src.data_processing import filter_xml_content, process_filtered_results, prepare_output_df
import pandas as pd


def setup_logging():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def process_cik(cik, form_type, keywords, scraper):
    submission_df = scraper.get_submission_df(cik, form_type)
    if submission_df.empty:
        logging.warning(f"No submissions found for CIK {cik}")
        return None

    logging.info(f"Processing CIK {cik}")
    urls = submission_df['reporting_url'].tolist()
    xml_data = scraper.fetch_and_parse_xml(urls)

    if not xml_data or not xml_data[0]:
        logging.warning(f"No XML data found for CIK {cik}")
        return None

    filtered_results = filter_xml_content(xml_data[0], keywords)
    processed_results = process_filtered_results(filtered_results)

    if processed_results.empty:
        logging.warning(f"No filtered results found for CIK {cik}")
        return None

    output_df = prepare_output_df(processed_results)

    if output_df.empty:
        logging.warning(f"No processed output for CIK {cik}")
        return None

    output_df['CIK'] = cik
    return output_df


def main(cik_list, form_type, keywords, output_file_path):
    setup_logging()
    scraper = EdgarFiling()

    df_list = []
    for cik in cik_list:
        result_df = process_cik(cik, form_type, keywords, scraper)
        if result_df is not None and not result_df.empty:
            df_list.append(result_df)

    if not df_list:
        logging.error("No valid data frames to concatenate. Exiting.")
        return

    big_df = pd.concat(df_list, ignore_index=True)

    cleaner = OutputProcessor(big_df, keywords)
    cleaned_data = cleaner.process()
    cleaned_data.to_csv(output_file_path, index=False)

    logging.info(f"Cleaned data saved to {output_file_path}")


if __name__ == "__main__":
    cik = pd.read_csv('inputs/CIK_Codes.txt', header=0)
    cik_list = cik['CIK'].tolist()[:100]
    form_type = '10-K'
    keywords = ['hedging', 'derivatives']
    output_file_path = 'outputs/cleaned_output_updated.csv'

    main(cik_list, form_type, keywords, output_file_path)


