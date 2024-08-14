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

def save_to_json(data: list[dict], filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def replace_symbols(text: str) -> str:
    return text.replace('\n', '').replace('\r', '').replace(':', '').replace('"', '')

# Bot detection prevention
def get_random_user_agent() -> str:
    return random.choice(user_agents)
def random_sleep()-> None:
    time.sleep(random.randint(1, 3))

# Safe request
def make_request(url: str) -> requests.Response:
    headers = {'User-Agent': get_random_user_agent()}
    response = requests.get(url, headers=headers)
    random_sleep()
    return response

def get_comment_text(object: html.HtmlElement) -> str:
    # TODO: here we will get text from various variants of comment
    pass

def parse_comments(url: str) -> list[dict]:
    comments_url = URL_TO_PARSE + url + '#usercomments'
    comments = []
    response = make_request(comments_url)
    tree = html.fromstring(response.text)
    book_name = replace_symbols(tree.xpath('//div[@class="row onebook"]/div/h1/text()')[0].strip())
    print(book_name)
    comments_data = tree.xpath('//div[@class="panel panel-info"]')
    if not comments_data:
        return {'book': book_name, 'comments': []}
    for comment_data in comments_data:
        name = comment_data.xpath('.//div[@class="panel-heading"]/text()')[0].strip()
        date = comment_data.xpath('.//div[@class="panel-heading"]/span/text()')[0].strip()
        if comment_data.xpath('.//div[@class="panel-body"]/text()')[0].strip() != "":
            text = comment_data.xpath('.//div[@class="panel-body"]/text()')[0].strip()  
        elif comment_data.xpath('.//div[@class="panel-body"]/p/text()')[0].strip() != "":
            # TODO: create comment text for list of spans
            text = comment_data.xpath('.//div[@class="panel-body"]/p/span/text()').strip()
        else:
            text = comment_data.xpath('.//div[@class="panel-body"]/p/text()')[0].strip()
        comments.append({'name': name, 'date': date, 'text': text})
    all_comments = {'book': book_name, 'comments': comments}
    return all_comments

def generate_pages_urls(url: str, last_page: int) -> list[str]:
    full_url = URL_TO_PARSE + url
    result = []
    result.append(full_url)
    for i in range(2, last_page + 1):
        result.append(full_url + f'/page{i}?sort=popular-desc&filter=stock,time,predorder') 
    return result

def parse_categories(url: str) -> list[dict]:
    category_url = URL_TO_PARSE + url
    response = make_request(category_url) # make request for pagination
    tree = html.fromstring(response.text)
    pages = tree.xpath('//ul[@class="pagination"]/li/a/text()')
    last_page = int(pages[-1]) # get last page number
    pages_urls = generate_pages_urls(url, last_page)
    comments = []
    for page in pages_urls[2:5]: # take a slice of the first 2 pages for example
        response = make_request(page)
        tree = html.fromstring(response.text)
        books = tree.xpath('//div[@class="gallery-grid"]//div[@class="gallery-text"]/div/a/@href')
        for book in books:
            comments.append(parse_comments(book))
    return comments

def main():
    print(f"Parsing site: {URL_TO_PARSE}")
    url = URL_TO_PARSE
    response = make_request(url)
    tree = html.fromstring(response.text)
    categories = tree.xpath('//div[@class="collapse navbar-collapse menu-navbar"]//div[@class="menu-grids"]/div/a/@href')
    titles = tree.xpath('//div[@class="collapse navbar-collapse menu-navbar"]//div[@class="menu-grids"]/div/a/text()')
    print(titles[23]) # just to show what category we are parsing
    info = parse_categories(categories[23])# taken one category for example: Саморозвиток
    # we can add for..in loop to parse all data from site
    for item in info:
        save_to_json(item['comments'], f'./reviews/{item["book"]}.json')
    print('Done!')
if __name__ == '__main__':
    main()