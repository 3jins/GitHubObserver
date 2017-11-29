from fbchat import Client
import json


class FacebookBot:
    def __init__(self):
        self.facebook_account = None

    def login(self):
        with open('facebookbot_account') as f:
            self.facebook_account = json.loads(f.read())
            self.facebook_client = Client(self.facebook_account['id'], self.facebook_account['password'])


    def send_message(self, updated_feeds):
        humanize_tag = {
            'fork': [' forked ', ' from '],
            'watch_started': [' starred ', ''],
            'create': [' created a repository ', ''],
            'public': [' made ', ' public.'],
        }

        target = self.facebook_client.searchForUsers('전세진')[0]

        for feed in updated_feeds:
            message = ""
            message += str(feed['user_name'])
            message += str(humanize_tag[feed['tag']][0])
            message += str(feed['link'])
            message += str(humanize_tag[feed['tag']][1])
            if 'original_link' in feed:
                message + str(feed['original_link'])

            sent = self.facebook_client.sendMessage(message, thread_id=target.uid)
            if not sent:
                print("Something in facebook_bot.py goes wrong... :(")
