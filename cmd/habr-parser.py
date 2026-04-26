import requests
from bs4 import BeautifulSoup
import time
from utils import check_and_crate_result

URL = 'https://habr.com/ru/feed/'

# article link
# article headers
# article views
#article tags
def parse_article(article):
    header = article.find('h2', class_='tm-title')

    if header == None:
        raise ValueError('Article do not have header. SKIP...')

    header_text = header.find('span').text
    article_link = header.find('a').attrs['href']
    article_views = article.find('span', class_='tm-icon-counter__value').text
    # article_tags = list(map(lambda tag: tag.find('span').text, article.find('div', class_='tm-publication-hubs')))
    return { 'header_text' : header_text, 'article_link' : article_link, 'article_views' : article_views}

def main():
    req = requests.get(URL, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
    })
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, 'html.parser')
        articles_list = soup.find_all('article', class_='tm-articles-list__item')
        parsed_articles = []
        for a in articles_list:
            try:
                parsed_articles.append(parse_article(a))
            except ValueError as e:
                print(e)
        
        result_path = check_and_crate_result()

        with open(f'{result_path}/habr-result-{time.time()}.txt', 'a', encoding='utf-8') as f:
            for el in parsed_articles:
                f.write(f"header: {el['header_text']}\nviews: {el['article_views']}\nlink: https://habr.com{el['article_link']}")

if __name__ == "__main__":
    main()