import os
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab

from app import create_app
from app.posts.parsers import vk_pars

load_dotenv()
login = os.environ.get('vk_login')
password = os.environ.get('vk_password')

flask_app = create_app()
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def get_vk_pics():
    with flask_app.app_context():
        vk_pars.write_posts(login,password, 30, -100817956, 'vk_pars1')

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minutes='*/10'), get_vk_pics.s())
