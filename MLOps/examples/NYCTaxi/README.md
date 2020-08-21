## NYC Taxi MLOps Example

Versions of the Jupyter notebook are provided for both Kubernetes and Epic.

For Tensorflow:
1. Create a Training Cluster with a minimum of 2 cores and 8gb ram in the RESTServer and LoadBalancer roles.
2. Create a Jupyter notebook cluster and attach it to the Training Cluster.
3. Upload small_yellow_tripdata_2009-01.csv and lookup-ipyheader.csv to the Project Repo under the data folder.
4. Upload TensorflowPipelineFullTaxiDataSet.ipynb to your Jupyter notebook instance.
5. Train the model by running the cells in the notebook.
6. After training the model, the model should be registered  in the Model Registry. For this, a sample scoring script called TFScoring.py is provided.
7. Create a Deployment Cluster. After deploying the model, query_api_script_tf.py can be used to validate that the deployment works. Postman can also be used.

For XGBoost:
- A truncated dataset (demodata.zip) is provided within the "Taxi Datasets" folder, please unzip it before running the demo.

Datasets:
- demodata.zip (for the XGBoost demo) contains a sample of approximately 375,000 NYC taxi rides from January-June 2019. Pickup and dropoff locations are specified as location ID numbers (lookup-ipyheader.csv contains the appropriate mappings).
- small_yellow_tripdata_2009-01.csv (for the TensorFlow demo) also contains a sample dataset that can be used with the TensorFlow example.
- lookup-ipyheader.csv is a lookup table between location ID numbers and the longitude/latitude coordinates.
