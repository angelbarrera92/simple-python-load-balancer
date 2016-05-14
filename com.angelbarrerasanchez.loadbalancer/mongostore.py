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

def getServers(appname):
    app = mongocollection.find_one({'id': appname})
    if app:
        return app['servers']
    else:
        raise Exception('TODO CAMBIAR, SERVER NO ENCONTRADO')


def addServer(appname, host, port, username, infouri=None):
    app = mongocollection.find_one({'id': appname, 'username': username})
    if app:
        app['servers'].append({'host': host, 'port': port, 'infouri' : infouri})
        mongocollection.save(app)
    else:
        app = {'id': appname, 'username': username, 'servers' : [{'host': host, 'port': port, 'infouri' : infouri}]}
        mongocollection.insert_one(app)
        #raise Exception('TODO CAMBIAR, SERVER NO ENCONTRADO')


def removeServer(appname, host, port, username):
    app = mongocollection.find_one({'id': appname, 'username': username})
    if app:
        for server in app['servers']:
            if server['host'] == host and server['port'] == port:
                app['servers'].remove(server)
        mongocollection.save(app)
    else:
        raise Exception('TODO CAMBIAR, SERVER NO ENCONTRADO')


def removeApp(appname, username):
    mongocollection.remove({'id': appname, 'username': username}, False)


def isAppOfUser(appname, username):
    app = mongocollection.find_one({'id': appname})
    if app and app['username'] == username:
        return True
    else:
        return False
