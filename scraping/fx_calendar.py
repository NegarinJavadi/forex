import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.append('/home/negarin/Desktop/Appendix/code')

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

def get_fx_calendar(from_date):

    session = requests.Session()

    fr_d_str = dt.datetime.strftime(from_date, "%Y-%m-%d 00:00:00")

    to_date = from_date + dt.timedelta(days=6)
    to_d_str = dt.datetime.strftime(to_date, "%Y-%m-%d 00:00:00")

    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Cookie": f"calendar-importance=3; cal-custom-range=2{fr_d_str}|{to_d_str}; TEServer=TEIIS2; cal-timezone-offset=0"
    }

    resp = session.get("https://tradingeconomics.com/calendar", headers=headers)


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
    
    #final_data = []

    start = parser.parse("2023-02-01T00:00:00Z")
    end = parser.parse("2024-02-18T00:00:00Z")
    
    database = DataDB()

    while start < end:
        data = get_fx_calendar(start)
        print(start, len(data))
        example_data = [
        {"data": "2024-01-17", "country": "GBP", "event": "CPI", "actual": 4, "previous":3.9, "forecast":3.8}
        ]
        database.add_many(DataDB.CALENDAR_COLL, example_data)
        database.query_all(DataDB.CALENDAR_COLL)
        database.add_many(DataDB.CALENDAR_COLL, data)
        start = start + dt.timedelta(days=7)
        time.sleep(random.randint(1,4))

   #print(pd.DataFrame.from_dict(final_data))


