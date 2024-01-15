from bs4 import BeautifulSoup
import pandas as pd
import requests
'''
def get_article(data):
    return dict(
        headline = data.get_text(),
        link = 'https://www.bloomberg.com' + data['href']
    )
'''
def bloomberg_com():

    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0"
    }

    session = requests.Session()
    session.timeout = 10
    resp = session.get('https://www.bloomberg.com/fx-center', headers=headers)


    soup = BeautifulSoup(resp.content, 'html.parser')

    headline = soup.select_one('a[href="/news/articles/2024-01-12/argentina-bonds-gain-as-milei-s-rework-passes-crucial-tests?srnd=fx-center"]')
    
    print(headline)

    #all_links = []
    #all_links.append(get_article(headline))

    grid_articles = soup.select('a[href="/news/articles/2024-01-12/brazil-funds-face-reality-check-after-best-month-since-march-22?srnd=fx-center"]')
    [print(x) for x in grid_articles]
    #[all_links.append(get_article(x)) for x in grid_articles]

    #side_articles = soup.select()
    #[print(x) for x in side_articles]
    #[all_links.append(get_article(x)) for x in side_articles]

    #return all_links