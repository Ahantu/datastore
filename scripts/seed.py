import json
import datetime
from pprint import pprint
from pymongo import MongoClient, GEOSPHERE, InsertOne
from pymongo.errors import BulkWriteError


CONNECTION_STRING = "mongodb+srv://arah:arahdb@cluster0.rdpdj.mongodb.net/rethink?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
database = client["rethink"]


def seed_db(collection_name):
    count = 1
    with open(f'../{collection_name}.geojson', 'r') as f:
        geojson = json.loads(f.read())
    collection = database[collection_name]
    collection.create_index([("geometry", GEOSPHERE)])
    bulk_requests = []
    # print(geojson['features'][2])
    for feature in geojson['features']:
        # print(len())
        transformed = {k.lower(): v for k, v in feature['properties'].items()}
        print(transformed)
        database[collection_name].insert_one(
            {**transformed, 'geometry': feature["geometry"]})
        # bulk_requests.append(InsertOne(feature))


def insertGeojson():
    collections = ['districts']
    for collection in collections:
        seed_db(collection)


if __name__ == "__main__":
    insertGeojson()
