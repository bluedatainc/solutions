#/bin/bash

export node=`bdvcli --get node.role_id`
export PASSWORD=admin
export CLUSTER_NAME=CDH5.10.1
#export CMHOST=10.39.250.14
#export CMPORT=7180
#export SERVICE=YARN
#export BASEURL=http://$CMHOST:$CMPORT

if [[ $node == "controller" ]]; then
	
	curl -iv -X PUT -H "Content-Type:application/json" -H "Accept:application/json" -d '{"items":[{ "name": "yarn_core_site_safety_valve","value":"<property><name>fs.defaultFS</name><value>dtap://TenantStorage</value></property>"}]}' http://admin:admin@10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/YARN/config
	curl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/HIVE/commands/restart'
	curl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/HUE/commands/restart'
	curl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/OOZIE/commands/restart'
	curl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/SQOOP/commands/restart'
	curl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/YARN/commands/restart'
	echo -n Restarting All services...
fi
