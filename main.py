from src.data_fetching import EdgarFiling
from src.output_processing import OutputProcessor
from src.data_processing import filter_xml_content, process_filtered_results, prepare_output_df
import pandas as pd


def main():
    # Example usage
    scraper = EdgarFiling()
    ciks = ['66740', '320193', '12927']  # Add more CIKs as needed
    form = '10-K'

    # Initialize an empty list to collect DataFrames
    df_list = []

    for cik in ciks:
        submission_df = scraper.get_submission_df(cik, form)

        if not submission_df.empty:
            urls = submission_df['reporting_url'].tolist()
            xml_data = scraper.fetch_and_parse_xml(urls[:1])  # Limit to first URL for example
            filtered_results = filter_xml_content(xml_data[0], ['hedging', 'derivatives'])
            processed_results = process_filtered_results(filtered_results)
            output_df = prepare_output_df(processed_results)

            # Add a new column to the output DataFrame that contains the CIK number
            output_df['CIK'] = cik

            # Append the output DataFrame to the list
            df_list.append(output_df)

    # Concatenate all DataFrames in the list into a single DataFrame
    big_df = pd.concat(df_list, ignore_index=True)
    keywords = ['hedge', 'hedging']
    cleaner = OutputProcessor(big_df, keywords)
    cleaned_data = cleaner.process()
    output_file_path = 'outputs/cleaned_output_updated.csv'
    cleaned_data.to_csv(output_file_path, index=False)
    print(f"Cleaned data saved to {output_file_path}")


if __name__ == "__main__":
    main()
