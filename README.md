# Data_Engineering_Project_Walmart_Sales
Automated ELT pipeline for Walmart sales data with Power BI visualization

## Project Overview
This project focuses on building a **data pipeline** to process and analyze Walmart sales data. It involves **extracting, loading, and transforming (ELT)** the data, which is then visualized using Power BI. The workflow is orchestrated using **Google Cloud Storage, BigQuery, Docker, and Cloud Run** to automate the ELT process.

### Problem Statement
Walmart requires a **sales analytics platform** to track revenue, customer trends, and product performance across different stores. The objective is to **ingest, process, and visualize** Walmart sales data efficiently to support business decision-making.

### Objectives
The primary objectives of this project are:
1. To build an automated ELT pipeline for processing Walmart sales data.
2. To create an interactive Power BI dashboard for visualizing sales trends and customer insights.
3. To deploy the pipeline on Google Cloud Run for scalability and automation.

### Project Structure
📂 **Google Cloud Storage:** Stores the raw CSV sales data.

📂 **BigQuery:** Serves as the data warehouse, where raw data is ingested and transformed.

📂 **Cloud Run (Dockerized Python Script):** Automates the ELT pipeline by fetching data from Cloud Storage and loading it into BigQuery.

📂 **Power BI Dashboard:** Visualizes sales trends, revenue insights, and customer behavior.
![image](https://github.com/user-attachments/assets/f4fb50dd-91c6-4056-9802-87782c753ef4)

### Technologies Used
- **Programming Languages**: Python, SQL
- **Cloud Services**: Google Cloud Storage, Google BigQuery, Google Cloud Run
- **Visualization**: Power BI
- **Containerization**: Docker
- **Version Control**: GitHub

### Data Collection and Storage
The dataset consists of Walmart sales data stored in CSV format, containing columns like:

Invoice ID
Branch & City
Customer Type & Gender
Product Line, Quantity, and Unit Price
Total Sales & Tax Amount
Date & Time of Purchase
Payment Method & Rating

### Google Cloud Storage
The raw CSV file is uploaded to a Google Cloud Storage bucket for processing.

### Data Processing and Transformation
A Dockerized Python script is deployed to Google Cloud Run, automating the ELT process:

Extracts CSV data from Google Cloud Storage.
Loads raw data into BigQuery without transformations.
Transforms data in BigQuery using SQL, including:
Cleaning null values.
Converting date/time formats.
Calculating total revenue, tax, and sales metrics.

### Data Analysis and Insights 
**BigQuery SQL Transformations
The primary transformation performed is on date formatting to ensure consistency across different formats. The transformation logic:
Converts Date from mixed formats (%m/%d/%Y and %d/%m/%Y) into a unified format using COALESCE(SAFE.PARSE_DATE(...)). Extracts Year, Month, and Day from the formatted date for time-based analysis. Potential Future Transformations Although the current transformation mainly handles date standardization, additional queries can be created to extract more insights:

Total Sales per Branch: Aggregates revenue per store location. Best-Selling Product Lines: Identifies top-performing product categories. Customer Segmentation: Analyzes spending patterns based on gender and customer type. Peak Sales Periods: Determines high-traffic days/times for strategic decision-making.

### PowerBI Dashboard
This project visualizes Walmart sales data using Power BI, providing insights into sales trends, customer behavior, and payment preferences. Key features include:
📈 Total Revenue & Sales Trends: A line chart tracks sales over time. 🏆 Top 3 Selling Product Lines: The most popular categories by gender. 💳 Payment Methods Breakdown: Pie chart shows the proportion of cash, e-wallet, and credit card transactions. 🏙️ Sales by City: Pie chart displays total revenue distribution across Mandalay, Naypyitaw, and Yangon. 🛍️ Branch & Customer Type: Bar chart shows total sales categorized by branch and customer type (Member vs. Normal). 💰 Gross Income Analysis: Displays total earnings from sales.

### Orchestration with Docker & Cloud Run
Docker & Cloud Run
Dockerfile: Defines the Python environment for processing Walmart sales data.
Cloud Run Deployment: Automates ELT execution.

### Getting Started
**Prerequisites**
✅ Google Cloud SDK & gcloud CLI
✅ Docker & Docker Compose
✅ Python 3.8+
✅ Google Cloud Account (BigQuery & Cloud Storage)

## Installation
1️⃣ Clone the Repository
   ```bash
   git clone https://github.com/habeeba-banaeem/Data_Engineering_Project_Walmart_Sales.git

2️⃣ Build & Run Docker Containers
   ```bash
docker-compose up --build

3️⃣ Deploy to Google Cloud Run
   ```bash
gcloud builds submit --tag gcr.io/your-project-id/walmart-sales-pipeline
gcloud run deploy walmart-sales-service --image gcr.io/your-project-id/walmart-sales-pipeline --platform managed
4️⃣ Check BigQuery Data
Open BigQuery UI and check if the tables have been updated.
5️⃣ View the Power BI Dashboard
Access the Power BI report embedded in index.html.

### Usage
🚀 Automated Sales Data Processing
📊 Real-Time Sales Dashboard in Power BI
📈 Business Insights for Decision-Making


