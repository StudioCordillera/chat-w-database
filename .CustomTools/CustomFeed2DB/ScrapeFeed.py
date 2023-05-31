import os
import feedparser
import psycopg2
from html.parser import HTMLParser
from html import unescape
from bs4 import BeautifulSoup

# Get the base directory of the script file
base_directory = os.path.dirname(os.path.abspath(__file__))

# Activate local environment path to python.exe
venv_python_path = os.path.join(base_directory, ".venv", "Scripts", "python.exe")
os.environ["PATH"] = f"{os.path.dirname(venv_python_path)};{os.environ['PATH']}"

feed_urls = [
    # Your feed URLs
    "https://www.upwork.com/ab/feed/jobs/atom?q=Photoshop&sort=recency&job_type=hourly%2Cfixed&proposals=0-4%2C5-9%2C10-14%2C15-19&budget=50-&verified_payment_only=1&hourly_rate=25-&paging=0%3B50&api_params=1&securityToken=5d53fdd5809c340cfe7034341784f715c8433ec350191c7f0ee5607d91b69227dc8481c3ef14b654d0a87a7211a52622e824e33ae3cce04de57c7398856752ec&userUid=1327243219150897152&orgUid=1327243219155091457",
    "https://www.upwork.com/ab/feed/jobs/atom?q=Photoshop&sort=recency&job_type=hourly%2Cfixed&proposals=0-4%2C5-9%2C10-14%2C15-19&budget=50-&verified_payment_only=1&hourly_rate=25-&paging=50%3B50&api_params=1&securityToken=5d53fdd5809c340cfe7034341784f715c8433ec350191c7f0ee5607d91b69227dc8481c3ef14b654d0a87a7211a52622e824e33ae3cce04de57c7398856752ec&userUid=1327243219150897152&orgUid=1327243219155091457",
    "https://www.upwork.com/ab/feed/jobs/atom?q=Photoshop&sort=recency&job_type=hourly%2Cfixed&proposals=0-4%2C5-9%2C10-14%2C15-19&budget=50-&verified_payment_only=1&hourly_rate=25-&paging=100%3B50&api_params=1&securityToken=5d53fdd5809c340cfe7034341784f715c8433ec350191c7f0ee5607d91b69227dc8481c3ef14b654d0a87a7211a52622e824e33ae3cce04de57c7398856752ec&userUid=1327243219150897152&orgUid=1327243219155091457",
    "https://www.upwork.com/ab/feed/jobs/atom?q=Photoshop&sort=recency&job_type=hourly%2Cfixed&proposals=0-4%2C5-9%2C10-14%2C15-19&budget=50-&verified_payment_only=1&hourly_rate=25-&paging=150%3B50&api_params=1&securityToken=5d53fdd5809c340cfe7034341784f715c8433ec350191c7f0ee5607d91b69227dc8481c3ef14b654d0a87a7211a52622e824e33ae3cce04de57c7398856752ec&userUid=1327243219150897152&orgUid=1327243219155091457"
]

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_data = []
        self.nested_tags = []
        self.pairings = []
        self.current_tag = None
        self.current_field = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_data(self, data):
        data = data.strip()
        if data:
            self.tag_data.append(f'{self.current_tag}-{data}')
            if self.current_tag == 'b':
                if self.current_field:  # If a previous field is not yet paired, pair it with empty data.
                    self.pairings.append(f'{self.current_field}-')
                self.current_field = data
            else:
                if self.current_field:
                    self.pairings.append(f'{self.current_field}-{data}')
                    self.current_field = None

def parse_additional_fields(content):
    parser = MyHTMLParser()
    parser.feed(content)
    return parser.tag_data, parser.pairings

def clean_data(raw_data):
    data = {}

    raw_data = unescape(raw_data)
    soup = BeautifulSoup(raw_data, 'html.parser')

    data['Description'] = soup.get_text(separator='\n').split('\nHourly Range')[0].strip()
    data['Hourly Range'] = soup.find('b', text='Hourly Range').next_sibling.strip(': ')
    data['Posted On'] = soup.find('b', text='Posted On').next_sibling.strip(': ')
    data['Category'] = soup.find('b', text='Category').next_sibling.strip(': ')
    data['Skills'] = [skill.strip() for skill in soup.find('b', text='Skills').next_sibling.strip(':').split(',')]
    data['Country'] = soup.find('b', text='Country').next_sibling.strip(': ')
    data['Apply Link'] = soup.find('a')['href']

    return data

def store_feed_entries_in_database(entries):
    # PostgreSQL database credentials
    db_host = 'your_database_host'
    db_name = 'your_database_name'
    db_user = 'your_username'
    db_password = 'your_password'

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()

    # Iterate over feed entries
    for entry in entries:
        # Check for duplicates using the entry URL
        entry_url = entry['link']

        cursor.execute('SELECT id FROM your_table WHERE entry_url = %s', (entry_url,))
        duplicate = cursor.fetchone()

        # If no duplicate found, insert the entry into the database
        if not duplicate:
            # Clean the data
            cleaned_data = clean_data(entry['raw_content'])
            
            # Insert the cleaned data into the database
            cursor.execute('INSERT INTO your_table (entry_url, title, updated, id, raw_content, description, hourly_range, posted_on, category, skills, country, apply_link) '
                           'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (entry['link'], entry['title'], entry['updated'], entry['id'], entry['raw_content'],
                            cleaned_data['Description'], cleaned_data['Hourly Range'], cleaned_data['Posted On'],
                            cleaned_data['Category'], cleaned_data['Skills'], cleaned_data['Country'],
                            cleaned_data['Apply Link']))
            conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

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
        tag_data, pairings = parse_additional_fields(entry.content[0].value)
        entry_data.update({
            'tags': '-'.join(tag_data),
            'pairings': '-'.join(pairings)
        })
        results.append(entry_data)
    return results

all_results = []
for url in feed_urls:
    all_results.extend(parse_feed(url))

# Store the feed entries in the PostgreSQL database
store_feed_entries_in_database(all_results)
