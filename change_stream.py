import time
from pymongo import MongoClient, errors

MONGO_HOSTNAME = 'mongo'
MONGO_PORT = 27017
REPLICASET_NAME = 'rs0'
DATABASE_NAME = 'demo'
COLLECTION_NAME = 'stock'

# initiate the connection
c = MongoClient(MONGO_HOSTNAME, MONGO_PORT, replicaset=REPLICASET_NAME)
db = c.get_database(DATABASE_NAME)
collection = db.get_collection(COLLECTION_NAME)

# pipeline to watch
# ref: https://docs.mongodb.com/manual/reference/operator/aggregation/match/#mongodb-pipeline-pipe.-match
pipeline = [
  {
    '$match': {
      '$and': [
        { 'operationType': 'insert' },
        { 'fullDocument.name': { '$regex': '^p' } },
        # { 'fullDocument.quantity': { '$gte': 1690 } },
      ]
    }
  }
]

# loop
try:
  resume_token = None
  with collection.watch(pipeline) as stream:
    for insert_change in stream:
      print(insert_change)
      resume_token = stream.resume_token
except errors.PyMongoError:
  # The ChangeStream encountered an unrecoverable error or the
  # resume attempt failed to recreate the cursor.
  if resume_token is None:
      # There is no usable resume token because there was a
      # failure during ChangeStream initialization.
      print("[ERROR] resume_token is None")
      exit(-1)