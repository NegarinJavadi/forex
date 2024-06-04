import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from openfx_api.openfx_api import OpenFxApi
from infrastructure.instrument_collection import instrumentCollection
from stream_example.streamer import run_streamer
from db.db import DataDB


if __name__ == '__main__':
   
    api = OpenFxApi()
    instrumentCollection.LoadInstrumentsDB()
    print(instrumentCollection.instruments_dict)
    #instrumentCollection.CreateDB(api.get_account_instruments())
    #instrumentCollection.LoadInstruments("./data")

