#!/bin/bash
#
# Copyright (c) 2017, BlueData Software, Inc.
#
# This script is used to setup s3 bucket as local access. It must be run
# as an action script with root privilege
# Argument to the script must be a comma separated list of bucket names
# This script must be run only on ec2 instances
# NOTE: This script doesn't do any bucket name or credential validation
#set -x

bold=$(tput bold)
blink=$(tput blink)
underline=$(tput sgr 0 1)
red=$(tput setaf 1)
green=$(tput setaf 2)
blue=$(tput setaf 4)
white=$(tput setaf 7)
normal=$(tput sgr0)

BUCKET_LIST="$1"
S3FS_CACHE="/s3fs/cache"

HOST_FSTAB="/hostfs/etc/fstab"

# Make sure the script it invoked as root
if [[ $EUID -ne 0 ]]; then
   echo "This action script must be run as root"
   exit 1
fi

# Get all the aws s3 endpoints for all our supported regions
declare -A AWS_ENDPOINTS
AWS_ENDPOINTS[us-east-1]="https://s3.amazonaws.com/"
AWS_ENDPOINTS[us-east-2]="https://s3.us-east-2.amazonaws.com/"
AWS_ENDPOINTS[us-west-1]="https://s3-us-west-1.amazonaws.com/"
AWS_ENDPOINTS[us-west-2]="https://s3-us-west-2.amazonaws.com/"
AWS_ENDPOINTS[eu-west-1]="https://s3-eu-west-1.amazonaws.com/"
AWS_ENDPOINTS[eu-west-2]="https://s3.eu-west-2.amazonaws.com/"
AWS_ENDPOINTS[eu-central-1]="https://s3.eu-central-1.amazonaws.com/"

# Check to make sure this instance is running on ec2
EC2_INSTANCE_ID=$(curl --connect-timeout 10 --max-time 10 --silent http://169.254.169.254/latest/meta-data/instance-id)
if [ -z "$EC2_INSTANCE_ID" ]
then
    echo "${bold}${red}Unable to access aws metadata server to fetch ec2 instance id.${normal}"
    exit 1
fi

EC2_AVAIL_ZONE=$(curl --connect-timeout 10 --max-time 10 --silent http://169.254.169.254/latest/meta-data/placement/availability-zone)
# Strip last character to extract the region
EC2_REGION="${EC2_AVAIL_ZONE%?}"

if [ -z "$BUCKET_LIST" ]
then
    echo "${bold}${red}Enter a comma-separated list of buckets.${normal}"
    exit 1
fi

# Fetch the iam instance profile for this instance
IAM_ROLE="$(curl --connect-timeout 10 --max-time 10 --silent http://169.254.169.254/latest/meta-data/iam/security-credentials/)"

if [ -z "$IAM_ROLE" ]
then
    echo "${bold}${red}Unable to fetch iam role for this instance.${normal}"
    exit 1
fi

BUCKETS=$(echo $BUCKET_LIST | tr ',' ' ')

for BUCKET_NAME in $BUCKETS
do
    # Check to see if the bucket already exists in /etc/fstab in which case just skip
    # it
    if grep -qe "/s3fs/$BUCKET_NAME fuse.s3fs" $HOST_FSTAB
    then
        echo "${bold}${red}Specified bucket $BUCKET_NAME is already configured on this instance.${normal}"
        continue
    else
        # Create a directory for the bucket
        mkdir -p /s3fs/$BUCKET_NAME

        ENDPOINT=${AWS_ENDPOINTS[$EC2_REGION]}

        cat >> $HOST_FSTAB <<EOF
$BUCKET_NAME /s3fs/$BUCKET_NAME fuse.s3fs _netdev,allow_other,use_cache=$S3FS_CACHE,iam_role=$IAM_ROLE,url=$ENDPOINT,endpoint=$EC2_REGION,umask=000,noatime 0 0
EOF
        echo "${green}s3fs successfully configured for bucket $BUCKET_NAME. Instance must be rebooted for configuration to take effect.${normal}"
    fi
done

exit 0
