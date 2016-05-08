from flask import Flask, request, jsonify
from flask_jwt import jwt_required, current_identity
from werkzeug.routing import Rule
import httplib
import redistore
import validator
import users
from app_exceptions.validationexception import validationexceptions

app = Flask('load_balancer_app')
app.url_map.add(Rule('/api/<string:appid>/<path:path>', endpoint='balancer')) #Did to allow all verbs/methods on the load balancer method :)

#POC AUTH JWT
@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


@app.route('/api', methods=['POST', 'DELETE'])
def register_or_delete_user():

    if request.method == 'POST':
        if validator.is_user_json_valid(request.json) and not users.user_exists(request.json['email']):
            users.register_user(request.json)
            return request.json['email']
        else:
            raise validationexceptions("01", "bad payload posted")
    elif request.method == 'DELETE':
        if validator.is_user_json_valid(request.json) and users.user_exists(request.json['email']):
            users.remove_user(request.json)
            return 'TODO OK'
        else:
            raise validationexceptions("01", "bad payload posted")



@app.route('/api/<string:appid>', methods=['POST', 'DELETE'])
#@jwt_required
def registerOrDeleteApplication(appid):
    if request.method == 'POST':
        if validator.is_machine_json_valid(request.json):
            redistore.register_endpoint(appid, request.json['host'], request.json['port'])
        action = 'register'
    elif request.method == 'DELETE':
        redistore.delete_app(appid)
        action = 'un-register'
    return 'you want to %s your application %s' % (action,appid)


@app.route('/api/status/<string:appid>')
def checkAppStatus(appid):
    return 'Your status for the app: %s' % (redistore.get_random_machine_for_app(appid))


@app.route('/api/nodes/<string:appid>', methods=['GET', 'POST', 'DELETE'])
def manage_app_nodes(appid):
    if request.method == 'GET':
        return None
    elif request.method == 'POST':
        return None
    elif request.method == 'DELETE':
        return None
    return 'Your status for the app: %s' % (redistore.get_random_machine_for_app(appid))


@app.endpoint('balancer')
def loadBalance(appid, path):
    print 'You %s want path: %s' % (appid, path)
    h1 = httplib.HTTPConnection(redistore.get_random_machine_for_app(appid)[0])
    headers = dict(request.headers)
    headers.pop("Content-Length", None)
    h1.request(method=request.method, url="/%s" % path, headers=headers)
    r = h1.getresponse()
    data = r.read()
    return data



@app.route("/<string:id>")
def helloId(id):
    return "Hello %s" % id


# ERRORS
@app.errorhandler(validationexceptions)
def handle_invalid_register(error):
    response = jsonify(error.to_dict())
    response.status_code = error.statuscode
    return response