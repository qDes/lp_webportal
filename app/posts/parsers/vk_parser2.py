import requests
import json

from app.posts.models import Post
from app.user.models import User
from app.posts.parsers.vk_parser import get_last_urls
from app.posts.parsers.parser_params import ACCESS_TOKEN, API_V, PIKABU_ID, SECOND_ID, DTHREE_ID

POST_COUNT = 10

r_pika = requests.get(f'https://api.vk.com/method/wall.get?owner_id={PIKABU_ID}&count={POST_COUNT}&access_token={ACCESS_TOKEN}&v={API_V}')
r_sec = requests.get(f'https://api.vk.com/method/wall.get?owner_id={SECOND_ID}&count={POST_COUNT}&access_token={ACCESS_TOKEN}&v={API_V}')
r_dthree = requests.get(f'https://api.vk.com/method/wall.get?owner_id={DTHREE_ID}&count={POST_COUNT}&access_token={ACCESS_TOKEN}&v={API_V}')


def take_posts():
    all_posts = []
    all_posts_pika = []
    all_posts_sec = []
    all_posts_dthree = []
    data_pika = r_pika.json()['response']['items']
    data_sec = r_sec.json()['response']['items']
    data_dthree = r_dthree.json()['response']['items']
    all_posts_pika.extend(data_pika)
    all_posts_sec.extend(data_sec)
    all_posts_dthree.extend(data_dthree)
    all_posts.extend(all_posts_pika)
    all_posts.extend(all_posts_sec)
    all_posts.extend(all_posts_dthree)
    return all_posts

def get_data(post):
    try:
        post_datetime = post['date']
    except:
        post_datetime = None
    try:
        if post['text'] != '':
            post_text = post['text']
        else:
            if 'attachments' not in post:
                post_text = 0
            if 'copy_history' in post:
                post_text = post['copy_history'][0]['text']
    except:
        post_text = None
    try:
        post_img = post['attachments'][0]['photo']['sizes'][-1]['url']
    except:
        if 'attachments' not in post:
            post_img = 'No Images'
            if 'copy_history' in post:
                post_img = post['copy_history'][0]['attachments'][0]['photo']['sizes'][-1]['url']
            if 'doc' in post:
                post_img = post['attachments'][0]['doc']['url']
            if 'video' in post:
                post_img = post['attachments'][0]['video']['first_frame'][-1]['url']
            else:
                if 'link' in post:
                    post_img = post['attachments'][-1]['link']['photo']['sizes'][-1]['url']
        else:
            post_img = None

    data = {
        'date': post_datetime,
        'text': post_text,
        'img': post_img
    }

    return data

def write_json(data):
    with open('test_data.json', 'a', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def write_to_db():
    posts = take_posts()
    user = User.objects(username='parser').get()
    last_posts_urls = get_last_urls(50)
    posts_value = Post.objects.count()
    for post in posts:
        data = get_data(post)
        if data.get('img') is None:
            continue
        if data.get('img') not in last_posts_urls:
            Post(title=f"Post {posts_value}",
                    urls=[data.get('img')],
                    tag='vk2',
                    text=data.get('text'),
                    user=user).save()
            posts_value += 1



if __name__ == "__main__":
    posts = take_posts()

    test_data = []

    for post in posts:
        post_data = get_data(post)
        test_data.extend([post_data])
        print(post_data)

