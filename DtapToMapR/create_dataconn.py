#!/usr/bin/env python

import getopt
import requests
import json
import sys
import settings
import session
import query_dataconn

json_debug = False

url = settings.get_setting('BASE_URL') + settings.get_setting('DATACONN_URL')

def usage():
    print "%s -n <name> [-p <path_from_endpoint>] -t <file|gluster|hdfs|swift|nfs> <type-specific-args> [--test <query_prefix>]" % (sys.argv[0])
    print "  args for file type: [-m <mount>]"
    print "  args for gluster type: -s <server> -v <volume> [-o <port>]"
    print "  args for hdfs type: -s <server> [-o <port>]"
    print "  args for swift type: -s <server> -a <account> -c <container> [--secure] [-u username -k key]"
    print "  args for nfs type: -s <server> -e <export> [-m <mount>]"

def dataconn_spec(endpoint_data, root_path, name):
    spec_data = {"endpoint": endpoint_data}
    spec_data["label"] = {"name": name}
    if root_path is not None:
        spec_data["bdfs_root"] = {"path_from_endpoint": root_path}
    spec = json.dumps(spec_data)
    if json_debug:
        print "debug:"
        print "  %s" %(spec)
    return spec

def post_dataconn(session_id, endpoint_data, root_path, name):
    spec = dataconn_spec(endpoint_data, root_path, name)
    session_header = session.get_session_hdr(session_id)
    return requests.post(url, spec, headers=session_header)

def post_file_dataconn(session_id, root_path, name, mount):
    endpoint_data = {"type" : "file"}
    if mount is not None:
        endpoint_data["mount_point"] = mount
    return post_dataconn(session_id, endpoint_data, root_path, name)

def post_gluster_dataconn(session_id, root_path, name, host, volume, port):
    endpoint_data = {"type" : "gluster", "host" : host, "volume" : volume}
    if port is not None:
        endpoint_data["port"] = port
    return post_dataconn(session_id, endpoint_data, root_path, name)

def post_hdfs_dataconn(session_id, root_path, name, host, backup_host, port):
    endpoint_data = {"type" : "hdfs", "host" : host}
    if backup_host is not None:
        endpoint_data["backup_host"] = backup_host
    if port is not None:
        endpoint_data["port"] = port
    return post_dataconn(session_id, endpoint_data, root_path, name)

def post_swift_dataconn(session_id, root_path, name, host, account, container, secure, username, key):
    endpoint_data = {"type" : "swift", "host" : host, "account" : account, "container" : container}
    if secure is not None:
        endpoint_data["secure"] = secure
    if username is not None or key is not None:
        auth_data = {}
        if username is not None:
            auth_data["username"] = username
        if key is not None:
            auth_data["password"] = key
        endpoint_data["auth"] = auth_data
    return post_dataconn(session_id, endpoint_data, root_path, name)

def post_nfs_dataconn(session_id, root_path, name, host, share, mount):
    endpoint_data = {"type" : "nfs", "host" : host, "share" : share}
    if mount is not None:
        endpoint_data["mount_point"] = mount
    return post_dataconn(session_id, endpoint_data, root_path, name)


def main(argv):
    global url

    try:
        opts, args = getopt.getopt(argv, "hn:p:t:s:v:o:a:c:u:k:e:m:",
                                   ["help", "name=", "path=", "type=",
                                    "server=", "volume=", "port=",
                                    "account=", "container=", "secure",
                                    "username=", "key=",
                                    "export=", "mount=", "test="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    conn_name = None
    conn_path = None
    conn_type = None
    host = None
    backup_host = None
    port = None
    gluster_volume = None
    swift_account = None
    swift_container = None
    swift_secure = False
    swift_username = None
    swift_key = None
    nfs_export = None
    mount = None
    test = False

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-n", "--name"):
            conn_name = arg
        elif opt in ("-p", "--path"):
            conn_path = arg
        elif opt in ("-t", "--type"):
            conn_type = arg
        elif opt in ("-s", "--server"):
            host = arg
        elif opt in ("-b", "--backup_server"):
            backup_host = arg
        elif opt in ("-v", "--volume"):
            gluster_volume = arg
        elif opt in ("-o", "--port"):
            port = int(arg)
        elif opt in ("-a", "--account"):
            swift_account = arg
        elif opt in ("-c", "--container"):
            swift_container = arg
        elif opt in ("--secure"):
            swift_secure = True
        elif opt in ("-u", "--username"):
            swift_username = arg
        elif opt in ("-k", "--key"):
            swift_key = arg
        elif opt in ("-e", "--export"):
            nfs_export = arg
        elif opt in ("-m", "--mount"):
            mount = arg
        elif opt in ("--test"):
            test = True
            url = settings.get_setting('BASE_URL') + settings.get_setting('TESTDATACONN_URL') + '?query=' + arg

    if conn_name is None:
        if not test:
            usage()
            sys.exit(2)
        else:
            conn_name = ""

    if conn_type not in ("file", "gluster", "hdfs", "swift", "nfs"):
        usage()
        sys.exit(2)

    # Current set of endpoint args: host, gluster_volume, port, swift_account,
    # swift_container, swift_secure, swift_username, swift_key, nfs_export, mount

    has_swift_only_args = swift_account is not None or swift_container is not None or swift_secure or swift_username is not None or swift_key is not None

    has_required_args = {}
    has_required_args["file"] = True
    has_required_args["gluster"] = host is not None and gluster_volume is not None
    has_required_args["hdfs"] = host is not None
    has_required_args["swift"] = host is not None and swift_account is not None and swift_container is not None
    has_required_args["nfs"] = host is not None and nfs_export is not None

    has_wrong_args = {}
    has_wrong_args["file"] = host is not None or gluster_volume is not None or port is not None or has_swift_only_args or nfs_export is not None
    has_wrong_args["gluster"] = has_swift_only_args or nfs_export is not None or mount is not None
    has_wrong_args["hdfs"] = gluster_volume is not None or has_swift_only_args or nfs_export is not None or mount is not None
    has_wrong_args["swift"] = gluster_volume is not None or port is not None or nfs_export is not None or mount is not None
    has_wrong_args["nfs"] = gluster_volume is not None or port is not None or has_swift_only_args

    if has_wrong_args[conn_type] or not has_required_args[conn_type]:
        usage()
        sys.exit(2)


    session_id = session.login(user='BDS_ADMIN')

    if conn_type == "file":
        response = post_file_dataconn(session_id, conn_path, conn_name, mount)
    elif conn_type == "gluster":
        response = post_gluster_dataconn(session_id, conn_path, conn_name, host, gluster_volume, port)
    elif conn_type == "hdfs":
        response = post_hdfs_dataconn(session_id, conn_path, conn_name, host, backup_host, port)
    elif conn_type == "swift":
        response = post_swift_dataconn(session_id, conn_path, conn_name, host, swift_account, swift_container, swift_secure, swift_username, swift_key)
    elif conn_type == "nfs":
        response = post_nfs_dataconn(session_id, conn_path, conn_name, host, nfs_export, mount)

    print

    if not test:
        if response.status_code != 201:
            print "Data connector creation failed!"
            print response.text
            sys.exit()
        print "Created: %s" % (response.headers["location"])
        print
    else:
        if response.status_code != 200:
            print "Data connector test failed!"
            print response.text
            sys.exit()
        query_results = response.json()["query_results"]
        if "matching_objects" in query_results:
            query_dataconn.print_objinfo(query_results["matching_objects"])
        else:
            print "errors:"
            for error in query_results["access_errors"]:
                print "  %s" %(error)
        if json_debug:
            print "debug:"
            print "  %s" %(response.json())

    session.logout(session_id)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
