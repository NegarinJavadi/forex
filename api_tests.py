import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
import time
from models.candle_timing import CandleTiming

if __name__ == '__main__':
    api = OandaApi()
    instrumentCollection.LoadInstruments("./data")
    api.place_trade("EUR_USD", 100, 1, take_profit=1.09, stop_loss=1.075)
    #dd = (api.last_complete_candle("EUR_USD", granularity="M5"))
    #print(CandleTiming(dd))