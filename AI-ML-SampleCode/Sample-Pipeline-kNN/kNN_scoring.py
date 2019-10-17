## This is a scoring script for running k-NN model. 


# Imports
import numpy as np
import pickle
import os
import sys
from sklearn import metrics

# Custom function to load data from disk
def saveInProjectRepo(path):
    ProjectRepo = os.popen('bdvcli --get cluster.project_repo').read().rstrip()
    return os.path.join(ProjectRepo, path)

print("Loading test data")

test_data = np.load(saveInProjectRepo(sys.argv[1]))
test_labels = np.load(saveInProjectRepo(sys.argv[2]))


print("Loaded test data")

# Load the PCA trnasformation model to project test data to a lower dimension
with open(saveInProjectRepo('models/pca_mnist.p'),'rb') as f:
    pca_mnist = pickle.load(f)


# Project test data to a lower dimension
pca_test = pca_mnist.transform(test_data)


print("Loaded PCA model")

# Load the k-NN classifier model
with open(saveInProjectRepo("models/kNN_mnist.p"), "rb") as f:
    kNN_model = pickle.load(f)

print("Loaded kNN  model. Now predicting ...")

# Use the transformed data to classify the image
pred = kNN_model.predict(pca_test)



# Calculate accuracy using accuracy_score. The set of labels predicted for a sample must exactly match
# the corresponding set of labels in test_labels
acc = metrics.accuracy_score(test_labels, pred)

print("Accuracy for kNN model is: ", float(acc*100.0),"%")



'''
Call: 

We call the script using the deployment cluster. The URL is specidifed under "Model Serving LoadBalancer" 
eg: http://<host>:<port>/<<model_name>>/<<model_version>>/predict


Sample JSON body to call POST service:


{
        "use_scoring": true,
        "scoring_args": "data/test_data.npy data/test_label.npy"
}

'scoring_args' are space-separated parameters to the scoring script. In this script, 
we read them on Line 18 and 19 with np.load() calls

Headers:

X-Auth-Token : <auth token in Deployment Cluster's Model Serving LoadBalancer service> 

This header is optional. In the case that this header is not used, it is required to have a auth=none parameter 
in the called URL. The URL in this case becomes http://<host>:<port>/<<model_name>>/<<model_version>>/predict?auth=none

----------------------------

Sample  Output:

{
    "id": 3,
    "input": "data/test_data.npy data/test_label.npy",
    "log_url": "<host>:<port>/logs/3",
    "node": "bluedata-35.bdlocal",
    "output": "\nLoading test data\nLoaded test data\nLoaded PCA model\nLoaded kNN  model. Now predicting ...\nAccuracy for kNN model is:  0.9723\nAccuracy for kNN model is:  97.23\n\n",
    "pid": 50665,
    "request_url": "<host>:<port>/history/3",
    "status": "Finished"
}

'''
