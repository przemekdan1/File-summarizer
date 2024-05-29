import os
import tempfile

from flask import Flask, request, render_template, jsonify
from data_handler import summarize_csv_file, summarize_text_file, summarize_json_file

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        # Zapisz plik tymczasowo
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            file.save(temp.name)
            # Wywołaj odpowiednią funkcję przetwarzającą na podstawie typu pliku
            if suffix in ['.csv']:
                result = summarize_csv_file(temp.name)
            elif suffix in ['.txt']:
                result = summarize_text_file(temp.name)
            elif suffix in ['.json']:
                result = summarize_json_file(temp.name)
            else:
                os.unlink(temp.name)
                return jsonify({'error': 'Unsupported file type'}), 400
            try:
                os.unlink(temp.name)
            except PermissionError as e:
                print(f"Nie można usunąć pliku: {e}")

            return jsonify(result), 200


