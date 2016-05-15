from flask import Flask, request, jsonify
from werkzeug.routing import Rule
from flask_jwt import jwt_required, current_identity

from exceptions.validationexception import validationexceptions
import appservice
import validator


app = Flask('load_balancer_app')
app.url_map.add(Rule('/api/<string:appid>/<path:path>', endpoint='balancer')) #Did to allow all verbs/methods on the load balancer method :)


# REMOVE WHEN SCHEDULER IS FULL DEVELOPED
@app.route('/status')
def check_status_route():
    appservice.statuschecker()



@app.endpoint('balancer')
def load_balance_route(appid, path):
    return appservice.balancerequest(appid, path)


@app.route('/api/users', methods=['POST', 'DELETE'])
def user_route():
    if request.method == 'POST':
        if validator.is_user_json_valid(request.json) and not appservice.user_exists(request.json['email']):
            return appservice.register_user(request.json['email'], request.json['password'])
        else:
            raise validationexceptions("01", "bad payload posted")
    elif request.method == 'DELETE':
        if validator.is_user_json_valid(request.json) and appservice.user_exists(request.json['email']):
            return appservice.remove_user(request.json['email'], request.json['password'])
        else:
            raise validationexceptions("01", "bad payload posted")


@app.route('/api/apps/<string:appid>', methods=['POST', 'DELETE'])
@jwt_required()
def app_route(appid):
    if request.method == 'POST':
        if validator.is_machine_json_valid(request.json) and not appservice.app_exists(appid):
            return appservice.register_app(str(current_identity), appid, request.json['host'], request.json['port'],
                                           request.json['statuspath'])
        else:
            raise validationexceptions("01", "bad payload posted")
    elif request.method == 'DELETE':
        if appservice.app_exists(appid):
            return appservice.remove_app(str(current_identity), appid)
        else:
            raise validationexceptions("01", "bad payload posted")


@app.route('/api/nodes/<string:appid>', methods=['POST', 'DELETE'])
@jwt_required()
def node_app_route(appid):
    if request.method == 'POST':
        if validator.is_machine_json_valid(request.json):
            if not appservice.app_exists(appid):
                return appservice.register_app(str(current_identity), appid, request.json['host'], request.json['port'],
                                               request.json['statuspath'])
            else:
                return appservice.register_server_app(str(current_identity), appid, request.json['host'],
                                                      request.json['port'], request.json['statuspath'])
        else:
            raise validationexceptions("01", "bad payload posted")
    elif request.method == 'DELETE':
        if validator.is_machine_json_valid(request.json) and appservice.app_exists(appid):
            return appservice.remove_server_app(str(current_identity), appid, request.json['host'], request.json['port'])
        else:
            raise validationexceptions("01", "bad payload posted")


#ERRORS
@app.errorhandler(validationexceptions)
def handle_invalid_register(error):
    response = jsonify(error.to_dict())
    response.status_code = error.statuscode
    return response