import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from stream_example.streamer import run_streamer
from db.db import DataDB

def db_tests():
    d = DataDB()

    print(d.query_distinct(DataDB.SAMPLE_COLL, 'age'))

if __name__ == '__main__':
    db_tests()
    #api = OandaApi()
    #instrumentCollection.CreateDB(api.get_account_instruments())
    #instrumentCollection.LoadInstruments("./data")

