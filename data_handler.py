import json
import os
import re

import pandas as pd
import numpy as np


def summarize_csv_file(filepath):
    """ Extracts unique values from each column in a CSV file and computes statistical measures for numerical columns.

    Args:
    filepath (str): Path to the CSV file.

    Returns:
    dict: JSON compatible dictionary containing unique values for each column and statistical summaries for numerical columns.
    """
    try:
        data = pd.read_csv(filepath)
        summary = {}

        for column in data.columns:
            # Ensure compatibility of numpy types with JSON
            unique_values = [x.item() if isinstance(x, np.generic) else x for x in data[column].dropna().unique()]
            summary[column] = {'Unique Values': unique_values}

            if pd.api.types.is_numeric_dtype(data[column]):
                summary[column].update({
                    'Sum': float(data[column].sum()),
                    'Average': float(data[column].mean()),
                    'Median': float(data[column].median()),
                    'Standard Deviation': float(data[column].std())
                })

        return summary  # return Python dictionary directly
    except Exception as e:
        print(f"Failed to process CSV file: {e}")
        return {}


def summarize_text_file(filepath):
    """Summarizes a text file, calculating the number of rows, words, characters, and searches for emails and phone numbers.

    Args:
    filepath (str): Path to the text file.

    Returns:
    str: JSON string containing the number of rows, words, characters, emails, and phone numbers.
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\b\d{9}\b'

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            summary = {
                "Number of rows": content.count('\n') + 1,
                "Number of words": len(content.split()),
                "Number of characters": len(content),
                "Email addresses": re.findall(email_pattern, content),
                "Phone numbers": re.findall(phone_pattern, content)
            }
            return summary
    except Exception as e:
        return json.dumps({})


def summarize_json_file(filepath):
    """Summarizes a JSON file, calculating the number of rows, words, and characters.

    Args:
    filepath (str): Path to the JSON file.

    Returns:
    str: JSON string containing the number of rows, words, and characters.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        summary = {'Number of rows': 0, 'Number of words': 0, 'Number of characters': 0}
        process_json_content(data, summary)
        return summary
    except Exception as e:
        return json.dumps({})


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
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if filename.endswith('.csv'):
                summary = summarize_csv_file(filepath)
            elif filename.endswith('.json'):
                summary = summarize_json_file(filepath)
            elif filename.endswith('.txt'):
                summary = summarize_text_file(filepath)
            else:
                continue
            return summary


if __name__ == "__main__":
    source_directory = 'example_data/'
    summarize_files_in_folder(source_directory)
