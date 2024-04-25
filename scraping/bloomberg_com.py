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

    #headline = soup.select_one('[href="/news/articles/2024-04-24/china-carbon-price-tops-100-yuan-for-first-time-as-rules-tighten?srnd=fx-center"]')
    headline = soup.select_one('[hover="underline"][focus="underline"][data-component="headline"]')
    
    print(headline)
'''
    #all_links = []
    #all_links.append(get_article(headline))

    grid_articles = soup.select('a[href="/news/articles/2024-01-12/brazil-funds-face-reality-check-after-best-month-since-march-22?srnd=fx-center"]')
    [print(x) for x in grid_articles]
    #[all_links.append(get_article(x)) for x in grid_articles]

    #side_articles = soup.select()
    #[print(x) for x in side_articles]
    #[all_links.append(get_article(x)) for x in side_articles]

    #return all_links

<div class="hover:underline focus:underline" data-component="headline"><a href="/news/articles/2024-04-24/china-carbon-price-tops-100-yuan-for-first-time-as-rules-tighten?srnd=fx-center"
    <a href="/news/articles/2024-04-24/china-carbon-price-tops-100-yuan-for-first-time-as-rules-tighten?srnd=fx-center"
    <div class="styles_storyInfo__iq1t7"><div class="capitalize text-sm mb-[5px] capitalize" data-component="eyebrow"><a href="/green" class="hover:underline">Green</a></div><div class="hover:underline focus:underline" data-component="headline"><a href="/news/articles/2024-04-24/china-carbon-price-tops-100-yuan-for-first-time-as-rules-tighten?srnd=fx-center">China Carbon Price Tops 100 Yuan For First Time as Rules Tighten<div></div><div></div><div></div></a></div><div class="media-ui-RecentTimestamp_wrapper-8RcZT34kfjY-" data-component="recent-timestamp"><time class="media-ui-RelativeDate_relativeDate-R4FcKtXV8S0-" datetime="2024-04-24T07:50:13.353Z" data-locale="en">31 minutes ago</time></div></div>
'''
    