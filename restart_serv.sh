. env/bin/activate
./stop_gunicorn.sh
./run_gunicorn.sh
pkill -9 celery
sudo systemctl daemon-reload
sudo systemctl start celeryd
sudo systemctl start celerybeat
