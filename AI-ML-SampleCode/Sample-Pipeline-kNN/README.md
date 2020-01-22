This is a Sample ML pipeline showcasing bluedata's MLOPs module
In this example we are using MNIST database to find handwritten digits.

Dataset can be downloaded from - http://yann.lecun.com/exdb/mnist/

Four files are available on this site:

1. train-images-idx3-ubyte.gz:  training set images (9912422 bytes)
2. train-labels-idx1-ubyte.gz:  training set labels (28881 bytes)
3. t10k-images-idx3-ubyte.gz:   test set images (1648877 bytes)
4. t10k-labels-idx1-ubyte.gz:   test set labels (4542 bytes)


Once these are downloaded, change the name(s) to 
1. train-images-idx3-ubyte.gz -> train-images
2. train-labels-idx1-ubyte.gz -> train-labels
3. t10k-images-idx3-ubyte.gz  -> test-images
4. t10k-labels-idx1-ubyte.gz  -> test-labels



Steps to run this pipeline

1. Download the dataset above and dump it under data/ directory in your project repo
2. Rename the files as described above
3. Create training cluster (Python ML and DL Toolkit)
4. Open Jupyter notebook and import first notebook - Decompose images and execute
5. Next import kNN in Training Enviornment notebook and execute
6. Last step would spit out a model, which you could then register with EPIC
7. While registering the model usee kNN_scrring.py script
8. Next create deployment cluster (Python ML/DL Toolkit) with model registered in previous step as attached model
9. Once deployment cluster comes up use the loadbalancer URL to make REST API calls to serve the model (this can be done using any REST client like 
postman, python request , curl etc)
10. POST JSON for this example - 



