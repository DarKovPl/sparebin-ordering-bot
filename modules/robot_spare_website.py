from robocorp import browser
from screeninfo import get_monitors, ScreenInfoError
from bs4 import BeautifulSoup
import re
from configuration.settings import (
    SPARE_BIN_HOME_URL, 
    BROWSER_ENGINE,
    SLOWMO,
    ERR_SCREENSHOT_FILE_PATH,
    ORDERED_ROBOT_IMG_FILE_PATH,
    FILES_DATE
)

def configure_browser_context():
    """Configures the browser context to open in full screen."""
    
    try:
        monitors = get_monitors()
        if monitors:
            monitor = monitors[0]
            width, height = monitor.width, monitor.height
        else:
            raise ScreenInfoError("No monitors detected.")
    except ScreenInfoError:
        print("Warning: No monitors detected. Using default resolution (1920x1080).")
        width, height = 1920, 1080

    browser.configure(
        browser_engine=BROWSER_ENGINE,
        slowmo=SLOWMO,
        headless=False
    )

    browser.configure_context(
        viewport={"width": width, "height": height}
    )

def open_website():

    print(f"Opening {SPARE_BIN_HOME_URL} in the firefox browser. ")
    browser.goto(url=SPARE_BIN_HOME_URL)

    page = browser.page()
    page.locator("text=/order your robot!/i").wait_for(state='attached', timeout=9000)
    page.click("a[href='#/robot-order']")

def manage_popup():
    """Manages the popup that appears on the website."""
    page = browser.page()
    try:
        page.locator("text=/yep/i").click()
    except Exception as e:
        print(f"Popup not found: {e}")

def refresh_page():
    """Refreshes the page."""
    page = browser.page()
    page.reload()

def _parse_html(model_info_html):
    """Parses the model information from the HTML."""

    soup = BeautifulSoup(model_info_html, "html.parser")
    headers = [th.get_text(strip=True) for th in soup.find_all("th")]

    data = {}
    for row in soup.find_all("tr")[1:]:
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(cells) == 2:
            part_number, model_name = cells[1], cells[0]
            data[part_number] = model_name

    return data

def get_model_info():
    """Gets the model information."""

    page = browser.page()
    page.click("button >> text=/show model info/i", timeout=9000)
    page.locator("table#model-info.table-dark").wait_for(state="attached", timeout=9000)

    model_info_html = page.locator("table#model-info.table-dark").evaluate("element => element.outerHTML")
    model_info = _parse_html(model_info_html)
    print(f"\nModel info: {model_info}\n")

    return model_info

def fill_the_form(row, model_info):
    """Fills the form with the data from the CSV file."""
    page = browser.page()

    page.select_option("select#head[name='head']", value=f"{row['Head']}")
    page.locator(f"input#id-body-{row['Body']}").set_checked(True, force=True)
    page.get_by_placeholder(re.compile("enter the part number for the legs", re.IGNORECASE)).fill(row["Legs"])
    page.get_by_placeholder(re.compile("shipping address", re.IGNORECASE)).fill(row["Address".strip()])
    
    page.click("button >> text=/order/i", timeout=9000)
    print("Clicked the order button.")

def check_receipt_appeared(row, transaction_no):
    """Checks if the receipt appeared after the order."""
    page = browser.page()

    try:
        page.locator("div#receipt").wait_for(state="attached", timeout=9000)
        print("Receipt found.")

    except Exception as e:
        message = f"Error while getting the receipt: {e}"
        screenshot_file_path = ERR_SCREENSHOT_FILE_PATH.replace(
            "$placeholder", f"{transaction_no}_{row['Order number']}_{FILES_DATE}"
        )
        page.screenshot(path=screenshot_file_path)
        print("Screenshot taken. Saved as: ", screenshot_file_path)
        
        raise Exception(message)

def extract_receipt_data():
    """Extracts the receipt data."""
    page = browser.page()
    receipt_html = page.locator("div#receipt").inner_html()

    soup = BeautifulSoup(receipt_html, "html.parser")
    timestamp = soup.find("div").text.strip()
    order_number = soup.find("p", class_="badge badge-success").text.strip()
    parts_section = soup.find("div", id="parts")

    parts = {}    
    for div in parts_section.find_all("div"):
        part_name, part_value = div.text.split(": ")
        parts[part_name.strip()] = part_value.strip()
    confirmation_message = soup.find_all("p")[-1].text.strip()

    receipt_data = {
        "timestamp": timestamp,
        "order_number": order_number,
        "parts": parts,
        "confirmation_message": confirmation_message
    }
    print("Receipt data extracted: ", receipt_data)

    return receipt_data

def get_image_of_robot(row, transaction_no):
    """Gets the image of the robot."""
    image_path = ORDERED_ROBOT_IMG_FILE_PATH.replace(
        "$placeholder", f"{transaction_no}_{row['Order number']}_{FILES_DATE}"
    )

    page = browser.page()
    robot_image__on_page = page.locator("div#robot-preview")
    image_size = robot_image__on_page.bounding_box()
    robot_image__on_page.screenshot(path=image_path)

    print("Image of the robot saved as: ", image_path)

    return image_size, image_path

def order_another_robot():
    """Orders another robot."""
    page = browser.page()
    page.click("button >> text=/order another robot/i", timeout=9000)
    print("Clicked the order another robot button.")
