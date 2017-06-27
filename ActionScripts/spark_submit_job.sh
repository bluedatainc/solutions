#/bin/bash
export node=`bdvcli --get node.role_id`
if [[ $node == "controller" ]]; then
    /usr/lib/spark/spark-2.1.1-bin-hadoop2.7/bin/spark-submit --class org.apache.spark.examples.SparkPi --master spark://bluedata-4.bdlocal:7077 /usr/lib/spark/spark-2.1.1-bin-hadoop2.7/examples/jars/spark-examples_2.11-2.1.1.jar 100
fi