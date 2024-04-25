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

    print(d.query_all(DataDB.SAMPLE_COLL))

if __name__ == '__main__':
    #api = OandaApi()
    #instrumentCollection.LoadInstruments("./data")
    #d = DataDB()
    #d.test_connection()
    db_tests()

