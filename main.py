from src.data_fetching import EdgarFiling
from src.data_processing import filter_xml_content, process_filtered_results, prepare_output_df

def main():
    # Example usage
    scraper = EdgarFiling()
    cik = '66740'
    form = '10-K'
    submission_df = scraper.get_submission_df(cik, form)

    if not submission_df.empty:
        urls = submission_df['reporting_url'].tolist()
        xml_data = scraper.fetch_and_parse_xml(urls[:1])  # Limit to first URL for example
        filtered_results = filter_xml_content(xml_data[0], ['hedge', 'derivatives'])
        processed_results = process_filtered_results(filtered_results)
        output_df = prepare_output_df(processed_results)
        print(output_df)

if __name__ == "__main__":
    main()
