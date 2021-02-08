import numpy as np
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import tensorflow as tf
from tensorflow.keras.models import load_model
import json
import sys
from sklearn.metrics import accuracy_score
import pickle

#Function for obtaining NFS path
def saveInProjectRepo(path):
    ProjectRepo = "/bd-fs-mnt/project_repo"
    return str(ProjectRepo + '/' + path)

model = load_model(saveInProjectRepo('models/testmodel/0_tf'))

# -----Reading from commandline from deployment as json
cli_input = json.loads(sys.argv[1])

#Formating data for prediction
df = pd.DataFrame(cli_input, index=[0])
sc = pickle.load(open(saveInProjectRepo('models/testmodel/scaler.pkl'), 'rb'))
df = sc.transform(df)
y_pred = model.predict(df)

print("The ride duration prediction is " + str(y_pred[0][0]) + " seconds.")