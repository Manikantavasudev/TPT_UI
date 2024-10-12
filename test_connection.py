import pytest
import logging
import os
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time
import yaml



@pytest.fixture
def driver_setup():
    logging.info("Setting up the browser for the test.")  
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    
    # Quit the driver after the test is done
    logging.info("Tearing down the browser after the test.")
    driver.quit()

def exe_yaml_dict():
    try:
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        logging.error("YAML config file not found.")
        raise
    except yaml.YAMLError as e:
        logging.error(f"Error reading YAML file: {str(e)}")
        raise

def yaml_msg(value):
    config = exe_yaml_dict()
    message = config.get(value, f"Message for {value} not found in YAML")
    return message

def read_file(path):
    try:
        with open(path, "r") as rf:
            values = json.load(rf)
        return values
    except FileNotFoundError:
        logging.error(f"File {path} not found.")
        raise
    except json.JSONDecodeError:
        logging.error(f"File {path} is not a valid JSON or is empty.")
        raise
Xpath = read_file('Xpath.json')



# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

directory_path = r"C:\GRL\GRL-C3-MP-TPT"


# Test to check the presence of ReadMe.txt
def test_check_readme_file():
    logging.info("*************** TC-1 ***************")
    logging.info("Check the ReadMe File is present")

    readme_path = os.path.join(directory_path, "ReadMe.txt")
    
    try:
        assert os.path.exists(readme_path), f"The ReadMe file was not found in the directory at: {directory_path}"
        logging.info(f"The ReadMe file was found at: {readme_path}")
    except AssertionError as e:
        logging.error(f"Test failed: {str(e)}")
        pytest.fail(str(e))


# Test to check the presence of Release Notes file
def test_check_release_file():
    logging.info("*************** TC-2 ***************")
    logging.info("Check the Release Notes File is present")

    release_notes_path = os.path.join(directory_path, "GRL-C3-TPT Release Notes.pdf")
    
    try:
        assert os.path.exists(release_notes_path), f"The Release Notes file does not exist at: {release_notes_path}"
        logging.info(f"The Release Notes file exists at: {release_notes_path}")
    except AssertionError as e:
        logging.error(f"Test failed: {str(e)}")
        pytest.fail(str(e))


# Test to check the presence of PPS_ELOAD.bin file
def test_check_eloadfile():
    logging.info("*************** TC-3 ***************")
    logging.info("Check the Eload File is present")
    directory_path = r"C:\GRL\GRL-C3-MP-TPT\Firmware_Files\BPP_EPP"

    pps_eloadfile = os.path.join(directory_path, "PPS_ELOAD.bin")
    
    try:
        assert os.path.exists(pps_eloadfile), f"PPS_ELOAD.bin was not found in the directory at: {pps_eloadfile}"
        logging.info(f"PPS_ELOAD.bin was found at: {pps_eloadfile}")
    except AssertionError as e:
        logging.error(f"Test failed: {str(e)}")
        pytest.fail(str(e))


# Test to check the presence of Firmware Files
def test_check_firmware_file():
    logging.info("*************** TC-4 ***************")
    logging.info("Check all the Firmware Files are present")

    firmware_directory = r"C:\GRL\GRL-C3-MP-TPT\Firmware_Files\BPP_EPP"
    files_to_check = ["BOOT.BIN", "image.ub", "start.sh", "PPS_ELOAD.bin"]

    missing_files = []

    for file in files_to_check:
        file_path = os.path.join(firmware_directory, file)
        if not os.path.exists(file_path):
            missing_files.append(file)

    if missing_files:
        logging.error(f"Missing files: {', '.join(missing_files)}")
        pytest.fail(f"The following files are missing: {', '.join(missing_files)}")
    else:
        logging.info("All firmware files are present")


# Initialize WebDriver
def initialize_browser(browser_type='chrome'):
    try:
        if browser_type == 'chrome':
            driver = webdriver.Chrome()  # Chrome Driver
        elif browser_type == 'firefox':
            driver = webdriver.Firefox()  # Firefox Driver
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
        
        driver.get(Xpath['URL'])
        driver.maximize_window()
        logging.info("The browser has been successfully opened and landed on the connection setup page.")
        return driver
    except WebDriverException as e:
        logging.error(f"Browser initialization failed: {str(e)}")
        raise

        raise


# Test to open the browser
def test_tc5_open_browser():
    logging.info("*************** TC-5 ***************")
    logging.info("Open Browser")
    
    driver = None
    try:
        driver = initialize_browser()
        # Add additional steps after browser initialization if necessary
    except Exception as e:
        logging.error(f"Test failed: {str(e)}")
        pytest.fail(f"Browser test failed: {str(e)}")
    finally:
        if driver:
            try:
                driver.quit()
                logging.info("Browser closed.")
            except Exception as quit_error:
                logging.error(f"Failed to close browser: {quit_error}")

def BrowserTitle(driver_setup):
    act_title = driver_setup.title
    return act_title
def test_tc6_browser_tab_title(driver_setup):
    logging.info("*************** TC-6 ***************")
    logging.info("Browser Tab Title")

    pass_or_fail = "Pass"
    remark = ""
    time.sleep(4)

    try:
        actual_title = BrowserTitle(driver_setup)

        # Check for a specific condition
        if actual_title == 'GRL-C3-TPT Software':
            expected_title = yaml_msg("BPP")
        else:
            expected_title = yaml_msg("TITLE")  # Assuming TITLE from YAML for comparison
            
            logging.info(f"Test failed: The browser title is different. Expected: {expected_title}, Actual: {actual_title}")

        # Compare the actual and expected titles
        if actual_title == expected_title:
            logging.info(f"The browser title in the UI tab is: {actual_title}")
        else:
            logging.critical(
                f"Browser title mismatch. Actual Value: {actual_title}, Expected Value: {expected_title}")
            pass_or_fail = "Fail"

        time.sleep(5)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        pass_or_fail = "Fail"
        remark = str(e)


        
# Run the test manually for demonstration purposes
if __name__ == "__main__":
    test_check_readme_file()
    test_check_release_file()
    test_check_eloadfile()
    test_check_firmware_file()
    test_tc5_open_browser()
    test_tc6_browser_tab_title()