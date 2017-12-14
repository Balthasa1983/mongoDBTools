import re
from pymongo import MongoClient


client = MongoClient('mongodb://mongodbenv:27017')

db = client['Interfacefiles']

collection = db['collection1']

cursor = collection.find({"day" : "20170101"})

for files in cursor:
    filecontent = re.sub(r'(\'_id\'.+\),)', " ", str(files)).replace('u', '').replace('\'', '\"')
    print filecontent



