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
    def query_field(self,  field=None, extra_filter=None, site=None ,created_at=None ):
        find_filter = {'site': site, 'CreatedAt': created_at}
        if extra_filter:
            find_filter.update(extra_filter)
        find_projection = {'_id': 0, field: 1,} if field else None
        query = self.collection.find(
            filter=find_filter,
            projection=find_projection,
            no_cursor_timeout=False
        )
        if field:
            query = {item[field] for item in query}
        else:
            query = set(query)

        return query        