import requests
from lxml import html
import time
import json
import random
from __init__ import URL_TO_PARSE

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
]
# Bot detection prevention
def get_random_user_agent() -> str:
    return random.choice(user_agents)
def random_sleep():
    time.sleep(random.randint(1, 3))

# Safe request
def make_request(url):
    headers = {'User-Agent': get_random_user_agent()}
    response = requests.get(url, headers=headers)
    random_sleep()
    return response


def parse_categories(url):
    category_url = URL_TO_PARSE + url
    response = make_request(category_url)
    tree = html.fromstring(response.text)
    books = tree.xpath('//div[@class="gallery-grid"]//div[@class="gallery-text"]/div/a/@href')
    print(books)

def main():
    print(f"We'll gon'na parse this site: {URL_TO_PARSE}")
    data = {} # gather all data for JSON
    url = URL_TO_PARSE
    response = make_request(url)
    tree = html.fromstring(response.text)
    categories = tree.xpath('//div[@class="collapse navbar-collapse menu-navbar"]//div[@class="menu-grids"]/div/a/@href')
    for category in categories:
        parse_categories(category)
        print()


if __name__ == '__main__':
    main()