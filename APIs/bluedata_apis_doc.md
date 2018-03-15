<span style="color:#f2cf4a; font-family: 'Bookman Old Style';">

# REST APIs

__Note__:

  - For Epic3.2 and later you can find v2 API docs for a given EPIC installation by connecting to the /apidocs URL on its controller host "http://<controller-IP>:8080/apidocs". For more information on difference between v1 and v2 APIs, here is the link 

  -  Make sure to run API#1 and API#37 prior to running other API's.

  - [1. Login and Session Creation](#1-login-and-session-creation)
  - [2. Retrieve available cluster images](#2-retrieve-available-cluster-images)
  - [3. Retrieve available tenants](#3-retrieve-available-tenants)
  - [4. Retrieve tenant information such as resources security and other settings](#4-retrieve-tenant-information-such-as-resources-security-and-other-settings)
  - [5. Retrieve tenant virtual clusters](#5-retrieve-tenant-virtual-clusters)
  - [6. Retrieve a virtual cluster configuration](#6-retrieve-a-virtual-cluster-configuration)
  - [7. Get created DataTap in a certain Tenant](#7-get-created-datatap-in-a-certain-tenant)
  - [8. Create a new cluster](#8-create-a-new-cluster)
  - [9. Create a cluster with gateway node](#9-create-a-cluster-with-gateway-node)
  - [10. Create a cluster DataTap](#10-create-a-cluster-datatap)
  - [11. Enable virtual cluster Kerberos](#11-enable-virtual-cluster-kerberos)
  - [12. Delete an existing cluster](#12-delete-an-existing-cluster)
  - [13. Delete an existing DataTap](#13-delete-an-existing-datatap)
  - [14. Create a new tenant](#14-create-a-new-tenant)
  - [15. Assign groups to a tenant](#15-assign-groups-to-a-tenant)
  - [16. Create a new user](#16-create-a-new-user)
  - [17. Delete an existing user](#17-delete-an-existing-user)
  - [18. Delete an existing tenant](#18-delete-an-existing-tenant)
  - [19. Assign security roles to a tenant](#19-assign-security-roles-to-a-tenant)
  - [20. Submit a job to persistent cluster](#20-submit-a-job-to-persistent-cluster)
  - [21. Submit a job to Transient cluster](#21-submit-a-job-to-transient-cluster)
  - [22. Retrieve list of all jobs](#22-retrieve-list-of-all-jobs)
  - [23. Assign a user to tenant](#23-assign-a-user-to-tenant)
  - [24. Get Tenant info for a user](#24-get-tenant-info-for-a-user)
  - [25. Get user info for a Tenant](#25-get-user-info-for-a-tenant)
  - [26. Reset User Password](#26-reset-user-password)
  - [27. Reboot Virtual Node](#27-reboot-virtual-node)
  - [28. Reboot Virtual Cluster](#28-reboot-virtual-cluster)
  - [29. Stop a Virtual Cluster](#29-stop-a-virtual-cluster)
  - [30. Start a Virtual Cluster](#30-start-a-virtual-cluster)
  - [31. Revoke User Access to a Tenant](#31-revoke-user-access-to-a-tenant)
  - [32. Retrieve a List of All Virtual Nodes](#32-retrieve-a-list-of-all-virtual-nodes)
  - [33. Delete a job](#33-delete-a-job)
  - [34. Invoke ActionScript](#34-invoke-actionscript)
  - [35. Update the hue.ini safety valve to point to datatap](#35-update-the-hue.ini-saftey-valve-to-point-to-datatap)
  - [36. Mount dtap to Virtual cluster ActionScript](#36-mount-dtap-to-virtual-cluster-actionscript)
  - [37. Switch Tenant](#37-switch-tenant)
  - [38. Verify current session role and tenant](#verify-current-session-role-and-tenant)
  - [39. Invoke ActionScript from dtap](#39-invoke-actionscript-from-dtap)
  - [40. Install catalog Image](#40-install-catalog-image)
  - [41. Get a tenant keypair file](#41-get-a-tenant-keypair-file)

## 1. Login and Session Creation

  __API-URI__: /api/v1/login

  __Curl command__:

      curl -i -X POST -d@login.json http://<controller-ip>:8080/api/v1/login

  __API Type__: `POST`

  __Example__:

      curl -i -X POST -d@login.json http://10.36.0.17:8080/api/v1/login

 __Json-file__: login.json:

        {
          "name" : "admin",
          "password": "admin123"
        }

  __Response__:

      HTTP/1.1 201 Created
      Server: BlueData EPIC 2.6
      Location: /api/v1/session/ad93b4bb-8908-4af9-8c36-ea4f92f29277
      Date: Thu, 18 May 2017 23:35:05 GMT
      Content-Length: 13


## 2. Retrieve available cluster images

  __API-URI__: /api/v1/catalog

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/catalog/

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/catalog/

  __Response__:

     {
       "_links":{
          "self":{
             "href":"/api/v1/catalog/"
          },
          "feed":[
             {
                "href":"http://10.36.0.17:8080/api/v1/feed/local",
                "name":"Feed generated from local bundles."
             },
             {
                "href":"http://10.2.12.27:8080/build/catalog-bundles/external-epic/feed/feed-centos-debug.json.nas3",
                "name":"Official BlueData EPIC Catalog"
             },
             {
                "href":"http://10.2.12.27:8080/build/catalog-bundles/internal-epic/feed/feed-centos-debug.json.nas3",
                "name":"     Internal BlueData EPIC catalog"
             }
          ]
       },
       "catalog_api_version":2,
       "feeds_refresh_period_seconds":86400,
       "feeds_read_counter":124,
       "catalog_write_counter":124,
       "_embedded":{
          "independent_catalog_entries":[
             {
                "_links":{
                   "self":{
                      "href":"/api/v1/catalog/1"
                   }
                }
             }......



## 3. Retrieve available tenants

  __API-URI__: /api/v1/tenant

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<Session-ID>" http://<controller-ip>:8080/api/v1/tenant

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/tenant

  __Response__:

      {
        "_links":{
          "self":{
            "href":"/api/v1/tenant"
          }
        },
        "_embedded":{
          "tenants":[{
            "_links":{
              "self":{
                "href":"/api/v1/tenant/2"
                }
              },
            "label":{
              "name":"Demo Tenant",
              "description":"Demo Tenant for BlueData Clusters"
              },
            "member_key_available":"all_admins",
            "status":"ready",
            "tenant_type":"docker",
            "qos_multiplier":1,
            "quota":{},
            "inusequota":{
              "cores":44,
              "memory":102400,
              "disk":552960
            },
            "tenant_storage_quota_supported":true,
            "external_user_groups":[]
          },
          {
            "_links":{
              "self":{
                "href":"/api/v1/tenant/1"
                }
              },
            "label":{
              "name":"Site Admin",
              "description":"Site Admin Tenant for BlueData clusters"
              },
            "member_key_available":"all_admins",
            "status":"ready"
          }



## 4. Retrieve tenant information such as resources, security, and other settings

  __API-URI__: /api/v1/tenant/{tenant-id}

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/tenant/<tenant-id>

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/tenant/3

  __Response__:

      {
        "_links":
        {
          "self":{
            "href":"/api/v1/tenant/3"
            },
          "all_tenants":{
            "href":"/api/v1/tenant"
            }
          },
        "label":{
          "name":"Active Directory",
          "description":"All clusters with AD integration"
          },
        "member_key_available":"all_admins",
        "status":"ready",
        "tenant_type":"docker",
        "qos_multiplier":1,
        "quota":{
          "cores":15,
          "memory":47104,
          "disk":561152,
          "tenant_storage":582
        },
        "inusequota":{
          "cores":4,
          "memory":8192,
          "disk":30720
        },
        "tenant_storage_quota_supported":true,
        "external_user_groups":
        [{
          "group":"CN=Eng,OU=Engineering,DC=BLUEDATA, DC=local",
          "role":"/api/v1/role/2"
        }],
        "kdc_type":"Active Directory",
        "kdc_host":"10.2.12.106",
        "kdc_admin_user":"admin@BLUEDATA.LOCAL",
        "kdc_admin_password":"Layer42!",
        "kdc_realm":"BLUEDATA.LOCAL",
        "krb_enc_types":["rc4-hmac","aes256-cts-hmac-sha1-96","aes128-cts-hmac-sha1-96","des3-cbc-sha1","arcfour-hmac","des-hmac-sha1","des-cbc-md5"],
        "kdc_ad_prefix":"ActiveDir",
        "kdc_ad_suffix":"ou=Engineering,dc=BLUEDATA,dc=local"
      }


## 5. Retrieve tenant virtual clusters

  __API-URI__: /api/v1/cluster

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/cluster

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/cluster

  __Response__:

      {"result":"Success","objects":[{"result":"Success","uuid":"65","cluster_name":"Spark-Nifi-test","cluster_type":"Spark","distro_name":"Spark 1.6.0","distro_version":"1.8","distro_state":"installed","cluster_context":"Persistent","master_flavor":{"root_disk_size":100,"label":{"name":"Medium","description":"system-created example flavor"},"cores":4,"memory":12288},"slave_count":2,"slave_flavor":{"root_disk_size":30,"label":{"name":"Small","description":"system-created example flavor"},"cores":4,"memory":8192},"status_message":"","error_info":"","ha_enabled":false,"apps_installed":false,"include_spark_installation":false,"mr_type":"","kerberos_enabled":false,"log_url":"http://10.36.0.17:8080/Logs/65.txt","client_config_xml":"","client_config_java":"","status":"ready","tenant_id":"/api/v1/tenant/2","tenant_name":"Demo Tenant","tenant_type":"docker"}



## 6. Retrieve a virtual cluster configuration

  __API-URI__: /api/v1/cluster/<uuid>?nodelist

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/cluster/<uuid>?nodelist

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/cluster/10?nodelist

  __Response__:

      {
    "node_list": [
        {
            "container_name": "bluedata-127",
            "distro_name": "CentOS 6.x",
            "distro_state": "installed",
            "distro_version": "2.6",
            "flavor": {
                "cores": 4,
                "label": {
                    "description": "system-created example flavor",
                    "name": "Small"
                },
                "memory": 8192,
                "root_disk_size": 30
            },
            "id": "1be5b57587256e867e8c16239fc5e49b503b2dc5b1616a4b517f054d4de5a1f8",
            "in_use": true,
            "job_or_cluster": "KDC-EnableKeytabs",
            "name": "bluedata-127.bdlocal",
            "node_ip": "10.35.234.9",
            "nodegroup_id": "1",
            "persistent": true,
            "process_list": [
                {
                    "endpoint": "10.35.234.9:22",
                    "is_dashboard": false,
                    "name": "SSH"
                }
            ],
            "role": "controller",
            "root_disk_size": "30"
        }
    ],
    "result": "Success"}




## 7. Get created DataTap in a certain tenant

  __API-URI__: /api/v1/cluster/?nodelist

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/dataconn

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/dataconn

  __Response__:

      {"_links":{"self":{"href":"/api/v1/dataconn"}},"_embedded":{"data_connectors":[{"_links":{"self":{"href":"/api/v1/dataconn/1"},"query":{"href":"/api/v1/dataconn/1{?query}","templated":true}},"_embedded":{"label":{"_links":{"self":{"href":"/api/v1/dataconn/1?label"}},"name":"TenantStorage","description":"Protected DataTap for a tenant-specific sandboxed storage space."},"endpoint":{"_links":{"self":{"href":"/api/v1/dataconn/1?endpoint"}},"type":"hdfs","host":"yav-114.lab.bluedata.com","kdc_data":[{"host":"10.36.0.17","port":88}],"keytab":"datasrvr.headless.keytab","realm":"BLUEDATA.SITE","client_principal":"datasrvr/yav-114.lab.bluedata.com@BLUEDATA.SITE","service_id":"hdfs"},"bdfs_root":{"_links":{"self":{"href":"/api/v1/dataconn/1?bdfs_root"}},"path_from_endpoint":"/2/default"},"flags":{"_links":{"self":{"href":"/api/v1/dataconn/1?flags"}},"read_only":false},"is_protected":true}}]}}


## 8. Create a new cluster


  __API-URI__: /api/v1/cluster

  __Curl command__:

      curl -X POST -d@hadoop_cluster.json -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/cluster

  __API Type__: `POST`

  __Example__:

      curl -X POST -d@hadoop_cluster.json -H "X-BDS-SESSION:/api/v1/session/446468df-6869-4e42-bbba-c8cc11cb4a54" http://127.0.0.1:8080/api/v1/cluster

 __Json-file__: hadoop_cluster.json:

        {
            "ha_enabled":false,
            "cluster_name":"Hadoop test",
            "cluster_type":"Hadoop",
            "distro_name":"CDH 5.4.3 with Cloudera Manager",
            "master_flavor":"/api/v1/flavor/2",
            "slave_count":2,
            "slave_flavor":"/api/v1/flavor/2",
            "spark_installed":false,
            "apps_installed":true,
            "mr_type":"YARN",
        }

  __Response__:

      {"result":"Success","uuid":"216"}



## 9. Create a cluster with gateway node


  __API-URI__: /api/v1/cluster

  __Curl command__:

      curl -X POST -d@spark_cluster.json -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/cluster

  __API Type__: `POST`

  __Example__:

      curl -X POST -d@spark_cluster.json -H "X-BDS-SESSION:/api/v1/session/446468df-6869-4e42-bbba-c8cc11cb4a54" http://127.0.0.1:8080/api/v1/cluster

 __Json-file__: spark_cluster.json:

        {
    "cluster_name": "Spark-Test",
    "cluster_type": "Spark",
    "debug": true,
    "dependent_distros": [
        {
            "distro_name": "Spark 2.0.1 Gateway",
            "flavor": "/api/v1/flavor/4",
            "scaleout_count": 1
        }
    ],
    "distro_name": "Spark 2.0.1",
    "master_flavor": "/api/v1/flavor/7",
    "slave_count": 2,
    "slave_flavor": "/api/v1/flavor/4" }

  __Response__:

      {"result":"Success","uuid":"107"}


## 10. Create a cluster DataTap



  __API-URI__: /api/v1/dataconn

  __Curl command__:

      curl -X POST -d@datatap.json -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/dataconn

  __API Type__: `POST`

  __Example__:

      curl -X POST -d@datatap.json -H "X-BDS-SESSION: /api/v1/session/230fe122-da47-47ab-bcd7 3431efb69cae" http://127.0.0.1:8080/api/v1/dataconn

 __Json-file__: datatap.json:

        {
          "bdfs_root": {
                          "path_from_endpoint": "/tmp/nanda"
                       },
          "endpoint": {
                          "host": "bd-045.lab.bluedata.com",
                          "type": "hdfs",
                          "port": 8020
                      },
          "label":    {
                          "name": "StagingDataLake",
                          "description": "External Staging Datalake"
                      }
        }

  __Response__:

      201 Created


## 11. Enable virtual cluster Kerberos



  __API-URI__: /api/v1/tenant/{tenant-id}?tenant_kdc

  __Curl command__:

      curl -X PUT -d@kerberos.json -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/tenant/<tenant-id>?tenant_kdc

  __API Type__: `PUT`

  __Example__:

      curl -X PUT -d@kerberos.json -H "X-BDS-SESSION:/api/v1/session/021a76e2-083d-42b2-afb1-b7f1de2cb72e" http://10.36.0.17:8080/api/v1/tenant/5?tenant_kdc

 __Json-file__: kerberos.json:

        {
        "kdc_host": "10.12.102.16",
        "kdc_admin_password": "***",
        "krb_enc_types": ["rhmac-type"],
        "kdc_realm": "BLUEDATA.LOCAL",
        "kdc_admin_user": "admin@BLUEDATA.LOCAL",
        "kdc_type": "MIT KDC"
        }

  __Response__:

      None


## 12. Delete an existing cluster



  __API-URI__: /api/v1/cluster/{uuid}

  __Curl command__:

      curl -v -X DELETE -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/cluster/<uuid>

  __API Type__: `DELETE`

  __Example__:

      curl -v -X DELETE -H "X-BDS-SESSION: /api/v1/session/46f80cd5- 972d-41df-bcba-61c809b5470f" http://<IP_address>:8080/api/v1/cluster/72

  __Response__:

      {"result":"Success"}


## 13. Delete an existing DataTap



  __API-URI__: /api/v1/dataconn/{datatap-id}

  __Curl command__:

      curl -v -X DELETE -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/dataconn/<datatap-id>

  __API Type__: `DELETE`

  __Example__:

      curl -v -X DELETE -H "X-BDS-SESSION:/api/v1/session/6a917f50-776b-4eea-8eaf-f1be402c8ea1" http://10.36.0.17:8080/api/v1/dataconn/5

  __Response__:

      {"result":"Success"}


## 14. Create a new tenant



  __API-URI__: /api/v1/tenant

  __Curl command__:

      curl -X POST -d@tenant.json -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/tenant

  __API Type__: `POST`

  __Example__:

      curl –X POST –d@tenant.json -H "X-BDS-SESSION:/api/v1/session/6a917f50-776b-4eea-8eaf-f1be402c8ea1"http://10.36.0.17:8080/api/v1/tenant

 __Json-file__: tenant.json:

On_Prem:

        {
          "qos_multiplier": 1,
          "member_key_available": "all_admins",
          "tenant_type": "docker",
          "quota":
              {"cores": 15,
              "disk": 561152,
              "tenant_storage": 582,
              "memory": 47104},
              "label":
                  {"name": "Marketing",
                  "description": "Marketing related clusters"
                }
              }
        }

AWS:

        {
        "aws_secret_key": "<Enter AWS Secret Key>",
        "aws_subnet_id": "<Enter your Subnet ID>",     
        "tenant_type": "ec2",
        "aws_access_key": "<Enter AWS Access Key",     
        "member_key_available": "all_admins",
        "aws_region": "<Enter AWS Region>",
        "quota": {
              "tenant_storage": 582,
                  }          
        "label": {
              "name": "<Enter Tenant Name>",
              "description": "<Enter Tenant Description>"
                  }  
        "aws_iam_instance_profile": "<Enter IAM name>"
        }    




  __Response__:

      201 Created


## 15. Assign groups to a tenant



  __API-URI__: /api/v1/tenant/{tenant-id}?external_user_groups

  __Curl command__:

      curl -X PUT -d@groups.json -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/tenant/<tenant-id>?external_user_groups

  __API Type__: `PUT`

  __Example__:

      curl -X PUT -d@groups.json -H "X-BDS-SESSION:/api/v1/session/021a76e2-083d-42b2-afb1-b7f1de2cb72e" http://10.36.0.17:8080/api/v1/tenant/5?external_user_groups

 __Json-file__: groups.json:

        {
           "external_user_groups": [
              {
                "role": "/api/v1/role/3",
                "group": "OU=Eng,DC=Bluedata,DC=local"
              }
              ]
        }


  __Response__:

      None


## 16. Create a new user


  __API-URI__: /api/v1/user

  __Curl command__:

      curl -X POST -d@user.json -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/user

  __API Type__: `POST`

  __Example__:

      curl –X POST –d@user.json -H "X-BDS-SESSION:/api/v1/session/6a917f50-776b-4eea-8eaf-f1be402c8ea1" http://10.36.0.17:8080/api/v1/user

 __Json-file__: user.json:

        {
           "password":"*******",
           "is_external":true,
           "label":{
                      "name":"admin",
                      "description":""
                   }
        }


  __Response__:

      201 Created


## 17. Delete an existing user



  __API-URI__: /api/v1/user/{user-id}

  __Curl command__:

      curl -v -X DELETE -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/user/<user-id>

  __API Type__: `DELETE`

  __Example__:

      curl -v -X DELETE -H "X-BDS-SESSION:/api/v1/session/6a917f50-776b-4eea-8eaf-f1be402c8ea1" http://10.36.0.17:8080/api/v1/user/631

  __Response__:

      About to connect() to 10.36.0.17 port 8080 (#0)* Trying 10.36.0.17... connected* Connected to 10.36.0.17 (10.36.0.17) port 8080 (#0) DELETE /api/v1/user/631 HTTP/1.1 User-Agent: curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.21 Basic ECC zlib/1.2.3 libidn/1.18 libssh2/1.4.2 Host: 10.36.0.17:8080 Accept: */* X-BDS-<SESSION:/api/v1/session/0cd0f847-1169-4d82-bb45-ed0d9c0dd45c> <HTTP/1.1 204 No Content < Server: BlueData EPIC 2.6 < Date: Thu, 25 May 2017 22:50:33 GMT < Content-Length: 0 <* Connection #0 to host 10.36.0.17 left intact* Closing connection #0



## 18. Delete an existing tenant



  __API-URI__: /api/v1/tenant/{tenant-id}

  __Curl command__:

      curl -v -X DELETE -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/tenant/<tenant-id>

  __API Type__: `DELETE`

  __Example__:

      curl -v -X DELETE -H "X-BDS-SESSION: /api/v1/session/46f80cd5- 972d-41df-bcba-61c809b5470f" http://<IP_address>:8080/api/v1/tenant/10

  __Response__:

      About to connect() to 10.36.0.17 port 8080 (#0)* Trying 10.36.0.17... connected* Connected to 10.36.0.17 (10.36.0.17) port 8080 (#0) DELETE /api/v1/user/631 HTTP/1.1 User-Agent: curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.21 Basic ECC zlib/1.2.3 libidn/1.18 libssh2/1.4.2 Host: 10.36.0.17:8080 Accept: */* X-BDS-<SESSION:/api/v1/session/0cd0f847-1169-4d82-bb45-ed0d9c0dd45c> <HTTP/1.1 204 No Content < Server: BlueData EPIC 2.6 < Date: Thu, 25 May 2017 22:50:33 GMT < Content-Length: 0 <* Connection #0 to host 10.36.0.17 left intact* Closing connection #0



## 19. Assign security roles to a tenant



  __API-URI__:  /api/v1/session/{session-id}?tenant

  __Curl command__:

      curl -X PUT -d@role_tenant.json -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080<session-id>?tenant

  __API Type__: `PUT`

  __Example__:

      curl -X PUT -d@role_tenant.json -H "X-BDS-SESSION:/api/v1/session/021a76e2-083d-42b2-afb1-b7f1de2cb72e" http://10.36.0.17:8080/api/v1/session/021a76e2-083d-42b2-afb1-b7f1de2cb72e?tenant

  __Json-file__: role_tenant.json:

        {
           "role": "/api/v1/role/2"
           "tenant": "/api/v1/tenant/3"
        }


  __Response__:

      201 Created




## 20. Submit a job to persistent cluster



  __API-URI__:  /api/v1/job

  __Curl command__:

      curl -X POST -d@job.json -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/job

  __API Type__: `POST`

  __Example__:

     curl -X POST -d@job.json -H "X-BDS-SESSION:/api/v1/session/20aa30d4-dc0e-478e-998a-9f264051eae5" http://10.36.0.17:8080/api/v1/job

  __Json-file__: job.json:

        {
          "spark_command_line": " ", "app_name": "wordcount", "jar_path": "/srv/bluedata/job-a1226be7083d6f4704febdb273023251/jar/hdp-examples.jar", "job_type": "Hadoop Custom Jar", "command_line": "hadoop jar  $jar_path$ $app_name$ dtap://TenantStorage/test/sahithi/customer_demographics.csvdtap://TenantStorage/test/out1", "dependencies": [], "cluster_context": "Persistent", "cluster_uuid": "78", "job_name": "WC-Test"
        }


  __Response__:

      {"result":"Success","uuid":"85"}



## 21. Submit a job to Transient cluster



  __API-URI__:  /api/v1/job

  __Curl command__:

      curl -X POST -d@transient-job.json -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/job

  __API Type__: `POST`

  __Example__:

     curl -X POST -d@transient-job.json -H "X-BDS-SESSION:/api/v1/session/20aa30d4-dc0e-478e-998a-9f264051eae5" http://10.36.0.17:8080/api/v1/job

  __Json-file__: transient-job.json:

        {
            "spark_command_line": " ",
            "app_name": "wordcount",
            "jar_path": "/srv/bluedata/job-0fbce6df8aa1feba2d0a9c7ee2e43d41/jar/hdp-examples.jar", "master_flavor": "/api/v1/flavor/2",
            "job_type": "Hadoop Custom Jar",
            "command_line": "hadoop jar  $jar_path$ $app_name$ dtap://TenantStorage/test/sahithi/customer_demographics.csv dtap://TenantStorage/test/TransientOutput",
            "slave_count": 1,
            "dependencies": [],
            "cluster_context": "Transient",
            "distro_name": "HDP 2.5 with Ambari 2.4",
            "slave_flavor": "/api/v1/flavor/1",
            "job_name": "Test-transient"
        }


  __Response__:

      {"result":"Success","uuid":"93"}



## 22. Retrieve list of all jobs



  __API-URI__: /api/v1/job

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/job

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/job

  __Response__:

      {"result":"Success","objects":[{"result":"Success","uuid":"92","job_name":"WC-transient","job_type":"Hadoop Custom Jar","jar_path":"/srv/bluedata/job-0fbce6df8aa1feba2d0a9c7ee2e43d41/jar/hdp-examples.jar","app_name":"wordcount","mapper":"","reducer":"","status":"complete","setup_time":482076,"run_time":35069,"cluster_context":"Transient","cluster_id":"92","update_ts":1496436965,"command_line":"hadoop jar  $jar_path$ $app_name$ dtap://TenantStorage/test/sahithi/customer_demographics.csv dtap://TenantStorage/test/TransOutput","status_message":"","error_info":"","start_time":1496436448,"duration":517,"spark_confs":" ","dependencies":[],"log_url":"http://10.36.0.17:8080/Logs/92.txt","output_url":"http://10.36.0.17:8080/Output/92.txt","cluster_name":"","distro_name":"HDP 2.5 with Ambari 2.4","distro_version":"2.0","distro_state":"installed","mr_type":"YARN","slave_count":1,"master_flavor":{"root_disk_size":100,"label":{"name":"Medium","description":"system-created example flavor"},"cores":4,"memory":12288},"slave_flavor":{"root_disk_size":30,"label":{"name":"Small","description":"system-created example flavor"},"cores":4,"memory":8192}},{"result":"Success","uuid":"26","job_name":"Spark2.1-Test","job_type":"Spark - Scala Jar","jar_path":"/srv/bluedata/job-b52132b15c5d1957d64d875432f16bb7/jar/spark-terasort-1.0.jar","app_name":"com.github.ehiggs.spark.terasort.TeraGen","mapper":"","reducer":"","status":"complete","setup_time":0,"run_time":5085,"cluster_context":"Persistent","cluster_id":"10","update_ts":1492623327,"command_line":"","status_message":"","error_info":"","start_time":1492623321,"duration":6,"spark_confs":" ","dependencies":["/srv/bluedata/job-b52132b15c5d1957d64d875432f16bb7/jar/spark-terasort-1.0-jar-with-dependencies.jar"],"log_url":"","output_url":"http://10.36.0.17:8080/Output/26.txt","cluster_name":"","distro_name":"Spark 2.1.0 Hadoop 2.7 Centos 7","distro_version":"1.0","distro_state":"installed","mr_type":""},{"result":"Success","uuid":"90","job_name":"test","job_type":"Hadoop Custom Jar","jar_path":"/srv/bluedata/job-098f6bcd4621d373cade4e832627b4f6/jar/hdp-examples.jar","app_name":"wordcount","mapper":"","reducer":"","status":"complete","setup_time":0,"run_time":35062,"cluster_context":"Persistent","cluster_id":"78","update_ts":1496432346,"command_line":"hadoop jar  $jar_path$ $app_name$ dtap://TenantStorage/test/sahithi/customer_demographics.csv dtap://TenantStorage/test/out1","status_message":"","error_info":"","start_time":1496432311,"duration":35,"spark_confs":" ","dependencies":[],"log_url":"","output_url":"http://10.36.0.17:8080/Output/90.txt","cluster_name":"HDP2.6+Nifi","distro_name":"HDP 2.6 with Ambari 2.5","distro_version":"1.1","distro_state":"installed","mr_type":"YARN"},{"result":"Success","uuid":"19","job_name":"Spark-terasorTest","job_type":"Spark - Scala Jar","jar_path":"/srv/bluedata/job-3e87223a71fcc06f42bfe0cdb79dd86f/jar/spark-terasort-1.0.jar","app_name":"com.github.ehiggs.spark.terasort.TeraGen","mapper":"","reducer":"","status":"complete","setup_time":0,"run_time":5055,"cluster_context":"Persistent","cluster_id":"10","update_ts":1492204942,"command_line":"","status_message":"","error_info":"","start_time":1492204936,"duration":6,"spark_confs":" ","dependencies":["/srv/bluedata/job-3e87223a71fcc06f42bfe0cdb79dd86f/jar/spark-terasort-1.0-jar-with-dependencies.jar"],"log_url":"","output_url":"http://10.36.0.17:8080/Output/19.txt","cluster_name":"","distro_name":"Spark 2.1.0 Hadoop 2.7 Centos 7","distro_version":"1.0","distro_state":"installed","mr_type":""}]}



## 23. Assign a user to tenant



  __API-URI__: /api/v1/tenant/{tenant-id}?user

  __Curl command__:

      curl -X PUT -d@assign_user.json -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/tenant/<tenant-id>?user

  __API Type__: `PUT`

  __Example__:

      curl -X PUT -d@assign_user.json -H "X-BDS-SESSION:/api/v1/session/021a76e2-083d-42b2-afb1-b7f1de2cb72e" http://10.36.0.17:8080/api/v1/tenant/3?user

 __Json-file__: groups.json:

        {
           "operation": "assign",
           "role": "/api/v1/role/3",
           "user": "/api/v1/user/261"
        }


  __Response__:

      None



## 24. Get Tenant info for a user



  __API-URI__: /api/v1/user/{UserObj}?tenant

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/user/<UserObj>?tenant

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/user/263?tenant

  __Response__:

      {"_links":{"self":{"href":"/api/v1/user/263?tenant"}},"_embedded":{"tenants":[{"_links":{"self":{"href":"/api/v1/tenant/2"}},"_embedded":{"label":{"name":"Demo Tenant","description":"Demo Tenant for BlueData Clusters"},"role":"/api/v1/role/3"}}]}}





## 25. Get user info for a tenant



  __API-URI__: /api/v1/tenant/{tenant-id}?user

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/tenant/<tenant-id>?user

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/tenant/2?user

  __Response__:

      {"_links":{"self":{"href":"/api/v1/tenant/2?user"}},"_embedded":{"users":[{"_links":{"self":{"href":"/api/v1/user/263"}},"_embedded":{"label":{"name":"demo.user","description":"BlueData Anonymous User"},"role":"/api/v1/role/3"}},{"_links":{"self":{"href":"/api/v1/user/257"}},"_embedded":{"label":{"name":"admin","description":"BlueData Administrator"},"role":"/api/v1/role/2"}}]}}





## 26. Reset User Password


  __API-URI__: /api/v1/user/{user-id}?password

  __Curl command__:

      curl -X PUT -d@password_reset.json -H "X-BDS-SESSION:<session-id> http://<controller-ip>:8080/api/v1/user/<user-id>?password

  __API Type__: `PUT`

  __Example__:

      curl -X PUT -d@password_reset.json -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/user/257?password


 __Json-file__: password_.json:

        {
           "password": "*****",
           "new_password": "<enter new password>"
        }


  __Response__:

      {"result":"Success"}



## 27. Reboot Virtual Node


  __API-URI__: /api/v1/user/{user-id}?password

  __Curl command__:

      curl -X PUT -d@password_reset.json -H "X-BDS-SESSION:<session-id> http://<controller-ip>:8080/api/v1/user/<user-id>?password

  __API Type__: `PUT`

  __Example__:

      curl -X PUT -d@password_reset.json -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/user/257?password


 __Json-file__: password_.json:

        {
           "password": "*****",
           "new_password": "<enter new password>"
        }


  __Response__:

      {"result":"Success"}



## 28. Reboot Virtual Cluster


  __API-URI__: /api/v1/cluster/{cluster-id}

  __Curl command__:

      curl -X PUT -d@reboot_cluster.json -H "X-BDS-SESSION:<session-id> http://<controller-ip>:8080/api/v1/cluster/<cluster-id>

  __API Type__: `PUT`

  __Example__:

      curl -X PUT -d@reboot_cluster.json -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/cluster/70

  __Json-file__: reboot_cluster.json:

        {
           "operation": "reboot"
        }

  __Response__:

      {"result":"Success"}



## 29. Stop a Virtual Cluster


  __API-URI__: /api/v1/cluster/{cluster-id}

  __Curl command__:

      curl -X PUT -d@stop_cluster.json -H "X-BDS-SESSION:<session-id> http://<controller-ip>:8080/api/v1/cluster/<cluster-id>

  __API Type__: `PUT`

  __Example__:

      curl -X PUT -d@stop_cluster.json -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/cluster/70

  __Json-file__: stop_cluster.json:

        {
           "operation": "stop"
        }

  __Response__:

      {"result":"Success"}



## 30. Start a Virtual Cluster


  __API-URI__: /api/v1/cluster/{cluster-id}

  __Curl command__:

      curl -X PUT -d@start_cluster.json -H "X-BDS-SESSION:<session-id> http://<controller-ip>:8080/api/v1/cluster/<cluster-id>

  __API Type__: `PUT`

  __Example__:

      curl -X PUT -d@start_cluster.json -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/cluster/70

  __Json-file__: start_cluster.json:

        {
           "operation": "start"
        }

  __Response__:

      {"result":"Success"}




## 31. Revoke User Access to a Tenant


  __API-URI__: /api/v1/tenant/{tenant-id}?user

  __Curl command__:

      curl -X PUT -d@revoke_user.json -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/tenant/<tenant-id>?user

  __API Type__: `PUT`

  __Example__:

      curl -X PUT -d@revoke_user.json -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/tenant/3?user

  __Json-file__: revoke_user.json:

        {
            "operation": "revoke",
            "role": "api/v1/role/<role-id>"
            "user": "api/v1/user/<user-id>"
        }

  __Response__:

      {"result":"Success"}




## 32. Retrieve a List of All Virtual Nodes


  __API-URI__: /api/v1/virtnode/

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/virtnode/

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/virtnode/

  __Response__:

      [{"id":"bdae6652204c4c66ebbec33a213d1bf69565a1da38a8a9505e06d25a399fbcd8","name":"bluedata-70.bdlocal","flavor":{"root_disk_size":30,"label":{"name":"Small","description":"system-created example flavor"},"cores":4,"memory":8192},"root_disk_size":"30","nodegroup_id":"1","distro_name":"Rstudio-Server with shiny-server on AWS","distro_version":"5.0","distro_state":"installed","in_use":true,"persistent":true,"job_or_cluster":"Rstudio","hypervisor_host":"yav-204.lab.bluedata.com","node_ip":"10.39.252.11","tenant_name":"SalesAnalytics","tenant_type":"docker"},{"id":"d5c650eb473ac81abb21147fb8459938f1c78586661829ed60b850af98443c36","name":"bluedata-138.bdlocal","flavor":{"root_disk_size":30,"label":{"name":"Small","description":"system-created example flavor"},"cores":4,"memory":8192},"root_disk_size":"30","nodegroup_id":"1","distro_name":"HDP 2.6 with Ambari 2.5","distro_version":"1.1","distro_state":"installed","in_use":true,"persistent":true,"job_or_cluster":"HDP2.6+Nifi","hypervisor_host":"yav-114.lab.bluedata.com","node_ip":"10.39.252.8","tenant_name":"Demo Tenant","tenant_type":"docker"}



## 33. Delete a job


  __API-URI__: /api/v1/job/{job-id}

  __Curl command__:

      curl -v -X DELETE -H "X-BDS-SESSION:<session-id> http://<controller-ip>:8080/api/v1/job/<job-id>

  __API Type__: `DELETE`

  __Example__:

      curl -v -X DELETE -H "X-BDS-SESSION:/api/v1/session/985585be-685d-4a6a-a0f0-0c563ae32e56" http://10.36.0.17:8080/api/v1/job/2

  __Response__:

      None



## 34. Invoke ActionScript


  __API-URI__: /api/v2/cluster/{cluster-id}/action_task

  __Curl command__:

      curl -X POST http://<controller-ip>:8080/api/v2/cluster/<cluster-id>/action_task -H 'cache-control:no-cache' -H 'content-type: application/json' -H 'x-bds-session:<session-id>' -d@Spark_submit.json

  __API Type__: `POST`

  __Example__:

      curl -X POST http://10.36.0.27:8080/api/v2/cluster/8/action_task -H 'cache-control:no-cache' -H 'content-type: application/json' -H 'x-bds-session:/api/v1/session/9b4e6dea-158e-484d-ad64-916cb738563c' -d@Spark_submit.json

 __Json-file__: Spark_submit.json:

        {
    "action_args": "",
    "action_as_root": "true",
    "action_cluster": "8",
    "action_cmd": "#/bin/bash\nexport node=`bdvcli --get node.role_id`\nif [[ $node == \"controller\" ]]; then\n    /usr/lib/spark/spark-2.1.1-bin-hadoop2.7/bin/spark-submit --class org.apache.spark.examples.SparkPi --master spark://bluedata-4.bdlocal:7077 /usr/lib/spark/spark-2.1.1-bin-hadoop2.7/examples/jars/spark-examples_2.11-2.1.1.jar 100\nfi",
    "action_name": "Spark-submit_ActionSource_spark_submit_job.sh",
    "action_nodegroupid": "1",
    "action_user": "admin" }


  __Response__:

      {"result":"Success","uuid":"action_170"}





## 35. Update the hue.ini safety valve to point to datatap


  __API-URI__: /api/v2/cluster/{cluster-id}/action_task

  __Curl command__:

      curl -X POST http://<controller-ip>:8080/api/v2/cluster/<cluster-id>/action_task -H 'cache-control:no-cache' -H 'content-type: application/json' -H 'x-bds-session:<session-id>' -d@hue_ini_dtap.json

  __API Type__: `POST`

  __Example__:

      curl -X POST http://10.36.0.27:8080/api/v2/cluster/132/action_task -H 'cache-control:no-cache' -H 'content-type: application/json' -H 'x-bds-session:/api/v1/session/9b4e6dea-158e-484d-ad64-916cb738563c' -d@hue_ini_dtap.json

 __Json-file__: hue_ini_dtap.json:

        {
          "action_args": "",
          "action_as_root": "true",
          "action_cluster": "132",
          "action_cmd": "#/bin/bash\n\nexport PASSWORD=admin\nexport VAL=dtap://TenantStorage\nsed -i \"s/^\\(fs\\_defaultfs\\s*=\\s*\\).*\\$/\\1$VAL/\" /etc/hue/conf/hue.ini\ncurl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/HUE/commands/restart'\n",
          "action_name": "hue-test_ActionSource_hue_Property_replace.sh",
          "action_nodegroupid": "1",
          "action_user": "admin"
        }

  __Response__:

      {"result":"Success","uuid":"action_166"}




## 36. Mount dtap to Virtual cluster ActionScript


  __API-URI__: /api/v2/cluster/{cluster-id}/action_task

  __Curl command__:

      curl -X POST http://<controller-ip>:8080/api/v2/cluster/<cluster-id>/action_task -H 'cache-control:no-cache' -H 'content-type: application/json' -H 'x-bds-session:<session-id>' -d@fs_defaultFS_dtap.json

  __API Type__: `POST`

  __Example__:

      curl -X POST http://10.36.0.27:8080/api/v2/cluster/132/action_task -H 'cache-control:no-cache' -H 'content-type: application/json' -H 'x-bds-session:/api/v1/session/9b4e6dea-158e-484d-ad64-916cb738563c' -d@fs_defaultFS_dtap.json

 __Json-file__: fs_defaultFS_dtap.json:

        {
            "action_args": "",
            "action_as_root": "true",
            "action_cluster": "132",
            "action_cmd": "#/bin/bash\n\nexport node=`bdvcli --get node.role_id`\nexport PASSWORD=admin\nexport CLUSTER_NAME=CDH5.10.1\n#export CMHOST=10.39.250.14\n#export CMPORT=7180\n#export SERVICE=YARN\n#export BASEURL=http://$CMHOST:$CMPORT\n\nif [[ $node == \"controller\" ]]; then\n\t\n\tcurl -iv -X PUT -H \"Content-Type:application/json\" -H \"Accept:application/json\" -d '{\"items\":[{ \"name\": \"yarn_core_site_safety_valve\",\"value\":\"<property><name>fs.defaultFS</name><value>dtap://TenantStorage</value></property>\"}]}' http://admin:admin@10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/YARN/config\n\tcurl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/HIVE/commands/restart'\n\tcurl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/HUE/commands/restart'\n\tcurl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/OOZIE/commands/restart'\n\tcurl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/SQOOP/commands/restart'\n\tcurl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/YARN/commands/restart'\n\techo -n Restarting All services...\nfi\n",
            "action_name": "final-dtapMount_ActionSource_cdh_defaultFS.sh",
            "action_nodegroupid": "1",
            "action_user": "admin"}


  __Response__:

      {"result":"Success","uuid":"action_170"}


## 37. Switch Tenant

  __API-URI__: /api/v1/tenant

  __Curl command__:

      curl -X PUT -d@switch_tenant.json -H "X-BDS-SESSION:<Session-ID>" http://<Controller-ID>:8080/api/v1/session/<session-id>?tenant

  __API Type__: `PUT`

  __Example__:

      curl -X PUT -d@switch_tenant.json -H "X-BDS-SESSION:/api/v1/session/2b7066ae-4ce2-49be-8294-d16b028a7657" http://10.36.0.17:8080/api/v1/session/2b7066ae-4ce2-49be-8294-d16b028a7657?tenant

 __Json-file__: switch_tenant.json:

           {"role": "/api/v1/role/1",
           "tenant": "/api/v1/tenant/2"}


  __Response__:

      None


## 38. Verify current session role and tenant:

  __API-URI__: /api/v1/session/{session-id}

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<Session-ID>" http://<controller-ip>:8080/api/v1/session/<session-id>

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/930dd6cc-57ef-4bb2-aa24-23a17744fe14" http://10.36.0.17:8080/api/v1/session/930dd6cc-57ef-4bb2-aa24-23a17744fe14

  __Response__:

    {"_links":{"self":{"href":"/api/v1/session/930dd6cc-57ef-4bb2-aa24-23a17744fe14"},"all_sessions":{"href":"/api/v1/session"}},"user":"/api/v1/user/257","tenant":"/api/v1/tenant/1","role":"/api/v1/role/1","expiry":"2017-7-14 11:22:29"}


## 39. Invoke ActionScript from dtap


  __API-URI__: /api/v2/cluster/{cluster-id}/action_task

  __Curl command__:

      curl -X POST http://<controller-ip>:8080/api/v2/cluster/<cluster-id>/action_task -H 'cache-control:no-cache' -H 'content-type: application/json' -H 'x-bds-session:<session-id>' -d@Spark_submit_dtap.json

  __API Type__: `POST`

  __Example__:

      curl -X POST http://10.36.0.27:8080/api/v2/cluster/8/action_task -H 'cache-control:no-cache' -H 'content-type: application/json' -H 'x-bds-session:/api/v1/session/78486fbe-be9c-49aa-8c72-1fef74191fc5' -d@Spark_submit_dtap.json


 __Json-file__: Spark_submit_dtap.json:

        {
    "action_args": "",
    "action_as_root": "true",
    "action_cluster": "8",
    "action_cmd": "hadoop fs -get dtap://TenantStorage/tmp/sample-scripts/spark_submit_job.sh /tmp/\n   chmod a+x /tmp/spark_submit_job.sh\n   /tmp/spark_submit_job.sh\n   rm /tmp/spark_submit_job.sh",
    "action_name": "Testdtap_ActionSource_Typed script commands",
    "action_nodegroupid": "1",
    "action_user": "admin"}



  __Response__:

      {"result":"Success","uuid":"action_316"}


## 40. Install catalog Image


  __API-URI__: /api/v1/catalog/{catalog-id}

  __NOTE__:

      Inorder to get catalog_id, run API#2


  __Curl command__:

      curl -X POST -d@install_image.json -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v1/catalog/<catalog_id>

  __API Type__: `POST`

  __Example__:

     curl -X POST -d@install_image.json -H "X-BDS-SESSION:/api/v1/session/3705cffd-de19-4a75-80a7-05797ab071d7" http://10.32.1.116:8080/api/v1/catalog/50


 __Json-file__: install_image.json:

        {
          "action" : "install"
    }



  __Response__:

      None

## 41. Get a tenant keypair file

  __API-URI__: /api/v1/tenant/<tenant-id>?privatekey

  __NOTE__:

      Inorder to get tenant_id, run API#3


  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-ID>" http://<controller-IP>:8080/api/v1/tenant/<tenant-id>?privatekey


  __API Type__: `GET`

  __Example__:

     curl -X GET -H "X-BDS-SESSION:/api/v1/session/7f27a1a9-5354-486f-ba44-f414e4f144b7" http://10.36.0.17:8080/api/v1/tenant/3?privatekey


  __Response__:

    {"private_key":"-----BEGIN RSA PRIVATE KEY-----\nMIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgH/YVs/NDEnVyVPKOgo0ShTjsg6u CaCYJL7tNcTR8EEMZmUHYy7Bd3Et8P5CZBK0GsJL/Phl2OAIXXZ60u4tTIVU8Jpf h2VquBSm4wNoXXL9W0tfjpGx7H97BnuUy1Q6PNqUDjTm1lixqq/4am9we/JTCb2L 
    lyKPlEhupS8kequ1AgMBAAE=\n-----END RSA PRIVATE KEY-----\n"}


</span>
