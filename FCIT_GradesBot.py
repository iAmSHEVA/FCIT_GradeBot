from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Correct path to the chromedriver
PATH = r"C:\Program Files (x86)\chromedriver.exe"

# Initialize the Chrome service
service = Service(PATH)

# Initialize the Chrome driver with the service
driver = webdriver.Chrome(service=service)

try:
    # Open a webpage
    driver.get("https://odusplus-ss.kau.edu.sa/")
    
    # Print the title of the page
    print(driver.title)
    
    # Wait for the elements to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "userid"))
    )
    
    # Find and interact with the username field
    username_field = driver.find_element(By.NAME, "userid")
    username_field.send_keys("YOUR_USERNAME")
    
    # Find and interact with the password field
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys("YOUR_PASSWORD")
    
    # Submit the form
    password_field.send_keys(Keys.RETURN)
    
    # Wait for the link to be present
    link = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.LINK_TEXT, "الطالب"))
    )
    
    # Click the link
    link.click()

    # Wait for the link to be present
    link = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.LINK_TEXT, "سجلات الطالب"))
    )
    
    # Click the link
    link.click()

    
    # Wait for the link to be present
    link = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.LINK_TEXT, "الاستعلام الاكاديمي الشامل"))
    )
    
    # Click the link
    link.click()

    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "(//table[@class='datadisplaytable'])[last()-2]"))
    )
    table_text = table.text
    
    # Split the text into lines
    lines = table_text.split('\n')
    
   # Get all rows in the table
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Iterate through each row
    for row in rows:
        # Find all cells in the row excluding header cells (th)
        cells = row.find_elements(By.XPATH, "./td")
    
        # Extract the first, second, and last cells
        if len(cells) >= 3:  # Ensure at least 3 cells in the row
            first_cell = cells[0].text.strip()
            second_cell = cells[1].text.strip()
            last_cell = cells[-1].text.strip()
        
            # Print the extracted cells
            print("Subeject:", first_cell+second_cell)
            print("Grade:", last_cell)

    # Wait for some time to observe the actions
    time.sleep(5)
    
finally:
    # Close the browser
    driver.quit()
    print("driver closed")
