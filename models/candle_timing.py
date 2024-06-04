import datetime as dt

class CandleTiming:

    def __init__(self, last_time, is_ready=False):
        self.last_time = last_time
        self.is_ready = is_ready

    def __repr__(self):
        if self.last_time is not None:
            return f"last_candle:{dt.datetime.strftime(self.last_time, '%y-%m-%d %H:%M')} is_ready:{self.is_ready}"
        else:
            return "last_candle:None is_ready:False"