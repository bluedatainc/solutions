import numpy as np
import pandas as pd
import os
import xgboost as xgb
import pickle
import json
import sys
from sklearn.metrics import accuracy_score

# Function for obtaining NFS path


def saveInProjectRepo(path):
    ProjectRepo = "/bd-fs-mnt/project_repo"
    return str(ProjectRepo + '/' + path)

# Loading XGB model file
# final_gb = xgb.Booster() #init model
# final_gb.load_model(saveInProjectRepo('models/XGB_Income/XGB.pickle.dat'))


# Loading XGB pickle file
final_gb = pickle.load(
    open(saveInProjectRepo('models/') + "XGB.pickle.dat", "rb"))

# Loading encoding file
# with open(saveInProjectRepo('data/encoding.json'), 'r') as file:
#    encoding = json.load(file)

# -----Reading from commandline from deployment as json
cli_input = json.loads(sys.argv[1])
test_columns = ['pqyellowtaxi.work', 'pqyellowtaxi.startstationlatitude', 'pqyellowtaxi.startstationlongitude',
                'pqyellowtaxi.endstationlatitude', 'pqyellowtaxi.endstationlongitude', 'pqyellowtaxi.trip_distance',
                'pqyellowtaxi.weekday', 'pqyellowtaxi.hour', 'pqyellowtaxi.month_1', 'pqyellowtaxi.month_2',
                'pqyellowtaxi.month_3', 'pqyellowtaxi.month_4', 'pqyellowtaxi.month_5', 'pqyellowtaxi.month_6']

# Encoding features with string values
# for feature in cli_input:
#	if feature in encoding:
#		for e in encoding[feature]:
#			if cli_input[feature] == e:
#				cli_input[feature] = encoding[feature][e]

# We convert the features to a readable format in the POSTMAN call. f0, f1, f2, ... are replaced by verbose feature names
# For xgb model, we convert these back to the f[0-13] format. 

# list of features from POST call
ip_keys = ["work", "start_latitude", "start_longitude", "end_latitude", "end_longitude",
           "distance", "weekday", "hour", "month_1", "month_2", "month_3", "month_4", "month_5", "month_6"]

# create a list expected by xgb model
ftr = ["f"+str(i) for i in range(0, 14)]

# map new values to old values
map_d = dict(zip(ftr, ip_keys))
for key, value in map_d.items():
    map_d[key] = cli_input[value]
# Formating data for prediction
# print(str(map_d))
df = pd.DataFrame(map_d, index=[0])
#testdmat = xgb.DMatrix(df)
y_pred = final_gb.predict(df)

# Using 0.5 as threshold for the wage class prediction
# 0 - 0.50 = '<=50k'
# 0.51 - 1 = '>50k'
# if y_pred[0] > 0.5:
#	print("Prediction: >50K with " + str( round(y_pred[0] * 100,2)) + "% confidence.")
# else:
#	print("Prediction: <=50K with " +  str( round((1-y_pred[0]) * 100, 2)) + "% confidence.")

print("The ride duration prediction is " + str(y_pred[0]) + " seconds.")


"""
 {
        "work": 0,
        "start_latitude": 40.57689727,
        "start_longitude": -73.99047356,
        "end_latitude": 40.72058154,
        "end_longitude": -73.99740673,
        "distance": 8,
        "weekday": 1,
        "hour": 9,
        "month_1": 0,
        "month_2": 1,
        "month_3": 0,
        "month_4": 0,
        "month_5": 0,
        "month_6": 0
    }
"""
