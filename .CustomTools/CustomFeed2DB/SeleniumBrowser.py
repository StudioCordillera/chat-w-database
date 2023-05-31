from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup

def scrape_content(link):
    # Initialize a Selenium webdriver
    driver = webdriver.Firefox()  # or webdriver.Chrome(), etc.

    driver.get(link)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    page_content = soup.text
    attachments = soup.find_all('a', {'class': 'attachment-link'})

    attachment_links = [attachment['href'] for attachment in attachments]

    # Don't forget to close the driver when you're done
    driver.quit()

    return page_content, attachment_links
