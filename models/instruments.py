class Instrument:

    def __init__(self,name, ins_type, displayName, 
                 pipLocation, tradeUnitsPrecision, marginRate,
                 displayPrecision):
    #This function takes several inputs
        self.name = name
        self.ins_type = ins_type
        self.displayName = displayName
        #This means the object will have these properties holding the respective values
        self.pipLocation = pow(10, pipLocation)
        #This means the object will store the pip location as a power of 10
        self.tradeUnitsPrecision = tradeUnitsPrecision
        self.marginRate = float(marginRate)
        self.displayPrecision = displayPrecision



    def __repr__(self):
        return str(vars(self))
    #It determines what will be shown when we print the object. 
    #The vars(self) function returns a dictionary of the object's properties, and str(vars(self)) converts this dictionary to a string. 
    #This means when you print the object, it will show all its properties and their values


    @classmethod
    #The @classmethod decorator means this method belongs to the class itself, not to any particular instance of the class
    def FromApiObject(cls, ob):
       return Instrument(
          ob.get('name'),
          ob.get('type'),
          ob.get('displayName'),
          ob.get('pipLocation'),
          ob.get('tradeUnitsPrecision'),
          ob.get('marginRate'),
          ob.get('diaplayPrecision')
         )
    #This part defines what the FromApiObject method does. It takes one parameter ob, which is expected to be a dictionary. 
    #It extracts values from this dictionary using the get method for each key 

