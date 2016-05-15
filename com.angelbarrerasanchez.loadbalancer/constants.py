import os

APP_HOST = str(os.getenv('APP_HOST', '0.0.0.0'))
APP_PORT = int(os.getenv('APP_PORT', '5000'))
APP_DEBUG = bool(os.getenv('APP_DEBUG', 'False'))

JWT_SECRET = str(os.getenv('JWT_SECRET', 'super-secret'))
JWT_AUTH_USERNAME_KEY = str(os.getenv('JWT_AUTH_USERNAME_KEY', 'email'))

JOB_ID = str(os.getenv('JOB_ID', 'app_servers_status_checker'))
JOB_INTERVAL_SECONDS = int(os.getenv('JOB_INTERVAL_SECONDS', '60'))

REDIS_HOST = str(os.getenv('REDIS_HOST', 'localhost'))
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_PASSSWORD = str(os.getenv('REDIS_PASSSWORD', 'mypass'))