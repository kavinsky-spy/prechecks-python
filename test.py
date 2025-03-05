import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def save_screenshot_with_info(driver, folder, base_name, url):
    # Saves a screenshot with a timestamp and includes the URL in the filename.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_url_part = url.replace("https://", "").replace("http://", "").replace("/", "_")
    filename = f"{base_name}_{timestamp}_{safe_url_part}.png"
    filepath = os.path.join(folder, filename)
    driver.save_screenshot(filepath)
    print(f"Screenshot saved: {filepath}")

def main():
    # Gather user inputs
    site_url = input("Enter the Drupal site URL: ").strip()
    uli = input("Enter the ULI (User Login URL): ").strip()
    page_to_test_url = input("Enter the URL of the page to be tested: ").strip()

    # Construct the full ULI URL
    if uli.startswith("/"):
        uli = site_url.rstrip("/") + uli

    # Create folder for screenshots
    folder_name = "drupal_site_screenshots"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Setup Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Step 1: Access the site URL and take a screenshot
        driver.get(site_url)
        time.sleep(2)  # Wait for the page to load
        save_screenshot_with_info(driver, folder_name, "site_home", site_url)

        # Step 2: Login using ULI and take a screenshot of the status report page
        driver.get(uli)
        time.sleep(2)  # Wait for the login to complete
        status_page_url = f"{site_url}/admin/reports/status"
        driver.get(status_page_url)
        time.sleep(2)
        save_screenshot_with_info(driver, folder_name, "status_report", status_page_url)

        # Step 3: Search for "test" if a search form exists
        driver.get(site_url)
        time.sleep(2)
        try:
            # Find any form whose ID contains "search"
            search_form = driver.find_element(By.XPATH, "//*[contains(@id, 'search')]")
            search_box = search_form.find_element(By.XPATH, ".//input[@type='search' or @type='text']")
            search_box.send_keys("test")
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)  # Wait for search results to load
            save_screenshot_with_info(driver, folder_name, "search_results", driver.current_url)
        except Exception as e:
            print("No search form found with 'search' in its ID.")

        # Step 4: Access the page to be tested and take a screenshot
        driver.get(page_to_test_url)
        time.sleep(2)
        save_screenshot_with_info(driver, folder_name, "page_to_test", page_to_test_url)

    finally:
        driver.quit()
        print("Process completed.")

if __name__ == "__main__":
    main()