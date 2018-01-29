#!/bin/bash
#
# Copyright (c) 2017, BlueData Software, Inc.
#
# This script is used to populate /etc/hosts for additional hostname resolution.
# It must be run as an action script with root privilege
# Argument to the script must be of this format
# This script must be run only on ec2 instances
# <host_name>:<ip_addr>,<host_name>:<ip_addr>
#set -x

bold=$(tput bold)
blink=$(tput blink)
underline=$(tput sgr 0 1)
red=$(tput setaf 1)
green=$(tput setaf 2)
blue=$(tput setaf 4)
white=$(tput setaf 7)
normal=$(tput sgr0)

HOST_LIST="$1"

# Make sure the script it invoked as root
if [[ $EUID -ne 0 ]]; then
   echo "This action script must be run as root"
   exit 1
fi

# Check to make sure this instance is running on ec2
EC2_INSTANCE_ID=$(curl --connect-timeout 10 --max-time 10 --silent http://169.254.169.254/latest/meta-data/instance-id)
if [ -z "$EC2_INSTANCE_ID" ]
then
    echo "${bold}${red}Unable to access aws metadata server to fetch ec2 instance id.${normal}"
    exit 1
fi

if [ -z "$HOST_LIST" ]
then
    echo "${bold}${red}Enter a comma-separated list of <host_name>:<ip_addr>${normal}"
    exit 1
fi

HOST_RES_LIST=$(echo $HOST_LIST | tr ',' ' ')
for HOST_RES in $HOST_RES_LIST
do
    HOST_NAME="$(echo $HOST_RES | cut -d ':' -f1)"
    IP_ADDR="$(echo $HOST_RES | cut -d ':' -f2)"
    if [ -z "$HOST_NAME" ] || [ -z "$IP_ADDR" ]
    then
        echo "Enter a comma-separated list of <host_name>:<ip_addr>"
        exit 1
    fi
    if grep -qwe "$IP_ADDR" /etc/hosts
    then
        echo "${bold}${red}Specified ipaddress $IP_ADDR already exists in /etc/hosts file. ${normal}"
    else
        cat >> /etc/hosts <<EOF
$IP_ADDR $HOST_NAME $HOST_NAME
EOF
    fi

    if grep -qwe "$IP_ADDR" /hostfs/etc/hosts
    then
        echo "${bold}${red}Specified ipaddress $IP_ADDR already exists in /hostfs/etc/hosts file. ${normal}"
    else
        cat >> /hostfs/etc/hosts <<EOF
$IP_ADDR $HOST_NAME $HOST_NAME
EOF
    fi
done

echo "${green} host entries are successfully populated.${normal}"
echo "${green}/etc/hosts DATA${normal}"
cat /etc/hosts
echo
echo "${green}/hostfs/etc/hosts DATA${normal}"
cat /hostfs/etc/hosts

exit 0
