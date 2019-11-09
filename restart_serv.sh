. env/bin/activate
./stop_gunicorn.sh
./run_guinicorn.sh
pkill -9 celery
sudo systemctl daemon-reload
sudo systemctl start celeryd
sudo systemctl start celerybeat
