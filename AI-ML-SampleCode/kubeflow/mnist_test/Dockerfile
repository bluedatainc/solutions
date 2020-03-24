FROM saurabhjogalekarhpe/baseaiml:latest
ENV http_proxy=http://web-proxy.corp.hpecorp.net:8080
ENV https_proxy=http://web-proxy.corp.hpecorp.net:8080
ENV ftp_proxy=http://web-proxy.corp.hpecorp.net:8080
ENV no_proxy="localhost,127.0.0.1"
RUN echo "proxy=http://web-proxy.corp.hpecorp.net:8080" >> /etc/yum.conf
ADD three_step_test.py /opt/three_step_test.py
ENTRYPOINT [ "/bin/python3", "/opt/three_step_test.py" ]
