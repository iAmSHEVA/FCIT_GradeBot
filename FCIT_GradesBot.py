from telegram import Bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import schedule

# Set up the bot with your token
BOT_TOKEN = 'TELEGRAM_TOKEN'
BOT_USERNAME = 'YOUR_BOT_USERNAME'

# Correct path to the chromedriver
PATH = r"C:\Program Files (x86)\chromedriver.exe"

def scrape_grades():
    # Initialize the Chrome service
    service = Service(PATH)

    # Initialize the Chrome driver with the service
    driver = webdriver.Chrome(service=service)

    try:
        # Open a webpage
        driver.get("https://odusplus-ss.kau.edu.sa/")
        
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

        scraped_data = ""
        # Iterate through each row
        for row in rows:
            # Find all cells in the row excluding header cells (th)
            cells = row.find_elements(By.XPATH, "./td")
        
            # Extract the first, second, and last cells
            if len(cells) >= 3:  # Ensure at least 3 cells in the row
                first_cell = cells[0].text.strip()
                second_cell = cells[1].text.strip()
                last_cell = cells[-1].text.strip()
            
                # Add the extracted cells to the scraped data
                scraped_data += f"Subject: {first_cell} {second_cell}\n"
                scraped_data += f"Grade: {last_cell}\n"

        return scraped_data
    
    finally:
        # Close the browser
        driver.quit()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Scrape grades
    scraped_data = scrape_grades()
    
    # Send the scraped data to the user
    await update.message.reply_text(scraped_data)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Schedule sending the /start command
    schedule.every(1).minute.do(send_scraped_data, update)

async def send_scraped_data(update: Update):
    # Scrape grades
    scraped_data = scrape_grades()
    
    # Send the scraped data to the user
    await update.message.reply_text(scraped_data)
        
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

if __name__ == '__main__':
    print('Starting Bot...')
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler('start', start_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)
    
    print('Polling...')
    app.run_polling(poll_interval=3)
