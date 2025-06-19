from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import datetime
import os
import time

# Set up Chrome options (Removed headless mode)
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Set up ChromeDriver path
chromedriver_path = "/Users/hannahjoo/Desktop/Beauty/Crawler/chromedriver"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

# Open Sephora Best Selling Makeup page
url = "https://www.sephora.com/beauty/best-selling-makeup"
driver.get(url)

# Scroll down multiple times to trigger lazy loading
for _ in range(5):  # Adjust as needed
    driver.execute_script("window.scrollBy(0, 500);")  # Scroll down
    time.sleep(2)  # Wait for content to load

# Wait for elements to be visible
WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-at='brand_link']"))
)

# Get page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Extract brand data
best_makeup_data = []

# Find all brand links
brand_links = driver.find_elements(By.CSS_SELECTOR, "a[data-at='brand_link']")

for a_tag in brand_links:
    brand_name = a_tag.text.strip()
    brand_url = a_tag.get_attribute("href")  # Get absolute URL

    # Check if "NEW" label is present
    try:
        new_label = a_tag.find_element(By.XPATH, ".//span[contains(text(), 'NEW')]")
        is_new = "Yes"
    except:
        is_new = "No"

    best_makeup_data.append([brand_name, brand_url, is_new])

print(f"✅ Extracted {len(best_makeup_data)} best selling makeup.")

# Close the driver
driver.quit()

# Define Folder Path for Saving CSV
save_folder = "/Users/hannahjoo/Desktop/Beauty/Sephora"
os.makedirs(save_folder, exist_ok=True)  # Ensure the folder exists

# Generate CSV filename with today's date
date_today = datetime.datetime.today().strftime('%Y-%m-%d')
filename = f"Sephora_brands_{date_today}.csv"
file_path = os.path.join(save_folder, filename)

# Save Data to CSV
with open(file_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Brand Name", "Brand Link", "New"])
    if brands_data:
        writer.writerows(brands_data)
    else:
        print("⚠️ Warning: No data found!")

print(f"✅ Data successfully saved to: {file_path}")




https://www.sephora.com/beauty/best-selling-skin-care
https://www.sephora.com/beauty/best-selling-hair-products
https://www.sephora.com/beauty/best-selling-perfume