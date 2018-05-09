<span style="color:#f2cf4a; font-family: 'Bookman Old Style';">

# REST APIs

__Note__:

  - For Epic3.2 and later you can find v2 API docs for a given EPIC installation by connecting to the "/apidocs" path on your controller host machine "http://{controller-IP}:8080/apidocs".

  - For more info on difference between v1 and v2 APIs, please refer to v1_vs_v2_apidocs.pdf in the same location.

  - The samples below are for v2 APIs but for more detail info please check the docs under "http://{controller-IP}:8080/apidocs".

  - Inorder to login and create a session and to switch to a non-siteadmin role/tenant, you will use the v1 APIs (Refer to v1_bluedata_apis_doc for the exact commands). For now you will use a combination of v1 and v2 APIs incase you choose to run the samples below.


  - [0. Fetch a session](#0-fetch-a-session)
  - [1. Retrieve all tenants](#1-retrieve-all-tenants)
  - [2. Retrieve a specific tenant](#2-retrieve-a-specific-tenant)
  - [3. Retrieve all clusters](#3-retrieve-all-clusters)
  - [4. Retrieve a specific virtual cluster](#4-retrieve-a-specific-virtual-cluster)
  - [5. Create a new cluster](#5-create-a-new-cluster)
  - [6. Retrieve cluster nodes](#6-retrieve-cluster-nodes)
  - [7. Retrieve tenant filesystem information](#7-retrieve-tenant-filesystem-information)
  - [8. Retrieve Epic platform configuration](#8-retrieve-epic-platform-configuration)
  - [9. Invoke ActionScript](#9-invoke-actionscript)
  - [10. Update the hue.ini safety valve to point to datatap](#10-update-the-hue.ini-safety-valve-to-point-to-datatap)
  - [11. Mount dtap to Virtual cluster ActionScript](#11-mount-dtap-to-virtual-cluster-actionscript)
  - [12. Invoke ActionScript from dtap](#12-invoke-actionscript-from-dtap)
  - [13. Retrieve public & private endpoints for cluster services](#13-retrieve-public-&-private-endpoints-for-cluster-services)



## 0. Fetch a session

  __API-URI__: /api/v2/session/{session-id}

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v2/session/{session-id}

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/b584b109-318c-4aa9-b704-21fab6c44e07" http://10.36.0.17:8080/api/v2/session/b584b109-318c-4aa9-b704-21fab6c44e07

  __Response__:

       % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
    100   382  100   382    0     0  48440      0 --:--:-- --:--:-- --:--:-- 54571
      {
         "_links": {
                "all_sessions": {
                    "href": "/api/v2/session"
                },
                "self": {
                    "href": "/api/v2/session/bf27e7b7-c2bc-4e49-8a0a-23b1246c2cad"
                }
            },
            "expiry": "2018-5-8 10:55:59",
            "expiry_time": 1525802159,
            "is_cluster_superuser": true,
            "is_site_admin_view": false,
            "role": "/api/v1/role/1",
            "role_name": "Site Admin",
            "tenant": "/api/v1/tenant/1",
            "tenant_name": "Site Admin",
            "user": "/api/v1/user/4",
            "user_name": "admin"
        }

## 1. Retrieve all tenants

  __API-URI__: /api/v2/tenant

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v2/tenant

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/b584b109-318c-4aa9-b704-21fab6c44e07" http://10.36.0.17:8080/api/v2/tenant

  __Response__:

        % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
    100   432  100   432    0     0  40498      0 --:--:-- --:--:-- --:--:-- 43200
    {
        "_embedded": {
            "tenants": [
                {
                    "_links": {
                        "self": {
                            "href": "/api/v2/tenant/1"
                        }
                    },
                    "label": {
                        "description": "Site Admin Tenant for BlueData clusters",
                        "name": "Site Admin"
                    }
                },
                {
                    "_links": {
                        "self": {
                            "href": "/api/v2/tenant/3"
                        }
                    },
                    "label": {
                        "description": "Test",
                        "name": "Analytics"
                    }
                },
                {
                    "_links": {
                        "self": {
                            "href": "/api/v2/tenant/2"
                        }
                    },
                    "label": {
                        "description": "Demo Tenant for BlueData Clusters",
                        "name": "Demo Tenant"
                    }
                }
            ]
        },
        "_links": {
            "self": {
                "href": "/api/v2/tenant"
            }
        }
    }

## 2. Retrieve a specific tenant

  __API-URI__: /api/v2/tenant/{tenant-id}

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v2/tenant/{tenant-id}

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/b584b109-318c-4aa9-b704-21fab6c44e07" http://10.36.0.17:8080/api/v2/tenant/2

  __Response__:

        % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
          100   128  100   128    0     0  14263      0 --:--:-- --:--:-- --:--:-- 18285
          {
              "_links": {
                  "self": {
                      "href": "/api/v2/tenant/2"
                  }
              },
              "label": {
                  "description": "Demo Tenant for BlueData Clusters",
                  "name": "Demo Tenant"
              }
          }



## 3. Retrieve all clusters

  __API-URI__: /api/v2/cluster

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v2/cluster

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/b584b109-318c-4aa9-b704-21fab6c44e07" http://10.36.0.17:8080/api/v2/cluster

  __Response__:

      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
      100 10092  100 10092    0     0   347k      0 --:--:-- --:--:-- --:--:--  365k
      {
          "_embedded": {
              "clusters": [
                  {
                      "_links": {
                          "all_cluster_action_histories": {
                              "href": "/api/v2/cluster/33/action_history"
                          },
                          "all_cluster_action_tasks": {
                              "href": "/api/v2/cluster/33/action_task"
                          },
                          "all_cluster_change_histories": {
                              "href": "/api/v2/cluster/33/change_history"
                          },
                          "all_cluster_change_tasks": {
                              "href": "/api/v2/cluster/33/change_task"
                          },
                          "all_cluster_nodes": {
                              "href": "/api/v2/cluster/33/node"
                          },
                          "all_clusters": {
                              "href": "/api/v2/cluster"
                          },
                          "include_nodes": {
                              "href": "/api/v2/cluster/33?nodes"
                          },
                          "include_services": {
                              "href": "/api/v2/cluster/33?services"
                          },
                          "self": {
                              "href": "/api/v2/cluster/33"
                          },
                          "tenant": {
                              "href": "/api/v1/tenant/2",
                              "title": "Demo Tenant"
                          }
                      },
                      "created_by_user": "/api/v1/user/4",
                      "created_by_user_name": "admin",
                      "created_time": 1525308032,
                      "debug": true,
                      "error_info": "",
                      "isolated": false,
                      "label": {
                          "description": "cdh",
                          "name": "cdh5121-test"
                      },
                      "log_url": "http://10.36.0.27:8080/Logs/33.txt",
                      "nodegroup": {
                          "catalog_entry": "/api/v1/catalog/21",
                          "catalog_entry_distro_id": "bluedata/cdh5121multicr",
                          "catalog_entry_label": {
                              "description": "CDH 5.12.1 with YARN and HBase support. Includes Pig, Hive, Hue and Spark.",
                              "name": "CDH 5.12.1 multirole 6x"
                          },
                          "catalog_entry_state": "installed",
                          "catalog_entry_version": "2.6",
                          "config_choice_selections": [
                              {
                                  "choice_id": "kerberos",
                                  "selection_id": false
                              },
                              {
                                  "choice_id": "mrtype",
                                  "selection_id": "yarn"
                              },
                              {
                                  "choice_id": "hbase",
                                  "selection_id": false
                              },
                              {
                                  "choice_id": "yarn_ha",
                                  "selection_id": false
                              },
                              {
                                  "choice_id": "apps",
                                  "selection_id": true
                              },
                              {
                                  "choice_id": "spark",
                                  "selection_id": true
                              }
                          ],
                          "config_meta": {
                              "cdh_full_version": "5.12.1",
                              "cdh_major_version": "CDH5",
                              "cdh_parcel_repo": "http://archive.cloudera.com/cdh5/parcels/5.12.1",
                              "cdh_parcel_version": "5.12.1-1.cdh5.12.1.p0.3",
                              "impala_jar_version": "0.1-SNAPSHOT",
                              "streaming_jar": "/opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar"
                          },
                          "constraints": [],
                          "id": "1",
                          "role_configs": [
                              {
                                  "flavor": {
                                      "cores": 4,
                                      "gpus": 0,
                                      "label": {
                                          "description": "system-created example flavor",
                                          "name": "Small"
                                      },
                                      "memory": 8192,
                                      "root_disk_size": 30
                                  },
                                  "node_count": 1,
                                  "role_id": "cmserver",
                                  "selected": true
                              },
                              {
                                  "flavor": {
                                      "cores": 4,
                                      "gpus": 0,
                                      "label": {
                                          "description": "system-created example flavor",
                                          "name": "Medium"
                                      },
                                      "memory": 12288,
                                      "root_disk_size": 100
                                  },
                                  "node_count": 1,
                                  "role_id": "controller",
                                  "selected": true
                              },
                              {
                                  "flavor": {
                                      "cores": 4,
                                      "gpus": 0,
                                      "label": {
                                          "description": "system-created example flavor",
                                          "name": "Small"
                                      },
                                      "memory": 8192,
                                      "root_disk_size": 30
                                  },
                                  "node_count": 0,
                                  "role_id": "edge",
                                  "selected": true
                              },
                              {
                                  "flavor": {
                                      "cores": 4,
                                      "gpus": 0,
                                      "label": {
                                          "description": "system-created example flavor",
                                          "name": "Small"
                                      },
                                      "memory": 8192,
                                      "root_disk_size": 30
                                  },
                                  "node_count": 1,
                                  "role_id": "worker",
                                  "selected": true
                              }
                          ],
                          "status": "created"
                      },
                      "status": "ready",
                      "status_message": "",
                      "tenant_id": "/api/v1/tenant/2",
                      "tenant_name": "Demo Tenant",
                      "tenant_type": "docker",
                      "two_phase_delete": false
                  }, ....


## 4. Retrieve a specific virtual cluster

  __API-URI__: /api/v2/cluster/<cluster_id>

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v2/cluster/<cluster_id>

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/b584b109-318c-4aa9-b704-21fab6c44e07" http://10.36.0.17:8080/api/v2/cluster/33

  __Response__:

     {
    "_links": {
        "self": {
            "href": "/api/v2/cluster/33"
        },
        "all_cluster_nodes": {
            "href": "/api/v2/cluster/33/node"
        },
        "all_clusters": {
            "href": "/api/v2/cluster"
        },
        "all_cluster_change_tasks": {
            "href": "/api/v2/cluster/33/change_task"
        },
        "all_cluster_change_histories": {
            "href": "/api/v2/cluster/33/change_history"
        },
        "all_cluster_action_histories": {
            "href": "/api/v2/cluster/33/action_history"
        },
        "all_cluster_action_tasks": {
            "href": "/api/v2/cluster/33/action_task"
        },
        "tenant": {
            "href": "/api/v1/tenant/2",
            "title": "Demo Tenant"
        },
        "include_services": {
            "href": "/api/v2/cluster/33?services"
        },
        "include_nodes": {
            "href": "/api/v2/cluster/33?nodes"
        }
    },
    "label": {
        "name": "cdh5121-test",
        "description": "cdh"
    },
    "debug": true,
    "isolated": false,
    "two_phase_delete": false,
    "status": "ready",
    "status_message": "",
    "error_info": "",
    "log_url": "http://10.36.0.27:8080/Logs/33.txt",
    "nodegroup": {
        "id": "1",
        "status": "created",
        "role_configs": [
            {
                "role_id": "cmserver",
                "selected": true,
                "flavor": {
                    "gpus": 0,
                    "root_disk_size": 30,
                    "label": {
                        "name": "Small",
                        "description": "system-created example flavor"
                    },
                    "cores": 4,
                    "memory": 8192
                },
                "node_count": 1
            },
            {
                "role_id": "controller",
                "selected": true,
                "flavor": {
                    "gpus": 0,
                    "root_disk_size": 100,
                    "label": {
                        "name": "Medium",
                        "description": "system-created example flavor"
                    },
                    "cores": 4,
                    "memory": 12288
                },
                "node_count": 1
            },......



## 5. Create a new cluster

  __Note__: Makesure to run Switch tenant API (v1 API) to create cluster incase you logged in as Siteadmin.

  __API-URI__: /api/v2/cluster

  __Curl command__:

      curl -X POST -d@hadoop_cluster.json -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v2/cluster

  __API Type__: `POST`

  __Example__:

      curl -X POST -d@hadoop_cluster.json -H "X-BDS-SESSION:/api/v1/session/446468df-6869-4e42-bbba-c8cc11cb4a54" http://10.36.0.17:8080/api/v2/cluster

 __Json-file__: hadoop_cluster.json:

        {
    "bootstrap_action": {
        "args": "",
        "as_root": true,
        "cmd": "echo \" Kafka\"",
        "label": {
            "description": "typed script commands",
            "name": "Test"
        },
        "nodegroup_id": "1"
    },
    "debug": true,
    "dependent_nodegroups": [
        {
            "catalog_entry_distro_id": "bluedata/cdh5101-7xedge",
            "constraints": [],
            "id": "2",
            "role_configs": [
                {
                    "flavor": "/api/v1/flavor/4",
                    "node_count": 1,
                    "role_id": "edge"
                }
            ]
        }
    ],
    "isolated": false,
    "label": {
        "description": "cdh",
        "name": "cdh5101-test"
    },
    "nodegroup": {
        "catalog_entry_distro_id": "bluedata/cdh51017x",
        "config_choice_selections": [
            {
                "choice_id": "hbase",
                "selection_id": true
            },
            {
                "choice_id": "mrtype",
                "selection_id": "yarn"
            },
            {
                "choice_id": "apps",
                "selection_id": true
            },
            {
                "choice_id": "kerberos",
                "selection_id": true
            },
            {
                "choice_id": "yarn_ha",
                "selection_id": true
            },
            {
                "choice_id": "spark",
                "selection_id": true
            }
        ],
        "constraints": [],
        "role_configs": [
            {
                "flavor": "/api/v1/flavor/5",
                "node_count": 1,
                "role_id": "controller"
            },
            {
                "flavor": "/api/v1/flavor/4",
                "node_count": 1,
                "role_id": "standby"
            },
            {
                "flavor": "/api/v1/flavor/4",
                "node_count": 1,
                "role_id": "arbiter"
            },
            {
                "flavor": "/api/v1/flavor/4",
                "node_count": 1,
                "role_id": "worker"
            }
        ]
    },
    "two_phase_delete": false
}


  __Response__:

      {"result":"Success","uuid":"216"}


## 6. Retrieve cluster nodes

  __API-URI__: /api/v2/cluster/<cluster_id>/node

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v2/cluster/<cluster_id>/node

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/b584b109-318c-4aa9-b704-21fab6c44e07" http://10.36.0.17:8080/api/v2/cluster/33/node

  __Response__:

       % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
      100  3549  100  3549    0     0   222k      0 --:--:-- --:--:-- --:--:--  231k
    {
        "_embedded": {
            "nodes": [
              {
                  "_links": {
                      "cluster": {
                          "href": "/api/v2/cluster/33",
                          "title": "cdh5121-test"
                      },
                    "include_catalog_entry": {
                        "href": "/api/v2/cluster/33/node/56?catalog_entry"
                    },
                    "include_flavor": {
                        "href": "/api/v2/cluster/33/node/56?flavor"
                    },
                    "include_services": {
                        "href": "/api/v2/cluster/33/node/56?services"
                    },
                    "self": {
                        "href": "/api/v2/cluster/33/node/56"
                    },
                    "tenant": {
                        "href": "/api/v1/tenant/2",
                        "title": "Demo Tenant"
                    }
                },
                "fqdn": "bluedata-56.bdlocal",
                "hypervisor_host": "yav-111.lab.bluedata.com",
                "metrics_instances": [
                    {
                        "metric_id": "cpu",
                        "selectors": [
                            {
                                "field": "docker.container.name",
                                "value": "bluedata-56"
                            }
                        ]
                    },
                    {
                        "metric_id": "memory",
                        "selectors": [
                            {
                                "field": "docker.container.name",
                                "value": "bluedata-56"
                            }
                        ]
                    },
                    {
                        "metric_id": "network",
                        "selectors": [
                            {
                                "field": "beat.hostname",
                                "value": "yav-111.lab.bluedata.com"
                            },
                            {
                                "field": "system.network.name",
                                "value": "29543-h"
                            }
                        ]
                    },
                    {
                        "metric_id": "disk",
                        "selectors": [
                            {
                                "field": "beat.hostname",
                                "value": "yav-111.lab.bluedata.com"
                            },
                            {
                                "field": "system.diskio.name",
                                "value": "dm-9"
                            }
                        ]
                    }
                ],
                "nodegroup_id": "1",
                "public_ip": "10.39.250.12",
                "role": "controller",
                "status": "ready"
            },
            {
                "_links": {
                    "cluster": {
                        "href": "/api/v2/cluster/33",
                        "title": "cdh5121-test"
                    },
                    "include_catalog_entry": {
                        "href": "/api/v2/cluster/33/node/57?catalog_entry"
                    },
                    "include_flavor": {
                        "href": "/api/v2/cluster/33/node/57?flavor"
                    },
                    "include_services": {
                        "href": "/api/v2/cluster/33/node/57?services"
                    },
                    "self": {
                        "href": "/api/v2/cluster/33/node/57"
                    },
                    "tenant": {
                        "href": "/api/v1/tenant/2",
                        "title": "Demo Tenant"
                    }
                }, ...


## 7. Retrieve tenant filesystem information

  __API-URI__: /api/v2/tenant_filesystem

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v2/tenant_filesystem

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/b584b109-318c-4aa9-b704-21fab6c44e07" http://10.36.0.17:8080/api/v2/tenant_filesystem

  __Response__:


      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
      100  2162  100  2162    0     0   132k      0 --:--:-- --:--:-- --:--:--  140k
      {
          "_embedded": {
              "filesystems": [
                  {
                      "_embedded": {
                          "mountspec": {
                              "_links": {
                                  "self": {
                                      "href": "api/v2/tenant_filesystem/8/mountspec"
                                  },
                                  "tenant": {
                                      "href": "/api/v1/tenant/3",
                                      "title": "Analytics"
                                  },
                                  "tenant_filesystem": {
                                      "href": "/api/v2/tenant_filesystem/8"
                                  }
                              },
                              "export_path": "/exports/tom",
                              "host": "10.2.12.86",
                              "mount_name": "TomsShare",
                              "read_only": false,
                              "type": "nfs"
                          },
                          "status": {
                              "_links": {
                                  "self": {
                                      "href": "api/v2/tenant_filesystem/8/status"
                                  },
                                  "tenant": {
                                      "href": "/api/v1/tenant/3",
                                      "title": "Analytics"
                                  },
                                  "tenant_filesystem": {
                                      "href": "/api/v2/tenant_filesystem/8"
                                  }
                              },
                              "status": "mounted"
                          }
                      },
                      "_links": {
                          "self": {
                              "href": "/api/v2/tenant_filesystem/8"
                          },
                          "tenant": {
                              "href": "/api/v1/tenant/3",
                              "title": "Analytics"
                          }
                      }
                  },
                  {
                      "_embedded": {
                          "mountspec": {
                              "_links": {
                                  "self": {
                                      "href": "api/v2/tenant_filesystem/5/mountspec"
                                  },
                                  "tenant": {
                                      "href": "/api/v1/tenant/2",
                                      "title": "Demo Tenant"
                                  },
                                  "tenant_filesystem": {
                                      "href": "/api/v2/tenant_filesystem/5"
                                  }
                              },
                              "export_path": "/jungle/customers",
                              "host": "bd-nas3.lab.bluedata.com",
                              "mount_name": "CustomerMount",
                              "read_only": false,
                              "type": "nfs"
                          },
                          "status": {
                              "_links": {
                                  "self": {
                                      "href": "api/v2/tenant_filesystem/5/status"
                                  },
                                  "tenant": {
                                      "href": "/api/v1/tenant/2",
                                      "title": "Demo Tenant"
                                  },
                                  "tenant_filesystem": {
                                      "href": "/api/v2/tenant_filesystem/5"
                                  }
                              },
                              "status": "mounted"
                          }
                      },
                      "_links": {
                          "self": {
                              "href": "/api/v2/tenant_filesystem/5"
                          },
                          "tenant": {
                              "href": "/api/v1/tenant/2",
                              "title": "Demo Tenant"
                          }
                      }
                  },
                  {
                      "_embedded": {
                          "mountspec": {
                              "_links": {
                                  "self": {
                                      "href": "api/v2/tenant_filesystem/6/mountspec"
                                  },
                                  "tenant": {
                                      "href": "/api/v1/tenant/2",
                                      "title": "Demo Tenant"
                                  },
                                  "tenant_filesystem": {
                                      "href": "/api/v2/tenant_filesystem/6"
                                  }
                              },
                              "export_path": "/jungle/support",
                              "host": "bd-nas3.lab.bluedata.com",
                              "mount_name": "SupportMount",
                              "read_only": true,
                              "type": "nfs"
                          },
                          "status": {
                              "_links": {
                                  "self": {
                                      "href": "api/v2/tenant_filesystem/6/status"
                                  },
                                  "tenant": {
                                      "href": "/api/v1/tenant/2",
                                      "title": "Demo Tenant"
                                  },
                                  "tenant_filesystem": {
                                      "href": "/api/v2/tenant_filesystem/6"
                                  }
                              },
                              "status": "mounted"
                          }
                      },
                      "_links": {
                          "self": {
                              "href": "/api/v2/tenant_filesystem/6"
                          },
                          "tenant": {
                              "href": "/api/v1/tenant/2",
                              "title": "Demo Tenant"
                          }
                      }
                  }
              ]
          },
          "_links": {
              "self": {
                  "href": "/api/v2/tenant_filesystem"
              }
          },
          "mount_timeout": "infinity",
          "mount_verbose": false,
          "unmount_timeout": "infinity",
          "unmount_verbose": false
      }



## 8. Retrieve Epic platform configuration

  __API-URI__: /api/v2/config

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v2/config

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/b584b109-318c-4aa9-b704-21fab6c44e07" http://10.36.0.17:8080/api/v2/config

  __Response__:

      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
      100  1256  100  1256    0     0  90869      0 --:--:-- --:--:-- --:--:-- 96615
    {
        "_embedded": {
            "auth": {
                "_links": {
                    "self": {
                        "href": "/api/v2/config/auth"
                    }
                },
                "available_authentication_methods": [
                   "Active Directory",
                    "Local"
                ],
                "external_identity_server": {
                   "base_dn": "dc=BLUEDATA,dc=local",
                    "bind_dn": "admin@BLUEDATA.LOCAL",
                    "bind_type": "search_bind",
                    "host": "10.2.12.106",
                    "port": 389,
                    "security_protocol": "starttls",
                    "type": "Active Directory",
                    "user_attribute": "sAMAccountName"
                },
            "supported_external_identity_servers": [
                "LDAP",
                "Active Directory"
            ],
            "supported_sso_workflows": [
                "SAML"
            ]
        },
        "tenant_types": {
            "_embedded": {
                "docker": {
                    "_embedded": {
                        "capabilities": {
                            "_links": {
                                "self": {
                                    "href": "/api/v2/config/tenant_types/docker/capabilities"
                                }
                            },
                            "cluster_isolation_supported": true,
                            "constraints_supported": true,
                            "filesystem_mount_supported": true,
                            "gpu_usage_supported": true
                        }
                    },
                    "_links": {
                        "self": {
                            "href": "/api/v2/config/tenant_types/docker"
                        }
                    }
                },
                "ec2": {
                    "_embedded": {
                        "capabilities": {
                            "_links": {
                                "self": {
                                    "href": "/api/v2/config/tenant_types/ec2/capabilities"
                                }
                            },
                            "cluster_isolation_supported": false,
                            "constraints_supported": false,
                            "filesystem_mount_supported": false,
                            "gpu_usage_supported": true
                        }
                    },
                    "_links": {
                        "self": {
                            "href": "/api/v2/config/tenant_types/ec2"
                        }
                    }
                }
            },
            "_links": {
                "self": {
                    "href": "/api/v2/config/tenant_types"
                }
            }
        }
    },
    "_links": {
        "self": {
            "href": "/api/v2/config"
        }
    },
    "tenant_independent_auth": false
}


## 9. Invoke ActionScript


  __API-URI__: /api/v2/cluster/{cluster-id}/action_task

  __Curl command__:

      curl -X POST http://<controller-ip>:8080/api/v2/cluster/<cluster-id>/action_task -H 'cache-control:no-cache' -H 'content-type: application/json' -H 'x-bds-session:<session-id>' -d@Spark_submit.json

  __API Type__: `POST`

  __Example__:

      curl -X POST http://10.36.0.27:8080/api/v2/cluster/8/action_task -H 'cache-control:no-cache' -H 'content-type: application/json' -H 'x-bds-session:/api/v1/session/9b4e6dea-158e-484d-ad64-916cb738563c' -d@Spark_submit.json

 __Json-file__: Spark_submit.json:

        {
    "args": "",
    "label":{
	"name":"Spark-submit_ActionSource_spark_submit_job.sh",
	"description":"test"
    },
    "as_root": "true",
    "cmd": "#/bin/bash\nexport node=`bdvcli --get node.role_id`\nif [[ $node == \"controller\" ]]; then\n    /usr/lib/spark/spark-2.1.1-bin-hadoop2.7/bin/spark-submit --class org.apache.spark.examples.SparkPi --master spark://bluedata-4.bdlocal:7077 /usr/lib/spark/spark-2.1.1-bin-hadoop2.7/examples/jars/spark-examples_2.11-2.1.1.jar 100\nfi",
    "nodegroupid": "1" }


  __Response__:

      201 created



## 10. Update the hue.ini safety valve to point to datatap


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




## 11. Mount dtap to Virtual cluster ActionScript


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



## 12. Invoke ActionScript from dtap


  __API-URI__: /api/v2/cluster/{cluster-id}/action_task

  __Curl command__:

      curl -X POST http://<controller-ip>:8080/api/v2/cluster/<cluster-id>/action_task -H 'cache-control:no-cache' -H 'content-type: application/json' -H 'x-bds-session:<session-id>' -d@Spark_submit_dtap.json

  __API Type__: `POST`

  __Example__:

      curl -X POST http://10.36.0.27:8080/api/v2/cluster/8/action_task -H 'cache-control:no-cache' -H 'content-type: application/json' -H 'x-bds-session:/api/v1/session/78486fbe-be9c-49aa-8c72-1fef74191fc5' -d@Spark_submit_dtap.json


 __Json-file__: Spark_submit_dtap.json:

      {
    "args":"",
    "label":{
	"name":"Testdtap_ActionSource_Typed script commands",
	"description":"test"
    },
    "as_root":"true",
    "cmd":"hadoop fs -get dtap://TenantStorage/tmp/sample-scripts/spark_submit_job.sh /tmp/\n   chmod a+x /tmp/spark_submit_job.sh\n   /tmp/spark_submit_job.sh\n   rm /tmp/spark_submit_job.sh",
    "nodegroupid":"1"
    }



  __Response__:

	 201 created


## 13. Retrieve public & private endpoints for cluster services


  __API-URI__: /api/v2/cluster/{cluster-id}/node?services

  __Curl command__:

      curl -X GET -H "X-BDS-SESSION:<session-id>" http://<controller-ip>:8080/api/v2/cluster/{cluster-id}/node?services

  __API Type__: `GET`

  __Example__:

      curl -X GET -H "X-BDS-SESSION:/api/v1/session/e7d4b65c-feca-4cf6-bc46-16a9ddbfd933" http://10.36.0.17:8080/api/v2/cluster/113/node?services

  __Response__:

       % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
        100  6025  100  6025    0     0   440k      0 --:--:-- --:--:-- --:--:--  490k
        {
            "_embedded": {
                "nodes": [
                    {
                        "_links": {
                            "cluster": {
                                "href": "/api/v2/cluster/113",
                                "title": "ESK624"
                            },
                            "include_catalog_entry": {
                                "href": "/api/v2/cluster/113/node/349?catalog_entry"
                            },
                            "include_flavor": {
                                "href": "/api/v2/cluster/113/node/349?flavor"
                            },
                            "self": {
                                "href": "/api/v2/cluster/113/node/349?services"
                            },
                            "tenant": {
                                "href": "/api/v1/tenant/3",
                                "title": "EPIC-EUR-1"
                            }
                        },
                        "fqdn": "bluedata-349.bdlocal",
                        "hypervisor_host": "yav-137.lab.bluedata.com",
                        "metrics_instances": [
                            {
                                "metric_id": "cpu",
                                "selectors": [
                                    {
                                        "field": "docker.container.name",
                                        "value": "bluedata-349"
                                    }
                                ]
                            },
                            {
                                "metric_id": "memory",
                                "selectors": [
                                    {
                                        "field": "docker.container.name",
                                        "value": "bluedata-349"
                                    }
                                ]
                            },
                            {
                                "metric_id": "network",
                                "selectors": [
                                    {
                                        "field": "beat.hostname",
                                        "value": "yav-137.lab.bluedata.com"
                                    },
                                    {
                                        "field": "system.network.name",
                                        "value": "59223-h"
                                    }
                                ]
                            },
                            {
                                "metric_id": "disk",
                                "selectors": [
                                    {
                                        "field": "beat.hostname",
                                        "value": "yav-137.lab.bluedata.com"
                                    },
                                    {
                                        "field": "system.diskio.name",
                                        "value": "dm-9"
                                    }
                                ]
                            }
                        ],
                        "nodegroup_id": "2",
                        "private_ip": "172.18.0.79",
                        "role": "kibana",
                        "services": [
                            {
                                "endpoint": {
                                    "is_dashboard": false,
                                    "port": "9200",
                                    "proxy_host": "yav-036.lab.bluedata.com",
                                    "proxy_port": "10209"
                                },
                                "id": "elasticsearch",
                                "label": {
                                    "description": "",
                                    "name": "Elastic Search"
                                }
                            },
                            {
                                "endpoint": {
                                    "is_dashboard": true,
                                    "path": "/",
                                    "port": "5601",
                                    "proxy_host": "yav-036.lab.bluedata.com",
                                    "proxy_port": "10207",
                                    "url_scheme": "http"
                                },
                                "id": "kibana",
                                "label": {
                                    "description": "",
                                    "name": "Kibana"
                                }
                            },
                            {
                                "endpoint": {
                                    "is_dashboard": false,
                                    "port": "22",
                                    "proxy_host": "yav-036.lab.bluedata.com",
                                    "proxy_port": "10208"
                                },
                                "id": "ssh",
                                "label": {
                                    "description": "",
                                    "name": "SSH"
                                }
                            }
                        ],
                        "status": "ready"
                    },
                    {
                        "_links": {
                            "cluster": {
                                "href": "/api/v2/cluster/113",
                                "title": "ESK624"
                            },
                            "include_catalog_entry": {
                                "href": "/api/v2/cluster/113/node/347?catalog_entry"
                            },
                            "include_flavor": {
                                "href": "/api/v2/cluster/113/node/347?flavor"
                            },
                            "self": {
                                "href": "/api/v2/cluster/113/node/347?services"
                            },
                            "tenant": {
                                "href": "/api/v1/tenant/3",
                                "title": "EPIC-EUR-1"
                            }
                        },
                        "fqdn": "bluedata-347.bdlocal",
                        "hypervisor_host": "yav-017.lab.bluedata.com",
                        "metrics_instances": [
                            {
                                "metric_id": "cpu",
                                "selectors": [
                                    {
                                        "field": "docker.container.name",
                                        "value": "bluedata-347"
                                    }
                                ]
                            },
                            {
                                "metric_id": "memory",
                                "selectors": [
                                    {
                                        "field": "docker.container.name",
                                        "value": "bluedata-347"
                                    }
                                ]
                            },
                            {
                                "metric_id": "network",
                                "selectors": [
                                    {
                                        "field": "beat.hostname",
                                        "value": "yav-017.lab.bluedata.com"
                                    },
                                    {
                                        "field": "system.network.name",
                                        "value": "15492-h"
                                    }
                                ]
                            },
                            {
                                "metric_id": "disk",
                                "selectors": [
                                    {
                                        "field": "beat.hostname",
                                        "value": "yav-017.lab.bluedata.com"
                                    },
                                    {
                                        "field": "system.diskio.name",
                                        "value": "dm-10"
                                    }
                                ]
                            }
                        ],
                        "nodegroup_id": "1",
                        "private_ip": "172.18.0.70",
                        "role": "index",
                        "services": [
                            {
                                "endpoint": {
                                    "is_dashboard": false,
                                    "path": "/",
                                    "port": "9200",
                                    "proxy_host": "yav-036.lab.bluedata.com",
                                    "proxy_port": "10203",
                                    "url_scheme": "http"
                                },
                                "id": "elasticsearch",
                                "label": {
                                    "description": "",
                                    "name": "Elastic Search"
                                }
                            },
                            {
                                "endpoint": {
                                    "is_dashboard": false,
                                    "port": "22",
                                    "proxy_host": "yav-036.lab.bluedata.com",
                                    "proxy_port": "10204"
                                },
                                "id": "ssh",
                                "label": {
                                    "description": "",
                                    "name": "SSH"
                                }
                            }
                        ],
                        "status": "ready"
                    }, ...

</span>
