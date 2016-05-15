import httplib
import mongostore, redistore


def statuschecker():
    print 'init the cron task'
    appsnames = mongostore.getapps()
    for appname in appsnames:
        print 'app to check %s' % appname
        servers = mongostore.getServers(appname)
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
                    mongostore.removeServer(appname, host, port)
                    redistore.delete_endpoint(appname, host, port)
            except:
                print 'server to remove %s:%s' % (host, port)
                mongostore.removeServer(appname, host, port)
                redistore.delete_endpoint(appname, host, port)

