import feedparser

def parse(url):
    d = feedparser.parse(url)
    return d.entries
