PATH=/sbin:/usr/sbin:/bin:/usr/bin:/opt/anaconda3/bin/
cd /etc/jupyterhub
sudo -u jupyter /opt/anaconda3/bin/jupyterhub -f /etc/jupyterhub/jupyterhub_config.py </dev/null & >>/var/log/jupyterhub.log
echo $! > /var/run/jupyterhub.pid
