from pyspark import SparkConf, SparkContext
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.feature import IDF
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.ml.feature import StringIndexer, IndexToString
from pyspark.ml import Pipeline
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import CountVectorizerModel
from pyspark.sql import SQLContext
import pickle
import numpy as np

spark = SparkSession.builder.appName("tfidf").config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.2.0").getOrCreate()
df =  spark.read.format("com.mongodb.spark.sql.DefaultSource").option("uri","mongodb://user:indeedjob@ec2-52-55-205-188.compute-1.amazonaws.com/appDatabase.jobs").load()
data = df.select('job_title_label','job_description_cleaned')
data = data.filter(data.job_title_label != 'unknown')
countVectors = CountVectorizer(inputCol="job_description_cleaned", outputCol="features", vocabSize=20000, minDF=5)
label_stringIdx = StringIndexer(inputCol = "job_title_label", outputCol = "label")
pipeline = Pipeline(stages=[countVectors, label_stringIdx])
pipelineFit = pipeline.fit(data)
dataset = pipelineFit.transform(data)
(trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed = 100)
lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)
lrModel = lr.fit(dataset)
stages = pipelineFit.stages
vectorizers = [s for s in stages if isinstance(s, CountVectorizerModel)]
vocab = vectorizers[0].vocabulary
coeff = lrModel.coefficientMatrix
inter = lrModel.interceptVector
coeff_array = coeff.toArray()
inter_array = inter.toArray()
np.save('coeff_array.npy', coeff_array)
np.save('inter_array.npy', inter_array)
np.save('coeff_array.npy', coeff_array)
with open('vocabfile.pkl', 'wb') as fp:
	pickle.dump(vocab, fp)





