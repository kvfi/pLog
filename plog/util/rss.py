import datetime
from urllib.parse import urlparse

import feedparser
import yaml

from util.mongo import MongoDB

db = MongoDB.getInstance()


def parse_rss(f, s):
    d = feedparser.parse(f)
    for x in d['entries'][:5]:
        o = urlparse(x['link'])
        i = {'site': k, 'domain': o.netloc.lstrip('www.'), 'title': x['title'], 'link': x['link'],
             'added_on': datetime.datetime.now()}
        store.append(i)
    return store


with open('../../config.yaml', 'r') as stream:
    try:
        feed = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

store = []

rss = feed['rss']
for a in rss:
    for k in a.keys():
        feed_url = a[k]
        if isinstance(feed_url, list):
            for feed_url_item in feed_url:
                parse_rss(feed_url_item, store)
        else:
            parse_rss(feed_url, store)

result = db.client.plog.links.insert_many(store)
print(len(result.inserted_ids))
