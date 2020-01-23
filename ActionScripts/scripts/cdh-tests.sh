echo "Starting testing jobs"
echo "generating data using teragen on tenant storage..."
echo "cleaning up dtap://TenantStorage/tmp from tenant storage if exists"
sudo -E -u hdfs hadoop fs -rm -r dtap://TenantStorage/tmp
sudo -E -u hdfs yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar teragen 10000 dtap://TenantStorage/tmp/teragen
sudo -E -u hdfs yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar wordcount dtap://TenantStorage/tmp/teragen/part-m-00000 dtap://TenantStorage/tmp/out
echo "Successfully ran teragen and wordcount on tenant storage"
echo "Test completed"
