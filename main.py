import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from simulation.ema_macd_mp import run_process
from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection

if __name__ == '__main__':
   
    api = OandaApi()
    instrumentCollection.LoadInstruments("./data")
    run_process()
    

