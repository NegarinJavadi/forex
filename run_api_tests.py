
import time
import constants.defs as defs
from api.oanda_api import OandaApi
from dateutil.parser import parse
from infrastructure.instrument_collection import instrumentCollection
from infrastructure.collect_data import run_collection

if __name__ == "__main__":
    api = OandaApi()
    
    instrumentCollection.LoadInstruments("./data")
    
    api.place_trade("EUR_USD", 100, 1, take_profit=1.076, stop_loss=1.084)

