from bs4 import BeautifulSoup
import pandas as pd


class OutputProcessor:
    def __init__(self, data, keywords):
        self.data = data
        self.keywords = keywords

    @staticmethod
    def clean_html_exclude_tables(text):
        if pd.isna(text) or not isinstance(text, str):
            return text
        soup = BeautifulSoup(text, "html.parser")
        # Extract and remove tables from the HTML
        for table in soup.find_all('table'):
            table.decompose()
        return soup.get_text()

    def check_keyword(self, text):
        if pd.isna(text):
            return False
        for keyword in self.keywords:
            if keyword in text.lower():
                return True
        return False

    @staticmethod
    def contains_html_tag(row):
        for col in row.index:
            if pd.notna(row[col]) and isinstance(row[col], str) and '<' in row[col] and '>' in row[col]:
                return True
        return False

    def process(self):
        # Filter rows that contain HTML tags
        filtered_data = self.data[self.data.apply(self.contains_html_tag, axis=1)]

        # Remove columns that contain only NaN values
        cleaned_data = filtered_data.dropna(axis=1, how='all').copy()

        # Apply the clean_html function to all relevant columns in the dataframe
        for column in cleaned_data.columns:
            cleaned_data[column] = cleaned_data[column].apply(self.clean_html_exclude_tables)

        # Apply the check_hedge function to each row and create a new column 'hedge'
        cleaned_data['hedge'] = cleaned_data.apply(lambda row: any(self.check_keyword(row[col]) for col in cleaned_data.columns), axis=1)

        return cleaned_data
