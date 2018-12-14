from pyspark import SparkConf, SparkContext
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.feature import IDF
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

spark = SparkSession.builder.appName("tfidf").config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.2.0").getOrCreate()
df =  spark.read.format("com.mongodb.spark.sql.DefaultSource").option("uri","mongodb://user:indeedjob@ec2-52-55-205-188.compute-1.amazonaws.com/appDatabase.jobs").load()
data = df.select('job_title_label','job_description_cleaned2')
data = data.filter(data.job_title_label != 'unknown')
countVectors = CountVectorizer(inputCol="job_description_cleaned2", outputCol="features", vocabSize=20000, minDF=5)
#countVectors = CountVectorizer(inputCol="job_description_cleaned2", outputCol="rawfeatures", vocabSize=20000, minDF=5)
#idf = IDF(inputCol='rawfeatures', outputCol="features", minDocFreq=5)
label_stringIdx = StringIndexer(inputCol = "job_title_label", outputCol = "label")
pipeline = Pipeline(stages=[countVectors, label_stringIdx])
pipelineFit = pipeline.fit(data)
dataset = pipelineFit.transform(data)
(trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed = 100)
lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)
lrModel = lr.fit(trainingData)
predictions = lrModel.transform(testData)
evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
print(evaluator.evaluate(predictions))

#with count vectoriser and idf 72.7% accuracy
#without idf 72.89% accuracy