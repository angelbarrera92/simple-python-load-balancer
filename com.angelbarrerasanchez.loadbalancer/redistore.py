from redis import Redis
import random


redis_db = Redis(host='localhost', port=6379, password='mypass')


def register_endpoint(appname, host, port=80):
    redis_db.sadd(appname, host + ':' + str(port))


def delete_endpoint(appname, host, port):
    redis_db.srem(appname, host + ':' + str(port))


def delete_app(appname):
    redis_db.delete(appname)


def get_machines_for_app(appname):
    machines = redis_db.smembers(appname)
    if len(machines) > 0:
        return machines
    else:
        return None


def get_random_machine_for_app(appname):
    machines = get_machines_for_app(appname)
    if machines:
        return random.sample(machines, 1)
    else:
        return None


def appExists(appname):
    if get_machines_for_app(appname):
        return True
    else:
        return False
