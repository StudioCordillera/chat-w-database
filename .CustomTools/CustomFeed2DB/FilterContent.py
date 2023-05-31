from html import unescape
from bs4 import BeautifulSoup

# replace this with your actual Atom feed data
raw_data = ""

raw_data = unescape(raw_data)
soup = BeautifulSoup(raw_data, 'html.parser')

data = {}

data['Description'] = soup.get_text(separator='\n').split('\nHourly Range')[0].strip()
data['Hourly Range'] = soup.find('b', text='Hourly Range').next_sibling.strip(': ')
data['Posted On'] = soup.find('b', text='Posted On').next_sibling.strip(': ')
data['Category'] = soup.find('b', text='Category').next_sibling.strip(': ')
data['Skills'] = [skill.strip() for skill in soup.find('b', text='Skills').next_sibling.strip(':').split(',')]
data['Country'] = soup.find('b', text='Country').next_sibling.strip(': ')
data['Apply Link'] = soup.find('a')['href']

with open('output.txt', 'w') as f:
    for key, value in data.items():
        if isinstance(value, list):
            value = ', '.join(value)
        f.write(f'{key}: {value}\n')
