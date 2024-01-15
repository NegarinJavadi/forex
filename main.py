from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from stream_example.streamer import run_streamer
from db.db import DataDB


if __name__ == '__main__':
    #api = OandaApi()
    #instrumentCollection.LoadInstruments("./data")
    #run_streamer()
    d = DataDB()
    d.test_connection()

