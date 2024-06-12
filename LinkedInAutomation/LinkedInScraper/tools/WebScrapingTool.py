from agency_swarm.tools import BaseTool
from pydantic import Field
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

# Define the path to your ChromeDriver
chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")

class WebScrapingTool(BaseTool):
    """
    This tool utilizes web scraping libraries such as BeautifulSoup and Selenium to gather additional data from LinkedIn.
    It handles dynamic content and ensures that the data gathered is accurate and up-to-date.
    """

    # Define the fields with descriptions using Pydantic Field
    url: str = Field(
        ..., description="The URL of the LinkedIn page to scrape."
    )
    wait_time: int = Field(
        5, description="Time to wait for the page to load dynamic content (in seconds)."
    )

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method should utilize the fields defined above to perform the task.
        """
        # Set up Selenium WebDriver with Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = ChromeService(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            # Open the LinkedIn URL
            driver.get(self.url)
            time.sleep(self.wait_time)  # Wait for the page to load dynamic content

            # Get the page source and parse it with BeautifulSoup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Extract the desired data from the page
            # Example: Extracting post content
            posts = soup.find_all('div', class_='feed-shared-update-v2')
            post_data = []
            for post in posts:
                content = post.find('span', class_='break-words').get_text(strip=True)
                post_data.append(content)

            return post_data

        finally:
            # Close the WebDriver
            driver.quit()

# Example usage:
# tool = WebScrapingTool(url="https://www.linkedin.com/feed/")
# result = tool.run()
# print(result)