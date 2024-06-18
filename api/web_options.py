import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

import constants.defs as defs

#create a specific type of dictionary
def make_option(k):
    return dict(key=k, text=k, value=k)

def get_options():
    #Get a list of keys from defs.INVESTING_COM_PAIRS
    ps = [p for p in defs.INVESTING_COM_PAIRS.keys()]

    ps.sort()
    
    #Create and return a dictionary 
    return dict(
        granularities=[make_option(g) for g in defs.TFS.keys()],
        pairs=[make_option(p) for p in ps]
    )
