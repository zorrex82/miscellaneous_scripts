# Import the libraries to connect and insert data in a Mongo DB
import json
from pymongo import MongoClient

# Variables with the connection information, the info will be passed like a dictionary python
client = MongoClient('localhost', 27017)  # Mongo DB address and port to connect (default is 27017)
db = client['DATABASE']  # The database name
collection = db['collection_name']  # The name of the collection where the data will be load

# Open the file will be load and put and some variable, in this case I use a json file to do that
with open("/home/edinorjr/Documents/mkt_cloud_files/2011.json", encoding='utf-8', errors='ignore') as f:
    file_data = json.load(f)

collection.insert(file_data)  # Call the function insert to load the json file

client.close()  # As always, close the connection with the database

