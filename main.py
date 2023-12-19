from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from simulation.ma_cross import run_ma_sim

if __name__ == '__main__':
#    run_ma_sim(curr_list=["EUR", "USD", "GBP", "JPY", "AUD", "CAD"])
    
    api = OandaApi()
    print(api.fetch_candles("EUR_USD", granularity="D", price="MB"))

#    instrumentCollection.CreateFile(api.get_account_instruments(), "./data")
#    instrumentCollection.LoadInstruments("./data")
#    instrumentCollection.PrintInstruments()
