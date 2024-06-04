
import time
import custom_constants.defs as defs
from openfx_api.openfx_api import OpenFxApi
from dateutil.parser import parse
from infrastructure.instrument_collection import instrumentCollection
from infrastructure.collect_data import run_collection

if __name__ == "__main__":
    api = OpenFxApi()
    instrumentCollection.LoadInstruments("./data")

    run_collection(instrumentCollection, api)