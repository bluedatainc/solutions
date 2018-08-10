SELF=$(readlink -nf $0)
BASE_DIR=$(dirname ${SELF})

source ${BASE_DIR}/logging.sh || exit 1
source ${BASE_DIR}/utils.sh || exit 1

PRIMARY_NODEGROUP=1
DISTRO=$(invoke_bdvcli --get node.distro_id)
Roles=($(invoke_bdvcli --get distros.${DISTRO}.${PRIMARY_NODEGROUP}.roles))
Role=$(echo $Roles | tr "," "\n")
TotalCores=0
for r in $Role
do
  RoleFqdn=($(invoke_bdvcli --get distros.${DISTRO}.${PRIMARY_NODEGROUP}.roles.${r}.fqdns | tr ',' '\n'))
  Cores=$(invoke_bdvcli --get distros.${DISTRO}.1.roles.${r}.flavor.cores)
  RoleCount=${#RoleFqdn[@]}
  T=$(echo "$(($Cores * $RoleCount))")
  TotalCores=$(echo "$(($TotalCores + ($Cores * $RoleCount)))")
done
echo $TotalCores

SPARK_MAX_CORES=`expr $TotalCores / 3`
PATTERN=@@@@SPARK_MAX_CORES@@@@
DESTFILE=/usr/lib/spark/spark-2.2.1-bin-hadoop2.7/conf/spark-defaults.conf
sed -i "s!${PATTERN}!${SPARK_MAX_CORES}!g" ${DESTFILE}

#ZEPP_CORES=`expr $TotalCores / 3`
#PATTERN=@@@@ZEPPELIN_CORES@@@@
#DESTFILE=/usr/lib/zeppelin/zeppelin-0.8.0-SNAPSHOT/conf/zeppelin-env.sh
#sed -i "s!${PATTERN}!${ZEPP_CORES}!g" ${DESTFILE}

