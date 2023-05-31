from selenium import webdriver
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service=Service('./chromedriver.exe'))

driver.get("https://www.upwork.com/jobs/Recreate-User-Manuals_%7E01147e92c97c9a6dde?source=rss")  # Replace with your URL

# Get all the text on the page
page_text = driver.find_element_by_tag_name('body').text

# Get all the links on the page
links = [element.get_attribute('href') for element in driver.find_elements_by_tag_name('a')]

driver.quit()

# Now `page_text` contains all the text on the page, and `links` contains all the URLs.
print(page_text)
print(links)
