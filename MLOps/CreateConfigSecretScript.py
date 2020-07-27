import requests
import pprint
from kubernetes import client, config
import base64
import json
import sys
from getpass import getpass

"""
This script can be run from the user's local laptop/computer.
Creates a namespaced secret (containing a kubeconfig) to be used as a KubeDirector connection.
The secret name is config-@@@USERNAME@@@
Purpose: to run kubectl commands from within notebook clusters.

"""

def getSession(ip, username, password):
    data = {"name":username, "password":password}
    headers  = {'content-type' : 'application/json'}
    response = requests.post("http://" + ip + ":8080/api/v1/login", json=data, headers=headers)
    session=response.headers['Location']
    return session


# List all tenant/namespace pairs.
def getTenantNamespacePairs(ip, username, password):
    session = getSession(ip, username, password)
    headers = { 'X-BDS-SESSION' : session}
    url = "http://" + ip + ":8080/api/v2/tenant"
    try:
        response = requests.request("GET", url, headers=headers)
    except:
        raise AssertionError("Error getting tenants, please verify that kubectl is set up on your machine.")
    allTenants = []
    for tenant in response.json()['_embedded']['tenants']:
        if (tenant['tenant_type'] == 'k8s'):
            allTenants.append([tenant['label']['name'], tenant['tenant_enclosed_properties']['namespace']])
    if (len(allTenants) == 0):
        raise AssertionError("No k8s tenants found, please verify that kubectl is set up on your machine.")
    return allTenants


# Prompt user to choose a namespace.
def getNamespace(allTenants):
    print('\n List of tenants/namespaces:')
    for i in range(len(allTenants)):
        print(' [' + str(i) + '] ' + 'Tenant: ' + allTenants[i][0] + ' Namespace: ' + allTenants[i][1])
    print('\n')
    tenant_num = int(input("Please enter the number from the list corresponding to your tenant/namespace: "))
    try:
        return allTenants[tenant_num][1]
    except:
        raise ValueError("Invalid tenant selection.")


# Return kubeconfig of the logged-in user
def getKubeconfigUser(ip, username, password):
    session = getSession(ip, username, password)
    headers = { 'X-BDS-SESSION' : session}
    url = "http://" + ip + ":8080/api/v2/k8skubeconfig"
    response = requests.request("GET", url, headers=headers)
    return response.text


# Create the secret containing the kubeconfig
def createKubeconfigSecret(ip, username, password):

    allTenants = getTenantNamespacePairs(ip, username, password)

    # namespace where the secret will be created
    namespace = getNamespace(allTenants)

    # load the logged-in user's kubeconfig that will be saved in the secret
    try:
        if sys.version_info[0] < 3:
            data = {'config': base64.b64encode(getKubeconfigUser(ip, username, password))}
        else:
            data = {'config': base64.b64encode(getKubeconfigUser(ip, username, password).encode("utf-8")).decode("utf-8")}
    except:
        raise ValueError("Error please verify that the IP, username, tenant, and password are correct.")

    # load kubeconfig from user's machine for the purpose of connecting to CoreV1Api, then create secret
    try:
        secret_name = 'config-' + username
        config.load_kube_config()
        core_api_instance = client.CoreV1Api()
        try:
            core_api_instance.delete_namespaced_secret(secret_name, namespace)
        except:
            pass
        body = client.V1Secret()
        body.api_version = 'v1'
        body.data = data
        body.kind = 'Secret'
        body.metadata = {'name': secret_name, "labels": {"kubedirector.hpe.com/secretType": "kubeconfig"}}
        body.type = 'Opaque'
        api_response = core_api_instance.create_namespaced_secret(namespace, body)
        print("\nA new secret containing the config has been created in the " + namespace + " namespace.")
        print("Secret name: " + secret_name)
    except:
        raise AssertionError("Error creating secret. Please verify that kubectl is set up on your machine.")


def main():
    # backwards compabitle with python 2 and 3
    global input
    if sys.version_info[0] < 3:
        input = raw_input

    createKubeconfigSecret(input("Please enter your controller IP: "),
                           input("Please enter your username: "),
                           getpass("Please enter your password (hidden input): "))


if __name__ == '__main__':
    main()
