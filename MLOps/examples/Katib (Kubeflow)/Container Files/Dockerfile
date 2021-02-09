FROM gcr.io/kubeflow-images-public/tensorflow-2.0.0a-notebook-cpu:v0.5.0
RUN pip install pandas
RUN pip install scikit-learn kfp==1.0.0 joblib fire kubernetes==10.0.1 fairing==0.5.1 urllib3==1.24.2
COPY taxi_for_katib.py /opt/taxi/taxi_for_katib.py
COPY testingalt_yellow_tripdata_2009-01.csv /opt/taxi/testingalt_yellow_tripdata_2009-01.csv

WORKDIR /opt/taxi

RUN chgrp -R 0 /opt/taxi \
  && chmod -R g+rwX /opt/taxi

ENTRYPOINT ["python", "/opt/taxi/taxi_for_katib.py"]