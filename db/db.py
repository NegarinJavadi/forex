import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.append('/home/negarin/Desktop/Appendix/code')

from pymongo import MongoClient, errors

from custom_constants.defs import MONGO_CONN_STR

class DataDB:

    SAMPLE_COLL = "forex_sample"

    def __init__(self):

        self.client = MongoClient(MONGO_CONN_STR)
        self.db = self.client.forex_learning
        

    def test_connection(self):
    
        print(self.db.list_collection_names())
    


