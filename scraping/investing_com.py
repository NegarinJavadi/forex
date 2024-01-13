from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import datetime as dt

#data_keys = []

'''
def get_data_object(text_list, pair_id, time_frame):
    data = {}
    data['pair_id'] = pair_id
    data['time_frame'] = time_frame
    data['updated'] = dt.datetime.utcnow()

    for item in text_list:
        temp_item = item.split("=")
        if len(temp_item) == 2 and temp_item[0] in data_keys:
            data[temp_item[0]] = temp_item[1]
    #if 'pair_name' in data:
    #    data['pair_name'] = data['pair_name'].replace("/", "_")
    
    return data

'''

def investing_com(text_list):
#def investing_com_fetch(pair_id, time_frame):

    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0"
    }

    params = dict(
        #action = 'get_studies',
        #pair_ID = 7,
        #time_frame = 3600
    )
    resp = requests.post("https://www.investing.com/technical/Service/GetStudiesContent",
                         headers=headers, timeout=10)
    
    print(resp.content)
    print(resp.status_code)

    #text = resp.content.decode("utf-8")

    #print(text)

    #index_start = text.index("pair_name=")
    #index_end = text.index("*;*quote_link")

    #print(text[index_start:index_end])
    #date_str = text[index_start:index_end]

    #split_date_str = date_str.split('*;*')

    #[print(x) for x in split_date_str]
    #keys = [x.split("=")[0] for x in split_date_str]
    #print(keys)

    #print(get_data_objcet(date_str.split('*;*')))
    #return get_data_objcet(date_str.split('*;*'), pair_id, time_frame)
'''
def investing_com():
    data = []
    for pair_id in range(1, 12):
        for time_frame in [3600, 86400]:
            print(pair_id, time_frame)
            data.append(investing_com_fetch(pair_id, time_frame))
            time.sleep(0.5)
    return pd.DataFrame.from_dict(data)
'''
