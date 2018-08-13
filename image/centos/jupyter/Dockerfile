# image for RHEL/CentOS

FROM bluedata/centos7:latest

# Install EPEL repo
RUN yum install -y epel-release

# Install EPEL repo
RUN yum install -y bzip2

RUN yum install -y expect mysql-server mysql-connector-java             \
                   php-5.3.3 php-xml php-pear php-gd R R-devel libcurl-devel openssl-devel libxml2-devel

#wget Ananconda parcels

RUN wget -q https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh -P /root/
RUN chmod +x /root/Anaconda3-5.2.0-Linux-x86_64.sh && /root/Anaconda3-5.2.0-Linux-x86_64.sh -b -p /opt/anaconda3 && rm -f /root/Anaconda3-5.2.0-Linux-x86_64.sh

#Install git
RUN sudo yum -y install git

#Install jupyter norebook

RUN mkdir -p /root/.ipython/kernels/pyspark

ADD configure_jupyter.sh /root/configure_jupyter.sh
RUN chmod +x /root/configure_jupyter.sh && /root/configure_jupyter.sh && rm -f /root/configure_jupyter.sh

RUN echo "export PATH=$PATH:/opt/anaconda3/bin/" > /etc/profile.d/updatePath.sh


## Install java 8 and configure
ADD configure_java8.sh /root/configure_java8.sh
RUN chmod +x /root/configure_java8.sh && /root/configure_java8.sh && rm -f /root/configure_java8.sh

RUN echo 1 | update-alternatives --config java

## Download and extract spark
RUN mkdir /usr/lib/spark; curl -s http://archive.apache.org/dist/spark/spark-2.2.1/spark-2.2.1-bin-hadoop2.7.tgz | tar xz -C /usr/lib/spark/

## Create spark-event dir and give permissions
RUN mkdir /tmp/spark-events
RUN chmod -R 777 /tmp/spark-events/
ADD configure_java8.sh /root/configure_java8.sh
RUN chmod +x /root/configure_java8.sh && /root/configure_java8.sh && rm -f /root/configure_java8.sh

# image for RHEL/CentOS
RUN mkdir /usr/lib/spark; curl -s http://archive.apache.org/dist/spark/spark-2.2.1/spark-2.2.1-bin-hadoop2.7.tgz | tar xz -C /usr/lib/spark/

## Give logs and conf permissions
RUN mkdir -p /usr/lib/spark/spark-2.2.1-bin-hadoop2.7/logs
RUN touch /usr/lib/spark/spark-2.2.1-bin-hadoop2.7/logs/Bluedata-spark-logs
RUN chmod -R 1777 /usr/lib/spark/spark-2.2.1-bin-hadoop2.7/logs/
RUN mkdir -p /usr/lib/spark/spark-2.2.1-bin-hadoop2.7/warehouse
RUN chmod -R 1777 /usr/lib/spark/spark-2.2.1-bin-hadoop2.7/warehouse/

# make spark bin dir accessible to all
RUN echo "export PATH=$PATH:/usr/lib/spark/spark-2.2.1-bin-hadoop2.7/bin/" > /etc/profile.d/updatePath.sh

#Install Toree kernel after Spark is installed
RUN /opt/anaconda3/bin/pip install --upgrade pip

RUN /opt/anaconda3/bin/pip install https://pypi.anaconda.org/hyoon/simple/toree/0.2.0.dev1/toree-0.2.0.dev1.tar.gz && /opt/anaconda3/bin/jupyter toree install --interpreters=Scala,PySpark,SQL --spark_home=/usr/lib/spark/spark-2.2.1-bin-hadoop2.7

# Run jupyter upgrade after Toree install
RUN /opt/anaconda3/bin/pip install jupyter -U
