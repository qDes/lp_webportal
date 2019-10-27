import datetime
import mongoengine
from app.db import db
from app.user.models import User


class Comment(db.Document):
    text = db.StringField(required=True)
    created = db.DateTimeField(default=datetime.datetime.now())
    from_user = db.ReferenceField(User,required=True)
    post = db.ReferenceField('Post')#, reverse_delete_rule=mongoengine.CASCADE)

    def __repr__(self):
        return f"Comment {self.text} by {self.from_user}"

class Post(db.Document):
    title = db.StringField(required=True)
    tag = db.StringField(max_length=25)
    text = db.StringField()
    urls = db.ListField(db.StringField())
    posted = db.DateTimeField(default=datetime.datetime.now)
    comments = db.ListField(db.ReferenceField(Comment,reverse_delete_rule=mongoengine.PULL))
    user = db.ReferenceField(User)
    def __repr__(self):
        return f"Post {self.title}"


Post.register_delete_rule(Comment,'post', mongoengine.CASCADE)


