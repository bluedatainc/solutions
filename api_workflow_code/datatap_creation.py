#!/usr/bin/python
#
# Copyright (c) 2017, BlueData Software, Inc.
#
# This script is used to create a datatap in specific tenant by making calls to REST APIs.
# The script demonstrates how to invoke the following REST APIs
#		1. Login 
#		2. Switch to specific Tenant and
#		3. Create Datatap.
#
# Requirements:
# 		1. User would need to define .json files for some APIs.
#		2. Mandatory arguments:
#			 -c <controllerIP>
#			 -u <username>
#			 -p <password>
#
# Example Usage:
# ./datatap_creation.py -c 10.36.0.17 -u admin -p admin123 
#
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
datatap_json_filename = "datatap.json"

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

######################################
### Switch to Tenant ### 
######################################  
tenant_url = api_url + session_id + "?" + "tenant"
switch_tenant_json = json.load(open(switch_tenant_json_filename))
headers['X-BDS-SESSION']=session_id
response = requests.put(tenant_url, data=json.dumps(switch_tenant_json), headers=headers)
response.raise_for_status()
print ("Switch tenant success! Tenant : " + switch_tenant_json['tenant'])

####################################
### Create Datatap  ###
######################################
datatap_url = api_url_v1 + "dataconn"
datatap_json = json.load(open(datatap_json_filename))
response = requests.post(datatap_url, data=json.dumps(datatap_json), headers=headers)
print ("Successfully created " + response.text)


