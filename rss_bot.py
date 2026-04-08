import feedparser
import requests
import os
import time
from datetime import datetime

# قراءة البيانات من GitHub Secrets
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('TARGET_CHANNEL')

# قائمة مصادر RSS (عروض وأخبار)
RSS_FEEDS = [
    "https://www.cnet.com/rss/news/",
    "https://www.techradar.com/rss",
    "https://www.engadget.com/rss.xml",
    "https://www.wired.com/feed/rss",
    "https://feeds.feedburner.com/egyptdeals",  # عروض مصر
]

# ملف لتتبع المنشورات المرسلة
SENT_FILE = "sent_urls.txt"

def load_sent():
    """تحميل الروابط المرسلة سابقاً"""
    try:
        with open(SENT_FILE, 'r') as f:
            return set(f.read().splitlines())
    except:
        return set()

def save_sent(url):
    """حفظ رابط تم إرساله"""
    with open(SENT_FILE, 'a') as f:
        f.write(url + "\n")

def send_message(text):
    """إرسال رسالة إلى القناة"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(url, json={
            "chat_id": CHANNEL_ID, 
            "text": text, 
            "parse_mode": "HTML"
        }, timeout=10)
        if response.status_code == 200:
            print("✅ تم الإرسال")
        else:
            print(f"❌ فشل الإرسال: {response.text}")
    except Exception as e:
        print(f"❌ خطأ: {e}")

def check_feeds():
    """فحص جميع مصادر RSS"""
    sent = load_sent()
    new_count = 0
    
    print(f"🚀 بدء فحص {len(RSS_FEEDS)} مصدر...")
    
    for feed_url in RSS_FEEDS:
        try:
            print(f"📡 جاري فحص: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:5]:  # آخر 5 منشورات
                if entry.link in sent:
                    continue
                
                # تنسيق الرسالة
                message = f"""
🔥 <b>عرض جديد</b> 🔥

<b>{entry.title}</b>

{entry.summary[:200] if hasattr(entry, 'summary') else ''}

📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}

🔗 <a href="{entry.link}">اضغط للتفاصيل</a>

#عروض #تخفيضات #تسوق_اونلاين
"""
                send_message(message)
                save_sent(entry.link)
                new_count += 1
                time.sleep(2)  # تأخير بين الرسائل
                
        except Exception as e:
            print(f"❌ خطأ في {feed_url}: {e}")
    
    print(f"✅ اكتمل! تم إرسال {new_count} منشور جديد")

if __name__ == "__main__":
    print("🚀 بوت RSS يعمل...")
    check_feeds()
