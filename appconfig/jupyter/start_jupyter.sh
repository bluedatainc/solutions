/opt/anaconda3/bin/pyvenv --without-pip /opt/p3env
source /opt/p3env/bin/activate
export USER=root
mkdir /opt/bluedata/jupyter
/opt/anaconda3/bin/jupyter-notebook --no-browser --allow-root </dev/null & >>/var/log/jupyter-notebook.log
echo $! > /var/run/jupyter-notebook.pid
