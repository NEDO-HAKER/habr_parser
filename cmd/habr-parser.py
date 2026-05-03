import requests
from bs4 import BeautifulSoup
import time
from utils import check_and_crate_result

URL = 'https://habr.com/ru/feed/'


def parse_article(soup):
    articles_list = soup.find_all('article', class_='tm-articles-list__item')
    print(f'Parsing articles..., find {len(articles_list)} articles')
    data = []

    for article in articles_list:
        header = article.find('h2', class_='tm-title')
        if header is None:
            raise ValueError('Article do not have header. SKIP...')
        header_text = header.find('span').text
        article_link = header.find('a').attrs['href']
        article_views = article.find('span', class_='tm-icon-counter__value').text
        data.append ({ 
            'header_text' : header_text, 
            'article_link' : article_link, 
            'article_views' : article_views
        })

    return data

def main():
    req = requests.get(URL, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
    })
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, 'html.parser')
        parsed_articles = []
        try:
            parsed_articles.append(parse_article(soup))
        except ValueError as e:
            print(e)

        count_page = soup.find_all('a', class_='tm-pagination__page')
        count_page = int(count_page[-1].text)
        print(f'Found {count_page} pages')

        need_pages = min(5, count_page)

        for i in range(2, need_pages + 1):
            url = f'{URL}/{i}'
            print(f'Parsing page {i}...')
            
            time.sleep(5)
            req = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
            })
            if req.status_code == 200:
                try:
                    parsed_articles.append(parse_article(soup))
                except ValueError as e:
                    print(e)
            else:
                print(f'Parsing page {i} error SKIP')
                continue
        
        
        result_path = check_and_crate_result()

        with open(f'{result_path}/habr-result-{time.time()}.txt', 'a', encoding='utf-8') as f:
            for el in parsed_articles:
                f.write(f"header: {el['header_text']}\nviews: {el['article_views']}\nlink: https://habr.com{el['article_link']}")

if __name__ == "__main__":
    main()