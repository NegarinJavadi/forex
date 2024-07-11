import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from dateutil import parser
from models.base_api_price import BaseApiPrice


class LiveApiPrice(BaseApiPrice):
#This means LiveApiPrice inherits properties and methods from BaseApiPrice

    def __init__(self, api_ob):
        
        super().__init__(api_ob)
        #This line calls the constructor method of the parent class (BaseApiPrice). 
        #The super().__init__(api_ob) line ensures that the properties defined in the BaseApiPrice class are also set up for the LiveApiPrice object
        self.time = parser.parse(api_ob['time'])
        #This line sets up a property called time for the object. 
        #It takes the value from the api_ob dictionary using the key 'time', and uses parser.parse to convert it into a datetime object

    def __repr__(self):
    #It determines what will be shown when we print the object
        return f"LiveApiPrice() {self.instrument} {self.ask} {self.bid} {self.time}"
    
    def get_dict(self):
        return dict(
            instrument=self.instrument,
            time=self.time,
            ask=self.ask,
            bid=self.bid
        )
    #It creates and returns a dictionary containing the properties instrument, time, ask, and bid of the object. 
    #This function provides a way to get the object's data in a dictionary format