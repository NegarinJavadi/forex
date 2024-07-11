class BaseApiPrice:

    def __init__(self, api_ob):
        self.instrument = api_ob['instrument']
        #This line sets a property called instrument for the object
        #It takes the value from the api_ob dictionary using the key 'instrument' and assigns it to self.instrument
        self.ask = float(api_ob['asks'][0]['price'])
        #It looks into the api_ob dictionary, finds the list under the key 'asks', 
        #takes the first item in that list ([0])
        self.bid = float(api_ob['bids'][0]['price'])
        #It looks into the api_ob dictionary, finds the list under the key 'bids', 
        #takes the first item in that list ([0])