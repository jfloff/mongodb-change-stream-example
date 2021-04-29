import sys
from pymongo import MongoClient, errors

MONGO_INSTANCES = [
  {
    'hostname': 'mongo-us',
    'port': 27017,
  },
  {
    'hostname': 'mongo-eu',
    'port': 27017,
  },
  {
    'hostname': 'mongo-jp',
    'port': 27017,
  }
]
REPLICASET_NAME = 'rs0'
DATABASE_NAME = 'demo'
COLLECTION_NAME = 'stock'

# check if we have a producer as an argument
# otherwise we choose mongo-us
mongo_consumer = next(inst for inst in MONGO_INSTANCES if inst['hostname'] == sys.argv[1])

# initiate the connection
c = MongoClient(mongo_consumer['hostname'], mongo_consumer['port'], replicaset=REPLICASET_NAME)
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