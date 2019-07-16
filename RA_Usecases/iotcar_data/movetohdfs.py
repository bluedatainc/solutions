#!/usr/bin/python
# Last updated 7/12/19

# DISCLAIMER OF WARRANTY
#This document may contain the following HPE or other software: XML, CLI statements, scripts, parameter files. These are provided as a courtesy, 
#free of charge, AS-IS by Hewlett-Packard Enterprise Company (HPE). HPE shall have no obligation to maintain or support this software. HPE MAKES
#NO EXPRESS OR IMPLIED WARRANTY OF ANY KIND REGARDING THIS SOFTWARE INCLUDING ANY WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, 
#TITLE OR NON-INFRINGEMENT. HPE SHALL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES, WHETHER BASED ON CONTRACT,
#TORT OR ANY OTHER LEGAL THEORY, CONNECTION WITH OR ARISING OUT OF THE FURNISHING, PERFORMANCE OR USE OF THIS SOFTWARE.

#Copyright 2011 Hewlett-Packard Enterprise Development Company, L.P. The information contained herein is subject to change without notice. The only
#warranties for HPE products and services are set forth in the express warranty statements accompanying such products and services. Nothing
#herein should be construed as constituting an additional warranty. HPE shall not be liable for technical or editorial errors or omissions 
#contained herein.



import argparse 
from argparse import RawTextHelpFormatter
import subprocess
import os
import  json


def run_cmd(args_list):
#    print('Running command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    (output, errors) = proc.communicate()
    if proc.returncode:
        raise RuntimeError(
            'Error running command: %s. Return code: %d, Error: %s' % (' '.join(args_list), proc.returncode, errors))
    return (output, errors) 

def run_cmd_exec(args_list):
#    print('Running command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    (output, errors) = proc.communicate()
    if proc.returncode:
        return(1)
    return (0) 


# Parse input arguments
def ParseArguments():
	parser = argparse.ArgumentParser(description='MoveData Example', formatter_class=RawTextHelpFormatter, epilog=" ")
	parser.add_argument('-localdir', '--localdir',help='CSV source directory /nfs', type=str)
	parser.add_argument('-hdfsdir', '--hdfsdir',help='HDFS destination directory /user/anayst1', type=str)
	args = parser.parse_args()
	if not args.localdir:
		print ("Please provide the directory path of csv files")
		exit(1)
	if not args.hdfsdir:
		print ("Please provide the path of the HDFS destination directory")
		exit(1)

	return args




#############################################################################################################
# Begin MoveData Main
#############################################################################################################

def Main():
    parsed_args = ParseArguments()
    dtapnfs = parsed_args.localdir
    dtaphdfs = parsed_args.hdfsdir



    dirlist=["/bluedata","/bluedata/usecase","/bluedata/usecase/iotcar","/bluedata/usecase/iotcar/data","/bluedata/usecase/iotcar/data/autos","/bluedata/usecase/iotcar/data/owners","/bluedata/usecase/iotcar/data/iotcar_stream"]


# Validate directories exist
    print ("\nValidating HDFS Directories")
    for dirlevel in dirlist:
        if  (run_cmd_exec(['hadoop','fs','-test', '-d',dtaphdfs+dirlevel])) == 1:
            print (" Creating HDFS directory " + dtaphdfs+dirlevel )
            (out, errors) = run_cmd(['hadoop','fs','-mkdir',dtaphdfs+dirlevel])


# Delete existing data
    print ("\nDeleting Existing Data")
    for dirlevel in ["/bluedata/usecase/iotcar/data/autos","/bluedata/usecase/iotcar/data/owners","/bluedata/usecase/iotcar/data/iotcar_stream"]:
        out=run_cmd_exec(['hdfs','dfs','-rm','-skipTrash',dtaphdfs+dirlevel+'/*'])

# Move data from Linux to HDFS

    print ( "\nMoving data to HDFS")
    print (" Moving data from " + dtapnfs+'/data/autos/' + " to " + dtaphdfs+'/bluedata/usecase/iotcar/data/autos/' )
    out = run_cmd_exec(['hadoop','fs','-copyFromLocal',dtapnfs+'/data/autos/',dtaphdfs+'/bluedata/usecase/iotcar/data/'])

    print (" Moving data from " + dtapnfs+'/data/owners/' + " to " + dtaphdfs+'/bluedata/usecase/iotcar/data/owners/' )
    out = run_cmd_exec(['hadoop','fs','-copyFromLocal',dtapnfs+'/data/owners/',dtaphdfs+'/bluedata/usecase/iotcar/data/'])

    print (" Moving data from " + dtapnfs+'/data/iotcar_stream/' + " to " + dtaphdfs+'/bluedata/usecase/iotcar/data/iotcar_stream' )
    out = run_cmd_exec(['hadoop','fs','-copyFromLocal',dtapnfs+'/data/iotcar_stream/',dtaphdfs+'/bluedata/usecase/iotcar/data'])

# Display Data
#    (out, errors) = run_cmd(['hadoop','fs','-ls','-R',dtaphdfs+"bluedata/usecase/iotcar/data/"])
#    print (out)    
    
    print ("\nData has been moved to HDFS" )
    

if __name__ == '__main__':
    Main()