import pandas as pd
from pymongo import MongoClient
import os

client = MongoClient("mongodb://root:a1B2c3D4e5@mongodb1:27017/", replicaset="rs0")
db = client['backup']
print(db.list_collection_names())

csv_file = '/csv/listings_Paris+(1).csv'
df = pd.read_csv(csv_file)

collection = db['listing_paris']
collection.insert_many(df.to_dict('records'))

print(f"Data imported successfully from {csv_file}")
