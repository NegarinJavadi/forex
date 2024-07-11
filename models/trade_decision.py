class TradeDecision:

    def __init__(self, row):
    #It takes self (referring to the instance of the class itself) and row as parameters
        self.gain = row.GAIN
        #This means that the gain attribute of the TradeDecision instance will hold the value of GAIN from row
        self.loss = row.LOSS
        self.signal = row.SIGNAL
        self.sl = row.SL
        self.tp = row.TP
        self.pair = row.PAIR

    def __repr__(self):
    #This defines the __repr__ method, which is a special method used to define how an object is represented as a string
        return f"TradeDecision(): {self.pair} dir:{self.signal} gain:{self.gain:.4f} sl:{self.sl:.4f} tp:{self.tp:.4f}"
        
