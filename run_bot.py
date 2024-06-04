import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from bot.bot import Bot
from infrastructure.instrument_collection import instrumentCollection

if __name__ == "__main__":
    instrumentCollection.LoadInstruments("./data")
    b = Bot()
    b.run()