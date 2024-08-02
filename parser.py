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

def parse_comments(url: str) -> list[dict]:
    comments_url = URL_TO_PARSE + url + '#usercomments'
    comments = []
    response = make_request(comments_url)
    tree = html.fromstring(response.text)
    book_name = tree.xpath('//div[@class="row onebook"]/div/h1/text()')[0].strip()
    comments_data = tree.xpath('//div[@class="panel panel-info"]')
    for comment_data in comments_data:
        name = comment_data.xpath('.//div[@class="panel-heading"]/text()')[0].strip()
        date = comment_data.xpath('.//div[@class="panel-heading"]/span/text()')[0].strip()
        text = comment_data.xpath('.//div[@class="panel-body"]/p/text()')[0].strip()
        comments.append({'name': name, 'date': date, 'text': text})
    all_comments = {'book': book_name, 'comments': comments}
    return all_comments

def parse_categories(url: str) -> list[dict]:
    category_url = URL_TO_PARSE + url
    response = make_request(category_url)
    tree = html.fromstring(response.text)
    books = tree.xpath('//div[@class="gallery-grid"]//div[@class="gallery-text"]/div/a/@href')
    comments = []
    for book in books:
        comments.append(parse_comments(book))
    return comments

def main():
    print(f"We'll gon'na parse this site: {URL_TO_PARSE}")
    url = URL_TO_PARSE
    response = make_request(url)
    tree = html.fromstring(response.text)
    categories = tree.xpath('//div[@class="collapse navbar-collapse menu-navbar"]//div[@class="menu-grids"]/div/a/@href')
    titles = tree.xpath('//div[@class="collapse navbar-collapse menu-navbar"]//div[@class="menu-grids"]/div/a/text()')
    print(titles[23])
    info = parse_categories(categories[23])# Саморозвиток
    print(info)

if __name__ == '__main__':
    main()