# Use an official Python runtime as a parent image
FROM python:alpine
# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apk update && \
    apk add --no-cache wget gnupg unzip && \
    rm -rf /var/cache/apk/*


# Add ChromeDriver
RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.78/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Set display port to avoid crash
ENV DISPLAY=:99

# Create and set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set default values for environment variables
ENV EXCEL_FILE="TESTING-FILE.xlsx"
ENV PARAM_OPTION="Badminton - Cyber Office"
ENV PARAM_DATE="3/28/2024"

# Run the script when the container launches
CMD ["python", "./form_filler.py"]
