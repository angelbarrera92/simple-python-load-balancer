from pymongo import MongoClient
import constants
from datetime import datetime, timedelta

mongo = MongoClient(constants.MONGO_URI)
mongo_db = mongo[constants.MONGO_DATABASE]
mongo_collection = mongo_db[constants.MONGO_LOGS_COLLECTION]


# Write logs for balancing results and invoke the purge logs collection
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
    remove_apps_log(constants.MONGO_LOGS_MAX_DAYS_DURATION)


# Remove old log collection
def remove_apps_log(max_days):
    date = datetime.utcnow() + timedelta(days=-max_days)
    mongo_collection.remove({'date': {"$lt": date}}, multi=True)


# Get logs of an application
def get_app_logs(app_name):
    return list(mongo_collection.find({'app_name': app_name}, {'_id': 0, 'app_name': 0}))