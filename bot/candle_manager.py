import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from api.oanda_api import OandaApi
from models.candle_timing import CandleTiming

class CandleManager:

    def __init__(self, api: OandaApi, trade_settings, log_message, granularity):
        #api: An instance of the OandaApi class for interacting with the API.
        #trade_settings: Settings for trading.
        #log_message: A function for logging messages.
        #granularity: The time interval for the candles (e.g., hourly).
        self.api = api
        #Stores the api parameter in the instance variable self.api
        self.trade_settings = trade_settings
        self.log_message = log_message
        self.granularity = granularity
        self.pairs_list = list(self.trade_settings.keys())
        #Creates a list of trading pairs (e.g., currency pairs) from the keys of the trade_settings dictionary and stores it in the instance variable self.pairs_list
        self.timings = { p: CandleTiming(self.api.last_complete_candle(p, self.granularity)) for p in self.pairs_list }
        #Creates a dictionary called timings where each key is a trading pair and each value is a CandleTiming object. The CandleTiming object is initialized with the last complete candle for each trading pair fetched from the API.
        for p, t in self.timings.items():
            #loop in the timings dictionary
            self.log_message(f"CandleManager() init last_candle:{t}", p)

    def update_timings(self):
        #pdates the candle timings and returns a list of triggered pairs
        triggered = []
        #Initializes an empty list called triggered to keep track of pairs that have new candles

        for pair in self.pairs_list:
            #starts a loop over each trading pair
            current = self.api.last_complete_candle(pair, self.granularity)
            #Fetches the last complete candle for the current trading pair from the API and stores it in the variable current
            if current is None:
                self.log_message("Unable to get candle", pair)
                #candle could not be retrieved for the current trading pair
                continue
            self.timings[pair].is_ready = False
            #Sets the is_ready attribute of the CandleTiming object for the current trading pair to False
            if current > self.timings[pair].last_time:
                self.timings[pair].is_ready = True
                self.timings[pair].last_time = current
                self.log_message(f"CandleManager() new candle:{self.timings[pair]}", pair)
                triggered.append(pair)
                #Adds the current trading pair to the triggered list, indicating that it has a new candle
        return triggered