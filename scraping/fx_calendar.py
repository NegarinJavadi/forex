import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import datetime as dt
import random

from dateutil import parser
from db.db import DataDB

pd.set_option("display.max_rows", None)

def get_date(c):
    tr = c.select_one("tr")
    ths = tr.select("th")
    for th in ths:
        if th.has_attr("colspan"):
            date_text = th.get_text().strip()
            return parser.parse(date_text)
    return None

def get_data_point(key, element):
    for e in ['span', 'a']:
        d = element.select_one(f"{e}#{key}")
        if d is not None:
            return d.get_text()
    return ''

def get_data_for_key(tr, key):
    if tr.has_attr(key):
        return tr.attrs[key]
    return ''

def get_data_dict(item_date, table_rows):
    data = []

    for tr in table_rows:

        data.append(dict(
            date = item_date,
            country = get_data_for_key(tr, 'data-country'),
            category = get_data_for_key(tr, 'data-category'),
            event = get_data_for_key(tr, 'data-event'),
            symbol = get_data_for_key(tr, 'data-symbol'),
            actual = get_data_point('actual', tr),
            previous = get_data_point('previous', tr),
            forecast = get_data_point('forecast', tr)
        ))
    return data


def get_fx_calendar(from_date, to_date):
    session = requests.Session()
    base_url = 'https://tradingeconomics.com/calendar'

    fr_d_str = dt.datetime.strftime(from_date, "%Y-%m-%d 00:00:00")
    #to_date = from_date + dt.timedelta(days=6)
    to_d_str = dt.datetime.strftime(to_date, "%Y-%m-%d 00:00:00")

    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Cookie": "calendar-importance=3; cal-custom-range={fr_d_str}|{to_d_str}; TEServer=TEIIS2; cal-timezone-offset=0;"
    }

    resp = session.get(base_url, headers=headers)

    soup = BeautifulSoup(resp.content, 'html.parser')

    table = soup.select_one("table#calendar")

    last_header_date = None
    trs = {}
    final_data = []

    for c in table.children:
        if c.name == 'thead':
            if 'class' in c.attrs and 'hidden-head' in c.attrs['class']:
                continue
            last_header_date = get_date(c)
            trs[last_header_date] = []
        elif c.name == "tr":
            trs[last_header_date].append(c)
    
    for item_date, table_rows in trs.items():
        final_data += get_data_dict(item_date, table_rows)
    
    #[print(x) for x in final_data]
    return final_data

def fx_calendar():
    
    final_data = []

    start_date = parser.parse("2023-10-27T00:00:00Z")
    end_date = parser.parse("2024-02-26T00:00:00Z")

    database = DataDB()

    while start_date < end_date:
        data = get_fx_calendar(start_date, start_date + dt.timedelta(days=6))
        print(start_date, len(data))
        database.add_many(DataDB.CALENDAR_COLL, final_data)
        start_date += dt.timedelta(days=7)
        time.sleep(random.randint(1,4))

    print(pd.DataFrame.from_dict(final_data))

