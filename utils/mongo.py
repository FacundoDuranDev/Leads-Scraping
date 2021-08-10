from pymongo import MongoClient

class Mongo:
    def __init__(self):
        client = MongoClient('localhost')
        self.db = client['local']
        self.collection = self.db['sites']

    def InsertOne(self, dict):
        self.collection.insert_one(dict)

    def insertMany(self, dict_list):
        self.collection.insert_many(dict_list)
    
    def deleteOne(self, dict):
        self.collection.delete_one(dict)