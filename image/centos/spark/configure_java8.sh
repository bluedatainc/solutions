#!/bin/bash
# Script to Install JAVA 8 (JDK 8u40) on CentOS/RHEL 7/6/5 and Fedora
# http://tecadmin.net/install-java-8-on-centos-rhel-and-fedora/

echo "Installing Java 8 (64bit)"

cd /opt/

wget -c --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u131-b11/d54c1d3a095b4ff2b6607d096fa80163/jdk-8u131-linux-x64.tar.gz
tar xzf jdk-8u131-linux-x64.tar.gz

cd /opt/jdk1.8.0_131/

alternatives --install /usr/bin/java java /opt/jdk1.8.0_131/bin/java 1
update-alternatives --config java 1

alternatives --install /usr/bin/jar jar /opt/jdk1.8.0_131/bin/jar 1
alternatives --install /usr/bin/javac javac /opt/jdk1.8.0_131/bin/javac 1
update-alternatives --set jar /opt/jdk1.8.0_131/bin/jar
update-alternatives --set javac /opt/jdk1.8.0_131/bin/javac

export JAVA_HOME=/opt/jdk1.8.0_131
