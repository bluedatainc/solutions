#/bin/bash 

export node=`bdvcli --get node.role_id`

if [[ $node == "jupyter" ]]; then
	
	hadoop fs -get dtap://TenantStorage/pythonScripts/randomforest.py /tmp
	chmod a+x /tmp/randomforest.py
	/usr/lib/spark/spark-2.1.1-bin-hadoop2.7/bin/spark-submit /tmp/randomforest.py
fi