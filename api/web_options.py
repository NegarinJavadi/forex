import os #provides functions for interacting with the operating system
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys #provides access to some variables used
sys.path.insert(0,main_dir)

import constants.defs as defs


def make_option(k): #take 1 argument
    return dict(key=k, text=k, value=k)
#return a dictionary with 3 key-value pairs

def get_options():
    #Get a list of keys from defs.INVESTING_COM_PAIRS
    ps = [p for p in defs.INVESTING_COM_PAIRS.keys()]

    ps.sort()
    
    #Create and return a dictionary with 2 key-value pairs
    return dict(
        granularities=[make_option(g) for g in defs.TFS.keys()],
        #a list with all keys
        pairs=[make_option(p) for p in ps]
        #create dictionary and add to the list
    )
