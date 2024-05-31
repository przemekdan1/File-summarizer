## Flask Project Documentation

### Table of Contents
1. [Overview](#overview)
2. [Setup Instructions](#setup-instructions)
3. [Running the Application](#running-the-application)
4. [Accessing the Application](#accessing-the-application)
5. [Prometheus Metrics](#prometheus-metrics)

### Overview

This project provides a Flask application that processes uploaded text files (CSV, TXT, JSON) and outputs summaries of the processed data. The application also exposes metrics for monitoring performance and health using Prometheus and Grafana.

### Build with

![Flask](https://img.shields.io/badge/Flask-3.0.3-green)
![Prometheus Client](https://img.shields.io/badge/Prometheus%20Client-0.20.0-red)]
![Pandas](https://img.shields.io/badge/Pandas-1.5.0-yellow)]
![NumPy](https://img.shields.io/badge/NumPy-1.23.5-purple)]
![Docker](https://img.shields.io/badge/Docker-latest-orange)]
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-latest-pink)]
![Prometheus](https://img.shields.io/badge/Prometheus-latest-teal)]
![Grafana](https://img.shields.io/badge/Grafana-latest-violet)]



### Setup Instructions

#### Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

#### Cloning the Repository

Clone the project repository from GitHub:

```bash
git clone https://github.com/przemekdan1/File-summarizer.git
cd flaskProject
```

### Running the Application
### Configuration

The project uses a configuration file to set up various parameters, including the port for Prometheus metrics exposition.

**config.py**

```python
class Config(object):
    DEBUG = False
    TESTING = False
    PROMETHEUS_PORT = 8000  # Default port for Prometheus metrics
    ENABLE_PROMETHEUS = True  # Flag to enable/disable Prometheus metrics

class ProductionConfig(Config):
    PROMETHEUS_PORT = 9090  # Different port in production
    ENABLE_PROMETHEUS = True

class DevelopmentConfig(Config):
    DEBUG = True
    PROMETHEUS_PORT = 8000
    ENABLE_PROMETHEUS = True

class TestingConfig(Config):
    TESTING = True
    PROMETHEUS_PORT = 8001
    ENABLE_PROMETHEUS = False  # Typically disable Prometheus in testing
```

### Running the Service

1. **Build and Run with Docker Compose:**

    ```bash
    docker-compose up --build
    ```

2. **Access the Web Interface:**

    Open your web browser and navigate to `http://127.0.0.1:5000`.

3. **Upload a File:**

    - Select a file (`.csv`, `.txt`, `.json`) using the "Choose File" button.
    - Click the "Upload" button.
    - The service will process the file and display a JSON summary of its content.

4. **View Metrics:**

    Prometheus will scrape metrics from the Flask service. Metrics can be accessed at `http://localhost:9090/metrics`.

### Accessing the Application

- **Flask Application:** [http://localhost:5000](http://localhost:5000)
  - Upload files and get summaries.

- **Prometheus:** [http://localhost:8000/metrics](http://localhost:8000/metrics)
  - Access the Prometheus raw metrics
  
- **Prometheus:** [http://localhost:9090](http://localhost:9090)
  - Access the Prometheus UI to query metrics.

- **Grafana:** [http://localhost:3000](http://localhost:3000)
  - Default login: `admin/admin`
  - Set up dashboards to visualize metrics.


### File Processing

The service processes different file types as follows:

- **CSV Files:** Summarizes unique values and computes statistical measures for numerical columns.
- **Text Files:** Calculates the number of rows, words, characters, and searches for email addresses and phone numbers.
- **JSON Files:** Counts rows, words, and characters.

### Example

**Uploading a CSV File**

1. Select a CSV file.
2. Click "Upload".
3. Receive a JSON response:

    ```json
    {
        "Email": {
            "Unique Values": [
                "jan.kowalski@example.com",
                "anna.nowak@example.com",
                "piotr.wisniewski@example.com"
            ]
        },
        "Imie": {
            "Unique Values": [
                "Jan",
                "Anna",
                "Piotr"
            ]
        },
        "Nazwisko": {
            "Unique Values": [
                "Kowalski",
                "Nowak",
                "Wiśniewski"
            ]
        },
        "Wiek": {
            "Average": 34.333333333333336,
            "Median": 35,
            "Standard Deviation": 6.02771377334171,
            "Sum": 103,
            "Unique Values": [
                28,
                35,
                40
            ]
        }
    }
    ```

### Prometheus Metrics

Prometheus is configured to scrape metrics from the Flask application. The metrics endpoint is exposed at `http://localhost:8000/metrics`.

#### Exposed Metrics

1. **`files_processed_total`:** Total number of files processed.

   
   ![image](https://github.com/przemekdan1/File-summarizer/assets/101727232/0aaf782e-350a-478f-b9c9-75758e40e4be)

3. **`file_processing_seconds`:** Time spent processing a file.

   

  ![image](https://github.com/przemekdan1/File-summarizer/assets/101727232/595b9239-8a8b-4ba2-9fd7-47f7ea6e5594)

5. **`file_processing_errors_total`:** Total file processing errors encountered.

   

   ![image](https://github.com/przemekdan1/File-summarizer/assets/101727232/dae72465-fa54-4776-8d43-77596b8f3fae)

7. **`file_processing_in_progress`:** Number of files currently being processed.



   ![image](https://github.com/przemekdan1/File-summarizer/assets/101727232/52b6982f-3fe1-4cd9-ac7c-73feb4a79bf0)


### 1. Performance Metrics
- **Total Number of Files Processed (`files_processed_total`)**
  - **Type:** Counter
  - **Description:** Tracks the total number of files successfully processed.
- **File Processing Time (`file_processing_seconds`)**
  - **Type:** Histogram
  - **Description:** Measures the time taken to process each file.
- **File Processing Duration Percentiles**
  - **Type:** Histogram with predefined buckets
  - **Description:** Provides insights into the distribution of processing times, useful for identifying outliers and ensuring the system meets performance SLAs.

### 2. Health Metrics
- **Total Number of Errors (`file_processing_errors_total`)**
  - **Type:** Counter
  - **Description:** Counts the total number of errors encountered during file processing.
- **Current Files Being Processed (`file_processing_in_progress`)**
  - **Type:** Gauge
  - **Description:** Tracks the number of files currently being processed. This helps in monitoring the real-time load on the system.

### 3. System Metrics (Optional)
- **Memory Usage**
  - **Type:** Gauge
  - **Description:** Tracks the memory usage of the application.
- **CPU Usage**
  - **Type:** Gauge
  - **Description:** Tracks the CPU usage of the application.

### 4. Application-Specific Metrics
- **File Type Metrics**
  - **Counters for Different File Types**
    - **Description:** Track the number of each type of file processed (e.g., CSV, JSON, TXT). Helps in understanding the usage patterns.
- **Custom Business Logic Metrics**
  - **Custom Counters, Gauges, or Histograms**
    - **Description:** Track any specific metrics relevant to your business logic, such as the size of files processed, number of records processed, etc.



## Contributing

Feel free to submit issues, fork the repository, and send pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---