import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from api.oanda_api import OandaApi
import constants.defs as defs
from infrastructure.instrument_collection import instrumentCollection as ic

def get_trade_units(api: OandaApi, pair, signal, loss, trade_risk, log_message):
#calculates the number of units to trade based on the given risk and loss parameters
    prices = api.get_prices([pair])
    #get the current prices for the specified currency pair
    if prices is None or len(prices) == 0:
        log_message("get_trade_units() Prices is none", pair)
    #f the prices are None or empty, logs an error message and returns False
        return False
    
    price = None
    for p in prices:
        if p.instrument == pair:
            price = p
            break
    if price == None:
        log_message("get_trade_units() price is None???", pair)
        return False
    
    log_message(f"get_trade_units() price {price}", pair)
    #for debugging and verification
    conv = price.buy_conv
    #Sets the conversion rate (conv) based on the trade signal
    if signal == defs.SELL:
        conv = price.sell_conv
    pipLocation = ic.instruments_dict[pair].pipLocation
    num_pips = loss / pipLocation
    #Calculates the number of pips corresponding to the specified loss amount
    per_pip_loss = trade_risk / num_pips
    #Calculates the monetary loss per pip
    units = per_pip_loss / (conv * pipLocation)
    #Calculates the number of units to trade
    
    log_message(f"{pipLocation} {num_pips} {per_pip_loss} {units:.1f}", pair)
    #Logs detailed information about the calculation for debugging and verification
    return units