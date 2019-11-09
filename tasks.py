import os
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab

from app import create_app
from app.posts.parsers import vk_parser
from app.posts.parsers import vk_parser2

load_dotenv()
login = os.environ.get('vk_login')
password = os.environ.get('vk_password')

flask_app = create_app()
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def get_vk_pics():
    with flask_app.app_context():
        vk_parser.write_posts(login,password, 10, -100817956, 'vk_pars1')

@celery_app.task
def parse_vk():
    with flask_app.app_context():
        vk_parser2.write_to_db()
    

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour='*/2'), get_vk_pics.s())
    sender.add_periodic_task(crontab(hour='*/2'), parse_vk.s())

if __name__=="__main__":
    parse_vk()
