#/bin/bash
 export node=`bdvcli --get node.role_id`
 if [[ $node == "controller" ]]; then
 sudo service jupyter-server stop && sudo service jupyter-server start &
 fi

 sudo service jupyter-server status &
