from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
import time

from models.candle_timing import CandleTiming
from bot.trade_risk_calculator import get_trade_units
import custom_constants.defs as defs

def lm(msg, pair):
    pass
    #print(msg, pair)

if __name__ == '__main__':
    api = OandaApi()
    instrumentCollection.LoadInstruments("./data")

    #print(api.get_prices("GBP_JPY"))

    print("GBP_JPY", get_trade_units(api, "GBP_JPY", defs.BUY, 0.4, 20, lm))
    print("GBP_USD", get_trade_units(api, "GBP_USD", defs.BUY, 0.4, 20, lm))