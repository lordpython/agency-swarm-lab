from selenium import webdriver

# Specify the path to chromedriver
chromedriver_path = 'C:\Users\yofii\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

# Set up the ChromeDriver service
service = webdriver.chrome.service.Service(chromedriver_path)

# Start the ChromeDriver service
service.start()

# Print the path of the ChromeDriver executable
print(service.path)

# Stop the ChromeDriver service
service.stop()
