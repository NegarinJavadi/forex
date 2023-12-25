from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from simulation.ma_cross import run_ma_sim
from simulation.ma_cross import run_ema_macd
from dateutil import parser
from infrastructure.collect_data import run_collection


if __name__ == '__main__':
#    run_ma_sim()
#    api = OandaApi()
    instrumentCollection.LoadInstruments("./data")
    run_ema_macd(instrumentCollection)
#    run_collection(instrumentCollection, api)
