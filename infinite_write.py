import time
import random
from pymongo import MongoClient, errors


MONGO_HOSTNAME = 'mongo'
MONGO_PORT = 27017
REPLICASET_NAME = 'rs0'
DATABASE_NAME = 'demo'
COLLECTION_NAME = 'stock'

# setup replicaset
c = MongoClient(MONGO_HOSTNAME, MONGO_PORT)
rs_config = {
  '_id': REPLICASET_NAME,
  'members': [{'_id': 0, 'host': f'{MONGO_HOSTNAME}:{MONGO_PORT}'}]
}
try:
  c.admin.command('replSetInitiate', rs_config)
except errors.OperationFailure as of:
  if of.code == 23:
    # do nothing - already initialized
    True
  else:
    raise(of)
finally:
  c.close()

# now we initiate the infinite write
c = MongoClient(MONGO_HOSTNAME, MONGO_PORT, replicaset=REPLICASET_NAME)
db = c.get_database(DATABASE_NAME)
collection = db.get_collection(COLLECTION_NAME)

i = 0
fruits = ['pineapple','apple','banana','peach','watermelon','pear']
while(True):
  doc = {
    'name': f'{random.choice(fruits)}-{i}',
    'quantity': i
  }
  res = collection.insert_one(doc);
  print(f"{doc['name']} inserted with id #{res.inserted_id}");
  time.sleep(1)
  i += 1