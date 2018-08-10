# image for RHEL/CentOS

FROM bluedata/centos7:latest

# Install EPEL repo
RUN yum install -y http://download.fedoraproject.org//pub/epel/epel-release-latest-7.noarch.rpm

#Remove java7 and install java 8
RUN yum -y erase java-1.7.0-openjdk-devel
## Install java 8 and configure
ADD configure_java8.sh /root/configure_java8.sh
RUN chmod +x /root/configure_java8.sh && /root/configure_java8.sh && rm -f /root/configure_java8.sh

RUN echo 1 | update-alternatives --config java

# Install EPEL repo
RUN yum install -y bzip2

RUN yum install -y expect mysql-server mysql-connector-java             \
                   php-5.3.3 php-xml php-pear php-gd R R-devel libcurl-devel openssl-devel libxml2-devel

RUN sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm


#wget Ananconda parcels (totally optional for additional packages like numpy, scipy etc.,)

RUN wget -q https://repo.continuum.io/archive/Anaconda3-5.2.0-Linux-x86_64.sh -P /root/
RUN chmod +x /root/Anaconda3-5.2.0-Linux-x86_64.sh && /root/Anaconda3-5.2.0-Linux-x86_64.sh -b -p /opt/anaconda3 && rm -f /root/Anaconda3-5.2.0-Linux-x86_64.sh

## Download and extract spark
RUN mkdir /usr/lib/spark; curl -s http://archive.apache.org/dist/spark/spark-2.2.1/spark-2.2.1-bin-hadoop2.7.tgz | tar xz -C /usr/lib/spark/

## Download thirdparty aws jars
RUN wget -q https://s3.amazonaws.com/bluedata-catalog/thirdparty/aws-jars/aws-java-sdk-1.7.4.jar -P /opt/bluedata/
RUN wget -q https://s3.amazonaws.com/bluedata-catalog/thirdparty/aws-jars/hadoop-aws-2.7.1.jar -P /opt/bluedata/

## Create spark-event dir and give permissions
RUN mkdir /tmp/spark-events
RUN chmod -R 777 /tmp/spark-events/

## Give logs and conf permissions
RUN mkdir -p /usr/lib/spark/spark-2.2.1-bin-hadoop2.7/logs
RUN touch /usr/lib/spark/spark-2.2.1-bin-hadoop2.7/logs/Bluedata-spark-logs
RUN chmod -R 1777 /usr/lib/spark/spark-2.2.1-bin-hadoop2.7/logs/
RUN mkdir -p /usr/lib/spark/spark-2.2.1-bin-hadoop2.7/warehouse
RUN chmod -R 1777 /usr/lib/spark/spark-2.2.1-bin-hadoop2.7/warehouse/

# make spark bin dir accessible to all
RUN echo "export PATH=$PATH:/usr/lib/spark/spark-2.2.1-bin-hadoop2.7/bin/" > /etc/profile.d/updatePath.sh

