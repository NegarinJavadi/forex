from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from simulation.ma_cross import run_ma_sim
from dateutil import parser
from db.db import DataDB
from infrastructure.collect_data import run_collection

#def db_tests():
#    d = DataDB()

    #d.add_one(DataDB.SAMPLE_COLL, dict(age=12, name='paddy', street= 'elm'))
    #print(d.query_single(DataDB.SAMPLE_COLL, age=34))
    
    #print(d.query_distinct(DataDB.SAMPLE_COLL, 'age'))

if __name__ == '__main__':
    #run_ma_sim()
    api = OandaApi()
    print(api.fetch_candles("EUR_USD", granularity="D", price="MB"))

    #instrumentCollection.LoadInstruments("./data")
    #run_collection(instrumentCollection, api)
    #instrumentCollection.PrintInstruments()
    
    #instrumentCollection.CreateDB(api.get_account_instruments())
    
    #instrumentCollection.LoadInstrumentsDB()
    #print(instrumentCollection.instruments_dict)
    
    #run_streamer()
    #d = DataDB()
    #d.test_connection()
    #db_tests()

