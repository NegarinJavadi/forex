import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from simulation.ma_cross import run_ma_sim
from simulation.ema_macd import run_ema_macd
from dateutil import parser
from infrastructure.collect_data import run_collection


if __name__ == '__main__':
    #api = OandaApi()
    instrumentCollection.LoadInstruments("./data")
    run_ema_macd(instrumentCollection)

