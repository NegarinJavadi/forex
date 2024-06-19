import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from api.oanda_api import OandaApi
from db.db import DataDB
from infrastructure.instrument_collection import instrumentCollection

def db_tests():
    d = DataDB()
    print(d.query_distinct(DataDB.SAMPLE_COLL, 'get'))

if __name__ == '__main__':
   
    api = OandaApi()
    instrumentCollection.CreateDB(api.get_account_instruments())
    

