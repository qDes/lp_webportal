import requests
import json
from parser_params import ACCESS_TOKEN, API_V, PIKABU_ID, SECOND_ID, DTHREE_ID

POST_COUNT = 10

r_pika = requests.get(f'https://api.vk.com/method/wall.get?owner_id={PIKABU_ID}&count={POST_COUNT}&access_token={ACCESS_TOKEN}&v={API_V}')
r_sec = requests.get(f'https://api.vk.com/method/wall.get?owner_id={SECOND_ID}&count={POST_COUNT}&access_token={ACCESS_TOKEN}&v={API_V}')
r_dthree = requests.get(f'https://api.vk.com/method/wall.get?owner_id={DTHREE_ID}&count={POST_COUNT}&access_token={ACCESS_TOKEN}&v={API_V}')

#with open('test_4.json', 'w', encoding='utf-8') as f:
#    json.dump(r.json(), f, indent=2, ensure_ascii=False)

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

#def filter_json(checkpost):
    #with open('test_data.json', 'r', encoding='utf-8') as file:
        #try:
            #test_filter = json.load(file)
        #except:
            #print('fail')

        #for post in test_filter:
            #if post['img'] == null:
                #del test_filter[0]
                #del test_filter[1]
                #del test_filter[2]
            #file.write(json.dumps(test_filter))
            #print(post)

posts = take_posts()

test_data = []

for post in posts:
    post_data = get_data(post)
    test_data.extend([post_data])
    print(post_data)

write_json(test_data)
#filter_json(test_data)