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
