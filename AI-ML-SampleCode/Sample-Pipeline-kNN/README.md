This is a Sample ML pipeline showcasing bluedata's MLOPs module
In this example we are using MNIST database to find handwritten digits.

Dataset can be downloaded from - http://yann.lecun.com/exdb/mnist/

Four files are available on this site:

1. train-images-idx3-ubyte.gz:  training set images (9912422 bytes)
2. train-labels-idx1-ubyte.gz:  training set labels (28881 bytes)
3. t10k-images-idx3-ubyte.gz:   test set images (1648877 bytes)
4. t10k-labels-idx1-ubyte.gz:   test set labels (4542 bytes)


## Steps to run this pipeline

1. Download the dataset above and dump it under data/ directory in your project repo
2. Create training cluster (Python ML and DL Toolkit)
3. Open Jupyter notebook and import first notebook and execute  - `DecomposeImages.ipynb`
   -  In the notebook, make sure to change the name of training cluster with the appropriate name. The current  `%%knntraining` attachment should be replaced by `%%<name of attached training cluster>`. Attached training clusters can be viewed with `%attachments` magic command.
4. Next import kNN in `kNNTrainingEnviornment.ipnyb` notebook and execute
5. Last step would spit out a model, which you could then register with EPIC
6. While registering the model use `kNN_scoring.py` script
7. Next create deployment cluster (Python ML/DL Toolkit) with model registered in previous step as attached model
8. Once deployment cluster comes up use the loadbalancer URL to make REST API calls to serve the model (this can be done using any REST client like postman, python request, curl, etc.)
9. Sample JSON body to call POST service:
   ```json
   {
       "use_scoring": true,
       "scoring_args": "data/test_data.npy data/test_label.npy"
   }
   ```
   - To have the job run, an Auth Token is usually required. This MUST be populated in an `X-Auth-Token` header. The value of the auth token can be retrieved from the screen with details of the deployment cluster.
   - The data MUST have a valid `Content-Type` header passed in. For JSON, the MIME type MUST be `application/json`.
10. Sample  Output:
  ```json
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
  ```

*Note*: We are predicting the labels for 10000 images with this REST call. As a result, the it should take around 3-4 minutes to get the response back for the call.


