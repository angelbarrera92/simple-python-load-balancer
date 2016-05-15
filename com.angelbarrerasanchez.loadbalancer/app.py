from controller import app as flaskapp
from flask_jwt import JWT
import userdao, appservice, constants
from flask_apscheduler import APScheduler


flaskapp.config['SECRET_KEY'] = constants.JWT_SECRET
flaskapp.config['JWT_AUTH_USERNAME_KEY'] = constants.JWT_AUTH_USERNAME_KEY

jwt = JWT(flaskapp, userdao.authenticate, userdao.identity)

scheduler = APScheduler()
scheduler.init_app(flaskapp)
scheduler.add_job(constants.JOB_ID, appservice.app_servers_status_checker, trigger='interval',
                  seconds=constants.JOB_INTERVAL_SECONDS)
scheduler.start()

flaskapp.run(debug=constants.APP_DEBUG, host=constants.APP_HOST, port=constants.APP_PORT)