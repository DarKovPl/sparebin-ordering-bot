import os
import datetime


# Project Directory Setup
folders_date = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
settings_file_path = os.path.dirname(os.path.abspath(__file__))
project_root_dir_path = os.path.dirname(settings_file_path)
data_folder_path = os.path.join(project_root_dir_path, "data")
OUTPUT_DATA_FOLDER_PATH = os.path.join(project_root_dir_path, "output")
SCREENSHOTS_FOLDER_PATH = os.path.join(OUTPUT_DATA_FOLDER_PATH, "screenshots")
err_screenshot_folder_path = os.path.join(
    SCREENSHOTS_FOLDER_PATH, f"err_robot_order_{folders_date}"
)
ordered_robot_folder_path = os.path.join(
    SCREENSHOTS_FOLDER_PATH, f"ordered_robot_{folders_date}"
)
RESULTS_PDF_FOLDER_PATH = os.path.join(
    OUTPUT_DATA_FOLDER_PATH, f"results_pdfs_{folders_date}"
)

def check_dirs_exist():
    os.makedirs(data_folder_path, exist_ok=True)
    os.makedirs(OUTPUT_DATA_FOLDER_PATH, exist_ok=True)
    os.makedirs(SCREENSHOTS_FOLDER_PATH, exist_ok=True)
    os.makedirs(err_screenshot_folder_path, exist_ok=True)
    os.makedirs(ordered_robot_folder_path, exist_ok=True)
    os.makedirs(RESULTS_PDF_FOLDER_PATH, exist_ok=True)

# Project configuration
FILES_DATE = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
BROWSER_ENGINE = "firefox"
SLOWMO = 2000

# File names
INPUT_FILE_NAME = "robot_orders.csv"
OUTPUT_FILE_NAME = "sales_results_$placeholder.pdf"
ERR_SCREENSHOT_FILE_NAME = "err_robot_order_$placeholder.png"
ORDERED_ROBOT_FILE_NAME = "ordered_robot_$placeholder.png"
ZIP_FILE_NAME = f"order_transactions_{FILES_DATE}.zip"

# File paths
IN_CSV_DATA_FILE_PATH = os.path.join(data_folder_path, INPUT_FILE_NAME)
OUT_PDF_FILE_PATH = os.path.join(RESULTS_PDF_FOLDER_PATH, OUTPUT_FILE_NAME)
ERR_SCREENSHOT_FILE_PATH = os.path.join(err_screenshot_folder_path, ERR_SCREENSHOT_FILE_NAME)
ORDERED_ROBOT_IMG_FILE_PATH = os.path.join(ordered_robot_folder_path, ORDERED_ROBOT_FILE_NAME)
ZIP_FILE_PATH = os.path.join(OUTPUT_DATA_FOLDER_PATH, ZIP_FILE_NAME)

# URLS
SPARE_BIN_HOME_URL = "https://robotsparebinindustries.com/"
SPARE_BIN_ORDER_CSV_URL = "https://robotsparebinindustries.com/orders.csv"