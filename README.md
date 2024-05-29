# Selenium Form Automation

This project automates the process of filling out a specific online form using data from an Excel file. It leverages Selenium for browser automation and Docker for containerization.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Docker installed on your machine
- An Excel file named `user.xlsx` or any other file that you can specify via environment variables
- The necessary environment variables set up (detailed below)

## Setup and Usage

### Clone the Repository

### Environment Variables

Create a `.env` file in the project directory with the following variables:

- EXCEL_FILE=TESTING-FILE.xlsx
- PARAM_OPTION=Badminton - Cyber Office
- PARAM_DATE=3/28/2024

### Build Docker Image

docker build -t selenium-automation .

### Run the Docker Container

Run the container with the environment variables specified in the `.env` file:
