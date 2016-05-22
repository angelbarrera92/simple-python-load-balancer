from validationexception import ValidationException
from flask import Flask, request, jsonify
from flask_jwt import jwt_required, current_identity
from werkzeug.routing import Rule

import appservice
import validator

app = Flask('load_balancer_app')
app.url_map.add(Rule('/api/apps/<string:app_name>/', endpoint='balancer')) #Did to allow the base uris of an app
app.url_map.add(Rule('/api/apps/<string:app_name>/<path:path>', endpoint='balancer')) #Did to allow all verbs/methods on the load balancer method :)


# REMOVE WHEN SCHEDULER IS FULL DEVELOPED
@app.route('/status')
def check_status_route():
    appservice.app_servers_status_checker()



@app.endpoint('balancer')
def load_balance_route(app_name, path=''):
    app.logger.debug('Requested to balance the appname %s, with path %s' % (app_name, str(path)))
    if appservice.app_exists(app_name):
        return appservice.balance_request(app_name, path)
    else:
        raise ValidationException('02', 'That app does not exists or it has not available endpoints')



@app.route('/api/users', methods=['POST', 'DELETE'])
def user_route():
    if validator.is_user_json_valid(request.json):
        if request.method == 'POST':
                if not appservice.user_exists(request.json['email']):
                    return appservice.register_user(request.json['email'], request.json['password'])
                else:
                    raise ValidationException('02', 'There is already an user registered with that email', 409)
        elif request.method == 'DELETE':
            if appservice.user_exists(request.json['email']):
                return appservice.remove_user(request.json['email'], request.json['password'])
            else:
                raise ValidationException('02', 'There is not an user registered with that email', 409)
    else:
        raise ValidationException('01', 'Bad payload posted. Check the payload before send it again', 400)


@app.route('/api/apps/<string:app_name>', methods=['POST', 'DELETE'])
@jwt_required()
def app_route(app_name):
    if request.method == 'POST':
        if validator.is_new_machine_json_valid(request.json):
            if not appservice.app_exists(app_name):
                return appservice.register_app(str(current_identity), app_name, request.json['host'],
                                               request.json['port'], request.json['statuspath'])
            else:
                raise ValidationException('02', 'That app already exists')
        else:
            raise ValidationException('01', 'Bad payload posted. Check the payload before send it again', 400)
    elif request.method == 'DELETE':
        if appservice.app_exists(app_name):
            return appservice.remove_app(str(current_identity), app_name)
        else:
            raise ValidationException('02', 'That app does not exists')


@app.route('/api/nodes/<string:app_name>', methods=['POST', 'DELETE'])
@jwt_required()
def node_app_route(app_name):
    if validator.is_machine_json_valid(request.json):
        if request.method == 'POST':
            if validator.is_new_machine_json_valid(request.json):
                if not appservice.app_exists(app_name):
                    return appservice.register_app(str(current_identity), app_name, request.json['host'],
                                                   request.json['port'], request.json['statuspath'])
                else:
                    return appservice.register_server_app(str(current_identity), app_name, request.json['host'],
                                                          request.json['port'], request.json['statuspath'])
            else:
                raise ValidationException('01', 'Bad payload posted. Check the payload before send it again', 400)
        elif request.method == 'DELETE':
            if appservice.app_exists(app_name):
                return appservice.remove_server_app(str(current_identity), app_name, request.json['host'], request.json['port'])
            else:
                raise ValidationException('02', 'That app does not exists')
    else:
        raise ValidationException('01', 'Bad payload posted. Check the payload before send it again', 400)


@app.route('/api/logs/<string:app_name>', methods=['GET'])
@jwt_required()
def log_app_route(app_name):
    if appservice.app_exists(app_name):
        return appservice.get_app_logs(app_name, str(current_identity))
    else:
        raise ValidationException('02', 'That app does not exists')


#ERRORS
@app.errorhandler(ValidationException)
def handle_invalid_register(error):
    response = jsonify(error.to_dict())
    response.status_code = error.statuscode
    return response