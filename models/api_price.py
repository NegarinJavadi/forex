import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from models.base_api_price import BaseApiPrice


class ApiPrice():

    def __init__(self, api_ob, homeConversions):
        super().__init__(api_ob)
        #The super() function allows us to run the parent class's __init__ method. This means we are doing some setup that the parent class requires, using api_ob

        base_instrument = self.instrument.split('_')[1]
        #This line takes a property called instrument from the object and splits it using the underscore (_) as a divider. 
        #It then takes the second part of the split result (because we use [1]), and stores it in a variable called base_instrument
        for hc in homeConversions:
        #This line starts a loop. It goes through each item in homeConversions, one by one
            if hc['currency'] == base_instrument:
            #This line checks if the currency in the current dictionary (hc) matches base_instrument
                self.sell_conv = float(hc['positionValue'])
                self.buy_conv = float(hc['positionValue'])
                #If the condition in the previous line is true, these lines store the value of positionValue from the current dictionary (hc) into two properties
    
    def __repr__(self):
    # It determines what will be shown when we print the object
        return f"ApiPrice() {self.instrument} {self.ask} {self.bid} {self.time}"
