import os

APP_HOST = str(os.getenv('APP_HOST', '0.0.0.0'))
APP_PORT = int(os.getenv('APP_PORT', '5000'))
APP_DEBUG = bool(os.getenv('APP_DEBUG', '')) #False with none, True otherwise

JWT_SECRET = str(os.getenv('JWT_SECRET', 'super-secret'))
JWT_AUTH_USERNAME_KEY = str(os.getenv('JWT_AUTH_USERNAME_KEY', 'email'))

JOB_SERVERS_ID = str(os.getenv('JOB_SERVERS_ID', 'app_servers_status_checker'))
JOB_SERVERS_INTERVAL_SECONDS = int(os.getenv('JOB_SERVERS_INTERVAL_SECONDS', '60'))

JOB_APPS_ID = str(os.getenv('JOB_APPS_ID', 'apps_status_checker'))
JOB_APPS_INTERVAL_SECONDS = int(os.getenv('JOB_APPS_INTERVAL_SECONDS', '200'))

REDIS_HOST = str(os.getenv('REDIS_HOST', 'localhost'))
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_PASSWORD = str(os.getenv('REDIS_PASSSWORD', 'mypass'))

MONGO_HOST = str(os.getenv('MONGO_HOST', 'localhost'))
MONGO_PORT = int(os.getenv('MONGO_PORT', '27017'))
MONGO_USERNAME = str(os.getenv('MONGO_USERNAME', 'user'))
MONGO_PASSWORD = str(os.getenv('MONGO_PASSWORD', 'mypass'))
MONGO_DATABASE = str(os.getenv('MONGO_DATABASE', 'mydatabase'))
MONGO_USERS_COLLECTION = str(os.getenv('MONGO_USERS_COLLECTION', 'users'))
MONGO_APPS_COLLECTION = str(os.getenv('MONGO_APPS_COLLECTION', 'serverstatus'))
MONGO_LOGS_COLLECTION = str(os.getenv('MONGO_APPS_COLLECTION', 'serverlogs'))
MONGO_LOGS_MAX_DAYS_DURATION = int(os.getenv('MONGO_LOGS_MAX_DAYS_DURATION', '1'))
MONGO_URI = "mongodb://%s:%s@%s:%s/%s" % (MONGO_USERNAME, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_DATABASE)