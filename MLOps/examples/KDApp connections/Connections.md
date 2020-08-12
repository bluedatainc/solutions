## Using `connections` in Cluster YAML

`connections` is useful in scenarios where there is a need to attach addditonal information to the cluster. There are three types of Kubernetes resources that can be used with `connections` - `configmap`, `secret`, and `kdcluster` (syntactically called `cluster` in the YAML).

**Note**: The resources that are to be used with connections should be created before using them in the YAMLs

Following are examples that illustrate the use of each resource

### 1. `configmap`

One of the most frequent use-cases of using a `configmap` is when we attach a model from the model registry to a deployment engine. The connected configmap needs to have the following label: `'kubedirector.hpe.com/cmType': '<some-type>'`

A sample configuration looks like:

```yaml
apiVersion: "kubedirector.hpe.com/v1beta1"
kind: "KubeDirectorCluster"
metadata: 
  name: "deployment-engine"

spec:
  app: model-serving
  connections:
    configmaps:
    - "convolutional-nn-model"
    - "fullyconnected-nn-model"
  roles:
  - id: RESTServer
    members: 1
    resources:
      requests:
        memory: "6Gi"
        cpu: "2"
      limits:
        memory: "6Gi"
        cpu: "2"
  - id: LoadBalancer
    members: 1
    resources:
      requests:
        memory: "2Gi"
        cpu: "1"
      limits:
        memory: "2Gi"
        cpu: "1"           

```

In this example, `convolutional-nn-model` and `fullyconnected-nn-model` are the `configmap` resources created by HPECP with relevant model information after the models are registered.


### 2. `secret`
An example that uses `secret` as a connection resource is while configuring a notebook cluster with source control. The connected secret needs to have the following label: `'kubedirector.hpe.com/secretType': '<some-type>'` 

The YAML snippet below illustrates the syntax:

```yaml
apiVersion: "kubedirector.hpe.com/v1beta1"
kind: "KubeDirectorCluster"
metadata:
  name: "jupyter-notebook"
spec:
  app: jupyter-notebook
  connections:
    secrets:
    - "source-control-secret"
  roles:
  - id: controller
    resources:
      requests:
        memory: "3Gi"
        cpu: "1"
      limits:
        memory: "3Gi"
        cpu: "1"

```
`source-control-secret` is a Kubernetes secret created by the platform with information required to configure the notebook with source control.


### 3. `cluster`

`cluster` is typically used as a connection resource in a scenario that requires accessing the connected cluster resource(s) via API(s). As an example, let's consider the YAML below:

```yaml
apiVersion: "kubedirector.hpe.com/v1beta1"
kind: "KubeDirectorCluster"
metadata:
  name: "jupyter-notebook"
spec:
  app: training-notebook
  connections:
    clusters:
    - "training-engine-tf"
    - "training-engine-pytorch"
    roles:
  - id: controller
    resources:
      requests:
        memory: "2Gi"
        cpu: "1"
      limits:
        memory: "2Gi"
        cpu: "1"
```

In the example, we have connected two clusters - `training-engine-tf` and `training-engine-pytorch` to the notebook cluster.

### 4. A combination of resources

It is possible to connect more than one type of resources to a cluster YAML. Here is an example:

```yaml
apiVersion: "kubedirector.hpe.com/v1beta1"
kind: "KubeDirectorCluster"
metadata:
  name: "jupyter-notebook"
spec:
  app: notebook-plus-plus
  connections:
    clusters:
    - "training-engine-tf"
    - "training-engine-pytorch"
    secrets:
    - "source-control-secret"
  roles:
  - id: controller
    resources:
      requests:
        memory: "4Gi"
        cpu: "1"
      limits:
        memory: "4Gi"
        cpu: "1"
```
In the above snippet, we have connected `cluster`s and a `secret`.
