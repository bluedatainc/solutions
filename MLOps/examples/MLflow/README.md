The following tutorial can be used to test Mlflow using KD apps untill registering a model on mlflow.
Once A KD notebook instance is ready with KD mlflow instance and mlflow secret attached to it, upload the following two files in the workspace:
1) train.ipynb
2) wine-quality.csv

Before running the cells, make sure to create a bucket with the name provided in mlflow secret in minio service if using the internal minio for s3 bucket.
Run all the cells to execute 3 runs of experiemnt 'demoexp' from KD notebook app and one run of exp 'demoexp-training' from KD training engine app.
The registered experiment's artifacts can be seen in mlflow tracking service. 
Click on the run and then click on the artifacts to register model.
To physically access the files related to the run, access them in minio s3 from the path provided in run page of mlflow.
