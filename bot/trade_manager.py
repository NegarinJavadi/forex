import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from api.oanda_api import OandaApi
from bot.trade_risk_calculator import get_trade_units
from models.trade_decision import TradeDecision


def trade_is_open(pair, api:OandaApi):
    #checks if there is an open trade for a given currency pair

    open_trades = api.get_open_trades()
    #to retrieve a list of currently open trades

    for ot in open_trades:
    #Iterates through each open trade (ot)
        if ot.instrument == pair:
        #f the trade's instrument matches the specified pair, it returns the open trade (ot)
            return ot
    
    return None

def place_trade(trade_decision: TradeDecision, api: OandaApi, log_message, log_error, trade_risk):
#places a trade
    ot = trade_is_open(trade_decision.pair, api)
    #check if there's already an open trade for the given pair

    if ot is not None:
        log_message(f"Failed to place trade {trade_decision}, already open: {ot}", trade_decision.pair)
        #Logs a message indicating the trade could not be placed because a trade is already open
        return None

    trade_amount = get_trade_units(api, trade_decision.pair, 
                            trade_decision.loss, trade_risk, log_message)
    #calculate the amount of units to trade based on the loss and risk parameters
    trade_id = api.place_trade(
        trade_decision.pair, 
        trade_amount,
        trade_decision.signal,
        trade_decision.sl,
        trade_decision.tp
    )
    #to place the trade with the calculated trade amount, signal (buy/sell), stop loss (SL), and take profit (TP) levels

    if trade_id is None:
        log_error(f"ERROR placing {trade_decision}")
        log_message(f"ERROR placing {trade_decision}", trade_decision.pair)
    else:
        log_message(f"placed trade_id:{trade_id} for {trade_decision}", trade_decision.pair)
