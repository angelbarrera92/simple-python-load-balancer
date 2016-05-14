from flask import Flask, request, jsonify

from flask_restful import reqparse, abort, Api, Resource

from flask_jwt import jwt_required, current_identity
from werkzeug.routing import Rule
import httplib
import redistore, mongostore
import validator
import users
from app_exceptions.validationexception import validationexceptions

class baseapi(Resource):
    def post(self):
        if validator.is_user_json_valid(request.json) and not users.user_exists(request.json['email']):
            users.register_user(request.json)
            return request.json['email']
        else:
            raise validationexceptions("01", "bad payload posted")

    def delete(self):
        if validator.is_user_json_valid(request.json) and users.user_exists(request.json['email']):
            users.remove_user(request.json)
            return 'TODO OK'
        else:
            raise validationexceptions("01", "bad payload posted")


class appapi(Resource):

    method_decorators = [jwt_required()]
    def post(self, appid):
        if validator.is_machine_json_valid(request.json) and not redistore.appExists(appid):
            mongostore.addServer(appid, request.json['host'], request.json['port'], str(current_identity))
            redistore.register_endpoint(appid, request.json['host'], request.json['port'])
        action = 'register'
        return 'you want to %s your application %s' % (action, appid)

    method_decorators = [jwt_required()]
    def delete(self, appid):
        if mongostore.isAppOfUser(appid, str(current_identity)):
            redistore.delete_app(appid)
            mongostore.removeApp(appid, str(current_identity))
        action = 'un-register'
        return 'you want to %s your application %s' % (action, appid)


class appnodesapi(Resource):

    method_decorators = [jwt_required()]
    def post(self, appid):
        if not redistore.appExists(appid) and validator.is_machine_json_valid(request.json):
            # REGISTER AN APP
            print 'registering a new app'
            mongostore.addServer(appid, request.json['host'], request.json['port'], str(current_identity))
            redistore.register_endpoint(appid, request.json['host'], request.json['port'])
        elif mongostore.isAppOfUser(appid, str(current_identity)) and validator.is_machine_json_valid(request.json):
            print 'registering a new server for app %s' % appid
            mongostore.addServer(appid, request.json['host'], request.json['port'], str(current_identity))
            redistore.register_endpoint(appid, request.json['host'], request.json['port'])

    method_decorators = [jwt_required()]
    def delete(self, appid):
        if mongostore.isAppOfUser(appid, str(current_identity)):
            print 'removing a server for app %s' % appid
            redistore.delete_endpoint(appid, request.json['host'], request.json['port'])
            mongostore.removeServer(appid, request.json['host'], request.json['port'], str(current_identity))


errors = {
    'validationexceptions': {
        'message': "some validation exception occurs",
        'status': 409,
    }
}

app = Flask('load_balancer_app')
api = Api(app, errors=errors)

api.add_resource(baseapi, '/api')
api.add_resource(appapi, '/api/<string:appid>')
api.add_resource(appnodesapi, '/nodes/<string:appid>')

app.url_map.add(Rule('/api/<string:appid>/<path:path>', endpoint='balancer')) #Did to allow all verbs/methods on the load balancer method :)


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


# ERRORS
#@app.errorhandler(validationexceptions)
#def handle_invalid_register(error):
    #    response = jsonify(error.to_dict())
    #response.status_code = error.statuscode
    #return response