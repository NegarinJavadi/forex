import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from pymongo import MongoClient, errors
from constants.defs import MONGO_CONN_STR


class DataDB:
    #interact with a MongoDB database

    SAMPLE_COLL = "forex_sample"
    CALENDAR_COLL = "forex_calendar"
    INSTRUMENTS_COLL = "forex_instruments"
    #are class variables. They store the names of collections

    def __init__(self):
        try:
        #This starts a block of code that will attempt to run. If there is an error, it will jump to the except block
            self.client = MongoClient(MONGO_CONN_STR)
            #store the connection
            #This line connects to the MongoDB server using a connection string
            self.db = self.client.forex_learning
            #sets self.db to the database
        except errors.ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            sys.exit(1)
            #This exits the program with an error code of 1


    def test_connection(self):
    #This defines a method to test the connection to the database
    
        print(self.db.list_collection_names())
        #prints the names of all collections

    
    def delete_many(self, collection, **kwargs):
    #defines a method to delete multiple documents from a collection
        try:
        #Starts a block to attempt the deletion
            _ = self.db[collection].delete_many(kwargs)
            #Deletes documents that match the criteria in kwargs
        except errors.InvalidOperation as error:
            print("delete_many error:", error)
    

    def add_one(self, collection, ob):
    #defines a method to add a single document to a collection
        try:
            _ = self.db[collection].insert_one(ob)
            #Inserts one document (ob) into the specified collection
        except errors.InvalidOperation as error:
            print("add_one error:", error)

    
    def add_many(self, collection, list_ob):
    #defines a method to add multiple documents to a collection
        try:
            _ = self.db[collection].insert_many(list_ob)
            #Inserts multiple documents (list_ob) into the specified collection
        except errors.InvalidOperation as error:
            print("add_many error:", error)
    
    
    def query_distinct(self, collection, key):
    #defines a method to get distinct values for a specified key in a collection
        try:
            return self.db[collection].distinct(key)
            #Returns distinct values for the key
        except errors.InvalidOperation as error:
            print("query_distinct error:", error)
    

    def query_single(self, collection, **kwargs):
    #defines a method to find a single document that matches the criteria
        try:
            r = self.db[collection].find_one(kwargs, {'_id':0})
            #Finds one document, excluding the _id field
            return r
        except errors.InvalidOperation as error:
            print("query_single error:", error)


    def query_all(self, collection, **kwargs):
    #defines a method to find all documents that match the criteria
        try:
            data = []
            #Initializes an empty list to store the results
            r = self.db[collection].find(kwargs, {'_id':0})
            #Finds all documents, excluding the _id field
            for item in r:
                data.append(item)
                #Adds each document to the data list
            return data
        except errors.InvalidOperation as error:
            print("query_all error:", error)

