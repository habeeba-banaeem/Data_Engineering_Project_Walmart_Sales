from google.cloud import storage, bigquery
import pandas as pd
import io
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "imposing-byway-451600-p2-2c4bad5aa5c7.json"

# Define Google Cloud variables
GCS_BUCKET_NAME = "walmart-hackathon"
CSV_FILE_NAME = "Walmart_Sales_Data.csv"  # Ensure this matches exactly
BQ_PROJECT = "imposing-byway-451600-p2"
BQ_DATASET = "walmart_sales_data"
BQ_TABLE = "walmart_sales"

def extract_data_from_gcs():
    """Extract CSV file from Google Cloud Storage and load into Pandas DataFrame."""
    try:
        logging.info("Extracting data from GCS...")
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(CSV_FILE_NAME)
        
        # Read file as string and convert to DataFrame
        data = blob.download_as_string()
        df = pd.read_csv(io.BytesIO(data))

        logging.info(f"Extracted {len(df)} rows successfully.")
        return df
    except Exception as e:
        logging.error(f"Error in extracting data from GCS: {str(e)}")
        raise

def load_raw_data_to_bigquery(df):
    """Loads the raw CSV data into BigQuery (staging table) with explicit schema."""
    try:
        logging.info("Loading raw data to BigQuery (staging table)...")
        client = bigquery.Client()
        table_ref = f"{BQ_PROJECT}.{BQ_DATASET}.walmart_sales_staging"  # Staging table
        
        # Note: We define 'Date' and 'Time' as STRING because the CSV dates might be in 
        # different formats (mm/dd/yyyy or dd/mm/yyyy) and cannot be parsed automatically.
        schema = [
            bigquery.SchemaField("Invoice ID", "STRING"),
            bigquery.SchemaField("Branch", "STRING"),
            bigquery.SchemaField("City", "STRING"),
            bigquery.SchemaField("Customer type", "STRING"),
            bigquery.SchemaField("Gender", "STRING"),
            bigquery.SchemaField("Product line", "STRING"),
            bigquery.SchemaField("Unit price", "FLOAT"),
            bigquery.SchemaField("Quantity", "INTEGER"),
            bigquery.SchemaField("Tax 5%", "FLOAT"),
            bigquery.SchemaField("Total", "FLOAT"),
            bigquery.SchemaField("Date", "STRING"),    # Load as STRING to avoid parsing errors
            bigquery.SchemaField("Time", "STRING"),    # Load as STRING (if needed)
            bigquery.SchemaField("Payment", "STRING"),
            bigquery.SchemaField("cogs", "FLOAT"),
            bigquery.SchemaField("gross margin percentage", "FLOAT"),
            bigquery.SchemaField("gross income", "FLOAT"),
            bigquery.SchemaField("Rating", "FLOAT")
        ]
        
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",
            create_disposition="CREATE_IF_NEEDED",
            source_format=bigquery.SourceFormat.CSV,
            schema=schema  # Use the explicit schema
        )
        
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()  # Wait for the job to complete
        
        logging.info("Raw data successfully loaded into BigQuery staging table!")
    except Exception as e:
        logging.error(f"Error in loading raw data to BigQuery: {str(e)}")
        raise

def transform_data_in_bigquery():
    """Performs transformations within BigQuery using SQL."""
    try:
        logging.info("Transforming data within BigQuery...")
        client = bigquery.Client()

        # Use COALESCE with SAFE.PARSE_DATE to attempt both formats.
        query = f"""
        CREATE OR REPLACE TABLE `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}` AS
        SELECT 
            `Invoice ID`, 
            Branch, 
            City, 
            `Customer type`, 
            Gender, 
            `Product line`, 
            `Unit price`, 
            Quantity, 
            `Tax 5%`, 
            Total, 
            COALESCE(
                SAFE.PARSE_DATE('%m/%d/%Y', Date), 
                SAFE.PARSE_DATE('%d/%m/%Y', Date)
            ) AS Date,
            EXTRACT(YEAR FROM COALESCE(
                SAFE.PARSE_DATE('%m/%d/%Y', Date), 
                SAFE.PARSE_DATE('%d/%m/%Y', Date)
            )) AS Year,
            EXTRACT(MONTH FROM COALESCE(
                SAFE.PARSE_DATE('%m/%d/%Y', Date), 
                SAFE.PARSE_DATE('%d/%m/%Y', Date)
            )) AS Month,
            EXTRACT(DAY FROM COALESCE(
                SAFE.PARSE_DATE('%m/%d/%Y', Date), 
                SAFE.PARSE_DATE('%d/%m/%Y', Date)
            )) AS Day,
            Time, 
            Payment, 
            cogs, 
            `gross margin percentage`, 
            `gross income`, 
            Rating
        FROM `{BQ_PROJECT}.{BQ_DATASET}.walmart_sales_staging`;
        """

        job = client.query(query)
        job.result()  # Wait for the job to complete
        
        logging.info("Transformation completed successfully in BigQuery!")
    except Exception as e:
        logging.error(f"Error in transforming data in BigQuery: {str(e)}")
        raise

def main():
    """ELT Pipeline Execution."""
    try:
        df = extract_data_from_gcs()
        load_raw_data_to_bigquery(df)  # Load raw data (staging)
        transform_data_in_bigquery()   # Transform within BigQuery
        logging.info("ELT Process Completed Successfully! 🚀")
    except Exception as e:
        logging.error(f"ELT process failed: {str(e)}")

if __name__ == "__main__":
    main()
