import json

import pandas as pd


def summarize_csv_file(filepath):
    """ Summarizes a CSV file, calculating the number of rows, words, and characters.

    Args:
    filepath (str): Path to the CSV file.

    Returns:
    dict: Dictionary containing the number of rows, words, and characters.
    """
    try:
        data = pd.read_csv(filepath)
        row_count = data.shape[0]
        word_count = data.apply(lambda row: sum(len(str(x).split()) for x in row), axis=1).sum()
        char_count = data.apply(lambda row: sum(len(str(x)) for x in row), axis=1).sum()

        return {
            "Number of rows": row_count,
            "Number of words": word_count,
            "Number of characters": char_count
        }
    except Exception as e:
        print(f"Failed to read the CSV file: {e}")
        return {}

def summarize_text_file(filepath):
    """ Summarizes a text file, calculating the number of rows, words, and characters.

    Args:
    filepath (str): Path to the text file.

    Returns:
    dict: Dictionary containing the number of rows, words, and characters.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            line_count = len(lines)
            word_count = sum(len(line.split()) for line in lines)
            char_count = sum(len(line) for line in lines)

            return {
                "Number of rows": line_count,
                "Number of words": word_count,
                "Number of characters": char_count
            }
    except Exception as e:
        print(f"Failed to read the text file: {e}")
        return {}

def summarize_json_file(filepath):
    """ Summarizes a JSON file, calculating the number of rows, words, and characters.

    Args:
    filepath (str): Path to the JSON file.

    Returns:
    dict: Dictionary containing the number of rows, words, and characters.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        summary = {'Number of rows': 0, 'Number of words': 0, 'Number of characters': 0}
        process_json_content(data, summary)
        return summary
    except Exception as e:
        print(f"Failed to read the JSON file: {e}")
        return {}

def process_json_content(element, summary):
    """ Recursively processes JSON elements to summarize.

    Args:
    element: Current JSON element being processed.
    summary (dict): Dictionary to update the summary.
    """
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






if __name__ == "__main__":
    file_path = 'example_data/data.txt'
    txt_data = summarize_text_file(file_path)

    file_path = 'example_data/data.json'
    json_data = summarize_json_file(file_path)

    file_path = 'example_data/data.csv'
    csv_data = summarize_csv_file(file_path)
    print(txt_data)
    print(json_data)
    print(csv_data)