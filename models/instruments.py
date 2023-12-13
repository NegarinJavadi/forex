class Instrument:

    def __init__(self, name, ins_type, displayName,
                 piplocation, tradeUnitsPrecision, marginRate):
        self.name = name
        self.ins_type = ins_type
        self.displayName = displayName
        self.piplocation = pow(10, piplocation) if piplocation is not None else None
        self.tradeUnitsPrecision = tradeUnitsPrecision
        self.marginRate = float(marginRate) if marginRate is not None else None



    def __repr__(self):
        return str(vars(self))


    @classmethod
    def FromApiObject(cls, ob):
       return Instrument(
          ob.get('name'),
          ob.get('type'),
          ob.get('displayName'),
          ob.get('iplocation', None),
          ob.get('tradeUnitsPrecision'),
          ob.get('marginRate'),

         )

