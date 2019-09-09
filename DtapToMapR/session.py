import sys
import json
try:
    import bdtest.bds_qa_requests as requests
except ImportError:
    import requests
import time
import settings


def get_session_hdr(session_id):
    return({settings.get_setting('BDS_SESSION_TAG'): session_id})


def login(user='BDS_USER', silent=False):
    url = settings.get_setting('BASE_URL') \
    + settings.get_setting('LOGIN_URL')
    try:
        data = json.dumps({"name": settings.get_setting(user),
                          "password": settings.get_setting('BDS_PASSWORD')})
        resp = requestOp(op="post", url=url, data=data)
        if resp is None:
            return ''
        if resp.status_code == 201:
            if not silent:
                print "Logged in Session ID: %s" % (resp.headers["location"])
            return resp.headers['location']
        else:
            return ''
    except:
        return ''


def logout(session_id):
    url = settings.get_setting('BASE_URL') \
    + settings.get_setting('LOGOUT_URL')
    try:
        requestOp(op="post", url=url, headers=get_session_hdr(session_id))
    except:
        return


def become_site_admin(session_id, session_header):
    site_admin_role_url = None
    url = settings.get_setting('BASE_URL') \
    + settings.get_setting('ROLE_URL')
    response = requestOp(op="get", url=url, headers=session_header)
    if response is None:
        print "Failed to perform requests.get"
        sys.exit(2)
    role_list = response.json()["_embedded"]["roles"]
    for role in role_list:
        if role["label"]["name"] == settings.get_setting('BDS_SITE_ADMIN_ROLE'):
            site_admin_role_url = role["_links"]["self"]["href"]
    if site_admin_role_url is None:
        print "site admin role not found!"
        sys.exit(2)
    admin_tenant_url = None
    url = settings.get_setting('BASE_URL') \
    + settings.get_setting('TENANT_URL')
    response = requestOp(op="get", url=url, headers=session_header)
    if response is None:
        print "Failed to perform requests.get"
        sys.exit(2)
    tenant_list = response.json()["_embedded"]["tenants"]
    for tenant in tenant_list:
        if tenant["label"]["name"] == settings.get_setting('BDS_ADMIN_TENANT'):
            admin_tenant_url = tenant["_links"]["self"]["href"]
    if admin_tenant_url is None:
        print "admin tenant not found!"
        sys.exit(2)
    url = settings.get_setting('BASE_URL') + session_id + '?tenant'
    role_data = {"role": site_admin_role_url, "tenant": admin_tenant_url}
    role_spec = json.dumps(role_data)
    response = requestOp(op="put", url=url, data=role_spec, headers=session_header)
    if response is None:
        print "Failed to perform requests.put"
        sys.exit(2)
    if response.status_code != 204:
        print "taking site admin role failed!"
        sys.exit(2)


def requestOp(op=None, url=None, data=None, role_spec=None, headers=None):
    i = 0
    maxRetries = 10
    response = None
    sleepTime = 30 # retry for 5 minutes
    while 1:
        try:
            if op == "get":
                response = requests.get(url, headers=headers, timeout=20)
            elif op == "put":
                response = requests.put(url, data=data, headers=headers, timeout=20)
            elif op == "post":
                response = requests.post(url, data=data, headers=headers, timeout=20)
            elif op == "delete":
                response = requests.delete(url, headers=headers, timeout=20)
            return response
        except Exception as error:
            print "Error while performing ", op, ". Error: ", error
            print "Retrying ", i+1, " of ", maxRetries, " times."
            i += 1
            time.sleep(sleepTime)
            print "Done sleeping ", sleepTime, " seconds"
            if i == maxRetries:
                print "Failed to connect after ", maxRetries, " attempts."
                return response
