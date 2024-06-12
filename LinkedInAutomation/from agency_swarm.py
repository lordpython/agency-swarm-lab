from agency_swarm.tools import BaseTool
from pydantic import Field
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the path to your ChromeDriver
chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")

class WebScrapingTool(BaseTool):
    url: str = Field(..., description="The URL of the LinkedIn page to scrape.")
    wait_time: int = Field(5, description="Time to wait for the page to load dynamic content (in seconds).")

    def run(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = ChromeService(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.get(self.url)
            # Use WebDriverWait to wait for a specific element
            WebDriverWait(driver, self.wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "some_selector"))
            )

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            # Process the soup object as needed

        except Exception as e:
            logger.error(f"An error occurred: {e}")
        finally:
            driver.quit()

        return soup
