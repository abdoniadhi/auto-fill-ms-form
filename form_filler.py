import os
import pandas as pd
import time
import logging
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


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
logging.info(f"Option : {param_option}")
param_date = get_env_variable('PARAM_DATE')
logging.info(f"Date : {param_date}")
param_port = get_env_variable('PORT')
logging.info(f"Port : {param_port}")

#set up service for new Selenium Docker
#service = webdriver.ChromeService(port=param_port)

#set option 
#chrome_options = Options()
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--headless")

# Set up Selenium WebDriver with the specified ChromeDriver path Docker
driver = webdriver.Chrome()
logging.info("WebDriver initialized.")
driver.get('https://forms.office.com/Pages/ResponsePage.aspx?id=dAKowprmR0WS2VWRH9i4krE_YecTiCpPscrkI42fbdJUMTEyV0JDMkZYM1FYWlhZTU5YQUxGNEtERC4u')
logging.info("Navigated to the form URL.")

# Loop through each row in the Excel file
for index, row in df.iterrows():
    try:
        logging.info(f"Processing row {index + 1}")

        # Fill in the 'NIK' field
        driver.find_element(By.CSS_SELECTOR, '[aria-labelledby="QuestionId_rb10767da339943b7aa49fb9e26308bd4 QuestionInfo_rb10767da339943b7aa49fb9e26308bd4"]').click()
        logging.info("Clicked on the 'NIK' field.")
        driver.find_element(By.CSS_SELECTOR, '[aria-labelledby="QuestionId_rb10767da339943b7aa49fb9e26308bd4 QuestionInfo_rb10767da339943b7aa49fb9e26308bd4"]').send_keys(row['NIK'])
        logging.info(f"Inserted NIK: {row['NIK']}")

        # Fill in the 'NAMA' field
        driver.find_element(By.CSS_SELECTOR,'[aria-labelledby="QuestionId_r86e5151e706b4b70ac0aed161f470b41 QuestionInfo_r86e5151e706b4b70ac0aed161f470b41"]').click()
        logging.info("Clicked on the 'NAMA' field.")
        driver.find_element(By.CSS_SELECTOR, '[aria-labelledby="QuestionId_r86e5151e706b4b70ac0aed161f470b41 QuestionInfo_r86e5151e706b4b70ac0aed161f470b41"]').send_keys(row['NAMA'])
        logging.info(f"Inserted NAMA: {row['NAMA']}")

        # Set the date
        driver.find_element(By.CSS_SELECTOR, '[aria-labelledby="QuestionId_r8d3dffc8ddf64aff9cc565a8572defb6 QuestionInfo_r8d3dffc8ddf64aff9cc565a8572defb6"]').click()
        logging.info("Clicked on the date field.")
        driver.find_element(By.CSS_SELECTOR, '[aria-labelledby="QuestionId_r8d3dffc8ddf64aff9cc565a8572defb6 QuestionInfo_r8d3dffc8ddf64aff9cc565a8572defb6"]').click()
        logging.info("Clicked on the date field.")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '[aria-labelledby="QuestionId_r8d3dffc8ddf64aff9cc565a8572defb6 QuestionInfo_r8d3dffc8ddf64aff9cc565a8572defb6"]').send_keys(param_date)
        logging.info(f"Inserted Date: {param_date}")
        time.sleep(1)

        # Click to select an option
        driver.find_element(By.CSS_SELECTOR, '[aria-labelledby="QuestionId_r0db7cfb2a11648e6a1dc4f413f0fcadb QuestionInfo_r0db7cfb2a11648e6a1dc4f413f0fcadb"]').click()
        driver.find_element(By.CSS_SELECTOR, f'[value="{param_option}"]').click()
        logging.info(f"Selected the option {param_option}.")

        # Submit
        driver.find_element(By.CSS_SELECTOR, '[data-automation-id="submitButton"]').click()
        logging.info("Clicked to proceed to next step.")
        time.sleep(3)
        # Back to home
        driver.get('https://forms.office.com/Pages/ResponsePage.aspx?id=dAKowprmR0WS2VWRH9i4krE_YecTiCpPscrkI42fbdJUMTEyV0JDMkZYM1FYWlhZTU5YQUxGNEtERC4u')
        logging.info("Navigated to the form URL.")

        # Log row submission
        logging.info(f"Submitted row {index + 1}")
        time.sleep(2)
    except Exception as e:
        driver.quit()
        logging.error(f"Error processing row {index + 1}: {e}")

# Close the browser after the process is complete
driver.quit()
logging.info("Browser closed. Automation complete.")
logging.info(f"Isi Absen {param_option} pada tanggal {param_date} selesai. ^_^")
