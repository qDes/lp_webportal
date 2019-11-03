gunicorn --bind 127.0.0.1:5000 wsgi:flask_app -w 3 --daemon
