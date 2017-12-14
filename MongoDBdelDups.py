from pymongo import MongoClient

client = MongoClient('mongodb://MongoDBEnv')

db = client['Interfacefiles']

coll = ['collection1', 'collection2', 'collection3', 'collection4', 'collection5', 'collection6']


for c in coll:
    try:
        collection = db[c]

        cursor = collection.aggregate(
            [
                { "$group": {
                            "_id": {"name": "$filename", "day": "$day"},
                            "unique_ids": {"$addToSet": "$_id"},
                            "count": {"$sum": 1}
                            }
                },
                { "$match": {
                            "count": {"$gt": 1}
                            }
                }
            ]
        ,allowDiskUse=True)


        response = []
        details = []
        hs = open(r"C:\MongoDups" + c + ".txt", "a") #write mongo duplicates into file for analysis
        for doc in cursor:
            del doc["unique_ids"][0]
            for id in doc["unique_ids"]:
                response.append(id)
                hs.write(str(doc["_id"]) + "\n")
        hs.close()
        print str(len(response)) + ' files were deleted in ' + c
        before = str(collection.count())
        collection.remove({"_id": {"$in": response}})
        after = str(collection.count())

        print before + " files before deletion in " + c
        print after + " files after deletion in " + c
    except Exception as e:
        print 'There was an Error ' + e.message
