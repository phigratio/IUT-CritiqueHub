# base_scraper.py
import requests
from bs4 import BeautifulSoup
import random
import time

# User-Agent to prevent blocking
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

# List of proxies (You can add more if needed)
proxies_list = [
    {"http": "http://220.248.70.237:9002"},
    {"http": "http://123.30.154.171:7777"}
]

# Select a random proxy
def get_random_proxy():
    return random.choice(proxies_list)

# Generic function to fetch and parse a webpage
def fetch_page(url):
    try:
        proxy = get_random_proxy()
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch page {url}: {e}")
        return None

# Sleep for a random time to avoid overloading servers
def random_sleep():
    time.sleep(random.uniform(1, 3))
