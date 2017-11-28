import json
import threading

import github_crawl
import facebook_message


# Get 차집합. 'set(list) - set(list)' doesn't support when a list contains dictionary.
def get_difference_set(list1, list2):
    result = []
    for item in list1:
        if item not in list2:
            result.append(item)
    return result


# Save older feeds info as a file
# Compare feeds in the file and feeds that the bot has just crawled
# If there are new feeds, return them.
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
        updated_feeds = []
        # process new data
        for feed in new_feeds:
            print("Change occured!!")
            updated_feeds.append(feed)
        return updated_feeds
    else:
        return []


def get_new(session, facebook_client):
    # Check if there is a new feed
    feed_list = github_crawl.crawl(session)
    updated_feeds = compare_feeds(feed_list)

    # Send new feeds by Facebook message
    if len(updated_feeds) > 0:
        facebook_message.send_message(updated_feeds, facebook_client)

    # Iterate until a user inputs 'quit'
    thread = threading.Timer(5, get_new, [session])
    thread.daemon = True
    thread.start()
    while input() != 'quit':
        continue
    print("Bye!  (^^)/")



