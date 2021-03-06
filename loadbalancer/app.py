from controller import app as flaskapp
from flask_jwt import JWT
import userdao, appservice, constants
from flask_apscheduler import APScheduler
import logging
from logging.handlers import RotatingFileHandler


flaskapp.config['SECRET_KEY'] = constants.JWT_SECRET
flaskapp.config['JWT_AUTH_USERNAME_KEY'] = constants.JWT_AUTH_USERNAME_KEY
flaskapp.config['JWT_AUTH_URL_RULE'] = '/api/auth'


jwt = JWT(flaskapp, userdao.authenticate, userdao.identity)

scheduler = APScheduler()
scheduler.init_app(flaskapp)
scheduler.add_job(constants.JOB_SERVERS_ID, appservice.app_servers_status_checker, trigger='interval',
                  seconds=constants.JOB_SERVERS_INTERVAL_SECONDS)
scheduler.add_job(constants.JOB_APPS_ID, appservice.check_orphans_apps, trigger='interval',
                  seconds=constants.JOB_APPS_INTERVAL_SECONDS)
scheduler.start()

formatter = logging.Formatter("[%(asctime)s] [%(pathname)s:%(lineno)d] [%(levelname)s] - %(message)s")
handler = RotatingFileHandler('./logs/app_load_balancer.log', maxBytes=10000, backupCount=5)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
flaskapp.logger.addHandler(handler)
flaskapp.logger.setLevel(logging.DEBUG)


flaskapp.run(debug=constants.APP_DEBUG, host=constants.APP_HOST, port=constants.APP_PORT)
