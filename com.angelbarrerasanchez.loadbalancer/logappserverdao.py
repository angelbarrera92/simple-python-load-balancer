from pymongo import MongoClient
import constants
import datetime

mongo = MongoClient(constants.MONGO_URI)
mongo_db = mongo[constants.MONGO_DATABASE]
mongo_collection = mongo_db[constants.MONGO_LOGS_COLLECTION]


def write_system_log():
    return None


def write_apps_log(app_name, path, end_point, total_time, http_response_code):
    log = {
        'app_name': app_name,
        'path': path,
        'end_point': end_point,
        'date': datetime.datetime.utcnow(),
        'total_time_ms': total_time,
        'response_code': http_response_code
    }
    mongo_collection.insert_one(log)


def remove_apps_log():
    return None