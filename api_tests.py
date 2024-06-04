import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from dateutil.parser import parse
from openfx_api.openfx_api import OpenFxApi
from infrastructure.instrument_collection import instrumentCollection
from infrastructure.collect_data import run_collection

if __name__ == '__main__':
    api = OpenFxApi()
    #instruments = api.get_account_instruments()
    #instrumentCollection.CreateFile(instruments, "./data")
    instrumentCollection.LoadInstruments("./data")
    
 
    #print(api.get_candles_df(pair_name="EURUSD", count=-10, granularity="H1"))
    run_collection(instrumentCollection, api)