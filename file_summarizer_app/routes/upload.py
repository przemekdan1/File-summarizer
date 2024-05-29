import os
import tempfile

from flask import request, jsonify, Blueprint

from file_summarizer_app.services.data_handler import summarize_text_file,summarize_csv_file,summarize_json_file

upload = Blueprint('upload', __name__)

@upload.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            file.save(temp.name)
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