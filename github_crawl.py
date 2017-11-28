from bs4 import BeautifulSoup


def crawl_feed(feeds):
    feed_list = []
    for no, feed in enumerate(feeds):
        if no < 5:      # meaningless divisors
            continue
        elif no > 10:   # too many feeds
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



def crawl(session):
    url = 'https://github.com'
    source_code = session.get(url)
    soup = BeautifulSoup(source_code.text, "html.parser")

    newsfeed = soup.find('div', class_='news')
    feed_list = crawl_feed(newsfeed)

    return feed_list
