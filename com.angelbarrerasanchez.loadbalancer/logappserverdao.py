from pymongo import MongoClient
import constants
from datetime import datetime, timedelta

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
        'date': datetime.utcnow(),
        'total_time_ms': total_time,
        'response_code': http_response_code
    }
    mongo_collection.insert_one(log)
    remove_apps_log(1)


def remove_apps_log(max_days):
    date = datetime.utcnow() + timedelta(days=-max_days)
    mongo_collection.remove({'date': {"$lt": date}}, multi=True)