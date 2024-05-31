import json
import os
import re

import pandas as pd
import numpy as np


def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Failed to read file: {e}")
        return None


def summarize_csv_file(filepath):
    try:
        data = pd.read_csv(filepath)
        summary = {}

        for column in data.columns:
            unique_values = [x.item() if isinstance(x, np.generic) else x for x in data[column].dropna().unique()]
            summary[column] = {'Unique Values': unique_values}

            if pd.api.types.is_numeric_dtype(data[column]):
                summary[column].update({
                    'Sum': float(data[column].sum()),
                    'Average': float(data[column].mean()),
                    'Median': float(data[column].median()),
                    'Standard Deviation': float(data[column].std())
                })

        return summary
    except Exception as e:
        print(f"Failed to process CSV file: {e}")
        return {}


def summarize_text_file(filepath):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\b\d{9}\b'
    content = read_file(filepath)

    if content is None:
        return {}

    summary = {
        "Number of rows": content.count('\n') + 1,
        "Number of words": len(content.split()),
        "Number of characters": len(content),
        "Email addresses": re.findall(email_pattern, content),
        "Phone numbers": re.findall(phone_pattern, content)
    }
    return summary


def summarize_json_file(filepath):
    content = read_file(filepath)

    if content is None:
        return {}

    try:
        data = json.loads(content)
        summary = {'Number of rows': 0, 'Number of words': 0, 'Number of characters': 0}
        process_json_content(data, summary)
        return summary
    except Exception as e:
        print(f"Failed to process JSON file: {e}")
        return {}


def process_json_content(element, summary):
    if isinstance(element, dict):
        summary['Number of rows'] += 1
        for key, value in element.items():
            summary['Number of characters'] += len(key)
            process_json_content(value, summary)
    elif isinstance(element, list):
        summary['Number of rows'] += 1
        for item in element:
            process_json_content(item, summary)
    elif isinstance(element, (str, int, float)):
        summary['Number of rows'] += 1
        words = str(element).split()
        summary['Number of words'] += len(words)
        summary['Number of characters'] += len(str(element))


def summarize_files_in_folder(directory):
    results = {}
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if filename.endswith('.csv'):
                results[filename] = summarize_csv_file(filepath)
            elif filename.endswith('.json'):
                results[filename] = summarize_json_file(filepath)
            elif filename.endswith('.txt'):
                results[filename] = summarize_text_file(filepath)
    return results

if __name__ == "__main__":
    source_directory = 'example_data/'
    summarize_files_in_folder(source_directory)
