## Running kubectl commands from Jupyter Notebooks

Workflow:
1. Kubectl should be set up on the user’s local computer.
2. User downloads their user-specific kubeconfig from Ezmeral onto their local computer, and places it at ~/.kube/config
3. User runs CreateConfigSecretScript.py from https://github.com/bluedatainc/solutions/tree/master/MLOps/kubeconfig-notebook
4. The script will return the name of the KubeDirector connections secret containing the user-specific kubeconfig
5. User logs into Ezmeral Container Platform
6. When launching a plain Jupyter notebook instance, user should specify the KubeDirector connections secret from step 4
7. Now, open a new Python3 Jupyter notebook. Kubectl commands can be run from Jupyter notebook cells. Kubectl commands should begin with an exclamation mark (such as !kubectl get pods)
8. If needed, set the context and namespace (run the following example commands from a notebook cell.
    1. Example: !kubectl config set-context CONTEXTNAME
        1. Without setting this, you may get a connection refused error
    2. Example: !kubectl config set-namespace --current --namespace=NAMESPACENAME
9. Jupyter terminal can also be used after the following command is run from the Jupyter terminal:
    1. export HOME=/root 
