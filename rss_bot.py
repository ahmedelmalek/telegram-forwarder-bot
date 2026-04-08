import feedparser
import requests
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('TARGET_CHANNEL')

RSS_FEEDS = [
    "https://www.cnet.com/rss/news/",
    "https://www.techradar.com/rss",
]

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHANNEL_ID, "text": text})

for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:3]:
        msg = f"🔥 {entry.title}\n🔗 {entry.link}"
        send_message(msg)
