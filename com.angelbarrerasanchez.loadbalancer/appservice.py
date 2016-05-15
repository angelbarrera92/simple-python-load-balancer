from flask import request, Response
import httplib
import appdao, userdao, appserversdao


# Method that purges the non functional servers of an application
def app_servers_status_checker():
    print 'init the cron task'
    appsnames = appdao.getapps()
    for appname in appsnames:
        print 'app to check %s' % appname
        servers = appdao.getServers(appname)
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


# Principal method of the app.
# Gets a server for the app and path request and makes the request.
def balance_request(appid, path):
    print 'You %s want path: %s' % (appid, path)
    h1 = httplib.HTTPConnection(appserversdao.get_random_endpoint_of_app(appid)[0])
    headers = dict(request.headers)
    headers.pop("Content-Length", None)
    h1.request(method=request.method, url="/%s" % path, headers=headers)
    r = h1.getresponse()
    data = r.read()
    res = Response()
    #TODO MAKE A VALID RESPONSE
    return res


def user_exists(email):
    return userdao.user_exists(email)


# Check if the app exists
def app_exists(app_name):
    return appserversdao.app_exists(app_name)


# Register a new user
def register_user(email, password):
    if userdao.register_user(email, password):
        # TODO MAKE A GOOD RESPONSE
        return None
    else:
        # TODO MAKE A BAD RESPONSE
        return None


# Remove a user
def remove_user(email, password):
    if userdao.remove_user(email, password):
        apps = appdao.get_user_apps(email)
        for app in apps:
            appdao.remove_app(app, email)
            appserversdao.remove_app(app)
        # TODO MAKE A GOOD RESPONSE
        return None
    else:
        # TODO MAKE A BAD RESPONSE
        return None


# Register a new app for a user,
# it is required to specify at least one server
def register_app(email, app_name, host, port, status_path):
    appdao.add_app_server(app_name, host, port, email, status_path)
    appserversdao.register_endpoint(app_name, host, port)
    return None


# Remove an existing app checking if the app is registered by the user (email)
def remove_app(email, app_name):
    if appdao.is_app_of_user(app_name, email):
        appserversdao.remove_app(app_name)
        appdao.remove_app(app_name, email)
        # TODO MAKE A GOOD RESPONSE
        return None
    else:
        # TODO MAKE A BAD RESPONSE
        return None


# Register a new server of an existing application
def register_server_app(email, app_name, host, port, status_path):
    if appdao.is_app_of_user(app_name, email):
        register_app(email, app_name, host, port, status_path)
        # TODO MAKE A GOOD RESPONSE
        return None
    else:
        # TODO MAKE A BAD RESPONSE
        return None


# Remove a server of an existing application
def remove_server_app(email, app_name, host, port):
    if appdao.is_app_of_user(app_name, email):
        appserversdao.delete_endpoint(app_name, host, port)
        appdao.remove_server(app_name, host, port, email)
        # TODO MAKE A GOOD RESPONSE
        return None
    else:
        # TODO MAKE A BAD RESPONSE
        return None