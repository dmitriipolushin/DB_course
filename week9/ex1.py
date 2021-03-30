import json
from pymongo import MongoClient
import re

client = MongoClient('localhost', 27017)
db = client['mongo_week9']
collection = db['restaurants']

# find all the documents in the collection
cursor = collection.find({})
for document in cursor:
    print(document)

print('\n\n')
# Find the fields restaurant_id, name, borough and cuisine for all the documents
cursor = collection.find({}, {'restaurant_id':1, 'name':1, 'borough':1, 'cuisine':1})
for document in cursor:
    print(document)

print('\n\n')
# Find the first 5 restaurant which is in the borough Bronx
cursor = collection.find({'borough':'Bronx'}).limit(5)
for document in cursor:
    print(document)


print('\n\n')
# Find the restaurant Id, name, borough and cuisine for those restaurants which
# prepared dish except 'American' and 'Chinees' or restaurant's name begins with
# letter 'Wil’.
cursor = collection.find({'cuisine': {'$nin': ['American', 'Chinese']}, 'name': {'$regex':'^Wil'}}, 
                         {'restaurant_id':1, 'name':1, 'borough':1, 'cuisine':1})
for document in cursor:
    print(document)


print('\n\n')
# Find the restaurant name, borough, longitude and attitude and cuisine for those
# restaurants which contains 'mon' as three letters somewhere in its name. 
s = re.compile(r'mon', re.I)
cursor = collection.find({'name': {'$regex':s}}, 
                         {'name':1, 'borough':1, 'cuisine':1, 'address.coord': 1})
for document in cursor:
    print(document)


print('\n\n')
# Find the restaurant Id, name, borough and cuisine for those restaurants which
# belong to the borough Staten Island or Queens or Bronx or Brooklyn.
s = re.compile(r'Staten|Queens|Bronx|Brooklyn', re.I)
cursor = collection.find({'borough': {'$regex':s}}, 
                         {'restaurant_id':1, 'name':1, 'borough':1, 'cuisine':1})
for document in cursor:
    print(document)


client.close()