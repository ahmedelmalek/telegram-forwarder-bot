import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os

# قراءة البيانات من GitHub Secrets
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
SESSION_STRING = os.environ.get('SESSION_STRING')
TARGET_CHANNEL = int(os.environ.get('TARGET_CHANNEL'))

# قنوات المصدر
SOURCE_CHANNELS = [
    "@EL_King_4",
    "@TCLSyria",
    "@syrian_company_sy",
    "@hhhhhhhnmhossam",
    "@belleni",
    "@awladmahmoud5",
    "@msyrshop",
]

# استخدام الجلسة الثابتة
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward(event):
    try:
        await client.send_message(TARGET_CHANNEL, event.message)
        print("✅ تم نسخ منشور جديد")
    except Exception as e:
        print(f"❌ خطأ: {e}")

async def main():
    print("🚀 بوت النسخ يعمل...")
    await client.start()
    print("✅ تم تسجيل الدخول بنجاح!")
    await client.run_until_disconnected()

asyncio.run(main())
