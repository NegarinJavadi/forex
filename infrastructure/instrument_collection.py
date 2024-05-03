import os
import sys

import requests

main_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, main_dir)

from db.db import DataDB
import json
from models.instruments import Instrument
from custom_constants import defs
from api import oanda_api

class InstrumentCollection:
    FILENAME = "instruments.json"
    API_KEYS = ['name', 'type', 'displayName','pipLocation', 
                'displayPrecision', 'tradeUnitsPrecision', 'marginRate']
    

    def get_account_instruments(self, ACCOUNT_ID):
        base_url = 'https://api-fxpractice.oanda.com/V3/'
        endpoint = f'/accounts/{defs.ACCOUNT_ID}/instruments'
        url = base_url + endpoint
        
        headers = {
            'Authorization': 'Bearer YOUR_API_KEY_HERE'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None


    def __init__(self):
        self.instruments_dict = {}


    def LoadInstruments(self, path):
        self.instruments_dict = {}
        fileName = f"{path}/{self.FILENAME}"
        with open(fileName, "r") as f:
            data = json.loads(f.read())
            for k, v in data.items():
                self.instruments_dict[k] = Instrument.FromApiObject(v)

    
    def LoadInstrumentsDB(self):
        self.instruments_dict = {}
        data = DataDB().query_single(DataDB.INSTRUMENTS_COLL)
        for k, v in data.items():
            self.instruments_dict[k] = Instrument.FromApiObject(v)


    def CreateFile(self, data, path):
        if data is None:
            print("Instrument file creation failed")
            return
        
        instruments_dict = {}
        for i in data:
            key = i['name']
            if key is not None:
                instruments_dict[key] = { k: i[k] for k in self.API_KEYS}

        fileName = f"{path}/{self.FILENAME}"
        with open(fileName, "w") as f:
            f.write(json.dumps(instruments_dict, indent=2))    
    
    def CreateDB(self, data):
        if data is None:
            print("Instrument file creation failed")
            return
        
        instruments_dict = {}
        for i in data:
            key = i['name']
            if key is not None:
                instruments_dict[key] = { k: i[k] for k in self.API_KEYS}
            
            database = DataDB()
            database.delete_many(DataDB.INSTRUMENTS_COLL)
            database.add_one(DataDB.INSTRUMENTS_COLL, instruments_dict)


    def PrintInstruments(self):
        [print(k,v) for k,v in self.instruments_dict.items()]
        print(len(self.instruments_dict.keys()), "instruments")


instrumentCollection = InstrumentCollection()


     