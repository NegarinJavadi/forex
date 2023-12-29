class Instrument:

    def __init__(self, name, ins_type, displayName,
                 pipLocation, tradeUnitsPrecision, marginRate,
                 displayPrecision):
        self.name = name
        self.ins_type = ins_type
        self.displayName = displayName
        self.pipLocation = pow(10, pipLocation) if pipLocation is not None else None
        self.tradeUnitsPrecision = tradeUnitsPrecision
        self.marginRate = float(marginRate) if marginRate is not None else None
        self.displayPrecision = displayPrecision



    def __repr__(self):
        return str(vars(self))


    @classmethod
    def FromApiObject(cls, ob):
       return Instrument(
          ob.get('name'),
          ob.get('type'),
          ob.get('displayName'),
          ob.get('pipLocation', None),
          ob.get('tradeUnitsPrecision'),
          ob.get('marginRate'),
          ob.get('displayPrecision')

         )

