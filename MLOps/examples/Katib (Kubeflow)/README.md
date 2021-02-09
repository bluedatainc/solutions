## Katib Example

Katib is a component of Kubeflow that does automated hyperparameter tuning.

IMPORTANT: to run this demo, you will need a container registry to push your container to (DockerHub works fine).
This demo was tested on a local minikube installation, so Kubeflow installations with corporate proxies may require more configuration to ensure Kubeflow can download the docker container images.

Instructions:
- Build the docker container using the Dockerfile found in the folder "Container Files"
- Push the container to a container registry of your choice.
- In the Katib web ui, select the "Hyperparameter Tuning" option.
- Copy and paste the yaml from this git repo AFTER you have edited the yaml to point to your container registry.
- Click deploy
- View the results of your experiment under the "Monitor" tab from the menu on the left.


Background info:
There are 2 main components to running Katib experiments:

1) YAML file describing the experiment
- Include the error metric that Katib should optimize for. Depending on what you specify in metricsCollectorSpec, it will read this error metric from the Docker container, either from stdout or from an error metrics file.]
- Include the hyperparameter ranges that Katib should test.

2) Docker container with model code
- Error metrics should be printed to stdout or a file within the container. The YAML in this repo configures Katib to read error metrics from stdout, although that can be edited.
- It should be set up to take hyperparameters as command line arguments (argparse). Katib will try different values of hyperparameters to determine the optimal ones.
