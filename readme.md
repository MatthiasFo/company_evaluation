# Stock Evaluation Project

## Purpose

The Stock Evaluation Project is designed to fetch, process, and analyze stock data from various financial APIs, including Yahoo Finance and Alpha Vantage. The project aims to provide insights into company performance and financial health by leveraging data from multiple sources. It utilizes tools like Terraform for infrastructure management and dbt for data transformation and modeling. The application code is written in Python and deployed via Github Actions to Google Cloud Platform.

## Features

- **Data Ingestion**: Automatically fetch stock data from multiple APIs.
- **Data Storage**: Store the fetched data in Google BigQuery for efficient querying and analysis.
- **Data Transformation**: Use dbt to transform raw data into structured models for analysis.
- **Scheduling**: Set up scheduled jobs to regularly fetch and update stock data.
- **CI/CD Integration**: Deploy the application using GitHub Actions for continuous integration and deployment.

## Usage

### Prerequisites

1. **Terraform**: Ensure you have Terraform installed to manage the infrastructure.
2. **Google Cloud SDK**: Install the Google Cloud SDK and authenticate your account.
3. **Python**: Make sure Python is installed along with the required libraries.

### Setup

1. **Install Requirements**:
   Set up a virtual environment and install the required Python packages:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
   - You need to put your GCP project id into the python adapters for secret manager and big query

2. **Terraform Configuration**:
    - You need to fill the `locals.tf` with your GCP data (project-id, region and default compute service account)

   - Initialize and apply the Terraform configuration:
   ```bash
   cd infrastructure
   terraform init
   terraform apply
   ```
   - Sets up your Google Cloud project and enable the necessary APIs (BigQuery, Cloud Run, etc.).
   - Creates a service account with the required permissions for CI/CD

3. **Schedule Jobs**:
   - Use the configured Cloud Scheduler to automate the data fetching process.

### Running dbt

1. **Set Up dbt**:
   - Ensure you have dbt installed and configured to connect to your BigQuery instance (adapt the `profiles.yml`).
   - Run the dbt models to transform the data:
   ```bash
   dbt build
   ```

### Deployment

- The project is set up for CI/CD using GitHub Actions. Upon pushing changes to the master branch, the application will automatically build and deploy to Google Cloud Run.
- You need to put credentials for the CI/CD service account into the Github secrets (`GCP_CREDENTIALS` and `GCP_PROJECT_ID`)

### TODOs

- stop allowing unauthenticated calls to Cloud Run