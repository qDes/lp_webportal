import datetime
from config import MONGO_URI
from mongoengine import connect

from flask_mongoengine import MongoEngine

db = MongoEngine()

class Post(db.Document):
    title = db.StringField(required=True)
    tag = db.StringField(max_length=25)
    text = db.StringField()
    urls = db.ListField(db.StringField())
    posted = db.DateTimeField(default=datetime.datetime.now)

    def __repr__(self):
        return f"Post {self.title}"

connect(db='testdb',host=MONGO_URI)



for post in Post.objects():
    print(post.text)

'''
Post(
        title='Engine test',
        tag='pytest',
        text='Hello Everyone!',
        urls= ['https://sun6-14.userapi.com/c855128/v855128189/10f4b2/J977kYyDEag.jpg',
            'https://sun9-45.userapi.com/c855128/v855128189/10f478/yH9fX5eBFOA.jpg'],
        ).save()
'''
