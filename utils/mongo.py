from pymongo import MongoClient

class Mongo:
    def __init__(self,collection='sites'):
        client = MongoClient('localhost')
        self.db = client['local']
        self.collection = self.db[collection]

    def InsertOne(self, dict):
        self.collection.insert_one(dict)

    def insertMany(self, dict_list):
        self.collection.insert_many(dict_list)
    
    def deleteOne(self, dict):
        self.collection.delete_one(dict)
    def search(self,dict):
        query = self.collection.find(dict, no_cursor_timeout=True).batch_size(10)
        if query.count() > 0:
            return query
        else:
            return False