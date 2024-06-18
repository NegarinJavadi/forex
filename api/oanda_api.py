import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

import os
import sys
import requests
import pandas as pd
import json
from dateutil import parser
from datetime import datetime as dt
import constants.defs as defs
from models.open_trade import OpenTrade
from models.api_price import ApiPrice

class OandaApi:

    def __init__(self):  
        self.session = requests.Session()  
        self.session.headers.update(defs.SECURE_HEADER)  

    def make_request(self, url, verb='get', code=200, params=None, data=None, headers=None):
        full_url= f"{defs.OANDA_URL}/{url}"

        if data is not None:
            data = json.dumps(data)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {defs.API_KEY}',
        }

        try:
            response = None
            if verb == "get":
                response = self.session.get(full_url, params=params, data=data, headers=headers)
            elif verb == "post":
                response = self.session.post(full_url, params=params, data=data, headers=headers)
            elif verb == "put":
                response = self.session.put(full_url, params=params, data=data, headers=headers)

            if response is None:
                return False, {'error': 'verb not found'}
            if response.status_code == code: 
                return True, response.json()
            else:
                return False, response.json()

        except Exception as error:
            return False, {'Exception': error}

    def get_account_ep(self, ep, data_key):
        url = f"accounts/{defs.ACCOUNT_ID}/{ep}"
        ok, data = self.make_request(url)

        if ok == True and data_key in data:
            return data[data_key]
        else:
            print("ERROR get_account_ep()", data)
            return None

    def get_account_summary(self):
        return self.get_account_ep("summary", "account")
    
    def get_account_instruments(self):
        return self.get_account_ep("instruments", "instruments")

    def fetch_candles(self, pair_name, count=10, granularity="H1",
                      price="MBA", date_f=None, date_t=None):
        instrument = pair_name.replace(' ', '_').upper()  # Ensure the format is correct
        print(f"Formatted instrument: {instrument}")  # Add this line for debugging

        endpoint = f"instruments/{pair_name}/candles"
        params = {
            "granularity": granularity,
            "price": price
        }

        if date_f is not None and date_t is not None:
            date_format = "%Y-%m-%dT%H:%M:%SZ"
            params["from"] = dt.strftime(date_f, date_format)
            params["to"] = dt.strftime(date_t, date_format)
        else:
            params["count"] = count

        print(f"Fetching candles for {pair_name} with params {params}")

        ok, data = self.make_request(endpoint, verb="get", params=params)

        if ok:
            return data.get("candles", [])
        else:
            print(f"ERROR fetch_candles() {params} {data}")
            return None

    def get_candles_df(self, pair_name, **kwargs):
        data = self.fetch_candles(pair_name, **kwargs)

        if data is None:
            return None
        if len(data) == 0:
            return pd.DataFrame()

        prices = ['mid', 'bid', 'ask']
        ohlc = ['o', 'h', 'l', 'c']

        final_data = []
        for candle in data:
            if candle['complete'] == False:
                continue
            new_dict = {}
            new_dict['volume'] = candle['volume']
            new_dict['time'] = parser.parse(candle['time'])
            for p in prices:
                if p in candle:
                    for o in ohlc:
                        new_dict[f"{p}_{o}"] = float(candle[p][o])
            final_data.append(new_dict)
        df = pd.DataFrame.from_dict(final_data)
        return df

    def last_complete_candle(self, pair_name, granularity):
        df = self.get_candles_df(pair_name, granularity=granularity, count=10)
        if df is None or df.shape[0] == 0:
            return None
        return df.iloc[-1].time

    def web_api_candles(self, pair_name, granularity, count):
        df = self.get_candles_df(pair_name, granularity=granularity, count=count)
        if df.shape[0] == 0:
            return None

        cols = ['time', 'mid_o', 'mid_h', 'mid_l', 'mid_c']
        df = df[cols].copy()

        df['time'] = df.time.dt.strftime("%y-%m-%d %H:%M")

        return df.to_dict(orient='list')

    def place_trade(self, pair_name: str, units: float, direction: int,
                stop_loss: float = None, take_profit: float = None):
    
        from infrastructure.instrument_collection import instrumentCollection as ic  # Local import

        base_url = 'https://api-fxpractice.oanda.com/v3'
        url = f"/accounts/{defs.ACCOUNT_ID}/orders"

        instrument = ic.instruments_dict[pair_name]
        units = round(units, instrument.tradeUnitsPrecision)

        if direction == defs.SELL:
            units = units * -1
        if direction == defs.BUY:
            units = units * 1

        data = dict(
            order=dict(
                units=str(units),
                instrument=pair_name,
                type="MARKET"
            )
        )

        if stop_loss is not None:
            sld = dict(price=str(round(stop_loss, instrument.displayPrecision)))
            data['order']['stopLossOnFill'] = sld

        if take_profit is not None:
            tpd = dict(price=str(round(take_profit, instrument.displayPrecision)))
            data['order']['takeProfitOnFill'] = tpd

        ok, response = self.make_request(url, verb="post", data=data, code=201)

        if ok == True and 'orderFillTransaction' in response:
            return response['orderFillTransaction']['id']
        else:
            return None


    def close_trade(self, trade_id):
        base_url = 'https://api-fxpractice.oanda.com/v3/'
        url = f"accounts/{defs.ACCOUNT_ID}/trades/{trade_id}/close"
        ok, _ = self.make_request(url, verb="put", code=200)

        if ok == True:
            print(f"Closed {trade_id} successfully")
        else:
            print(f"Failed to close {trade_id}")

        return ok

    def get_open_trade(self, trade_id):
        base_url = 'https://api-fxpractice.oanda.com/v3/'
        url = f"accounts/{defs.ACCOUNT_ID}/trades/{trade_id}"
        ok, response = self.make_request(url)

        if ok == True and 'trade' in response:
            return OpenTrade(response['trade'])

    def get_open_trades(self):
        base_url = 'https://api-fxpractice.oanda.com/v3/'
        url = f"accounts/{defs.ACCOUNT_ID}/openTrades"
        ok, response = self.make_request(url)

        if ok == True and 'trades' in response:
            return [OpenTrade(x) for x in response['trades']]

    def get_prices(self, instruments_list):
        base_url = 'https://api-fxpractice.oanda.com/v3/'
        url = f"accounts/{defs.ACCOUNT_ID}/pricing"

        params = dict(
            instruments=','.join(instruments_list),
            includeHomeConversions=True
        )

        ok, response = self.make_request(url, params=params)

        if ok == True and 'prices' in response and 'homeConversions' in response:
            return [ApiPrice(x, response['homeConversions']) for x in response['prices']]

        return None
