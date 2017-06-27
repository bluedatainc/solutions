#/bin/bash
 export node=`bdmacro node --get_self_index`
 if [[ $node == 0 ]]; then
 /usr/lib/spark/spark-2.1.1-bin-hadoop2.6/bin/spark-submit --class org.apache.spark.examples.SparkPi --master mesos://zk://10.39.250.6:2181,10.39.250.7:2181,10.39.250.10:2181/mesos /usr/lib/spark/spark-2.1.1-bin-hadoop2.6/examples/jars/spark-examples_2.11-2.1.1.jar 100
 /usr/lib/spark/spark-2.1.0-bin-hadoop2.6/bin/spark-submit --class org.apache.spark.examples.SparkPi --master mesos://zk://10.39.250.6:2181,10.39.250.7:2181,10.39.250.10:2181/mesos /usr/lib/spark/spark-2.1.0-bin-hadoop2.6/examples/jars/spark-examples_2.11-2.1.0.jar 100
 /usr/lib/spark/spark-2.0.1-bin-hadoop2.6/bin/spark-submit --class org.apache.spark.examples.SparkPi --master mesos://zk://10.39.250.6:2181,10.39.250.7:2181,10.39.250.10:2181/mesos /usr/lib/spark/spark-2.0.1-bin-hadoop2.6/examples/jars/spark-examples_2.11-2.0.1.jar 100
 fi

