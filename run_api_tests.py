
import time
import custom_constants.defs as defs
from api.oanda_api import OandaApi
from dateutil.parser import parse
from infrastructure.instrument_collection import instrumentCollection
from infrastructure.collect_data import run_collection

if __name__ == "__main__":
    api = OandaApi()
    instrumentCollection.LoadInstruments("./data")

    run_collection(instrumentCollection, api)