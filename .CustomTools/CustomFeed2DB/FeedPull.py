from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
import feedparser
import requests
from bs4 import BeautifulSoup

def parse_feed(feed_url):
    feed_data = feedparser.parse(feed_url)
    results = []
    for entry in feed_data.entries:
        entry_data = {
            "title": entry.title,
            "link": entry.link,
            "updated": entry.updated,
            "id": entry.id,
            "raw_content": entry.content[0].value,
        }

        # Initialize WebDriver and navigate to the job post page
        driver = webdriver.Chrome(service=Service('./chromedriver.exe'))  # Use the path to your ChromeDriver
        driver.get(entry.link)

        # Wait until the element is present in the DOM
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.job-post-content')))

        # Scrape job post content
        content = driver.find_element_by_css_selector('div.job-post-content').text

        # Scrape attachment links
        attachments = driver.find_elements_by_css_selector('a.attachment-link')
        attachment_links = [attachment.get_attribute('href') for attachment in attachments]

        # Add the scraped data to entry_data
        entry_data.update({
            'job_post_content': content,
            'attachment_links': ', '.join(attachment_links),
        })

        driver.quit()  # Remember to quit the driver after you're done with it

        results.append(entry_data)
    return results

def write_to_file(content, filename="first_entry.txt"):
    with open(filename, "w") as file:
        file.write(content)

def write_links_to_file(links, filename="attachment_links.txt"):
    with open(filename, "w") as file:
        for link in links:
            file.write(f"{link}\n")

feed_url = "https://www.upwork.com/ab/feed/jobs/atom?q=Photoshop&job_type=hourly%2Cfixed&budget=50-&proposals=0-4%2C5-9%2C10-14%2C15-19&verified_payment_only=1&hourly_rate=25-&sort=recency&paging=0%3B50&api_params=1&securityToken=5d53fdd5809c340cfe7034341784f715c8433ec350191c7f0ee5607d91b69227dc8481c3ef14b654d0a87a7211a52622e824e33ae3cce04de57c7398856752ec&userUid=1327243219150897152&orgUid=1327243219155091457"  # Replace with your actual feed URL
entries = parse_feed(feed_url)
first_entry = entries[0]

# Write the raw content and links to separate files
write_to_file(first_entry['raw_content'])
write_to_file(first_entry['job_post_content'], "webpage_content.txt")
write_links_to_file(first_entry['attachment_links'])
