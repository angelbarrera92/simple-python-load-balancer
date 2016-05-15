from redis import Redis
import constants
import random

# Redis Connection
redis_db = Redis(host=constants.REDIS_HOST, port=constants.REDIS_PORT, password=constants.REDIS_PASSSWORD)


# Register an endpoint to an application
def register_endpoint(app_name, host, port=80):
    redis_db.sadd(app_name, host + ':' + str(port))


# Remove an endpoint of an application
def remove_endpoint(app_name, host, port):
    redis_db.srem(app_name, host + ':' + str(port))


# Removes all the endpoints of an application
def remove_app(app_name):
    redis_db.delete(app_name)


# Return a set of machines (host:port) if the app exists,
# otherwise it returns None
def get_machines_of_app(app_name):
    machines = redis_db.smembers(app_name)
    if len(machines) > 0:
        return machines
    else:
        return None


# If there is endpoints registered of an application,
# it will return one endpoint,
# otherwise it returns None
def get_random_endpoint_of_app(app_name):
    machines = get_machines_of_app(app_name)
    if machines:
        return random.sample(machines, 1)
    else:
        return None


# Check if the app exists looking for servers
def app_exists(app_name):
    if get_machines_of_app(app_name):
        return True
    else:
        return False