from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("WordCountJob") \
    .getOrCreate()

# Sample text
text = "Hello Spark Hello Python Hello Airflow Hello Docker Hello Himanshu"

# Simple word count using RDD
words = spark.sparkContext.parallelize(text.split(" "))
word_counts = words.map(lambda word: (word, 1)) \
                   .reduceByKey(lambda a, b: a + b)

# Print results
print("=== Word Count Results ===")
for word, count in sorted(word_counts.collect()):
    print(f"{word}: {count}")

spark.stop()
