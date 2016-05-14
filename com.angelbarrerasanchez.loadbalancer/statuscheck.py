from datetime import datetime
from pymongo import MongoClient

mongouser = "user"
mongopass = "mypass"
mongohost = "localhost"
mongoport = "27017"
mongodbname = "mydatabase"
mongocollectionname = "serverstatus"
mongouri = "mongodb://%s:%s@%s:%s/%s" % (mongouser, mongopass, mongohost, mongoport, mongodbname)

mongo = MongoClient(mongouri)
mongodb = mongo[mongodbname]
mongocollection = mongodb[mongocollectionname]

def tick():
    print('Tick! The time is: %s' % datetime.now())