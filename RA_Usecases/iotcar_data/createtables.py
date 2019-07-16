#!/usr/bin/python

# last updated  7/12/19
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
import os, sys
import  json
import shutil

def run_cmd(args_list):
    print('  Running command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    (output, errors) = proc.communicate()
    if proc.returncode:
        raise RuntimeError(
            '  Error running command: %s. Return code: %d, Error: %s' % (' '.join(args_list), proc.returncode, errors))
    return (output, errors) 

def run_cmd_exec(args_list):
    print('  Running command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    (output, errors) = proc.communicate()
    if proc.returncode:
        return(1)
    return (0) 


# Parse input arguments
def ParseArguments():
	parser = argparse.ArgumentParser(description='Create IoT connected car tables', formatter_class=RawTextHelpFormatter, epilog=" ")
	parser.add_argument('-hdfsdir', '--hdfsdir',help='HDFS destination directory /user/anayst1', type=str)
	args = parser.parse_args()
	if not args.hdfsdir:
		print ("Please provide the path of the HDFS directory. Example: -hdfsdir /user/analyst1")
		exit(1)

	return args




#############################################################################################################
# Begin Create Tables Main
#############################################################################################################

def Main():
    parsed_args = ParseArguments()
    dtaphdfs = parsed_args.hdfsdir


    print ("\n HDFS source directory: " + dtaphdfs + "\n"  )
  
    input = sys.stdin
    output = sys.stdout

    dirlist=["/bluedata","/bluedata/usecase","/bluedata/usecase/iotcar","/bluedata/usecase/iotcar/data","/bluedata/usecase/iotcar/data/autos","/bluedata/usecase/iotcar/data/owners","/bluedata/usecase/iotcar/data/iotcar_stream"]


# Validate directories exist
    print (" Validating HDFS Directories exist")

    for dirlevel in dirlist:
        if  (run_cmd_exec(['hadoop','fs','-test', '-d',dtaphdfs+dirlevel])) == 1:
            print (" Missing directory " + dirlevel )
            exit(1)



# modify location

    try:
        input = open('hive_ddl/hive-iotcar-external-ddl-python.sql')
        output = open('hive_ddl/hive-iotcar-external-ddl-python-new.sql', 'w')
        
        for s in input.xreadlines(  ):
            output.write(s.replace('<iotloc>', dtaphdfs ))
        output.close(  )
        input.close(  )
    except Exception as er:
        print ("Error processing hive_ddl/hive-iotcar-external-ddl.sql" )
        print (er)
        exit(1)

    print "\nCreating Hive external Tables "  
    (out, errors) = run_cmd(['hive','-f',"hive_ddl/hive-iotcar-external-ddl-python-new.sql"])
    print (out)    
    print "\nCreating Hive orc Tables "  
    (out, errors) = run_cmd(['hive','-f',"hive_ddl/hive-iotcar-orc-ddl.sql"])
    print (out)    
    print "\nCreating Hive parquet Tables "  
    (out, errors) = run_cmd(['hive','-f',"hive_ddl/hive-iotcar-parquet-ddl.sql"])
    print (out)    
   
    print "\n Tables were loaded"  
  

if __name__ == '__main__':
    Main()