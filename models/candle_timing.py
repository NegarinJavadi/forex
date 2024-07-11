import datetime as dt

class CandleTiming:

    def __init__(self, last_time, is_ready=False):
    #The is_ready parameter has a default value of False, which means if we don't provide a value for it when creating an object,
    #it will automatically be set to False
        self.last_time = last_time
        #This line sets a property called last_time for the object
        self.is_ready = is_ready
        #This line sets a property called is_ready for the object

    def __repr__(self):
    #It determines what will be shown when we print the object
        if self.last_time is not None:
            return f"last_candle:{dt.datetime.strftime(self.last_time, '%y-%m-%d %H:%M')} is_ready:{self.is_ready}"
        else:
            return "last_candle:None is_ready:False"