from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("MyApp")
SparkContext.getOrCreate(conf=conf)
