#!/usr/bin/python
#
# Copyright (c) 2017, BlueData Software, Inc.
#
# This script is used to retrieve all datataps per tenant by making calls to REST APIs.
# The script demonstrates how to invoke the following REST APIs
#		1. Login 
#		2. Switch to specific Tenant and
#		3. List datataps per Tenant.
#
# Requirements:
# 		1. User would need to define .json files for some APIs.
#		2. Mandatory arguments:
#			 -c <controllerIP>
#			 -u <username>
#			 -p <password>
#
# Example Usage:
# ./list_datataps_per_tenant.py -c 10.36.0.17 -u admin -p admin123 
#
# 
#############################################################
# Note: Please replace json payload names with your json files
#############################################################


import argparse
import argparse
import requests, json

# Replace these .json files with your appropriate files
#switch_tenant_json_filename = "workflow_conf/switch_tenant.json"

# Parse input arguments
def ParseArguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--controllerip', help='EPIC controller ip')
	parser.add_argument('-u', '--username',help='EPIC controller userid')
	parser.add_argument('-p', '--password',help='EPIC controller password')
	parser.add_argument('-conf', '--conf',help='Workflow Configuration json file, type=str')
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
	if not args.conf:
                args.conf="workflow_conf/workflow_config.json"
	return args

parsed_args = ParseArguments()
# Construct API URLs
api_url = "http://"+parsed_args.controllerip+":8080"
api_url_v1 = api_url + "/api/v1/"
api_url_v2 = api_url + "/api/v2/"
# Headers for JSON
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

######################################
### Load switch_tenant file        ###
######################################
workflow_filename = parsed_args.conf 

try:
    workflow_conf = json.load(open(workflow_filename))
except:
    print ("Could not load " + workflow_filename)
    exit()

switch_tenant_json_filename = workflow_conf["config"]["switch_tenant_json_filename"]


######################################
### Login and retrieve session_id ###
######################################
login_url = api_url_v1 + "login"
#login = json.load(open("login.json"))
login_info = {u'name': parsed_args.username, u'password': parsed_args.password}
response = requests.post(login_url, data=json.dumps(login_info), headers=headers)
response.raise_for_status()
session_id = response.headers['Location']
#print ("Retrieved session_id = " + session_id)

####################################
### Switch to Tenant ### 
####################################  
tenant_url = api_url + session_id + "?" + "tenant"
switch_tenant_json = json.load(open(switch_tenant_json_filename))
headers['X-BDS-SESSION']=session_id
response = requests.put(tenant_url, data=json.dumps(switch_tenant_json), headers=headers)
response.raise_for_status()
#print ("Switch tenant success! Tenant : " + switch_tenant_json['tenant'])

######################################
### retrieve clusters  ###
######################################
datatap_url = api_url_v2 + "cluster"
response = requests.get(datatap_url, headers=headers)
response_text = json.loads(response.text)
 
print "\nVirtual clusters"
for clust in response_text['_embedded']['clusters']:
     clust_uuid = clust['_links']['self']["href"]
     clust_uuid = clust_uuid.split("/")[4]
     clust_name = clust['label']['name']   
     clust_desc = clust['label']['description']   
     print " " + clust_name + " " + clust_desc + " uuid: " + clust_uuid 




######################################
### retrieve roles  ###
######################################
datatap_url = api_url_v1 + "role"
#datatap_url = api_url_v2 + "tenant"
response = requests.get(datatap_url, headers=headers)
response_text = json.loads(response.text)
 
print "\nRoles"
for role in response_text['_embedded']['roles']:
     role_uuid = role['_links']['self']["href"]
     role_uuid = role_uuid.split("/")[4]
     role_name = role['label']['name']   
     role_desc = role['label']['description']   
     print " " + role_name + " " + role_desc + " uuid: " + role_uuid



######################################
### retrieve tenants  ###
######################################
#datatap_url = api_url_v1 + "tenant"
datatap_url = api_url_v2 + "tenant"
response = requests.get(datatap_url, headers=headers)
response_text = json.loads(response.text)
 
print "\nTenants"
for tenant in response_text['_embedded']['tenants']:
    tenant_uuid = tenant['_links']['self']["href"]
    tenant_uuid =  tenant_uuid.split("/")[4]
    tenant_name = tenant['label']['name']   
    tenant_desc = tenant['label']['description']   
    print " " + tenant_name + " " + tenant_desc + " " + " uuid: " + tenant_uuid



######################################
### retrieve flavors for this tenant #
######################################
datatap_url = api_url_v1 + "flavor"
#datatap_url = api_url_v2 + "tenant"
response = requests.get(datatap_url, headers=headers)
response_text = json.loads(response.text)
 
print "\nFlavors"
for flavor in response_text['_embedded']['flavor']:
    flavor_uuid = flavor ['_links']['self']["href"]
    flavor_uuid =  flavor_uuid.split("/")[4]
    flavor_name = flavor ['label']['name']   
    flavor_desc = flavor['label']['description']   
    print " " + flavor_name + " " + flavor_desc +  " uuid: " + flavor_uuid




