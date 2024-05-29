import json
import os
import re

import pandas as pd
import numpy as np


def summarize_csv_file(filepath):
    """Extracts unique values from each column in a CSV file and computes statistical measures for numerical columns.

    Args:
    filepath (str): Path to the CSV file.

    Returns:
    str: JSON string containing unique values for each column and statistical summaries for numerical columns.
    """
    try:
        data = pd.read_csv(filepath)
        summary = {}

        for column in data.columns:
            unique_values = data[column].dropna().unique().tolist()
            summary[column] = {
                'Unique Values': [x.item() if isinstance(x, np.generic) else x for x in unique_values]
                # Convert NumPy types to native Python types
            }

            if pd.api.types.is_numeric_dtype(data[column]):
                summary[column].update({
                    'Sum': data[column].sum().item(),  # Convert to native Python int/float
                    'Average': data[column].mean().item(),  # Convert to native Python float
                    'Median': data[column].median().item(),  # Convert to native Python float
                    'Standard Deviation': data[column].std().item()  # Convert to native Python float
                })

        return json.dumps(summary, indent=4)
    except Exception as e:
        print(f"Failed to read the CSV file: {e}")
        return json.dumps({})


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
            return json.dumps(summary, indent=4)
    except Exception as e:
        print(f"Failed to read the text file: {e}")
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
        return json.dumps(summary, indent=4)
    except Exception as e:
        print(f"Failed to read the JSON file: {e}")
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
                print(f"Unsupported file type for file: {filename}")
                continue
            print(f"Summary for {filename}:")
            print(summary)


if __name__ == "__main__":
    source_directory = 'example_data/'
    summarize_files_in_folder(source_directory)
