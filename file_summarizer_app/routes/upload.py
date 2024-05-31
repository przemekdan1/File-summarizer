import os
import tempfile

from flask import request, jsonify, Blueprint
from prometheus_client import Counter, Histogram, Gauge

from file_summarizer_app.services.data_handler import summarize_text_file, summarize_csv_file, summarize_json_file


FILES_PROCESSED = Counter('files_processed_total', 'Total number of files processed')
FILE_PROCESSING_TIME = Histogram('file_processing_seconds', 'Time spent processing a file')
PROCESSING_ERRORS = Counter('file_processing_errors_total', 'Total file processing errors encountered')
PROCESSING_IN_PROGRESS = Gauge('file_processing_in_progress', 'Number of files currently being processed')

upload = Blueprint('upload', __name__)

@upload.route('/upload', methods=['POST'])
def upload_file():
    PROCESSING_IN_PROGRESS.inc()
    with FILE_PROCESSING_TIME.time():
        if 'file' not in request.files:
            PROCESSING_IN_PROGRESS.dec()
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            PROCESSING_IN_PROGRESS.dec()
            return jsonify({'error': 'No selected file'}), 400
        if file:
            suffix = os.path.splitext(file.filename)[1]
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            try:
                file.save(temp.name)
                temp.close()
                if suffix in ['.csv']:
                    result = summarize_csv_file(temp.name)
                elif suffix in ['.txt']:
                    result = summarize_text_file(temp.name)
                elif suffix in ['.json']:
                    result = summarize_json_file(temp.name)
                else:
                    PROCESSING_ERRORS.inc()
                    return jsonify({'error': 'Unsupported file type'}), 400
                FILES_PROCESSED.inc()
                return jsonify(result), 200
            except Exception as e:
                PROCESSING_ERRORS.inc()
                return jsonify({'error': str(e)}), 500
            finally:
                os.unlink(temp.name)
                PROCESSING_IN_PROGRESS.dec()