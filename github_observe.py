import json
import threading

import github_crawl


# Get 차집합. 'set(list) - set(list)' doesn't support when a list contains dictionary.
def get_difference_set(list1, list2):
    result = []
    for item in list1:
        if item not in list2:
            result.append(item)
    return result


def compare_feeds(feed_list):
    try:
        with open('recent_feeds', 'r') as f:
            recent_feeds = f.read()
            recent_feeds = json.loads(recent_feeds)
    except FileNotFoundError:
        recent_feeds = []

    new_feeds = get_difference_set(feed_list, recent_feeds)
    if len(new_feeds) > 0:
        # update data file
        with open('recent_feeds', 'w') as f:
            json.dump(feed_list, f)
        # process new data
        for feed in new_feeds:
            print(feed)


def get_new(session):
    feed_list = github_crawl.crawl(session)
    compare_feeds(feed_list)
    thread = threading.Timer(30, get_new, [session])
    thread.daemon = True
    thread.start()
    while input() != 'quit':
        continue
    print("Bye!  (^^)/")



