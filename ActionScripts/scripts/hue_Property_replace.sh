#/bin/bash

export PASSWORD=admin
sed -i -e '/fs_defaultfs=/ s/=.*/= dtap:\/\/TenantStorage\//' /etc/hue/conf/hue.ini
curl -u admin:$PASSWORD -X POST 'http://10.39.250.14:7180/api/v14/clusters/CDH5.10.1/services/HUE/commands/restart'
