import numpy as np
import pandas as pd
import os
import xgboost as xgb
import pickle
import json
import sys 
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

#Function for obtaining NFS path
def saveInProjectRepo(path):
   ProjectRepo = os.popen('bdvcli --get cluster.project_repo').read().rstrip()
   return str(ProjectRepo + '/' + path)

#Loading XGB model file 
#final_gb = xgb.Booster() #init model
#final_gb.load_model(saveInProjectRepo('models/XGB_Income/XGB.model'))

#Loading XGB pickle file 
final_gb = pickle.load(open(saveInProjectRepo('models/XGB_Income/') + "XGB.pickle.dat", "rb"))

#Loading encoding file 
with open(saveInProjectRepo('data/UCI_Income/encoding.json'), 'r') as file:
    encoding = json.load(file)

# -----Reading from commandline from deployment as json
cli_input = json.loads(sys.argv[1])
test_columns= ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status', 'occupation', 
              'relationship', 'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week', 'native_country']

#Encoding features with string values 
for feature in cli_input:
	if feature in encoding:
		for e in encoding[feature]:
			if cli_input[feature] == e:
				cli_input[feature] = encoding[feature][e]

#Formating data for prediction 
df = pd.DataFrame(cli_input, index=[0])
testdmat = xgb.DMatrix(df)
y_pred = final_gb.predict(testdmat)

#Using 0.5 as threshold for the wage class prediction
# 0 - 0.50 = '<=50k'
# 0.51 - 1 = '>50k'
if y_pred[0] > 0.5:
	print("Prediction: >50K with " + str( round(y_pred[0] * 100,2)) + "% confidence.")
else:
	print("Prediction: <=50K with " +  str( round((1-y_pred[0]) * 100, 2)) + "% confidence.")


