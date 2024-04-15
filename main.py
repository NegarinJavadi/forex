import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from simulation.ma_cross import run_ma_sim
from dateutil import parser


if __name__ == '__main__':
    api = OandaApi()
    
    dfr = parser.parse("2021-04-21T01:00:00Z")
    dto = parser.parse("2021-04-28T16:00:00Z")

    df_candles = api.get_candles_df("EUR_USD", granularity="H1",
                                    date_f=dfr, date_t=dto)
    
    print(df_candles.head())
    print()
    print(df_candles.tail())

