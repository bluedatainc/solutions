<span style="color:#f2cf4a; font-family: 'Bookman Old Style';">

# Datascience-Pipelines

  - [1. JupyterHub Server with Spark2.1.1](#1-jupyterhub-server-with-spark2.1.1)
  - [2. Nifi or HDF2.1 with embedded Zookeepers](#2-nifi-or-hdf2.1-with-embedded-zookeepers)
  - [3. Kafka Spark and Cassandra pipeline in BlueData](#3-kafka-spark-and-cassandra-pipeline-in-bluedata)
  - [4. RStudio Server with Spark 2.1.0 ](#4-rstudio-server-with-spark-2.1.0)

  
## 1. JupyterHub Server with Spark2.1.1

_Location_: https://s3.amazonaws.com/bluedata-catalog/solutions/bins/bdcatalog-centos-bluedata-jupyterhubsp-1.2.bin

_DistroId_: bluedata/jupyterhubsp

_Version_: 1.2

_Category_: Notebooks

_Software Included_: 

      Jupyterhub version - 0.7.2
      Python 3.6.0 |Anaconda 4.3.1 (64-bit)
      Anaconda on Python 3 : conda 4.3.14
      Spark-2.1.1-bin-hadoop2.6, configured to run on Python 3
      Jupyter Toree kernels - Scala, PySpark, SQL (toree-0.2.0.dev1.tar.gz)

_Jupyterhub access_:

     Jupyterhub server  - Create a OS user for each user who needs access on cluster controller node.
     ‘sudo useradd test’
     ‘sudo passwd test’ -> provide password  
     Login with test/password

_Systemv Service names and commands_:

     sudo service jupyterhub status (start, stop)
     sudo service spark-master status (start, stop)
     sudo service spak-slave status (start, stop)


_OS_: Centos. Works with both Bluedata Centos and RHEL hosts


_Sample Code for Testing_:

     1. Create a linux user on master controller node
     2. Login

_Spark Scala testing_:
     
     3. Start a toree scala kernel -> Wait till kernel creates a spark shell. Run following Pearson’s correlation. You can run upto 4 Spark shells with current configurations. If your shell doesn’t start, you may have used up all the cores. Kill unused Kernels to release resources
     Code : Running Pearson’s correlation using mllib
     
     import org.apache.spark.mllib.linalg._
     import org.apache.spark.mllib.stat.Statistics
     import org.apache.spark.rdd.RDD
     val seriesX: RDD[Double] = sc.parallelize(Array(1, 2, 3, 3, 5))  // a series
     // must have the same number of partitions and cardinality as seriesX
     val seriesY: RDD[Double] = sc.parallelize(Array(11, 22, 33, 33, 555))
     // compute the correlation using Pearson's method. Enter "spearman" for Spearman's method. If  a
     // method is not specified, Pearson's method will be used by default.
     val correlation: Double = Statistics.corr(seriesX, seriesY, "pearson")
     println(s"Correlation is: $correlation")
     val data: RDD[Vector] = sc.parallelize(
      Seq(
        Vectors.dense(1.0, 10.0, 100.0),
        Vectors.dense(2.0, 20.0, 200.0),
        Vectors.dense(5.0, 33.0, 366.0))
        )  // note that each Vector is a row and not a column
        // calculate the correlation matrix using Pearson's method. Use "spearman" for Spearman's method
        // If a method is not specified, Pearson's method will be used by default.
        val correlMatrix: Matrix = Statistics.corr(data, "pearson")
        println(correlMatrix.toString)
 

_Input_:  Input is generated within the code. No external input is provided.
 
 
_Output_: Sample output is as given below.
 
 
_PySpark testing_:
 
 
     4. Start a toree pySpark kernel -> Wait till kernel creates a spark shell. You can run upto 4 Spark shells with current configurations. If your shell doesn’t start, you may have used up all the cores. Kill unused Kernels to release resources.
     Code: 
     from pyspark import SparkConf, SparkContext
     from sklearn.datasets import make_classification
     from sklearn.ensemble import ExtraTreesClassifier
     import pandas as pd
     import numpy as np
     # Build a classification task using 3 informative features
     X, y = make_classification(n_samples=12000,
                        n_features=10,
                        n_informative=3,
                        n_redundant=0,
                        n_repeated=0,
                        n_classes=2,
                        random_state=0,
                        shuffle=False)
    # Partition data
    def dataPart(X, y, start, stop): return dict(X=X[start:stop, :], y=y[start:stop])
    def train(data):
        X = data['X']
        y = data['y']
        return ExtraTreesClassifier(n_estimators=100,random_state=0).fit(X,y)
    # Merge 2 Models
    from sklearn.base import copy
    def merge(left,right):
        new = copy.deepcopy(left)
        new.estimators_ += right.estimators_
        new.n_estimators = len(new.estimators_) 
        return new
    data = [dataPart(X, y, 0, 4000), dataPart(X,y,4000,8000),dataPart(X,y,8000,12000)]
    forest = sc.parallelize(data).map(train).reduce(merge)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
          axis=0)
    indices = np.argsort(importances)[::-1]
    # Print the feature ranking
    print("Feature ranking:")
    for f in range(10):
            print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
 
 
_Input_: No input files used. Data is generated in the code. 
 
_Output_: Sample output is as given below.
 


## 2. Nifi or HDF2.1 with embedded Zookeepers
 
_Location_: https://s3.amazonaws.com/bluedata-catalog/solutions/bins/bdcatalog-centos-bluedata-hdf21base-3.0.bin

_DistroId_: bluedata/hdf21base

_Version_: 3.0

_Category_: ETLTools

_Software Included_: 

      java version "1.8.0_40"
      nifi-1.1.0.2.1.2.0-10-bin.tar.gz
      zookeeper-3.4.6.tar.gz


_Notebook access_:

     Nifi UI (open to everyone, once deployed)

_Systemv Service names and commands_:

     sudo service HDF-master status (stop, start)
     sudo service HDF-slave status(stop, start)
     sudo service Zookeeper-service status (start, stop)



_OS_: Centos6. Works on both Centos and RHEL base machines


_Sample workflow for Testing_:

     1. Let us build a small flow on NiFi canvas to read app log generated by NiFi itself to feed to Spark:
     2. Drop a "TailFile" Processor to canvas to read lines added to"/opt/HDF-2.1.1/nifi-1.1.0.2.1.1.0-2/logs/nifi-app.log". Auto Terminate relationship Failure.
     <image>
     3. Drop a "SplitText" Processor to canvas to split the log file into separate lines. Auto terminate Original and Failure Relationship for now. Connect TailFile processor to SplitText Processor for Success Relationship.
     <image>

     4. Drop a "ExtractText" Processor to canvas to extract portions of the log content to attributes as below. Connect SplitText processor to ExtractText Processor for splits relationship.
        - BULLETIN_LEVEL:([A-Z]{4,5})
        - CONTENT:(^.*)
        - EVENT_DATE:([^,]*)
        - EVENT_TYPE:(?<=\[)(.*?)(?=\])
     <image>
     5. Now create a PutFile Processor to store end result in local.
     <image>
     6. The final workflow looks like the image below.
     <image>
 
_Output_: Sample output is as given below. 

    <image>   
 


## 3. Kafka Spark and Cassandra pipeline in BlueData 
 
 
_Location_: 

_DistroId_: 

_Version_: 

_Category_: Notebooks

_Software Included_: 

      
 

_Sample code for Testing_: 
 
_Description_:

    The sample program is designed to do the following:
        1.Generate “consumer complaints” topics generated periodically from a file downloaded from data.gov, into a Kafka queue called “consumer_complaints”

        2.Spark cluster will read these complaints and process them on an on-going basis
        3.Processed complaints are then stored in Cassandra for iterative and further use.

_Generate Kafka events_:
 
       1.Log into Kafka cluster command line using “ssh -i “Tenant Keypair” bluedata@kafka-node-ip
       2.Create a new “src” directory. CD to src
       3.Setup the environment for running applications
                a.Install Maven to build the sample code using standard Maven documentation. Sample installation from http://preilly.me/2013/05/10/how-to-install-maven-on-centos/
                        i) $ wget http://mirror.cc.columbia.edu/pub/software/apache/maven/maven-3/3.0.5/binaries/apache-maven-3.0.5-bin.tar.gz
                        ii) $ sudo tar xzf apache-maven-3.0.5-bin.tar.gz -C /usr/local
                        iii) $ cd /usr/local
                        iv) $ sudo ln -s apache-maven-3.0.5 maven
                        v) $ sudo vi /etc/profile.d/maven.sh
                                export M2_HOME=/usr/local/maven
                                export PATH=${M2_HOME}/bin:${PATH}
                b.Exit and re-login. cd to src.
                c.Run “mvn -version” and validate maven home and java home variables
        4.If you don’t have git installed, run “sudo yum install git”
        5.git clone https://github.com/nandav/Realtime-Pipeline.git
        6.cd to “Realtime-Pipeline”
        7.tar -xvzf Consumer.tgz -C ./file-producer/
        8.cd to “file-producer”
        9.Edit  “src/main/resources/config.properties”. Update the hostname “bluedata-175.bdlocal” with your kafka hostname
        10.Run the command “mvn clean install”. If all goes well you should see success when this command finishes running. 
        11.Create a kafka topic called “consumer_complains” by running the following command. Be sure to change the <hostname> with the name of your kafka machine.
            /usr/local/kafka_2.10-0.8.2.2/bin/kafka-topics.sh --create  --zookeeper <hostname>:2181 --replication-factor 1 --partition 1 --topic consumer_complaints
        12.Run the command “java -cp target/kafkamessages-0.0.1-SNAPSHOT.jar com.bluedata.messages.TestProducer 10”
        13.You should see producer creating messages
        14.<ctrl> c (kill process )now to stop the messages at this point. 
 
_Consume Kafka events and add data to a Cassandra table using Spark streaming_:
 
      1.Login to Spark cluster master using “ssh -i “Tenant KeyPair” bluedata@spark-master-ip
      2.Create a directory src.  “mkdir src”. Then “cd src”
      3.You need sbt to build the source code. Install sbt using standard sbt documentation. A sample installation is given here. Following this should also work
      
      wget http://dl.bintray.com/sbt/rpm/sbt-0.13.5.rpm
      sudo yum localinstall sbt-0.13.5.rpm
      
      4.Install git to clone “Spark consumer” for consumer complaints. <sudo yum install git>
      5.git clone https://github.com/nandav/Realtime-Pipeline.git
      6.cd into “Realtime-Pipeline”
      7.cd into “spark_consumer”
      8.Edit “consumer.conf” file. Modify “spark.master”,  “spark.kafka.broker”, and “spark.cassandra.connection.host” to point to  the right hosts. spark master should be the hostname of spark master. Kafka broker to point to first node of kafka cluster. Similarly, update Cassandra connection host to the ip address of Cassandra first node. 
      9.Run “sbt assembly”. Runs for sometime and downloads all the dependencies for Kafka and Cassandra from Spark. 
      10.Run “sudo bash” to login as root to the container. There are some log files that need “root” permission. 
      11.If you like less verbose logs from Spark, edit the following file and update INFO to ERROR as shown below. 
            a.vi /usr/lib/spark/spark-1.4.0-bin-hadoop2.4/conf/log4j.properties  (If you have a different version of Spark, be sure to replace 1.4 with your version of Spark in “build.sbt”). Cassandra connector is 1.5.0 of Spark
            b.Update line “log4j.rootLogger=” from INFO to ERROR
            c.Modified line looks like “log4j.rootLogger=ERROR, file, stdout ,stderr”
      12.Run the following command. Be sure to update <SparkMaster> with actual Spark Master hostname.  spark-submit --properties-file consumer.conf --class KafkaSparkCassandra --master spark://<SparkMaster>:7077 target/scala-2.10/kafka-streaming-cassandra-assembly-1.0.jar
 
_Check updates on Cassandra cluster_:

      3.Login to Cassandra cluster using “ssh -i “Tenant KeyPair” bluedata@<Cassandra_Node>
      4.Run “export CQLSH_HOST=<IP of first cassandra node>”. 
        Example: export CQLSH_HOST=10.39.249.18
      5.Run “cqlsh”
      6.Type command “describe keyspaces;”. You should see ‘bluedata’ as one of the key spaces. 
      7.Type “use bluedata;”
      8.Type “describe tables;”. You should see a table called ‘consumer_complaints’
      9.Type “select count(*) from consumer_complaints;”. Counts should keep increasing. 
      10.Type “Select * from consumer_complaints;”.
 
_Summary_:
 
       At the end of this workflow, you should see that Kafka is reading a file, creating messages into Kafka queue. Spark streaming is processing it and storing it in Cassandra. This is a powerful workflow that can be altered to suit your needs. 
 
 
_Running sample 2_:

_Description_:

      The sample program is designed to do the following:
        1.Collect tweets into a Kafka queue called “twitter-topic”
        2.Spark cluster will read these tweets and process popular hashtags in last 60 seconds, on a continuous basis
 
_Generate Kafka events_:

      1.Log into Kafka cluster command line using “ssh -i “Tenant Keypair” bluedata@kafka-node-ip
      2.Create a new “src” directory. CD to src
      3.Setup the environment for running applications
            a.Install Maven to build the sample code using standard Maven documentation. Sample installation from http://preilly.me/2013/05/10/how-to-install-maven-on-centos/
                    i. $ wget http://mirror.cc.columbia.edu/pub/software/apache/maven/maven-3/3.0.5/binaries/apache-maven-3.0.5-bin.tar.gz
                    ii. $ sudo tar xzf apache-maven-3.0.5-bin.tar.gz -C /usr/local
                    iii. $ cd /usr/local
                    iv. $ sudo ln -s apache-maven-3.0.5 maven
                    v.$ sudo vi /etc/profile.d/maven.sh
                            export M2_HOME=/usr/local/maven
                            export PATH=${M2_HOME}/bin:${PATH}
            b.Exit and log back into the shell
            c.Run mvn -version and validate maven home and java home variables
      4.If you don’t have git installed, run “sudo yum install git”
      5.git clone https://github.com/nandav/twitter-producer.git
      6.cd to “twitter-producer”
      7.Edit  “config.properties”. Update the hostname  with your kafka hostname and change all twitter access credentials to your credentials. If you do not have twitter app credentials, please login to apps.twitter.com->Create New App following directions. You should be able to obtain all 4 credentials. 
      8.Run the command “mvn clean install”. If all goes well you should see success when this command finishes running. 
      9.Create a kafka topic called “twitter-topic” by running the following command. Please make sure to change <hostname> to appropriate name, It is the first node of Kafka cluster where zookeeper is installed. Mostly your current logged in machine. “/usr/local/kafka_2.10-0.8.2.2/bin/kafka-topics.sh --create  --zookeeper <hostname>:2181 --replication-factor 1 --partition 1 --topic twitter-topic”
      10.Start twitter producer using the following command “java -cp target/kafkamessages-0.0.1-SNAPSHOT.jar com.bluedata.messages.TwitterKafkaProducer”
      11.Open a new shell window and start a kafka console consumer.  Be sure to change name of kafka-first-name before running the command. /usr/local/kafka_2.10-0.8.2.2/bin/kafka-console-consumer.sh --zookeeper <kafka-first-node>:2181 --topic twitter-topic
 
 
_Consume Kafka events using Spark streaming_:

      1.Login to Spark cluster master using “ssh -i “Tenant KeyPair” bluedata@spark-master-ip
      2.Create a directory src.  “mkdir src”. Then “cd src”
      3.You need sbt to build the source code. Install sbt using standard sbt documentation. A sample installation is given here. Following this should also work
      4.wget http://dl.bintray.com/sbt/rpm/sbt-0.13.5.rpm
      5.sudo yum localinstall sbt-0.13.5.rpm
      6.Install git to clone “Spark consumer” for Kafka tweets. <sudo yum install git>
      7.git clone https://github.com/nandav/twitter-spark-consumer.git
      8.cd into “twitter-spark-consumer/
      9.Edit “consumer.conf” file. Modify “spark.master”,  “spark.kafka.broker”, to point to  the right hosts. spark master should be the hostname of spark master. Kafka broker to point to first node of kafka cluster.
      10.Run “sbt assembly”. Runs for sometime and downloads all the dependencies for Kafka and Spark Streaming. (If you have a different version of Spark, be sure to replace 1.4 with your version of Spark in “build.sbt”)
      11.Run “sudo bash” to login as root to the container. There are some files that need “root” permission. 
      12.If you like less verbose logs from Spark, edit the following file and update INFO to ERROR as shown below. 
                a.vi /usr/lib/spark/spark-1.4.0-bin-hadoop2.4/conf/log4j.properties (Or modify the spark directory to reflect your cluster)
                b.Update line “log4j.rootLogger=” from INFO to ERROR
                c.Modified line looks like “log4j.rootLogger=ERROR, file, stdout ,stderr”
      13.Run the following command “spark-submit --properties-file consumer.conf --class KafkaSparkStreaming --master spark://<Spark-master>:7077 target/scala-2.10/kafka-streaming-assembly-1.0.jar”
      14.You should see popular hashtags in last 60 seconds in rolling fashion 
      15.End producer and consumer  using <ctrl> c - kill the process


 
## 4. R-Studio Server with Spark 2.1.0 
 
 
_Location_: https://s3.amazonaws.com/bluedata-catalog/solutions/bins/bdcatalog-centos-bluedata-rstudio136sp210-3.0.bin

_DistroId_: bluedata/rstudio136sp210

_Version_: 3.0

_Category_: DataScience

_Software Included_: 

      R version 3.3.2
      R libraries pre-installed on all nodes - sparklyr, devtools, knitr, tidyr, ggplot2, shiny
      R Hadoop client for accessing HDFS from R - rHadoopClient_0.2.tar.gz
      spark-2.1.0-bin-hadoop2.6

 
_R-Studio access_:

     R-Studio Server - Create a OS user for each user who needs access on cluster controller node.
     ‘sudo useradd test’
     ‘sudo passwd test’ -> provide password 
     Login with test/test


_Systemv Service names and commands_:

     sudo service rstudioserver status (start, stop)
     sudo service spark-master status (start, stop)
     sudo service spak-slave status (start, stop)


_OS_: Centos. Works on both Centos and RHEL base machines


_Sample code for Testing_: 
 
_Base-R Testing_:

    data(iris)  # Load the dataset iris
    str(iris)  # Structure of the dataset
    mean(iris$Sepal.Length)
    str(iris$Sepal.Length)
    tapply(iris$Sepal.Length, iris$Species, mean)

_Sparklyr Testing_: 
 
     if (nchar(Sys.getenv("SPARK_HOME")) < 1) {
        Sys.setenv(SPARK_HOME = "/usr/lib/spark/spark-2.1.0-bin-hadoop2.6")}
     library(sparklyr)
     sc <- spark_connect(master = "spark://bluedata-266.bdlocal:7077")  (*Replace with your master)
     # Simple Test
     data(iris)  # Load the dataset iris
     str(iris)  # Structure of the dataset
     mean(iris$Sepal.Length)
     str(iris$Sepal.Length)
     tapply(iris$Sepal.Length, iris$Species, mean)
     #MLLib usage test
     library(dplyr)
     # copy mtcars into spark
     mtcars_tbl <- copy_to(sc, mtcars)
     #  ** May show an error regarding problem with database. Seems to work OK after that
     src_tbls(sc)
     # transform our data set, and then partition into 'training', 'test'
     partitions <- mtcars_tbl %>%
     filter(hp >= 100) %>%
     mutate(cyl8 = cyl == 8) %>%
     sdf_partition(training = 0.5, test = 0.5, seed = 1099)
     # fit a linear model to the training dataset
     fit <- partitions$training %>%
     ml_linear_regression(response = "mpg", features = c("wt", "cyl"))
     summary(fit)


_Reading data from dtap_:
 
       count_lines <- function(sc, file) {
        spark_context(sc) %>% 
          invoke("textFile", file, 1L) %>% 
          invoke("count")}
    count_lines(sc, "dtap://TenantStorage/data/samples/bank-full.csv")
  