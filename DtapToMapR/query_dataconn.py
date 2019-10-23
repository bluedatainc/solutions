#!/usr/bin/env python

import requests
import sys
import settings
import session

json_debug = False

def usage():
    print "%s <dataconn> [<path_prefix>]" % (sys.argv[0])
    print "or"
    print "%s <rem_obj>" % (sys.argv[0])

def print_objinfo(objects):
    size_field_width = 4
    for object in objects:
        len_size_str = len(str(object["size"]))
        if len_size_str > size_field_width:
            size_field_width = len_size_str
    print 'dir {0:>{1}} path'.format('size', size_field_width)
    for object in objects:
        object_path = object["path_from_dataconn"]
        object_size = object["size"]
        if object["is_folder"]:
            object_annotation = '*'
        else:
            object_annotation = ' '
        print ' {0}  {1:>{2}} {3}'.format(object_annotation, object_size, size_field_width, object_path)
    print

def main(argv):
    if len(argv) < 1 or len(argv) > 2:
        usage()
        sys.exit(2)
    dataconn_path = argv[0]
    obj_id = dataconn_path[len(settings.get_setting('DATACONN_URL')):]
    rem_obj = "/" in obj_id
    if len(argv) == 2:
        if rem_obj:
            usage()
            sys.exit(2)
        query = '?query=' + argv[1]
    else:
        if rem_obj:
            query = ''
        else:
            query = '?query='
    session_id = session.login()
    print
    url = settings.get_setting('BASE_URL') + dataconn_path + query
    response = requests.get(url, headers=session.get_session_hdr(session_id))
    if response.status_code == 404:
        print "object not found"
    else:
        if rem_obj:
            print_objinfo([response.json()])
        else:
            query_results = response.json()["_embedded"]["query_results"]
            if "matching_objects" in query_results:
                print_objinfo(query_results["matching_objects"])
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
