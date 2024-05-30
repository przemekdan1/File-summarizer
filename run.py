from prometheus_client import start_http_server
from file_summarizer_app import create_app

app = create_app()

if __name__ == "__main__":
    start_http_server(8000)
    app.run(debug=1)
