# Add Spark Python Files to Python Path
import sys
import os
SPARK_HOME = "/opt/bitnami/spark" # Set this to wherever you have compiled Spark
os.environ["SPARK_HOME"] = SPARK_HOME # Add Spark path
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1" # Set Local IP
sys.path.append( SPARK_HOME + "/python") # Add python files to Python Path

import pyspark
from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark import SparkConf, SparkContext

def turn_iris_to_sc(sc):
    from sklearn import datasets
    iris = datasets.load_iris()
    iris_target = iris['target']
    table = list(map(lambda a, b: a+[b], iris['data'].tolist(), iris['target']))
    return sc.parallelize(table)


def distanceAbs(training, test, numfields = 4):
    ret = 0
    #training = training.collect() #test = training.collect()
    print
    for i in range(numfields):
        ret += abs(float(training[i])-float(test[i]))
    return ret

def accuracy_score(test , li, k):
    ret = 0
    #print("debug:", test, li)
    dic = { test[4]:0 }
    for i in range(k):
        if li[i][1] in dic.keys() :
            dic[ li[i][1] ] += 1
        else:
            dic[ li[i][1] ] = 1
    
    for i in dic.keys():
        if dic[test[4]] < dic[i]:
            return 0
    return 1


def KNN(input_data='./dis.txt',_numfields=4, _numNearestNeigbours=5 ):

    # prepare sc
    sc = pyspark.SparkContext()
    opt_file = 'output'

    # prepare data
    if input_data == 'buildin_iris':
        total_data = turn_iris_to_sc(sc)
    else:
        # url= './dis.txt'
        text_file = sc.textFile(input_data)
        total_data = text_file.map(lambda line: line.split(" "))

    testset,trainingset = total_data.randomSplit([3,7], 10)

    numfields = _numfields # Feature columns
    numNearestNeigbours = _numNearestNeigbours # K

    print("test set:", testset.collect(),"\n================\n")

    counts = testset.cartesian(trainingset) \
    .map(lambda tt : (tt[0], distanceAbs(tt[0], tt[1], numfields), tt[1][4]))\
    .map(lambda p: (tuple(p[0]), (p[1], p[2])) ) \
    .groupByKey().map(lambda p: (p[0], sorted(p[1]) ) )\
    .map( lambda t: accuracy_score(t[0], t[1], numNearestNeigbours))

    print("[debug]: in final.py :", counts.collect())
    ret = counts.collect()
    sc.stop()
    return ret

#KNN()