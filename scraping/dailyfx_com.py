from bs4 import BeautifulSoup
import pandas as pd
import requests

def dailyfx_com():

    session = requests.Session()
    session.timeout = 10
    resp = session.get('https://www.dailyfx.com/sentiment')


    #resp = requests.get('https://www.dailyfx.com/sentiment')

    #print(resp.content)
    #print(resp.status_code)

    soup = BeautifulSoup(resp.content, 'html.parser')

    #print(soup)

    rows = soup.select(".dfx-technicalSentimentCard")

    for r in rows:
        print(r)