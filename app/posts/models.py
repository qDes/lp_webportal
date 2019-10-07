import datetime

#from flask_mongoengine import MongoEngine
#db = MongoEngine()

from app.db import db

class Post(db.Document):
    title = db.StringField(required=True)
    tag = db.StringField(max_length=25)
    text = db.StringField()
    urls = db.ListField(db.StringField())
    posted = db.DateTimeField(default=datetime.datetime.now)

    def __repr__(self):
        return f"Post {self.title}"
