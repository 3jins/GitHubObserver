from bs4 import BeautifulSoup
import threading
import json


class GitHubLogin:
    def __init__(self, session, id, pw):
        self.session = session
        self.id = id
        self.pw = pw

    # Get inputs that have a specific name.
    def get_specific_name_input(self, inputs, names):
        specific_inputs = []
        for input in inputs:
            if input['name'] in names:
                specific_inputs.append(input)
        return specific_inputs

    # Get tokens in GitHub login page
    def get_login_token(self):
        tokens = {}
        url = 'https://github.com/login'
        source_code = self.session.get(url)
        soup = BeautifulSoup(source_code.text, "html.parser")

        inputs = soup.find_all('input')
        inputs = self.get_specific_name_input(inputs, ['authenticity_token'])

        for input in inputs:
            tokens[input['name']] = input['value']

        return tokens

    # Sign in with given accoutn information
    def login(self):
        token = self.get_login_token()
        login_info = {
            'login': self.id,
            'password': self.pw,
        }
        login_info.update(token)

        login_response = self.session.post('https://github.com/session', data=login_info)
        if login_response.status_code == 200:
            print("Login Success")
        else:
            print(str(login_response.status_code) + ": " + str(login_response.reason))
            self.login()


class GitHubCrawl:
    def __init__(self, session):
        self.session = session

    def crawl_feed(self, feeds, num_feeds_save):
        feed_list = []
        if len(feeds) > 0:
            for no, feed in enumerate(feeds):
                if no < 5:  # meaningless divisors
                    continue
                elif no > 7 + num_feeds_save:  # too many feeds
                    break
                try:
                    feed_info = {}
                    tag = feed['class']
                    soup = BeautifulSoup(str(feed), "html.parser")
                    anchors = soup.find_all('a')
                    feed_info['tag'] = tag[0]
                    for no, anchor in enumerate(anchors):
                        if no == 0:
                            soup = BeautifulSoup(str(anchor), "html.parser")
                            images = soup.find_all('img')
                            for image in images:
                                feed_info['icon'] = image['src']
                        elif no == 1:
                            soup = BeautifulSoup(str(anchor), "html.parser")
                            strings = soup.stripped_strings
                            for string in strings:
                                feed_info['user_name'] = string
                        elif no == 2:
                            feed_info['link'] = "https://github.com" + str(anchor['href'])
                        else:
                            feed_info['original_link'] = "https://github.com" + str(anchor['href'])
                    feed_list.append(feed_info)
                except TypeError:
                    continue
        return feed_list

    def crawl(self):
        url = 'https://github.com'
        source_code = self.session.get(url)
        soup = BeautifulSoup(source_code.text, "html.parser")

        newsfeed = soup.find('div', class_='news')
        feed_list = self.crawl_feed(newsfeed, 10)

        return feed_list


class GitHubObserve:
    def __init__(self, session, fb_bot):
        self.session = session
        self.fb_bot = fb_bot
        self.github_crawl = GitHubCrawl(self.session)
        pass

    # Get 차집합. 'set(list) - set(list)' doesn't support when a list contains dictionary.
    def get_difference_set(self, list1, list2):
        result = []
        for item in list1:
            if item not in list2:
                result.append(item)
        return result

    # Save older feeds info as a file
    # Compare feeds in the file and feeds that the bot has just crawled
    # If there are new feeds, return them.
    def compare_feeds(self, feed_list):
        try:
            with open('recent_feeds', 'r') as f:
                recent_feeds = f.read()
                recent_feeds = json.loads(recent_feeds)
        except FileNotFoundError:
            recent_feeds = []

        new_feeds = self.get_difference_set(feed_list, recent_feeds)
        if len(new_feeds) > 0:
            # update data file
            with open('recent_feeds', 'w') as f:
                json.dump(feed_list, f)
            updated_feeds = []
            # process new data
            for feed in new_feeds:
                print("Change occured!!")
                updated_feeds.append(feed)
            return updated_feeds
        else:
            return []

    def get_new(self, facebook_client):
        # Check if there is a new feed
        feed_list = self.github_crawl.crawl()
        updated_feeds = self.compare_feeds(feed_list)

        # Send new feeds by Facebook message
        if len(updated_feeds) > 0:
            self.fb_bot.send_message(updated_feeds)

        # Iterate until a user inputs 'quit'
        thread = threading.Timer(30, self.get_new, [self.session])
        thread.daemon = True
        thread.start()
        while input() != 'quit':
            continue
        print("Bye!  (^^)/")



