import sys

from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.util import MLUtils
from pyspark import SparkContext, SparkConf

# #Spark Config
conf = SparkConf().setAppName("sample_app")
sc = SparkContext(conf=conf)

# Load and parse the data file into an RDD of LabeledPoint.

data = MLUtils.loadLibSVMFile(sc, 'dtap://TenantStorage/data/sample_libsvm_data.txt')
# Split the data into training and test sets (30% held out for testing)
(trainingData, testData) = data.randomSplit([0.7, 0.3])

# Train a RandomForest model.
#  Empty categoricalFeaturesInfo indicates all features are continuous.
#  Note: Use larger numTrees in practice.
#  Setting featureSubsetStrategy="auto" lets the algorithm choose.

model = RandomForest.trainRegressor(trainingData, categoricalFeaturesInfo={},
                                    numTrees=3, featureSubsetStrategy="auto",
                                    impurity='variance', maxDepth=4, maxBins=32)                   
# Evaluate model on test instances and compute test error

predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
testMSE = labelsAndPredictions.map(lambda vp : (vp[0] - vp[1]) * (vp[0] - vp[1])).sum() /\
    float(testData.count())
print('Test Mean Squared Error = ' + str(testMSE))
print('Learned regression forest model:')
print(model.toDebugString())

# Save and load model
model.save(sc, "dtap://TenantStorage/output_test")
sameModel = RandomForestModel.load(sc, "dtap://TenantStorage/output_test")
print(sameModel)
