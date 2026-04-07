import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os

API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
SESSION_STRING = os.environ.get('SESSION_STRING')
TARGET_CHANNEL = int(os.environ.get('TARGET_CHANNEL'))

SOURCE_CHANNELS = ["@EL_King_4"]

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def main():
    print("جاري بدء البوت...")
    await client.start()
    print("تم الدخول بنجاح!")
    
    # جلب آخر منشور
    messages = await client.get_messages(SOURCE_CHANNELS[0], limit=1)
    if messages:
        print(f"تم العثور على منشور: {messages[0].text[:50] if messages[0].text else 'بدون نص'}")
        await client.send_message(TARGET_CHANNEL, messages[0])
        print("تم إرسال المنشور إلى قناتك!")
    else:
        print("لا توجد منشورات")

asyncio.run(main())
