from db.db import DataDB
from scraping.dailyfx_com import dailyfx_com
from scraping.investing_com import investing_com
from scraping.bloomberg_com import bloomberg_com
from scraping.fx_calendar import fx_calendar

if __name__ == "__main__":
    print(fx_calendar())
     
    #bloomberg_com()
    #print(bloomberg_com())
    #[print(x) for x in bloomberg_com()]

    #investing_com()
    #print(investing_com()) 