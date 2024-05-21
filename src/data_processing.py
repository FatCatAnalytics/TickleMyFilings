import pandas as pd


def filter_xml_content(xml_data, keys):
    results = []

    def search_dict(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if any(key.lower() in k.lower() for key in keys):
                    results.append((k, v))
                if isinstance(v, dict):
                    search_dict(v)
                elif isinstance(v, list):
                    for item in v:
                        search_dict(item)
        elif isinstance(d, list):
            for item in d:
                search_dict(item)

    search_dict(xml_data)
    return results


def process_filtered_results(results):
    rows = []
    for key, value in results:
        if isinstance(value, dict):
            rows.append({**value, 'Category': key})
        elif isinstance(value, list):
            rows.extend([{**item, 'Category': key} for item in value])
    return pd.DataFrame(rows)


def prepare_output_df(df):
    context_ref_df = pd.DataFrame(df)

    # Check for duplicates and handle them
    if context_ref_df.duplicated(subset=['@contextRef', 'Category']).any():
        context_ref_df = context_ref_df.drop_duplicates(subset=['@contextRef', 'Category'])

    pivoted_df = context_ref_df.pivot(index='@contextRef', columns='Category', values='#text').reset_index()

    return pivoted_df
