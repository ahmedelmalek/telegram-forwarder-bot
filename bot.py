import requests
import time
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
TARGET_CHANNEL = os.environ.get('TARGET_CHANNEL')

# قنوات المصدر (سنستخدم البوت لقراءة الرسائل منها)
SOURCE_CHANNELS = [
    "@EL_King_4",
    "@TCLSyria",
    "@syrian_company_sy",
    "@hhhhhhhnmhossam",
    "@belleni",
    "@awladmahmoud5",
    "@msyrshop",
]

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

# رسالة تجريبية للتأكد من أن البوت يعمل
send_message(TARGET_CHANNEL, "✅ البوت يعمل بنجاح! سينسخ العروض الجديدة تلقائياً.")

print("✅ تم إرسال رسالة تجريبية إلى قناتك")
