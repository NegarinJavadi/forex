import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

import pandas as pd
pd.set_option('display.max_columns', None)
#when printing a DataFrame, all columns will be displayed
pd.set_option('expand_frame_repr', False)
#DataFrame display does not wrap columns across multiple lines

from technicals.indicators import BollingerBands
from api.oanda_api import OandaApi
from models.trade_settings import TradeSettings
from models.trade_decision import TradeDecision
import constants.defs as defs


ADDROWS = 20

def apply_signal(row, trade_settings: TradeSettings):
    #whether to buy, sell, or do nothing based on specific conditions

    if row.SPREAD <= trade_settings.maxspread and row.GAIN >= trade_settings.mingain:
    #Checks if the spread and gain meet the criteria from trade_settings
        if row.mid_c > row.BB_UP and row.mid_o < row.BB_UP:
        #If the current price (mid_c) crosses above the upper Bollinger Band (BB_UP), it signals to sell.
            return defs.SELL
        elif row.mid_c < row.BB_LW and row.mid_o > row.BB_LW:
        #If the current price crosses below the lower Bollinger Band (BB_LW), it signals to buy
            return defs.BUY
    return defs.NONE

def apply_SL(row, trade_settings: TradeSettings):
    if row.SIGNAL == defs.BUY:
        return row.mid_c - (row.GAIN / trade_settings.riskreward)
    #SL is set below the current price minus a calculated risk/reward ratio
    elif row.SIGNAL == defs.SELL:
        return row.mid_c + (row.GAIN / trade_settings.riskreward)
    #SL is set above the current price plus a calculated risk/reward ratio
    return 0.0

def apply_TP(row):
    if row.SIGNAL == defs.BUY:
        return row.mid_c + row.GAIN
    #TP is set above the current price by the gain amount
    elif row.SIGNAL == defs.SELL:
        return row.mid_c - row.GAIN
    #TP is set below the current price by the gain amount
    return 0.0

def process_candles(df: pd.DataFrame, pair, trade_settings:TradeSettings, log_message):
#processes a DataFrame of candle data
    df.reset_index(drop= True, inplace=True)
    df['PAIR'] = pair
    df['SPREAD'] = df.ask_c- df.bid_c

    df = BollingerBands(df, trade_settings.n_ma, trade_settings.n_std)
    df ['GAIN'] = abs(df.mid_c - df.BB_MA)
    #Calculates the gain as the absolute difference between the current price and the Bollinger Bands moving average (BB_MA)
    df['SIGNAL'] = df.apply(apply_signal, axis=1, trade_settings=trade_settings)
    df['TP'] = df.apply(apply_TP, axis=1)
    df['SL'] = df.apply(apply_SL, axis=1, trade_settings=trade_settings)
    df['LOSS'] = abs(df.mid_c - df.SL)

    log_cols = ['PAIR', 'time', 'mid_c', 'mid_o', 'SL', 'TP', 'SPREAD', 'GAIN', 'LOSS', 'SIGNAL']
    log_message(f"process_candles:\n{df[log_cols].tail()}", pair)
    #Logs the last few rows of the relevant columns
    return df[log_cols].iloc[-1]


def fetch_candles(pair, row_count, candle_time, granularity,
                    api: OandaApi, log_message):
    #fetches candle data from the Oanda API

    df = api.get_candles_df(pair, count=row_count, granularity=granularity)
    #Requests the specified number of candles for a currency pair

    if (df is None) or (df.shape[0] == 0):
        log_message("tech_manager fetch_candles failed to get candles", pair)
        return None
    
    if df.iloc[-1].time != candle_time:
        log_message(f"tech_manager fetch_candles {df.iloc[-1].time} not correct", pair)
        return None

    return df

def get_trade_decision(candle_time, pair, granularity, api: OandaApi, 
                            trade_settings: TradeSettings, log_message):
#decides whether to trade based on the most recent candle data

    max_rows = trade_settings.n_ma + ADDROWS
    #Calculates the number of rows to fetch based on trade settings and ADDROWS

    log_message(f"tech_manager: max_rows:{max_rows} candle_time:{candle_time} granularity:{granularity}", pair)

    df = fetch_candles(pair, max_rows, candle_time,  granularity, api, log_message)

    if df is not None:
        last_row = process_candles(df, pair, trade_settings, log_message)
        #Processes the candle data to get the last row
        return TradeDecision(last_row)

    return None