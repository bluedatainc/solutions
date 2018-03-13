<span style="color:#f2cf4a; font-family: 'Bookman Old Style';">

   __BDVCLI OVERVIEW__


      Bdvcli is a CLI tool that is available within each docker container instance to add, remove, or query the metadata at

        1. Container or current node level information

        2. Using Node Namespace

        3. Parent cluster level information from individual containers using Cluster NameSpace

        4. Parent tenant level information of the node/cluster using Tenant NameSpace

        As an example, available information includes node fqdn, 
        node ip, cluster name, cluster type, tenant AD/KDC setup
        and more. This basic and extended metadata allows
        users to automate and/or script appropriate actions
        and provide successful implementations of big data clusters.  


  __NOTE__:

        -  Make sure to run all "bdvcli" commands inside the cluster container
           and "bdconfig" commands on Epic controller physical machine.

        -  Each node has a set of attributes including fqdn,
           ip_address, role within the cluster,
           services on this node, node-group of this node, and more.

  __BDVCLI & BDCONFIG COMMANDS__:

  - [0. Get list of namespaces](#0-get-list-of-namespaces)
  - [1. Get Role ID of the container](#1-get-role-id-of-the-container)
  - [2. Get Hostname of the container](#2-get-hostname-of-the-container)
  - [3. Get Domain name of the container](#3-get-domain-name-of-the-container)
  - [4. Get FQDN of the container](#4-get-fqdn-of-the-container)
  - [5. Get Distro ID of the container](#5-get-distro-id-of-the-container)
  - [6. Get Nodegroup ID of the cluster](#6-get-nodegroup-id-of-the-cluster)
  - [7. Get Controller FQDN of the cluster](#7-get-controller-fqdn-of-the-cluster)
  - [8. Get Depends on parent distro id of the container](#8-get-depends-on-parent-distro-id-of-the-container)
  - [9. Get Cluster name](#9-get-cluster-name)
  - [10. Get Cluster config selections](#10-get-cluster-config-selections)
  - [11. Get Keys for specific node group](#11-get-keys-for-specific-node-group)
  - [12. Get Value assigned to the specific key](#12-get-value-assigned-to-the-specific-key)
  - [13. Get List of node group ids](#13-get-list-of-node-group-ids)
  - [14. Get List of config metadata keys for a specific node group](#14-get-list-of-config-metadata-keys-for-a-specific-node-group)
  - [15. Get Value assigned to specific config metadata key](#15-get-value-assigned-to-specific-config-metadata-key)
  - [16. Get List of virtual nodes or container names](#16-get-list-of-virtual-nodes-or-container-names)
  - [17. Get List of all current mappings](#17-get-list-of-all-current-mappings)
  - [18. Add a port mapping](#18-add-a-port-mapping)
  - [19. Get Clusters and Tenant ids](#19-get-clusters-and-tenant-ids)


## 0. Get list of namespaces

  __Description__:

    List of namespaces

  __Command__:

    bdvcli --get namespaces

  __Example__:

        > bdvcli --get namespaces
        version,node,cluster,services


## 1. Get Role ID of the container

  __Description__:

    Role identifier of the node as specified in the catalog

  __Command__:

    bdvcli --get node.role_id

  __Example__:

      > bdvcli --get node.role_id
      controller

## 2. Get Hostname of the container

  __Description__:

    The hostname assigned to the node

  __Command__:

    bdvcli --get node.hostname

  __Example__:

      > bdvcli --get node.hostname
      bluedata-100.bdlocal


## 3. Get Domain name of the container

  __Description__:

    The domain name of the node

  __Command__:

    bdvcli --get node.domain

  __Example__:

      > bdvcli --get node.domain
      bdlocal


## 4. Get FQDN of the container

  __Description__:

    The fully qualified domain name of the host

  __Command__:

    bdvcli --get node.fqdn

  __Example__:

      > bdvcli --get node.fqdn
      bluedata-100.bdlocal


## 5. Get Distro ID of the container

  __Description__:

    Distro identification of the node as specified by the catalog.
    This value may be empty

  __Command__:

    bdvcli --get node.distro_id

  __Example__:

      > bdvcli --get node.distro_id
      bluedata/cdh5121multicr


## 6. Get Nodegroup ID of the cluster

  __Description__:

    Cluster wide unique node group identifier this node belongs to

  __Command__:

    bdvcli --get node.nodegroup_id

  __Example__:

      > bdvcli --get node.nodegroup_id
      1


## 7. Get Controller FQDN of the cluster

  __Description__:

    The Controller FQDN of the cluster

  __Note__:

    Run #5 to get ${DISTRO} and #6 to get ${NODEGROUP}

  __Command__:

    bdvcli --get distros.${DISTRO}.${NODEGROUP}.roles.controller.fqdns

  __Example__:

      > bdvcli --get distros.bluedata/cdh5121multicr.1.roles.controller.fqdns
      bluedata-100.bdlocal


## 8. Get Depends on parent distro id of the container

  __Description__:

    Cluster wide unique services ids that this node depends on

  __Command__:

    bdvcli --get node.depends_on

  __Example__:

      > bdvcli --get node.depends_on
      bluedata/cdh591base


## 9. Get Cluster name

  __Description__:

    The cluster name assigned by user

  __Command__:

    bdvcli --get cluster.name

  __Example__:

      > bdvcli --get cluster.name
      cdh5121-test


## 10. Get Cluster config selections

  __Description__:

    A list of all node group ids that are part of the virtual cluster.
    This information is based on what is specified in the catalog and
    specific selections made by the user at cluster creation time.

  __Command__:

    bdvcli --get cluster.config_choice_selections

  __Example__:

      > bdvcli --get cluster.config_choice_selections
      1


## 11. Get Keys for specific node group

  __Description__:

    Keys that may be available for the specific node group.

  __Command__:

    bdvcli --get cluster.config_choice_selections.<ng_id>

  __Example__:

      > bdvcli --get cluster.config_choice_selections.1
      mrtype,yarn_ha,kerberos,apps,spark,hbase


## 12. Get Value assigned to the specific key

  __Description__:

    Value assigned to the specific key.

  __Command__:

    bdvcli --get cluster.config_choice_selections.<ng_id>.<key>

  __Example__:

      > bdvcli --get cluster.config_choice_selections.1.mrtype
      yarn




## 13. Get List of node group ids

  __Description__:

    A list of all node group ids that are part of the virtual cluster.

  __Command__:

    bdvcli --get cluster.config_metadata

  __Example__:

      > bdvcli --get cluster.config_metadata
      1


## 14. Get List of config metadata keys for a specific node group

  __Description__:

    List of all configuration metadata keys available
    for the particular node group.
    The available keys are gathered from the
    information specified in the catalog of this distribution.

  __Command__:

    bdvcli --get cluster.config_metadata.<ng_id>

  __Example__:

      > bdvcli --get cluster.config_metadata.1




## 15. Get Value assigned to specific config metadata key

  __Description__:

    Value assigned to the specific key.

  __Command__:

    bdvcli --get cluster.config_metadata.<ng_id>.<key>

  __Example__:

      > bdvcli --get cluster.config_metadata.1.




## 16. Get List of virtual nodes or container names

  __Description__:

    Prints the list of container names.

  __Note__:

    Run this command on Epic controller host machine.

  __Command__:

    bdconfig --getvms

  __Example__:

       > bdconfig --getvms

       INSTANCE ID      CLUSTER ID  HOSTNAME     HYPERVISOR IP    FQDN                 INSTANCE IP    TENANT TYPE
       -------------  ------------  -----------  ---------------  -------------------  -------------  -------------
       3a70662d7e93             20  bluedata-61  10.32.1.116      bluedata-61.bdlocal  10.35.239.2    docker
       874815fca681             20  bluedata-60  10.32.1.116      bluedata-60.bdlocal  10.35.239.3    docker


## 17. Get List of all current mappings

  __Description__:

    Prints current mappings list.

  __Note__:

    Run this command on Epic controller host machine.

  __Command__:

    bdconfig --getmapping --vmName <vmname>

  __Example__:

    > bdconfig --getmapping --vmName bluedata-61

      VM NAME       GATEWAY SET HOSTNAME            MAPPINGS
      ---------     ----------------------          ----------
      bluedata-61   yav-141-esx1.lab.bluedata.com    ('http', 8055, 10000)
                                                     ('http', 8080, 10001)
                                                     ('tcp', 22, 10004)


## 18. Add a port mapping

  __Description__:

    Adds a port mapping where, "vm name" is the name of the virtual node/container,
    "port" is the port number being mapped (such as 22 for SSH or 443 for https),
    "map mode" Either http or tcp, depending on the service you are mapping
    and <tenant-id> is the ID of the tenant where this port mapping will apply.

 __Note__:

      Run this command on Epic controller host machine.

  __Command__:

       bdconfig --addmapping --vmName <vm name> --mappingPort <port> --mappingMode <map mode> --tenantid
       <tenant-id>

  __Example__:

      > bdconfig --addmapping --vmName bluedata-458 --mappingMode=http --mappingPort 8983 --tenantId 3



## 19. Get Clusters and Tenant ids

  __Description__:

    Gets cluster and tenant ids

  __Note__:

    Run this command on Epic controller host machine.

  __Command__:

    bdconfig --getclusters

  __Example__:

      > bdconfig --getclusters

      CLUSTER ID   CLUSTER NAME   CLUSTER CONTEXT  TENANT ID    STATUS
      ------------  ------------   -------------   -----------  ---------
       23           Spark211-Multirole  Persistant         2      ready
       28           Cdh591              Persistant         2      ready


# Other BDVCLI Commands


__Note__: In your cluster container , run the following commands below.

__[root@bluedata-100 ~]# bdvcli --help__

Usage: bd_vcli.py [options] [arg1 arg2 ... ]

__Options__:

     -h, --help        show this help message and exit

     --startconfiguration_with_api=STARTCONFAPI  Indicates the beginning  of application configuration
                                              at a particular config api version.

     --baseimg_version         Returns the base image version used to build the
                            application's image.

  __Metadata querying for Application configuration scripts:__

    -g KEY, --get=KEY   Get the value for a '.' delimited KEY. The KEY must
                        begin with a valid namespace keyword. Use'namespaces'
                        key to get all the availalbe namespaces.

  __Distributed synchronization for Application configuration scripts:__

    -w KEY(S), --wait=KEY(S)
                        A comma separated list of KEY(S) specifying which
                        services to wait for. The KEY(S) used could specify
                        the end services or represent a group of services but
                        not both at the same time.

    -t SECONDS, --timeout=SECONDS
                        Maximum time (specified in seconds) to wait for a
                        response when -w/--wait API is invoked.

    --tokenwait=TOKEN   A token to wait for on the specified node. Will
                        unblock when an explicit wake is called.

    --fqdn=FQDN     The fully qualified domain name of the host on which
                    the corresponding wake is expected

    --tokenwake=TOKEN   Wake up all cluster processes waiting on the given
                        token

    --success     Indicates that waiters would be woken with success
                  status. This is the default if nothing is specified

    --error         Indicates that waiters would be woken with error
                    status

  __Advanced cluster configurations:__

    --restart_all_services
                        Restarts all the services previously registered during
                        the cluster configuration on this node. This is
                        expected to be used after modifying configuration
                        parameters.

  __Application services un/registration:__

    --service_key=KEY   A key to uniquely identify an application's service
                        being registered.
    --systemv=SERVICE   A SystemV service name who's lifecycle is to be
                        managed by vAgent. The "service" command will be used
                        for handling the lifecycle events.
    --systemctl=SERVICE
                        A SystemD service name who's lifecycle is to be
                        managed by vAgent. The 'systemctl' command will be
                        used for handling the lifecycle events.
    --unregister_srvc=KEY
                        A namespace key uniquely identifying the application's
                        service to unregister.

  __System services un/registration:__

    --system_sysv=SRVC_NAME
                        The system SysV service name whose lifecycle should be
                        managed by the vAgent.
    --system_sysctl=SRVC_NAME
                        A system SysD service name whose lifecycle should be
                        managed by the vAgent.
    --unregister_system_srvc=SRVC_NAME
                        The system SysV service name to unregister.
    --unregister_system_sysctl=SRVC_NAME
                        The system SysD service name to unregister.

  __Tenant information:__

    --tenant_info       Get the tenant specific information as key-value pairs
    --tenant_info_lookup=TENANT_INFO_KEY
                        Lookup the value of the given key in the tenant
                        information.

  __Miscellaneous:__

    --get_local_group_fqdns
                        Get all FQDNs deployed for the node group that the
                        local node belongs to.
    --get_nodegroup_fqdns=GETNODEGROUPFQDNS
                        Get all FQDNs in the given Node group.
    --get_all_fqdns     Get FQDNs of all the nodes in the cluster.

</span>
