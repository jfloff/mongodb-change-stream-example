import time
import random
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
mongo_producer = next(inst for inst in MONGO_INSTANCES if inst['hostname'] == sys.argv[1])

# setup replicaset
c = MongoClient(mongo_producer['hostname'], mongo_producer['port'])
rs_config = {
  '_id': REPLICASET_NAME,
  'members': [{'_id': i, 'host': f"{inst['hostname']}:{inst['port']}" } for i,inst in enumerate(MONGO_INSTANCES)]
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
c = MongoClient(mongo_producer['hostname'], mongo_producer['port'], replicaset=REPLICASET_NAME)
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