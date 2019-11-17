from app.posts.models import Post
from app.user.models import User
import vk_api

def get_pic_urls(login, password, count, owner_id): 
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth()
    except vk_api.AuthError as err:
        print(err)
        return None
    
    vk = vk_session.get_api()
    wall = vk.wall.get(owner_id=owner_id, count = count)
    posts = wall['items']
    pic_urls= []
    #get picture urls
    for num,post in enumerate(posts):
        try:
            url = post['attachments'][-1]['photo']['sizes'][-1]['url']
        except (KeyError, IndexError):
            continue
        if url:
            pic_urls.append(url)
    return pic_urls

def get_last_urls(count):
    urls = []
    for post in Post.objects().order_by("-posted").limit(count):
        urls.append(post.urls)
    urls = sum(urls,[])
    return urls

def write_posts(login, password, count, owner_id, username):
    urls = get_pic_urls(login,password, count, owner_id)
    user = User.objects(username=username).get()
    posts_value = Post.objects.count()
    last_posts_urls = get_last_urls(500)
    for url in urls:
        if url not in last_posts_urls:
            Post(title=f"Post {posts_value}",
                    urls=[url],
                    tag='vk',
                    text='',
                    user=user).save()
            posts_value += 1

