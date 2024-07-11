import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
#directory of the current file and joins it with '..' to move one level up in the directory structure. The result is stored in main_dir
import sys
sys.path.insert(0,main_dir)
#allows importing modules from the parent directory

import json
import time
import constants.defs as defs
from bot.candle_manager import CandleManager
from infrastructure.log_wrapper import LogWrapper
from models.trade_settings import TradeSettings
from api.oanda_api import OandaApi
from bot.technicals_manager import get_trade_decision
from bot.trade_manager import place_trade


class Bot:

    ERROR_LOG = "error"
    #This sets a class attribute ERROR_LOG to the string "error"
    MAIN_LOG = "main"
    #This sets a class attribute MAIN_LOG to the string "main"
    GRANULARITY = "H1"
    #This sets a class attribute GRANULARITY to the string "H1"
    SLEEP = 10
    #represents a delay in seconds

    def __init__(self):
        #method called when an instance of the class is created
        self.load_settings()
        #method to load bot settings
        self.setup_logs()
        #method to set up logging

        self.api = OandaApi()
        #Creates an instance of OandaApi
        self.candle_manager = CandleManager(self.api, self.trade_settings, self.log_message, Bot.GRANULARITY)
        #Creates an instance of CandleManager

        self.log_to_main("Bot started")
        #Logs a message indicating the bot has started using the log_to_main method
        self.log_to_error("Bot started")
        #Logs a message indicating the bot has started using the log_to_error method.

    def load_settings(self):
        with open("./bot/settings.json", "r") as f:
            #Opens the settings.json file in read mode
            data = json.loads(f.read())
            #Reads the file content and parses it as JSON, storing the result in data
            self.trade_settings = { k: TradeSettings(v, k) for k,v in data['pairs'].items()}
            #Creates a dictionary of TradeSettings objects from the pairs in the JSON data
            self.trade_risk = data['trade_risk']
            #Assigns the trade_risk from the JSON data to self.trade_risk

    def setup_logs(self):
        self.logs = {}
        #Initializes an empty dictionary for logs.
        for k in self.trade_settings.keys(): #iterates over the keys
            self.logs[k] = LogWrapper(k)
            #Creates a LogWrapper for each key and adds it to the logs dictionary
            self.log_message(f"{self.trade_settings[k]}", k)
            #Logs the trade settings for each key
        self.logs[Bot.ERROR_LOG] = LogWrapper(Bot.ERROR_LOG)
        #Creates a LogWrapper for error logs
        self.logs[Bot.MAIN_LOG] = LogWrapper(Bot.MAIN_LOG)
        #Creates a LogWrapper for main logs
        self.log_to_main(f"Bot started with {TradeSettings.settings_to_str(self.trade_settings)}")
        #Logs a message indicating the bot started with the trade settings

    def log_message(self, msg, key):
        self.logs[key].logger.debug(msg)
        #Logs a message at the debug level using the logger for the given key

    def log_to_main(self, msg):
        self.log_message(msg, Bot.MAIN_LOG)

    def log_to_error(self, msg):
        self.log_message(msg, Bot.ERROR_LOG)

    def process_candles(self, triggered):
        if len(triggered) > 0:
            #Checks if there are any triggered candles
            self.log_message(f"process_candles triggered:{triggered}", Bot.MAIN_LOG)
            #Logs the triggered candles
            for p in triggered:
                #Iterates over the triggered candles
                last_time = self.candle_manager.timings[p].last_time
                #Gets the last time for the candle
                trade_decision = get_trade_decision(last_time, p, Bot.GRANULARITY, self.api, 
                                                    self.trade_settings[p], self.log_message)
                #Gets the trade decision based on the last time, pair, granularity, API, trade settings, and log message
                if trade_decision is not None and trade_decision.signal != defs.NONE:
                    self.log_message(f"Place Trade: {trade_decision}", p)
                    #Logs the trade decision
                    self.log_to_main(f"Place Trade: {trade_decision}")
                    #Logs the trade decision to the main log
                    place_trade(trade_decision, self.api, self.log_message, self.log_to_error, self.trade_risk)
                    #Places the trade
    
    def run(self):
        #run method to start the bot
        while True:
            #infinite loop to keep the bot running
            time.sleep(Bot.SLEEP)
            try:
                self.process_candles(self.candle_manager.update_timings())
                #updated timings from the candle manager
            except Exception as error:
                self.log_to_error(f"CRASH: {error}")
                #Logs the error to the error log
                break
