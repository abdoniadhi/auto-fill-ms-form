import os
import pandas as pd
import time
import logging
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get environment variable and exit if not found
def get_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        logging.error(f"Environment variable {var_name} not found. Exiting.")
        sys.exit(1)
    return value

# Read the Excel file path from environment variables
excel_file = get_env_variable('EXCEL_FILE')
logging.info(f"Loading Excel file: {excel_file}")

# Load data from Excel file
df = pd.read_excel(excel_file)
logging.info("Excel file loaded successfully.")

# Read other parameters from environment variables
param_option = get_env_variable('PARAM_OPTION')
logging.info(f"Option: {param_option}")
param_date = get_env_variable('PARAM_DATE')
logging.info(f"Date: {param_date}")
param_port = get_env_variable('PORT')
logging.info(f"Port: {param_port}")

# Set up Selenium WebDriver
# Path to your Chrome user data directory
user_data_dir = "/app/user-data"

# Profile you want to use (e.g., "Default" or "Profile 1")
profile_dir = "Default"

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={user_data_dir}")
options.add_argument(f"profile-directory={profile_dir}")
options.add_argument("--no-sandbox")  # Required when running as root in Docker
options.add_argument("--disable-dev-shm-usage")  # May help if there are shared memory issues
#options.add_argument("--headless")  # Optional: Runs Chrome in headless mode
options.add_argument("--disable-gpu")  # Optional: Disables GPU acceleration
options.add_argument("start-maximized")  # Optional: Starts Chrome in maximized mode

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

logging.info("WebDriver initialized.")
driver.get('https://forms.office.com/Pages/ResponsePage.aspx?id=dAKowprmR0WS2VWRH9i4krE_YecTiCpPscrkI42fbdJUMTEyV0JDMkZYM1FYWlhZTU5YQUxGNEtERC4u')
logging.info("Navigated to the form URL.")
time.sleep(20)
# Define a wait object
wait = WebDriverWait(driver, 10)

# Loop through each row in the Excel file
for index, row in df.iterrows():
    try:
        logging.info(f"Processing row {index + 1}")

        # Fill in the 'NIK' field
        nik_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-labelledby="QuestionId_rb10767da339943b7aa49fb9e26308bd4 QuestionInfo_rb10767da339943b7aa49fb9e26308bd4"]')))
        nik_element.click()
        logging.info("Clicked on the 'NIK' field.")
        nik_element.send_keys(row['NIK'])
        inserted_nik = nik_element.get_attribute('value').strip()
        logging.info(f"Inserted NIK: {inserted_nik}")
        assert inserted_nik == str(row['NIK']).strip(), f"NIK field value mismatch: expected {row['NIK']}, got {inserted_nik}"

        # Fill in the 'NAMA' field
        nama_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-labelledby="QuestionId_r86e5151e706b4b70ac0aed161f470b41 QuestionInfo_r86e5151e706b4b70ac0aed161f470b41"]')))
        nama_element.click()
        logging.info("Clicked on the 'NAMA' field.")
        nama_element.send_keys(row['NAMA'])
        inserted_nama = nama_element.get_attribute('value').strip()
        logging.info(f"Inserted NAMA: {inserted_nama}")
        assert inserted_nama == str(row['NAMA']).strip(), f"NAMA field value mismatch: expected {row['NAMA']}, got {inserted_nama}"

        # Set the date
        date_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-labelledby="QuestionId_r8d3dffc8ddf64aff9cc565a8572defb6 QuestionInfo_r8d3dffc8ddf64aff9cc565a8572defb6"]')))
        #date_element.click()
        #logging.info("Clicked on the date field.")
        date_element.send_keys(param_date)
        inserted_date = date_element.get_attribute('value').strip()
        logging.info(f"Inserted Date: {inserted_date}")
        assert inserted_date == param_date.strip(), f"Date field value mismatch: expected {param_date}, got {inserted_date}"

        # Click to select an option
        #option_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-labelledby="QuestionId_r0db7cfb2a11648e6a1dc4f413f0fcadb QuestionInfo_r0db7cfb2a11648e6a1dc4f413f0fcadb"]')))
        #option_element.click()
        #logging.info("Clicked on the option field.")
        driver.find_element(By.CSS_SELECTOR, f'[value="{param_option}"]').click()
        logging.info(f"Selected the option {param_option}.")

        # Submit
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-automation-id="submitButton"]')))
        submit_button.click()
        logging.info("Clicked to proceed to next step.")
        time.sleep(3)
        # Back to home
        driver.get('https://forms.office.com/Pages/ResponsePage.aspx?id=dAKowprmR0WS2VWRH9i4krE_YecTiCpPscrkI42fbdJUMTEyV0JDMkZYM1FYWlhZTU5YQUxGNEtERC4u')
        logging.info("Navigated to the form URL.")

        # Log row submission
        logging.info(f"Submitted row {index + 1}")
        time.sleep(2)
    except AssertionError as e:
        logging.error(f"Assertion error on row {index + 1}: {e}")
        driver.quit()
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error processing row {index + 1}: {e}")
        driver.quit()
        sys.exit(1)

# Close the browser after the process is complete
driver.quit()
logging.info("Browser closed. Automation complete.")
logging.info(f"Isi Absen {param_option} pada tanggal {param_date} selesai. ^_^")
