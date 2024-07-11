import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.append(main_dir)

import pandas as pd
import datetime as dt
from dateutil import parser
from infrastructure.instrument_collection import InstrumentCollection
from api.oanda_api import OandaApi

#This code involves fetching and saving financial market data (candlestick data) for different currency pairs using an API and organizing it for further use
CANDLE_COUNT = 3000
#sets the number of candlesticks to fetch and process for each time increment

INCREMENTS = {
    'M5' : 5 * CANDLE_COUNT,
    'H1' : 60 * CANDLE_COUNT,
    'H4' : 240 * CANDLE_COUNT
}
#defines the number of minutes corresponding to each granularity (time period)


def save_file(final_df: pd.DataFrame, file_prefix, granularity, pair):
#saves the final DataFrame to a file
    filename = f"{file_prefix}{pair}_{granularity}.pkl"
    #Constructs the filename
    final_df.drop_duplicates(subset=['time'], inplace=True)
    #Removes duplicate rows based on the 'time' column
    final_df.sort_values(by='time', inplace=True)
    #Sorts the DataFrame by time
    final_df.reset_index(drop=True, inplace=True)
    #Resets the index of the DataFrame
    final_df.to_pickle(filename)
    #Saves the DataFrame to a pickle file

    s1 = f"*** {pair} {granularity} {final_df.time.min()} {final_df.time.max()}"
    #Constructs a summary string
    print(f"*** {s1} --> {final_df.shape[0]} candles ***")


def fetch_candles(pair, granularity, date_f: dt.datetime,
                  date_t: dt.datetime, api: OandaApi):
#fetches candle data from the API
    attempts = 0
    #Initializes the attempt counter

    while attempts < 3:
    #Tries up to 3 times to fetch the data

        candles_df = api.get_candles_df(
            pair,
            granularity=granularity,
            date_f=date_f,
            date_t=date_t
        )
        #Calls the API to get the candle data

        if candles_df is not None:
            break

        attempts += 1
        #Increments the attempt counter if data is not received

    if candles_df is not None and candles_df.empty == False:
        return candles_df
    else:
        return None


def collect_data(pair, granularity, date_f, date_t, file_prefix, api: OandaApi):
#collects and processes data for a given pair and granularity

    time_step = INCREMENTS[granularity]
    #Gets the time step in minutes from the INCREMENTS dictionary

    end_date = parser.parse(date_t)
    #Parses the end date
    from_date = parser.parse(date_f)

    candle_dfs = []
    #Initializes a list to store fetched DataFrames

    to_date = from_date
    #Sets the initial to_date to from_date

    while to_date < end_date:
    #Loops until to_date reaches end_date
        to_date = from_date + dt.timedelta(minutes=time_step)
        #Increments to_date by time_step
        if to_date > end_date:
            to_date = end_date
        #Adjusts to_date if it exceeds end_date

        candles = fetch_candles(
            pair,
            granularity, 
            from_date,
            to_date,
            api
        )
        #Fetches candle data for the current time range

        if candles is not None:
            candle_dfs.append(candles)
            #Adds the data to the list if it is not None
            print(f"{pair} {granularity} {from_date} {to_date} --> {candles.shape[0]} candles loaded")
        else:
            print(f"{pair} {granularity} {from_date} {to_date} --> NO CANDLES")
            
        from_date = to_date
        #Updates from_date to to_date for the next iteration

    if len(candle_dfs) > 0:
        final_df = pd.concat(candle_dfs)
        #Concatenates all fetched DataFrames if any data is collected
        save_file(final_df, file_prefix, granularity, pair)
        #Saves the final DataFrame to a file
    else:
        print(f"{pair} {granularity} --> NO DATA SAVED!")


def run_collection(ic: InstrumentCollection, api: OandaApi):
#runs the data collection process for all currency pairs and granularities
    our_curr = [ "AUD", "CAD", "JPY", "USD", "EUR", "GBP", "NZD"]
    #List of currencies to process
    for p1 in our_curr:
    #Nested loops to create currency pairs
        for p2 in our_curr:
            pair = f"{p1}_{p2}"
            #Constructs the currency pair string
            if pair in ic.instruments_dict.keys():
            #Checks if the pair is in the instrument collection
                for granularity in ["M5", "H1", "H4"]:
                #Loops through each granularity
                    print(pair, granularity)
                    collect_data(
                        pair,
                        granularity,
                        "2021-10-01T00:00:00Z",
                        "2024-05-03T00:00:00Z",
                        "./data/",
                        api
                    )
                    #Calls collect_data to fetch and save data for the pair and granularity


