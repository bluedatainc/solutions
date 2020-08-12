## Using `connections` inside a kdcluster

When a resource is connected, its data gets appended to `configmeta.json`. 

`configmeta.json` is a file that stores metadata related to the cluster. It is in `/etc/guestconfig/` directory.

Example: Lets assume we create a cluster with the following YAML, connecting a `configmap` resource with the label `cmType` as `source-control`:

```yaml
apiVersion: "kubedirector.hpe.com/v1beta1"
kind: "KubeDirectorCluster"
metadata:
  name: "jupyter-notebook"
spec:
  app: jupyter-notebook
  appCatalog: local
  connections:
    configmaps:
    - source-control-info
  roles:
  - id: controller
    members: 1
    resources:
      limits:
        cpu: "1"
        memory: 4Gi
      requests:
        cpu: "1"
        memory: 4Gi
```

The `configmeta.json`  in the cluster looks like:

```json
{
    "version": "7",
    "services": {
        "jupyter-nb": {
            "1": {
                "controller": {
                    "bdvlibrefkey": ["nodegroups", "1", "roles", "controller", "services", "jupyter-nb"]
                }
            }
        },
        "ssh": {
            "1": {
                "controller": {
                    "bdvlibrefkey": ["nodegroups", "1", "roles", "controller", "services", "ssh"]
                }
            }
        }
    },
    "nodegroups": {
        "1": {
            "roles": {
                "controller": {
                    "services": {
                        "jupyter-nb": {
                            "qualifiers": [],
                            "name": "Jupyter Notebook",
                            "id": "jupyter-nb",
                            "hostnames": {
                                "bdvlibrefkey": ["nodegroups", "1", "roles", "controller", "hostnames"]
                            },
                            "global_id": "1_controller_jupyter-nb",
                            "fqdns": {
                                "bdvlibrefkey": ["nodegroups", "1", "roles", "controller", "fqdns"]
                            },
                            "exported_service": "",
                            "endpoints": ["http://kdss-dnlkm-0.kdhs-f2vb7.kubecon.svc.cluster.local:8888"],
                            "authToken": "7aaae3eaafeeb3a777f8547ab2197e84"
                        },
                        "ssh": {
                            "qualifiers": [],
                            "name": "SSH",
                            "id": "ssh",
                            "hostnames": {
                                "bdvlibrefkey": ["nodegroups", "1", "roles", "controller", "hostnames"]
                            },
                            "global_id": "1_controller_ssh",
                            "fqdns": {
                                "bdvlibrefkey": ["nodegroups", "1", "roles", "controller", "fqdns"]
                            },
                            "exported_service": "",
                            "endpoints": ["://kdss-dnlkm-0.kdhs-f2vb7.kubecon.svc.cluster.local:22"],
                            "authToken": ""
                        }
                    },
                    "node_ids": ["1"],
                    "hostnames": ["kdss-dnlkm-0.kdhs-f2vb7.kubecon.svc.cluster.local"],
                    "fqdns": ["kdss-dnlkm-0.kdhs-f2vb7.kubecon.svc.cluster.local"],
                    "fqdn_mappings": {
                        "kdss-dnlkm-0.kdhs-f2vb7.kubecon.svc.cluster.local": "1"
                    },
                    "flavor": {
                        "storage": "n/a",
                        "name": "n/a",
                        "memory": "4096",
                        "description": "n/a",
                        "cores": "1"
                    }
                }
            },
            "distro_id": "hpecp/jupyter-notebook",
            "catalog_entry_version": "1.0",
            "config_metadata": null
        }
    },
    "distros": {
        "hpecp/jupyter-notebook": {
            "1": {
                "bdvlibrefkey": ["nodegroups", "1"]
            }
        }
    },
    "cluster": {
        "name": "jupyter-notebook-instance",
        "isolated": false,
        "id": "b78091cc-ac55-4b4f-800d-12e039597684",
        "config_metadata": {
            "1": {
                "bdvlibrefkey": ["nodegroups", "1", "config_metadata"]
            }
        }
    },
    "node": {
        "role_id": "controller",
        "nodegroup_id": "1",
        "id": "1",
        "hostname": "kdss-dnlkm-0.kdhs-f2vb7.kubecon.svc.cluster.local",
        "fqdn": "kdss-dnlkm-0.kdhs-f2vb7.kubecon.svc.cluster.local",
        "domain": "kdhs-f2vb7.kubecon.svc.cluster.local",
        "distro_id": "hpecp/jupyter-notebook",
        "depends_on": {}
    },
    "connections": {
        "clusters": {},
        "configmaps": {
            "source-control": [{
                "annotations": {
                    "kubectl.kubernetes.io/last-applied-configuration": "{\"apiVersion\":\"v1\",\"data\":{\"branch\":\"master\",\"proxy-hostname\":\"web-proxy.corp.hpecorp.net\",\"proxy-port\":\"8080\",\"proxy-protocol\":\"http\",\"repo-url\":\"http://repo:8080/scm/~user/test-repo-sj.git\",\"type\":\"bitbucket\",\"user-email\":\"suser@hpe.com\",\"user-name\":\"saurabhj\"},\"kind\":\"ConfigMap\",\"metadata\":{\"annotations\":{},\"labels\":{\"kubedirector.hpe.com/cmType\":\"source-control\"},\"name\":\"source-control-info\",\"namespace\":\"kubecon\"}}\n"
                },
                "data": {
                    "branch": "master",
                    "proxy-hostname": "web-proxy.corp.hpecorp.net",
                    "proxy-port": "8080",
                    "proxy-protocol": "http",
                    "repo-url": "http://repo:8080/scm/~saurabhj/test-repo-sj.git",
                    "type": "bitbucket",
                    "user-email": "user@hpe.com",
                    "user-name": "user"
                },
                "labels": {
                    "kubedirector.hpe.com/cmType": "source-control"
                },
                "metadata": {
                    "name": "source-control-info"
                }
            }]
        },
        "secrets": {}
    }
}

```

`connections` are a part of the object with same name in the JSON. The three possible resources types form the sub-objects and every sub-object contains another child object with the key same as the `type` that it had been labelled with. The `type` is applicable only to `configmap` and `secret`. 

Since `configmeta.json ` is a JSON, we can use any json parser to parse and use metadata to our use. A sample python script is:

```python
import json

# load json
with open("configmeta.json", "r") as f:
    obj = json.load(f)

# access objects
obj['connections']['configmaps']['source-control']

```



