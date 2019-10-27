from app import create_app
from app.posts.models import Post
from app.user.models import User

flask_app = create_app()

user = User.objects(username="test").get()
for post in Post.objects():
    post.user=user
    post.save()
    print(post.user)
