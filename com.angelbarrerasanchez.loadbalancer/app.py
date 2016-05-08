from controller import app as flaskapp
from flask_jwt import JWT
import users

# TODO CHANGE SECRET KEY
flaskapp.config['SECRET_KEY'] = 'super-secret'
flaskapp.config['JWT_AUTH_USERNAME_KEY'] = 'email'

jwt = JWT(flaskapp, users.authenticate, users.identity)

flaskapp.run(debug=True, host='0.0.0.0')