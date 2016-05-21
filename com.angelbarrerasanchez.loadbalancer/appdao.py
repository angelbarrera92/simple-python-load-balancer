from pymongo import MongoClient
import constants

mongo = MongoClient(constants.MONGO_URI)
mongo_db = mongo[constants.MONGO_DATABASE]
mongo_collection = mongo_db[constants.MONGO_APPS_COLLECTION]


def get_servers(app_name):
    app = mongo_collection.find_one({'id': app_name})
    if app:
        return app['servers']
    else:
        raise Exception('TODO CAMBIAR, SERVER NO ENCONTRADO')


def add_app_server(app_name, host, port, username, infouri=None):
    app = mongo_collection.find_one({'id': app_name, 'username': username})
    if app:
        app['servers'].append({'host': host, 'port': port, 'infouri' : infouri})
        mongo_collection.save(app)
    else:
        app = {'id': app_name, 'username': username, 'servers' : [{'host': host, 'port': port, 'infouri' : infouri}]}
        mongo_collection.insert_one(app)
        #raise Exception('TODO CAMBIAR, SERVER NO ENCONTRADO')


def remove_server(app_name, host, port, username=None):
    if username:
        app = mongo_collection.find_one({'id': app_name, 'username': username})
    else:
        app = mongo_collection.find_one({'id': app_name})
    if app:
        for server in app['servers']:
            if server['host'] == host and server['port'] == port:
                app['servers'].remove(server)
        mongo_collection.save(app)
    else:
        raise Exception('TODO CAMBIAR, SERVER NO ENCONTRADO')


def get_user_apps(username):
    cursor = mongo_collection.find({'username': username})
    app_list = list()
    for app in cursor:
        app_list.append(app['id'])
    cursor.close()
    return app_list


def get_apps():
    cursor = mongo_collection.find()
    app_list = list()
    for app in cursor:
        app_list.append(app['id'])
    cursor.close()
    return app_list


def remove_app(app_name, username=None):
    if username:
        mongo_collection.remove({'id': app_name, 'username': username}, False)
    else:
        mongo_collection.remove({'id': app_name}, False)


def is_app_of_user(app_name, username):
    app = mongo_collection.find_one({'id': app_name})
    if app and app['username'] == username:
        return True
    else:
        return False
