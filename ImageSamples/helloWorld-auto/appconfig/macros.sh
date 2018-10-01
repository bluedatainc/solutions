#!/bin/env bash
################################################################################
# Copyright (c) 2016, BlueData Software, Inc.                                  #
#                                                                              #
# Macro definitions for various node config parameters.                        #
#                                                                              #
# Requirements:                                                                #
#    - logging.sh and utils.sh must be sourced before sourcing this file.      #
#
################################################################################


## Node details.
FQDN="$(invoke_bdvcli --get node.fqdn)"
ROLE="$(invoke_bdvcli --get node.role_id)"
DOMAIN="$(invoke_bdvcli --get node.domain)"
DISTRO="$(invoke_bdvcli --get node.distro_id)"
HOSTNAME="$(invoke_bdvcli --get node.hostname)"
NODEGROUP="$(invoke_bdvcli --get node.nodegroup_id)"
DEPENDS_ON="$(invoke_bdvcli --get node.depends_on)"
DTAP_JAR="/opt/bluedata/bluedata-dtap.jar"
CLUSTER_NAME="$(invoke_bdvcli --get cluster.name)"
TOTAL_VCPU=$(invoke_bdvcli --get distros.${DISTRO}.${NODEGROUP}.roles.${ROLE}.flavor.cores)
TOTAL_VMEM=$(invoke_bdvcli --get distros.${DISTRO}.${NODEGROUP}.roles.${ROLE}.flavor.memory)

## Get the value of a specific config choice key for any nodegroup of the
## cluster.
##
## Input:
##      NGID     -> Nodegroup id
##      KEY      -> Config choice key to get the value for.
## Return:
##      Success: returns the value for the requested key
##      Failure: exits the script with a non-zero status.
CLUSTER_CONFIG_CHOICE() {
    local NGID=$1; shift
    local KEY=$1
    invoke_bdvcli_ignore_error --get cluster.config_choice_selections.${NGID}.${KEY}
}

## Get the value of a specific config metadata key for any nodegroup of the
## cluster.
##
## Input:
##      NGID     -> Nodegroup id
##      KEY      -> Config choice key to get the value for.
## Return:
##      Success: returns the value for the requested key
##      Failure: exits the script with a non-zero status.
CLUSTER_CONFIG_METADATA() {
    local NGID=$1; shift
    local KEY=$1
    invoke_bdvcli_ignore_error --get cluster.config_metadata.${NGID}.${KEY}
}

## Get the value of a specific config choice key for the nodegroup the current
## node is part of.
##
## Input:
##      KEY      -> Config choice key to get the value for.
## Return:
##      Same as CLUSTER_CONFIG_CHOICE()
NODEGROUP_CONFIG_CHOICE() {
    local KEY=$1
    CLUSTER_CONFIG_CHOICE ${NODEGROUP} ${KEY}
}

## Get the value of a specific config metadata key for the nodegroup the current
## node is part of.
##
## Input:
##      KEY      -> Config choice key to get the value for.
## Return:
##      Same as CLUSTER_CONFIG_METADATA()
NODEGROUP_CONFIG_METADATA() {
    local KEY=$1
    CLUSTER_CONFIG_METADATA ${NODEGROUP} ${KEY}
}


## Replace a pattern in the specified file with the output of the MACRO.
##
## Input:
##      PATTERN     -> A pattern to replace.
##      DESTFILE    -> The file to modify
##      MACRO       -> A macro whose output is used to replace the PATTERN.
## Return:
##      Success: All occurences of the patter are replaced in the file.
##      Failure: Exits the script with the approriate failure return status.
REPLACE_PATTERN() {
    local PATTERN=$1; shift
    local DESTFILE=$1; shift
    local MACRO=$@

    local macroOutput=$(log_exec_no_exit ${MACRO})
    STATUS=$?
    if [[ ${STATUS} -eq 0 ]]; then
        log "MACRO OUTPUT: ${macroOutput}"
        log_exec "sed -i 's!${PATTERN}!${macroOutput}!g' ${DESTFILE}"
    else
        log "Not replacing pattern '${PATTERN}' in '${DESTFILE}'. '${MACRO}' returned status '${STATUS}'"
    fi
}

## Common 'register a service' function.
##
## Input:
##      SRVCID      -> Id of the service to register
##      SVC_NAME    -> Service Name
##      IS_SYSTEMD  -> Boolean that indicates if it is a systemD service
## Return:
##      Success: zero return status
##      Failure: exits if the service registration was attempted and failed.
REGISTER_START_SERVICE_COMMON() {
    local SRVCID=$1
    local SVC_NAME=$2
    local IS_SYSTEMD=$3

    SRVC_NODEGRPS=$(invoke_bdvcli --get services.${SRVCID} | tr ',' ' ')
    if  grep -wq ${NODEGROUP} <<< ${SRVC_NODEGRPS}; then
        SRVC_ROLES=$(invoke_bdvcli --get services.${SRVCID}.${NODEGROUP} | tr ',' ' ')
        if  grep -wq ${ROLE} <<< ${SRVC_ROLES}; then
            # If systemd, then register with systemd directly
            if [ "$IS_SYSTEMD" == "true" ]
            then
                systemctl enable ${SVC_NAME}
                systemctl start ${SVC_NAME}
                REG_OPTION="--systemctl=${SVC_NAME}"
            else
                REG_OPTION="--systemv=${SVC_NAME}"
            fi

            # if vagent is setup, then register the service with vagent also
            if [[ $(util_is_vagent_setup) == "true" ]];
            then
                invoke_bdvcli --service_key "services.${SRVCID}.${NODEGROUP}.${ROLE}" ${REG_OPTION}
            fi
        fi
    fi
}

## Register a systemV service.
##
## The service should only be registered (and automatically started with vagent)
## if it is expected to run on the node.
##
## Input:
##      SRVCID      -> Id of the catalog service to register
##      SYSV        -> SystemV service name.
## Return:
##      Same as REGISTER_START_SERVICE_COMMON()
REGISTER_START_SERVICE_SYSV() {
    local SRVCID=$1
    local SYSV=$2

    REGISTER_START_SERVICE_COMMON "${SRVCID}" "${SYSV}" "false"
}

## Register a SystemD service.
##
## The service should only be registered (and automatically started with vagent)
## if it is expected to run on the node.
##
## Input:
##      SRVCID      -> Id of the catalog service to register
##      SYSCTL      -> SystemV service name.
## Return:
##      Same as REGISTER_START_SERVICE_COMMON()
REGISTER_START_SERVICE_SYSCTL() {
    local SRVCID=$1
    local SYSCTL=$2

    REGISTER_START_SERVICE_COMMON "${SRVCID}" "${SYSCTL}" "true"
}

## Returns an integer for the host which is unique across the nodegroup. The
## integer generated is guaranteed to be between 1 and the number of hosts in
## the nodegroup. The function is guaranteed to return the same unique integer
## on a given node on multiple invocation.
##
## Input:
##      (nothing)
## Return:
##      Success: An integer is echoed as an output
##      Failure: nothing is echoed from the function.
UNIQUE_SELF_NODE_INT() {
    ALLHOSTS=($(invoke_bdvcli --get_local_group_fqdns | tr ',' '\n' | sort -V))
    for i in $(seq ${#ALLHOSTS[@]}); do
        index=$(expr ${i} - 1)
        if [[ "${ALLHOSTS[${index}]}" == "${FQDN}" ]]; then
            echo "${index}"
            return 0
        fi
    done
    return 1
}

## Returns an integer for the host which is unique across the nodegroup. The
## integer generated is guaranteed to be between 1 and the number of hosts in
## the nodegroup. The function is guaranteed to return the same unique integer
## on a given node on multiple invocation.
##
## Input:
##      (remote host name)
## Return:
##      Success: An integer is echoed as an output
##      Failure: nothing is echoed from the function.
UNIQUE_ANOTHER_NODE_INT() {
    ALLHOSTS=($(invoke_bdvcli --get_local_group_fqdns | tr ',' '\n' | sort -V))
    HOST=$1
    for i in $(seq ${#ALLHOSTS[@]}); do
        index=$(expr ${i} - 1)
        if [[ "${ALLHOSTS[${index}]}" == "$HOST" ]]; then
            echo "${index}"
            return 0
        fi
    done
    return 1
}



## Returns a unique integer based on an unspecified criterion. The integer
## generated is guaranteed to be between 1 and the number of hosts in the
## nodegroup that run the specified service. The function is guaranteed to
## return the same unique integer on a given node on multiple invocation.
##
## Input:
##      SRVCID      -> Id of the catalog service
## Return:
##      Success: An integer is echoed as an output
##      Failure: nothing is echoed from the function.
UNIQUE_INT_ID_BY_SRVC() {
    local SRVCID=$1

    SRVC_NODEGRPS=$(invoke_bdvcli --get services.${SRVCID} | tr ',' ' ')
    if grep -wq ${NODEGROUP} <<< ${SRVC_NODEGRPS}; then
        SRVC_ROLES=$(invoke_bdvcli --get services.${SRVCID}.${NODEGROUP} | tr ',' ' ')
        if grep -wq ${ROLE} <<< ${SRVC_ROLES}; then
            HOSTS=($(invoke_bdvcli --get services.${SRVCID}.${NODEGROUP}.${ROLE}.fqdns | tr ',' '\n' | sort))
            for i in "$(seq ${#HOSTS[@]})"; do
                index=$(expr ${i} - 1)
                if [[ "${HOSTS[$index]}" == "${FQDN}" ]]; then
                    echo "${index}"
                    return 0
                fi
            done
        fi
    fi
    return 1
}

## Automatically assign one node from this node's nodegroup as the primary for
## that nodegroups.
##
## Input:
##      (nothing)
## Return:
##      Success: (nothing)
##      Failure: exits when the return status of bd_vcli is non-zero
AUTO_ASSIGN_PRIMARY() {
    local VER=$(invoke_bdvcli --get version)

    if [[ ${VER} -lt 4 ]];
    then
        if [[ "$(UNIQUE_SELF_NODE_INT)" == "0" ]]; then
            invoke_bdvcli --nodegroup_primary
        fi
    fi

    return 0
}

## Get total virtual memory available in MB
## Input:
##      (nothing)
## Return:
##      Success: (nothing)
##      Failure: exits when the return status of bd_vcli is non-zero
GET_TOTAL_VMEMORY_MB() {
    echo $TOTAL_VMEM
    return 0
}

## Get total virtual cores available for spark
## Input:
##      (nothing)
## Return:
##      Success: (nothing)
##      Failure: exits when the return status of bd_vcli is non-zero
GET_TOTAL_VCORES() {
     echo $TOTAL_VCPU
     return 0
}

## Get FQDN List
## Input:
##      Role (eg: controller, worker, etc.)
## Return:
##      Success: (nothing)
##      Failure: exits when the return status of bd_vcli is non-zero
GET_FQDN_LIST() {
    role=$1
    ROLE_FQDN="$(invoke_bdvcli --get distros.${DISTRO}.${NODEGROUP}.roles.${role}.fqdns)"
    echo $ROLE_FQDN
    return 0
}

## Get IP address List
## Input:
##      Role (eg: controller, worker, etc.)
## Return:
##      Success: (nothing)
##      Failure: exits when the return status of bd_vcli is non-zero
GET_IPADDR_LIST() {
    local IPADDR=''
    for f in $(GET_FQDN_LIST $1 | tr ',' ' ');
    do
        ip=$(util_fqdn_to_ipaddr ${f})
        if [[ $? -eq 0 ]];
        then
            [[ -z ${IPADDR} ]] && IPADDR=${ip} || IPADDR="${IPADDR},${ip}"
        else
            return 1
        fi
    done
    echo $IPADDR
    return 0
}

## Get Node FQDN
## Input:
##      (nothing)
## Return:
##      Success: (nothing)
##      Failure: exits when the return status of bd_vcli is non-zero
GET_NODE_FQDN() {
    echo "${FQDN}"
    return 0
}

## Get Node IP address
## Input:
##      (nothing)
## Return:
##      Success: (nothing)
##      Failure: returns with a non-zero status
GET_NODE_IPADDR() {
    IP=$(util_fqdn_to_ipaddr ${FQDN})
    if [[ $? -eq 0 ]];
    then
        echo "${IP}"
        return 0
    else
        return 1
    fi
}

## Generate an app specific url
## Input:
##      SRVC_ID    -> Service id
##      ROLE       -> ROLE of the service
##      NODEGRP    -> Nodegroup ID to disambiguate the case when the named
##                    service is running in multiple nodegroups. If this arg
##                    is not specified and the same service name exists in
##                    multiple nodegroups the first nodegroup id is automatically
##                    used to disambiguate.
## Return:
##      Success: the app URL
##      Failure: exits when the return status of bd_vcli is non-zero
GET_SERVICE_URL() {
    local SRVC=$1
    local SRVC_ROLE=$2
    local NODEGRP=$3

    if [[ -z ${NODEGRP} ]];
    then
        local NODEGRP_IDS_ARRAY=($(invoke_bdvcli --get services.${SRVC} 2>/dev/null | tr ',' '\n' | sort))
        if [[ ${#NODEGRP_IDS_ARRAY[@]} -ge 1 ]];
        then
            NODEGRP=${NODEGRP_IDS_ARRAY[0]}
        else
            log_error "Service (${SRVC}) does not exit in any nodegroup."
            return 1
        fi
    fi

    APP_URL="$(invoke_bdvcli --get services.${SRVC}.${NODEGRP}.${SRVC_ROLE}.endpoints)"
    echo "${APP_URL}"
    return 0
}

## TENANT_INFO
## Input:
##      KEY -> eg: aws_access_key aws_secret_key
## Return:
##      Success: (nothing)
##      Failure: exits when the return status of bd_vcli is non-zero
TENANT_INFO() {
    KEY=$1
    TENANT_INFO="$(invoke_bdvcli_ignore_error --get tenant 2>/dev/null)"
    if [[ ${TENANT_INFO} == "" ]]; then
        echo ""
    else
        CONFIG_VALUE="$(invoke_bdvcli_ignore_error --get tenant.${KEY} 2>/dev/null)"
        echo "${CONFIG_VALUE}"
    fi
    return 0
}
