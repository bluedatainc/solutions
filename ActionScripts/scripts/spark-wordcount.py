textFile = sc.textFile("dtap://TenantStorage/spark.test.text")  
counts = textFile.flatMap(lambda line: line.split(" ")) .map(lambda word: (word, 1)) .reduceByKey(lambda a, b: a + b) 
print(counts.collect()) 
