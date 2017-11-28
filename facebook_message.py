from fbchat import Client
import json


facebook_account = ""

def login():
    facebook_client = None
    global facebook_account
    
    with open('facebookbot_account') as f:
        facebook_account = json.loads(f.read())
        facebook_client = Client(facebook_account['id'], facebook_account['password'])

    return facebook_client


def send_message(updated_feeds, facebook_client):
    humanize_tag = {
        'fork': [' forked ', ' from '],
        'watch_started': [' starred ', ''],
        'create': [' created a repository ', ''],
        'public': [' made ', ' public.'],
    }

    target = facebook_client.searchForUsers(facebook_account['id'])[0]
    # target = facebook_client.searchForUsers('우용하')[0]

    for feed in updated_feeds:
        message = ""
        message + str(feed['user_name'])
        message + str(humanize_tag[feed['tag']][0])
        message + str(feed['link'])
        message + str(feed['tag'][1])
        if 'original_link' in feed:
            message + str(feed['original_link'])

        sent = facebook_client.sendMessage(message, thread_id=target.uid)
        if not sent:
            print("Something in facebook_message.py goes wrong... :(")
