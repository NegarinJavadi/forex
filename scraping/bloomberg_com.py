from bs4 import BeautifulSoup
import pandas as pd
import requests
'''
def get_article(data):
    return dict(
        headline = data.get_text(),
        link = 'https://www.bloomberg.com' + data['href']
    )

def bloomberg_com():
    
    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"
    }

    resp = requests.get('https://www.bloomberg.com/fx-center', headers=headers)

    soup = BeautifulSoup(resp.content, 'html.parser')

    #session = requests.Session()
    #session.timeout = 10
    #resp = session.get('https://www.bloomberg.com/fx-center', headers=headers)

    #headline = soup.select_one('[href="/news/articles/2024-04-24/china-carbon-price-tops-100-yuan-for-first-time-as-rules-tighten?srnd=fx-center"]')
    headline_links = soup.select('a.headline-link') 

    if headline_links:
        for link in headline_links:
            headline_text = link.get_text(strip=True)
            headline_url = 'https://www.bloomberg.com' + link['href']
            print(f"Headline: {headline_text}")
            print(f"Link: {headline_url}")
    else:
        print('No headlines found on the page.')


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
def bloomberg_com():
    url = 'https://www.bloomberg.com'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, 'html.parser')

        headline_elements = soup.select('.latest-news__headline-text')

        if headline_elements:
            for headline in headline_elements:
            
                headline_text = headline.get_text(strip=True)
                print(f"Headline: {headline_text}")
                print("------------------------")
            else:
                print("No headlines found on the page.")

    except requests.exceptions.RequestException as e:
        print(f"Error making HTTP request: {e}")
    except Exception as ex:
        print(f"An error occurred: {ex}")
