<span style="color:#f2cf4a; font-family: 'Bookman Old Style';">

# Action Scripts

  - [1. Run Spark-submit job](#1-run-spark-submit-job)
  - [2. Run python job](#2-run-python-job)
  - [3. Install python libraries](#3-install-python-libraries)
  - [4. Run multiple Spark jobs on mesos](#4-run-multiple-spark-jobs-on-mesos)
  - [5. Run Spark-submit job with mesos](#5-run-spark-submit-job-with-mesos)
  - [6. Check Spark version](#6-check-spark-version)
  - [7. Restart Jupyter Server](#7-restart-jupyter-server)
  - [8. Run a wordcount Java program](#8-run-a-wordcount-java-program)
  - [9. Mount the created DataTap to the virtual cluster created](#9-mount-the-created-datatap-to-virtual-cluster-created)
  - [10.Update the hue.ini safety valve to point to dtap](#10-update-the-hue.ini-saftey-valve-to-point-to-dtap)



## 1. Run Spark-submit job


  __Script__:

      #/bin/bash
      export node=`bdvcli --get node.role_id`
      if [[ $node == "controller" ]]; then
            /usr/lib/spark/spark-2.1.1-bin-hadoop2.7/bin/spark-submit --class org.apache.spark.examples.SparkPi --master spark://bluedata-4.bdlocal:7077 /usr/lib/spark/spark-2.1.1-bin-hadoop2.7/examples/jars/spark-examples_2.11-2.1.1.jar 100
      fi


  __Result__:

      17/06/11 20:06:20 INFO TaskSetManager: Finished task 96.0 in stage 0.0 (TID 96) in 18 ms on 10.39.250.9 (executor 0) (97/100)
      17/06/11 20:06:20 INFO TaskSetManager: Starting task 98.0 in stage 0.0 (TID 98, 10.39.250.9, executor 0, partition 98, PROCESS_LOCAL, 6085 bytes)
      17/06/11 20:06:20 INFO TaskSetManager: Finished task 97.0 in stage 0.0 (TID 97) in 18 ms on 10.39.250.9 (executor 0) (98/100)
      17/06/11 20:06:20 INFO TaskSetManager: Starting task 99.0 in stage 0.0 (TID 99, 10.39.250.9, executor 0, partition 99, PROCESS_LOCAL, 6085 bytes)
      17/06/11 20:06:20 INFO TaskSetManager: Finished task 98.0 in stage 0.0 (TID 98) in 18 ms on 10.39.250.9 (executor 0) (99/100)
      17/06/11 20:06:20 INFO TaskSetManager: Finished task 99.0 in stage 0.0 (TID 99) in 22 ms on 10.39.250.9 (executor 0) (100/100)
      17/06/11 20:06:20 INFO DAGScheduler: ResultStage 0 (reduce at SparkPi.scala:38) finished in 5.169 s
      17/06/11 20:06:20 INFO TaskSchedulerImpl: Removed TaskSet 0.0, whose tasks have all completed, from pool 
      17/06/11 20:06:20 INFO DAGScheduler: Job 0 finished: reduce at SparkPi.scala:38, took 5.576396 s
      Pi is roughly 3.1417587141758716
      17/06/11 20:06:20 INFO SparkUI: Stopped Spark web UI at http://10.39.250.4:4042


## 2. Run python job


  __Script__:

      #!/usr/bin/env /opt/anaconda3/bin/python
      import numpy as np
      import sys
      
      a = np.array([1, 2, 3])  # Create a rank 1 array
      print (type(a))            # Prints ""
      print (a.shape)            # Prints "(3,)"
      print (a[0], a[1], a[2])   # Prints "1 2 3"
      a[0] = 5                 # Change an element of the array
      print  (a)                  # Prints "[5, 2, 3]"
      b = np.array([[1,2,3],[4,5,6]])   # Create a rank 2 array
      print (b.shape)                     # Prints "(2, 3)"
      print (b[0, 0], b[0, 1], b[1, 0])   # Prints "1 2 4"

  
  __Result__:


      (3,)
      1 2 3
      [5 2 3]
      (2, 3)
      1 2 4

 

## 3. Install python libraries


  __Script__:

      sudo yum -y install epel-release &&
      sudo yum -y install gcc gcc-c++ python-pip python-devel atlas atlas-devel gcc-gfortran openssl-devel libffi-devel;


  __Result__:

      
      Package gcc-4.4.7-18.el6.x86_64 already installed and latest version
      Package gcc-c++-4.4.7-18.el6.x86_64 already installed and latest version
      Package python-pip-7.1.0-1.el6.noarch already installed and latest version
      Package python-devel-2.6.6-66.el6_8.x86_64 already installed and latest version
      Package atlas-3.8.4-2.el6.x86_64 already installed and latest version
      Package atlas-devel-3.8.4-2.el6.x86_64 already installed and latest version
      Package gcc-gfortran-4.4.7-18.el6.x86_64 already installed and latest version
      Package openssl-devel-1.0.1e-57.el6.x86_64 already installed and latest version
      Package libffi-devel-3.0.5-3.2.el6.x86_64 already installed and latest version



## 4. Run multiple Spark jobs on mesos


  __Script__:

      #/bin/bash
      export node=`bdmacro node --get_self_index`
      if [[ $node == 0 ]]; then
      /usr/lib/spark/spark-2.1.1-bin-hadoop2.6/bin/spark-submit --class org.apache.spark.examples.SparkPi --master mesos://zk://10.39.250.6:2181,10.39.250.7:2181,10.39.250.10:2181/mesos /usr/lib/spark/spark-2.1.1-bin-hadoop2.6/examples/jars/spark-examples_2.11-2.1.1.jar 100
      /usr/lib/spark/spark-2.1.0-bin-hadoop2.6/bin/spark-submit --class org.apache.spark.examples.SparkPi --master mesos://zk://10.39.250.6:2181,10.39.250.7:2181,10.39.250.10:2181/mesos /usr/lib/spark/spark-2.1.0-bin-hadoop2.6/examples/jars/spark-examples_2.11-2.1.0.jar 100
      /usr/lib/spark/spark-2.0.1-bin-hadoop2.6/bin/spark-submit --class org.apache.spark.examples.SparkPi --master mesos://zk://10.39.250.6:2181,10.39.250.7:2181,10.39.250.10:2181/mesos /usr/lib/spark/spark-2.0.1-bin-hadoop2.6/examples/jars/spark-examples_2.11-2.0.1.jar 100
      fi

  __Result__:

      Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
      17/06/15 16:20:00 INFO SparkContext: Running Spark version 2.1.1
      17/06/15 16:21:03 INFO TaskSchedulerImpl: Removed TaskSet 0.0, whose tasks have all completed, from pool 
      17/06/15 16:21:03 INFO DAGScheduler: Job 0 finished: reduce at SparkPi.scala:38, took 18.662711 s
      Pi is roughly 3.1417439141743913
      Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
      17/06/15 16:21:35 INFO SparkContext: Running Spark version 2.1.0
      17/06/15 16:21:34 INFO TaskSchedulerImpl: Removed TaskSet 0.0, whose tasks have all completed, from pool 
      17/06/15 16:21:34 INFO DAGScheduler: Job 0 finished: reduce at SparkPi.scala:38, took 23.048201 s
      Pi is roughly 3.1426543142654313
      Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
      17/06/15 16:21:35 INFO SparkContext: Running Spark version 2.0.1
      17/06/15 16:22:08 INFO TaskSchedulerImpl: Removed TaskSet 0.0, whose tasks have all completed, from pool 
      17/06/15 16:22:08 INFO DAGScheduler: Job 0 finished: reduce at SparkPi.scala:38, took 27.550108 s
      Pi is roughly 3.1419911141991115



## 5. Run Spark-submit job with mesos


  __Script__:

     #/bin/bash
     export node=`bdmacro node --get_self_index`
     if [[ $node == 0 ]]; then
     /usr/lib/spark/spark-2.1.1-bin-hadoop2.6/bin/spark-submit --class org.apache.spark.examples.SparkPi --master mesos://zk://10.39.250.6:2181,10.39.250.7:2181,10.39.250.10:2181/mesos /usr/lib/spark/spark-2.1.1-bin-hadoop2.6/examples/jars/spark-examples_2.11-2.1.1.jar 100
     fi

  __Result__:

      17/06/15 13:24:23 INFO DAGScheduler: ResultStage 0 (reduce at SparkPi.scala:38) finished in 17.877 s
      17/06/15 13:24:23 INFO DAGScheduler: Job 0 finished: reduce at SparkPi.scala:38, took 18.138106 s
      Pi is roughly 3.1416447141644714



## 6. Check Spark version


  __Scripts__:

      #/bin/bash
      export node=`bdmacro node --get_self_index`
      if [[ $node == 0 ]]; then
      ls -l /usr/lib/spark
      fi

  __Result__:

      drwxrwxrwx. 12 nanda nanda 4096 Nov  2  2016 spark-1.6.3-bin-hadoop2.drwxrwxrwx. 12 nanda nanda 4096 Sep 28  2016 spark-2.0.1-bin-hadoop2.6
      drwxrwxrwx. 12 nanda nanda 4096 Dec 15 18:26 spark-2.1.0-bin-hadoop2.drwxrwxrwx. 12 nanda nanda 4096 Apr 25 17:10 spark-2.1.1-bin-hadoop2.6


## 7. Restart Jupyter Server


  __Script__:

     #/bin/bash
     export node=`bdvcli --get node.role_id`
     if [[ $node == "controller" ]]; then
     sudo service jupyter-server stop && sudo service jupyter-server start &
     fi

     sudo service jupyter-server status &
  

  __Result__:

      


## 8. Run a wordcount Java program


  __Script__:

      #/bin/bash
      export node=`bdvcli --get node.role_id`
      if [[ $node == "controller" ]]; then
      sudo -u hdfs /bin/bash  << EOF
      echo "Running Map Reduce WordCount example"
      cd /usr/hdp/current/hadoop-mapreduce-client/
      hadoop jar hadoop-mapreduce-examples.jar wordcount /tmp/input.txt /tmp/outfile
      echo "Successfully completed job"
      EOF
      fi


  __Result__:

      


## 9. Mount the created DataTap to the virtual cluster created


  __Script__:

      #/bin/bash
      export node=`bdvcli --get node.role_id`
      export PASSWORD=admin
      export CLUSTER_NAME=CDH5.10.1
      if [[ $node == "controller" ]]; then
          curl -iv -X PUT -H "Content-Type:application/json" -H "Accept:application/json" -d '{"items":[{ "name": "yarn_core_site_safety_valve","value":"fs.defaultFSdtap://TenantStorage"}]}' http://admin:admin@10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/YARN/config
          curl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/HIVE/commands/restart'
          curl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/HUE/commands/restart'
          curl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/OOZIE/commands/restart'
          curl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/SQOOP/commands/restart'
          curl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/YARN/commands/restart'
          echo -n Restarting All services...
    fi


  __Result__:

      



## 10.Update the hue.ini safety valve to point to dtap


  __Script__:

      #/bin/bash
      export PASSWORD=admin
      sed -i -e '/fs_defaultfs=/ s/=.*/= dtap:\/\/TenantStorage\//' /etc/hue/conf/hue.ini
      curl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/HUE/commands/restart'



  __Result__:

      # Enter the filesystem uri
      fs_defaultfs= dtap://TenantStorage/


</span>
