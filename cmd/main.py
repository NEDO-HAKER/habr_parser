import os
import requests
from bs4 import BeautifulSoup

URL1 = 'https://www.python.org/'
URL2 = 'https://www.wikipedia.org/'

def main():
    req = requests.get(URL2, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
    })
    if req.status_code == 200:
        print(req.headers)
        print()
        soup = BeautifulSoup(req.content, 'html.parser')
        
        lang_list = soup.find_all('a', class_="link-box")
        
        result_path = '../results'
        if not os.path.exists(result_path):
            os.makedirs(result_path)

        with open(f'{result_path}/wikipedia-result.txt', 'w', encoding='utf-8') as f:
            for el in lang_list:
                url = f"https:{el['href']}"
                lang = el.find('strong').text
                cnt = el.find('small').text
                print(lang, url, cnt)
                f.write(f'{url};{lang};{cnt}\n')



    else:
        print(f'Ошибка запроса\n Status Code: {req.status_code}')
        with open('error.html', 'wb') as f:
            f.write(req.content)

if __name__ == '__main__':
    main()
