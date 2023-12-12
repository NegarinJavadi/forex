class instruments:



    def __init__(self, name, ins_type, displayName,
                 piplocation, tradeUnitsPrecision, marginRate):
        self.name = name
        self.ins_type = ins_type
        self.displayName = displayName
        self.piplocation = pow(10, piplocation)
        self.tradeUnitsPrecision = tradeUnitsPrecision
        self.marginRate = float(marginRate)



    def __repr__(self):
        return str(vars(self))
    

    @classmethod
    def FromApiObject(cls, ob):
        return instruments(
            ob['name'],
            ob['type'],
            ob['displayName'],
            ob['piplocatio'],
            ob['tradeUnitsPrecision'],
            ob['marginRate']
        )