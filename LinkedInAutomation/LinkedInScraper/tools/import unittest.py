import unittest
from unittest.mock import patch, MagicMock
from agency_swarm.tools import BaseTool
from pydantic import Field
import os

# Mock the WebScrapingTool class for testing
class WebScrapingTool(BaseTool):
    url: str = Field(..., description="The URL of the LinkedIn page to scrape.")
    wait_time: int = Field(5, description="Time to wait for the page to load dynamic content (in seconds).")

    def run(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = ChromeService(executable_path=os.getenv("CHROME_DRIVER_PATH"))
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.get(self.url)
            time.sleep(self.wait_time)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            posts = soup.find_all('div', class_='feed-shared-update-v2')
            post_data = [post.find('span', class_='break-words').get_text(strip=True) for post in posts]
            return post_data
        finally:
            driver.quit()

class TestWebScrapingTool(unittest.TestCase):

    @patch('selenium.webdriver.Chrome')
    def test_webdriver_closes_after_execution(self, MockWebDriver):
        mock_driver = MockWebDriver.return_value
        tool = WebScrapingTool(url="https://www.linkedin.com/feed/")
        tool.run()
        mock_driver.quit.assert_called_once()

    @patch('selenium.webdriver.Chrome')
    def test_webdriver_closes_on_exception(self, MockWebDriver):
        mock_driver = MockWebDriver.return_value
        mock_driver.get.side_effect = Exception("Test Exception")
        tool = WebScrapingTool(url="https://www.linkedin.com/feed/")
        with self.assertRaises(Exception):
            tool.run()
        mock_driver.quit.assert_called_once()

    @patch('selenium.webdriver.Chrome')
    def test_webdriver_closes_with_no_posts(self, MockWebDriver):
        mock_driver = MockWebDriver.return_value
        mock_driver.page_source = "<html></html>"
        tool = WebScrapingTool(url="https://www.linkedin.com/feed/")
        result = tool.run()
        self.assertEqual(result, [])
        mock_driver.quit.assert_called_once()

    @patch('selenium.webdriver.Chrome')
    def test_webdriver_closes_with_multiple_posts(self, MockWebDriver):
        mock_driver = MockWebDriver.return_value
        mock_driver.page_source = """
        <html>
            <div class='feed-shared-update-v2'>
                <span class='break-words'>Post 1</span>
            </div>
            <div class='feed-shared-update-v2'>
                <span class='break-words'>Post 2</span>
            </div>
        </html>
        """
        tool = WebScrapingTool(url="https://www.linkedin.com/feed/")
        result = tool.run()
        self.assertEqual(result, ["Post 1", "Post 2"])
        mock_driver.quit.assert_called_once()

    @patch('selenium.webdriver.Chrome')
    def test_webdriver_closes_with_empty_url(self, MockWebDriver):
        mock_driver = MockWebDriver.return_value
        tool = WebScrapingTool(url="")
        with self.assertRaises(Exception):
            tool.run()
        mock_driver.quit.assert_called_once()

if __name__ == '__main__':
    unittest.main()