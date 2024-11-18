# Use an official Python runtime as a parent image
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apk update && \
    apk add --no-cache gnupg udev ttf-freefont bash chromium chromium-chromedriver && \
    rm -rf /var/cache/apk/*

# Set display port to avoid crash
ENV DISPLAY=:99

# Create and set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set default values for environment variables
ENV EXCEL_FILE="coba.xlsx"
ENV PARAM_OPTION="Badminton - Cyber Office"
ENV PARAM_DATE="10/07/2024"

# Run the script when the container launches
CMD ["python", "./form_filler.py"]
