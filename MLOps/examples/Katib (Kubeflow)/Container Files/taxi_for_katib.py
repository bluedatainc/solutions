# To make this taxi demo code work with Katib, there were 2 main changes that were already made in this file:
# 1) Parameters taken in via argparse
# 2) LossHistoryCallback to print out error metrics
# These two changes are further detailed in comments below.



from warnings import simplefilter 
simplefilter(action='ignore', category=FutureWarning)

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Activation,Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model


import urllib
import sys


from scipy import stats
import math
import datetime


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from math import sqrt


listMonthsToTrain = [[2009, 1]]

modelDirectory = '10yrdatasetchecknames'

# Katib reads in parameters via argparse command line arguments that are also specified in the yaml.
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('--first_layer', type=int, default=100)
parser.add_argument('--second_layer', type=int, default=50)
parser.add_argument('--third_layer', type=int, default=25)
parser.add_argument('--batch_size', type=int, default=128)
parser.add_argument('--epochs', type=int, default=5)
parser.add_argument('--verbose', type=int, default=0)
parser.add_argument('--validation_split', type=float, default=0.2)
args = vars(parser.parse_args())


def strAppendZero(month):
    if (month < 10):
        return "0" + str(month)
    else:
        return str(month)


def fileName(year, month, extension):
    year = str(year)
    month = strAppendZero(month)
    return "yellow_tripdata_" + year + "-" + month + "." + extension






# Get full name of the dataframe column by appending the database name to the beginning (a vestige from working with Hive) 
def fullName(colName):
    return dbName + '.' + colName

# Downloads data into the Project Repo if not present, then returns a dataframe containing that data.
def downloadDataDf(year, month):
#    url = baseDataUrl + fileName(year, month, "csv")

    df = pd.read_csv('/opt/taxi/testingalt_yellow_tripdata_2009-01.csv')

    df.columns = [x.lower() for x in df.columns]
    for str in ['vendor_name', 'passenger_count', 'rate_code', 'store_and_forward', 'payment_type', 'fare_amt', 'surcharge', 'mta_tax', 'tip_amt', 'tolls_amt', 'total_amt']:
        if str in df.columns:
            del df[str]
    for str in ['vendor_id', 'passenger_count', 'store_and_fwd_flag', 'fare_amount', 'surcharge', 'tip_amount', 'tolls_amount', 'total_amount', 'congestion_surcharge', 'improvement_surcharge']:
        if str in df.columns:
            del df[str]
    df = df.add_prefix('pqyellowtaxi.')
    return df

def mergeData(df, lookup):
    if fullName('pulocationid') in df.columns:
        df = pd.merge(df, dflook[[lookupDbName + '.location_i', lookupDbName + '.long', lookupDbName + '.lat']], how='left', left_on=dbName + '.pulocationid', right_on=lookupDbName + '.location_i')
        df.rename(columns = {(lookupDbName + '.long'):(dbName + '.startstationlongitude')}, inplace = True)
        df.rename(columns = {(lookupDbName + '.lat'):(dbName + '.startstationlatitude')}, inplace = True)
        df = pd.merge(df, dflook[[lookupDbName + '.location_i', lookupDbName + '.long', lookupDbName + '.lat']], how='left', left_on=dbName + '.dolocationid', right_on=lookupDbName + '.location_i')
        df.rename(columns = {(lookupDbName + '.long'):(dbName + '.endstationlongitude')}, inplace = True)
        df.rename(columns = {(lookupDbName + '.lat'):(dbName + '.endstationlatitude')}, inplace = True)
    else:
        if fullName('pickup_longitude') in df.columns:
            df.rename(columns = {(dbName + '.pickup_longitude'):(dbName + '.startstationlongitude')}, inplace = True)
            df.rename(columns = {(dbName + '.pickup_latitude'):(dbName + '.startstationlatitude')}, inplace = True)
            df.rename(columns = {(dbName + '.dropoff_longitude'):(dbName + '.endstationlongitude')}, inplace = True)
            df.rename(columns = {(dbName + '.dropoff_latitude'):(dbName + '.endstationlatitude')}, inplace = True)
        elif fullName('start_lon') in df.columns:
            df.rename(columns = {(dbName + '.start_lon'):(dbName + '.startstationlongitude')}, inplace = True)
            df.rename(columns = {(dbName + '.start_lat'):(dbName + '.startstationlatitude')}, inplace = True)
            df.rename(columns = {(dbName + '.end_lon'):(dbName + '.endstationlongitude')}, inplace = True)
            df.rename(columns = {(dbName + '.end_lat'):(dbName + '.endstationlatitude')}, inplace = True)
        if fullName('trip_pickup_datetime') in df.columns:
            df.rename(columns = {(dbName + '.trip_pickup_datetime'):(dbName + '.tpep_pickup_datetime')}, inplace = True)
            df.rename(columns = {(dbName + '.trip_dropoff_datetime'):(dbName + '.tpep_dropoff_datetime')}, inplace = True)
        elif fullName('pickup_datetime') in df.columns:
            df.rename(columns = {(dbName + '.pickup_datetime'):(dbName + '.tpep_pickup_datetime')}, inplace = True)
            df.rename(columns = {(dbName + '.dropoff_datetime'):(dbName + '.tpep_dropoff_datetime')}, inplace = True)
    return df
    

    
def generateFeatures(df):
    df[dbName + '.tpep_pickup_datetime'] = pd.to_datetime(df[dbName + '.tpep_pickup_datetime'])
    df[dbName + '.tpep_dropoff_datetime'] = pd.to_datetime(df[dbName + '.tpep_dropoff_datetime'])
    df[fullName('duration')] = (df[fullName("tpep_dropoff_datetime")] - df[fullName("tpep_pickup_datetime")]).dt.total_seconds()

    df[fullName("weekday")] = (df[fullName('tpep_pickup_datetime')].dt.dayofweek < 5).astype(float)
    df[fullName("hour")] = df[fullName('tpep_pickup_datetime')].dt.hour
    df[fullName("work")] = (df[fullName('weekday')] == 1) & (df[fullName("hour")] >= 8) & (df[fullName("hour")] < 18)
    return df
    
def removeOutliers(df):
    df = df[df[fullName('duration')] > 20]
    df = df[df[fullName('duration')] < 10800]
    df = df[df[fullName('trip_distance')] > 0]
    df = df[df[fullName('trip_distance')] < 150]
    return df

dbName = "pqyellowtaxi"
lookupDbName = "pqlookup"
dflook = 0


# This printout of error metrics is necessary for Katib to work. In this example, I printed out to stdout. If the metricsCollectorSpec in the yaml file is changed, error metrics can also be read from a file in the container.
ep = 1
class LossHistoryCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, batch, logs=None):
        global ep        
        print("epoch " + str(ep) + ":")
        print("mean_squared_error=" + str(logs['mean_squared_error']))
        print("root_mean_squared_error=" + str(sqrt(logs['mean_squared_error'])))
        print()
        ep = ep + 1


for step in range(0, len(listMonthsToTrain)):   
    year, month = listMonthsToTrain[step]
    

    df = downloadDataDf(year, month)

    df = mergeData(df, dflook)

    df = generateFeatures(df)

    df = removeOutliers(df)



    cols = [fullName('work'), fullName('startstationlatitude'), fullName('startstationlongitude'), fullName('endstationlatitude'), fullName('endstationlongitude'), fullName('trip_distance'), fullName('weekday'), fullName('hour'), fullName('duration')]
    dataset = df[cols]
    dataset = dataset.dropna(how='any',axis=0)

    del df

    X = dataset.iloc[:, 0:(len(cols) - 1)].values
    y = dataset.iloc[:, (len(cols) - 1)].values
    X = X.copy()
    y = y.copy()


    del dataset




    X_train,X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)




    
    input_layer = Input(shape=(X.shape[1],))
    dense_layer_1 = Dense(args['first_layer'], activation='relu')(input_layer)
    dense_layer_2 = Dense(args['second_layer'], activation='relu')(dense_layer_1)
    dense_layer_3 = Dense(args['third_layer'], activation='relu')(dense_layer_2)
    output = Dense(1)(dense_layer_3)
    model = Model(inputs=input_layer, outputs=output)
    model.compile(loss="mean_squared_error" , optimizer="adam", metrics=["mean_squared_error"])        


    history_callback = model.fit(X_train, y_train, batch_size=args['batch_size'], epochs=args['epochs'], verbose=args['verbose'], validation_split=args['validation_split'], callbacks=[LossHistoryCallback()])


    loss_history = history_callback.history["loss"]

    lossHistoryDirPath = 'models/' + modelDirectory + '/' + 'history'
    lossHistoryFilePath = lossHistoryDirPath + '/' + str(step) + '.txt'
    

    y_pred = model.predict(X_test)
    y_pred = y_pred.clip(min=0)

  


