from controller import app as flaskapp
from flask_jwt import JWT
import users, statuscheck
from flask_apscheduler import APScheduler

# TODO CHANGE SECRET KEY
flaskapp.config['SECRET_KEY'] = 'super-secret'
flaskapp.config['JWT_AUTH_USERNAME_KEY'] = 'email'

jwt = JWT(flaskapp, users.authenticate, users.identity)

scheduler = APScheduler()
scheduler.init_app(flaskapp)
scheduler.add_job('job1', statuscheck.tick, trigger='interval', seconds=3)
scheduler.start()

flaskapp.run(debug=False, host='0.0.0.0')