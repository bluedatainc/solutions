#!/usr/bin/python
#
# Copyright (c) 2017, BlueData Software, Inc.
#
# This script is used to submit a new job on existing cluster by making calls to REST APIs.
# The script demonstrates how to invoke the following REST APIs
#		1. Login 
#		2. Switch to specific Tenant and
#		3. Submit a Job
#
# Requirements:
# 		1. User would need to define .json files for some APIs.
#		2. Mandatory arguments:
#			 -c <controllerIP>
#			 -u <username>
#			 -p <password>
#
# Example Usage:
# ./submit_job.py -c 10.36.0.17 -u admin -p admin123 
#
# 
#############################################################
# Note: Please replace json payload names with your json files
#############################################################


import argparse
import argparse
import requests, json

# Replace these .json files with your appropriate files
switch_tenant_json_filename = "switch_tenant.json"
job_json_filename = "job.json"

# Parse input arguments
def ParseArguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--controllerip')
	parser.add_argument('-u', '--username')
	parser.add_argument('-p', '--password')
	args = parser.parse_args()
	if not args.controllerip:
		print ("Please provide a Controller IP")
		exit(1)
	if not args.username:
		print ("Please provide a username")
		exit(1)
	if not args.password:
		print ("Please provide a password")
		exit(1)
	return args

parsed_args = ParseArguments()
# Construct API URLs
api_url = "http://"+parsed_args.controllerip+":8080"
api_url_v1 = api_url + "/api/v1/"
api_url_v2 = api_url + "/api/v2/"
# Headers for JSON
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

######################################
### Login and retrieve session_id ###
######################################
login_url = api_url_v1 + "login"
#login = json.load(open("login.json"))
login_info = {u'name': parsed_args.username, u'password': parsed_args.password}
response = requests.post(login_url, data=json.dumps(login_info), headers=headers)
response.raise_for_status()
session_id = response.headers['Location']
print ("Retrieved session_id = " + session_id)

####################################
### Switch to Tenant ###   
####################################
tenant_url = api_url + session_id + "?" + "tenant"
switch_tenant_json = json.load(open(switch_tenant_json_filename))
headers['X-BDS-SESSION']=session_id
response = requests.put(tenant_url, data=json.dumps(switch_tenant_json), headers=headers)
response.raise_for_status()
print ("Switch tenant success! Tenant : " + switch_tenant_json['tenant'])

######################################
### Create a hadoop(CDH) cluster  ###
######################################
cluster_url = api_url_v1 + "cluster"
hadoop_cluster_json = json.load(open(hadoop_cluster_json_filename))
response = requests.post(cluster_url, data=json.dumps(hadoop_cluster_json), headers=headers)
response.raise_for_status()
response_text = json.loads(response.text)
cluster_uuid = response_text['uuid']
print ("Cluster successfully created! UUID = " + cluster_uuid)


####################################
### Submit a Job  ###
####################################
job_url = api_url_v1 + "job"
job_json = json.load(open(job_json_filename))
job_json['cluster_uuid'] = cluster_uuid
response = requests.post(job_url, data=json.dumps(job_json), headers=headers)
print ("Job submitted succesfully!" + response.text)

####################################
### Delete cluster ###
####################################
delete_cluster_url = api_url_v1 + "cluster" + "/" + "+cluster_uuid+"
headers['X-BDS-SESSION']=session_id
response = requests.delete(delete_cluster_url, headers=headers)
print ("cluster deleted successfully" + response)




