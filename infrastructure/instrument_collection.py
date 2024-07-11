import os
import sys
main_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, main_dir)

import requests
from db.db import DataDB
import json
from models.instruments import Instrument
from constants import defs
from api import oanda_api

class InstrumentCollection:
    FILENAME = "instruments.json"
    #A constant that stores the name of the file where instrument data will be saved or loaded from
    API_KEYS = ['name', 'type', 'displayName', 'pipLocation',
                'displayPrecision', 'tradeUnitsPrecision', 'marginRate']
    # A list of keys that are important for each instrument. These keys will be used to filter relevant information from the data


    def __init__(self):
        self.instruments_dict = {}
        #Initializes an empty dictionary to store instrument data


    def LoadInstruments(self, path):
    #Defines a method to load instrument data from a file.
        self.instruments_dict = {}
        #Resets the instruments dictionary to empty
        fileName = f"{path}/{self.FILENAME}"
        #Constructs the full file path
        with open(fileName, "r") as f:
        #Opens the file for reading
            data = json.loads(f.read())
            #Reads and parses the JSON data from the file
            for k, v in data.items():
                self.instruments_dict[k] = Instrument.FromApiObject(v)
            #Iterates over the data and converts each item to an Instrument object, storing it in self.instruments_dict
    

    def LoadInstrumentsDB(self):
    #load instrument data from a database
        self.instruments_dict = {}
        #Resets the instruments dictionary to empty
        data = DataDB().query_single(DataDB.INSTRUMENTS_COLL)
        #Queries the database to get the instruments data

        #data = DataDB().query_single('forex_calendar')
        #relevant_data = {k: v for k, v in data.items() if hasattr(v, 'get')}
        for k, v in data.items():
            self.instruments_dict[k] = Instrument.FromApiObject(v)
        #Iterates over the data and converts each item to an Instrument object, storing it in self.instruments_dict


    def CreateFile(self, data, path):
    #to create a file from provided data
        if data is None:
            print("Instrument file creation failed")
            return
        
        instruments_dict = {}
        #Initializes an empty dictionary to store filtered instrument data
        for i in data:
            key = i['name']
        #Iterates over the data and extracts the name as a key
            if key is not None:
                instruments_dict[key] = { k: i[k] for k in self.API_KEYS}
            #Filters the data to include only relevant keys

        fileName = f"{path}/{self.FILENAME}"
        #Constructs the full file path
        with open(fileName, "w") as f:
            f.write(json.dumps(instruments_dict, indent=2))    
        #Constructs the full file path

    def CreateDB(self, data):
    # to create a database from provided data
        if data is None:
            print("Instrument file creation failed")
            return
        
        instruments_dict = {}
        #Initializes an empty dictionary to store filtered instrument data
        for i in data:
            key = i['name']
            instruments_dict[key] = { k: i[k] for k in self.API_KEYS }
        #Iterates over the data and filters it to include only relevant keys

        database = DataDB()
        #Creates an instance of the DataDB class
        database.delete_many(DataDB.INSTRUMENTS_COLL)
        #Deletes any existing data in the instruments collection
        database.add_one(DataDB.INSTRUMENTS_COLL, instruments_dict)
        #Adds the filtered data to the database


    def PrintInstruments(self):
        #to print the instruments
        [print(k,v) for k,v in self.instruments_dict.items()]
        # Iterates over the instruments dictionary and prints each key-value pair
        print(len(self.instruments_dict.keys()), "instruments")
        #Prints the total number of instruments


instrumentCollection = InstrumentCollection()
#Creates an instance of the InstrumentCollection class


     