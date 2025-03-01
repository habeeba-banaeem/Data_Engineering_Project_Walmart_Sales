# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Copy the Python script to the container
COPY Elt_script.py /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Google Cloud credentials file into the container
COPY imposing-byway-451600-p2-2c4bad5aa5c7.json /app/imposing-byway-451600-p2-2c4bad5aa5c7.json

# Set the Google Cloud credentials environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/imposing-byway-451600-p2-2c4bad5aa5c7.json"

# Expose the port the app runs on
EXPOSE 8080

# Command to run the correct Python script
CMD ["python", "Elt_script.py"]
