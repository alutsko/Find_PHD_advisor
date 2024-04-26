import pymongo, pymongo.errors

def create_mongo_connection():
    # Making connection to MongoDB
    try:
        conn = pymongo.MongoClient()
        db = conn.academicworld
    except pymongo.errors.ConnectionFailure as e:
        print("Failed to connect to MongoDB: %s" % e)

    return db

