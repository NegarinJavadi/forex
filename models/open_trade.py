from dateutil import parser

class OpenTrade:

    def __init__(self, api_ob):
    #self refers to the instance of the class that is being created
    #api_ob is expected to be a dictionary containing the data for initializing the object
        self.id = api_ob['id']
        #This line sets the id attribute of the object to the value of the 'id' key from the api_ob dictionary
        self.instrument = api_ob['instrument']
        self.price = float(api_ob['price'])
        self.currentUnits = float(api_ob['currentUnits'])
        self.unrealizedPL = float(api_ob['unrealizedPL'])
        self.marginUsed = float(api_ob['marginUsed'])


    def __repr__(self):
    #This method is used to define how the object should be represented as a string
        return str(vars(self))
        #vars(self) returns the __dict__ attribute for the instance self.
        #str(vars(self)) converts this dictionary to a string