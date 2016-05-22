from flask import request, Response, json
import httplib
import threading
import time
import appdao
import userdao
import appserversdao
import logappserverdao


# Method that purges the non available servers of an application
def app_servers_status_checker():
    print 'init the cron task'
    for appname in appdao.get_apps():
        print 'app to check %s' % appname
        servers = appdao.get_servers(appname)
        for server in servers:
            host = server['host']
            port = server['port']
            print 'server to check %s:%s' % (host, port)
            statuspath = server['infouri']
            try:
                h1 = httplib.HTTPConnection(host=host, port=port)
                h1.request('GET', statuspath)
                res = h1.getresponse()
                if res.status != httplib.OK:
                    print 'server to remove %s:%s' % (host, port)
                    appdao.remove_server(appname, host, port)
                    appserversdao.remove_endpoint(appname, host, port)
            except:
                print 'server to remove %s:%s' % (host, port)
                appdao.remove_server(appname, host, port)
                appserversdao.remove_endpoint(appname, host, port)


# Another cron task. Detects if an app has no available servers/endpoints and removes it
def check_orphans_apps():
    print 'init orphans cron task'
    for app_name in appdao.get_apps():
        if not appdao.get_servers(app_name):
            appdao.remove_app(app_name)
            appserversdao.remove_app(app_name)


# Principal method of the app.
# Gets a server for the app and path request and makes the request.
def balance_request(app_name, path):
    # print 'You %s want path: %s' % (app_name, path) #TODO SHOW IN DEBUG MODE
    init_milli_time = int(round(time.time() * 1000))
    endpoint = appserversdao.get_random_endpoint_of_app(app_name)
    if endpoint:
        try:
            h1 = httplib.HTTPConnection(endpoint)
            headers = dict(request.headers)
            headers.pop("Content-Length", None)
            h1.request(method=request.method, url="/%s" % path, headers=headers)
            r = h1.getresponse()
            resp = Response()
            data = r.read()
            for header in r.getheaders():
                # print 'header %s value %s' % (header[0], r.getheader(header[0])) #TODO SHOW IN DEBUG MODE
                if header[0] != 'transfer-encoding':
                    resp.headers[header[0]] = str(r.getheader(header[0]))
            resp.data = data
            end_milli_time = int(round(time.time() * 1000))
            total_milli_time = end_milli_time - init_milli_time
            thr = threading.Thread(target=logappserverdao.write_apps_log,
                                   args=(app_name, str(path), endpoint, total_milli_time, r.status), kwargs={})
            thr.start()
            return resp
        except:
            endpoint = appserversdao.get_another_endpoint_of_app(app_name, endpoint)
            try:
                h1 = httplib.HTTPConnection(endpoint)
                headers = dict(request.headers)
                headers.pop("Content-Length", None)
                h1.request(method=request.method, url="/%s" % path, headers=headers)
                r = h1.getresponse()
                resp = Response()
                data = r.read()
                for header in r.getheaders():
                    # print 'header %s value %s' % (header[0], r.getheader(header[0])) #TODO SHOW IN DEBUG MODE
                    if header[0] != 'transfer-encoding':
                        resp.headers[header[0]] = str(r.getheader(header[0]))
                resp.data = data
                end_milli_time = int(round(time.time() * 1000))
                total_milli_time = end_milli_time - init_milli_time
                thr = threading.Thread(target=logappserverdao.write_apps_log,
                                       args=(app_name, str(path), endpoint, total_milli_time, r.status), kwargs={})
                thr.start()
                return resp
            except:
                return create_response('We can not request the app in two attempts', httplib.PRECONDITION_FAILED, '04')

    else:
        return create_response('No endpoints registered for that app', httplib.CONFLICT, '03')


# Checks if an user exists
def user_exists(email):
    return userdao.user_exists(email)


# Check if the app exists
def app_exists(app_name):
    return appserversdao.app_exists(app_name)


# Register a new user
def register_user(email, password):
    if userdao.register_user(email, password):
        return create_response(email, httplib.CREATED)
    else:
        return create_response('An error occurred when trying to register with email %s ' % email, httplib.CONFLICT,
                               '03')


# Remove a user
def remove_user(email, password):
    if userdao.remove_user(email, password):
        apps = appdao.get_user_apps(email)
        for app in apps:
            appdao.remove_app(app, email)
            appserversdao.remove_app(app)
        return create_response(email, httplib.OK)
    else:
        return create_response('An error occurred when trying to un-register with email %s ' % email, httplib.CONFLICT,
                               '03')


# Register a new app for a user,
# it is required to specify at least one server
def register_app(email, app_name, host, port, status_path):
    appdao.add_app_server(app_name, host, port, email, status_path)
    appserversdao.register_endpoint(app_name, host, port)
    return create_response(app_name, httplib.CREATED)


# Remove an existing app checking if the app is registered by the user (email)
def remove_app(email, app_name):
    if appdao.is_app_of_user(app_name, email):
        appserversdao.remove_app(app_name)
        appdao.remove_app(app_name, email)
        return create_response(app_name, httplib.OK)
    else:
        return create_response('An error occurred when trying to un-register the app %s ' % app_name,
                               httplib.CONFLICT, '03')


# Register a new server of an existing application
def register_server_app(email, app_name, host, port, status_path):
    if appdao.is_app_of_user(app_name, email):
        register_app(email, app_name, host, port, status_path)
        return create_response('%s:%s' % (host, port), httplib.CREATED)
    else:
        return create_response('An error occurred when trying to register with node %s:%s ' % (host, port),
                               httplib.CONFLICT, '03')


# Remove a server of an existing application
def remove_server_app(email, app_name, host, port):
    if appdao.is_app_of_user(app_name, email):
        appserversdao.remove_endpoint(app_name, host, port)
        appdao.remove_server(app_name, host, port, email)
        return create_response('%s:%s' % (host, port), httplib.OK)
    else:
        return create_response('An error occurred when trying to un-register with node %s:%s ' % (host, port),
                               httplib.CONFLICT, '03')


# Checks if the user has that app and gets the logs
def get_app_logs(app_name, email):
    if appdao.is_app_of_user(app_name, email):
        f = {
            'app_name': app_name,
            'logs': logappserverdao.get_app_logs(app_name)
        }
        return create_response(None, httplib.OK, None, 'application/json', f)
    else:
        return create_response('An error occurred when trying to get the %s logs' % app_name, httplib.CONFLICT, '03')


# Auxiliary method that creates a common response structure
def create_response(description, status_code, error=None, mimetype='application/json', content=None):
    res = Response()
    res.status_code = status_code
    res.mimetype = mimetype
    if content:
        res.data = json.dumps(content)
    else:
        f = dict()
        f['description'] = description
        if error:
            f['error'] = error
        f['status_code'] = status_code
        res.data = json.dumps(f)
    return res
