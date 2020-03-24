FROM saurabhjogalekarhpe/baseaiml:latest
ENV http_proxy=""
ENV https_proxy=""
ENV ftp_proxy=""
ENV no_proxy=""
ADD model.py /opt/model.py
ENTRYPOINT [ "/bin/python3", "/opt/model.py" ]
