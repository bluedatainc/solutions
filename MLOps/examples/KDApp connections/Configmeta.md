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
obj['connections']['configmaps']['source-control'][0]['data']['proxy-hostname'] 
# >> 'web-proxy.corp.hpecorp.net'

```



