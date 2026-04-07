import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os

API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
SESSION_STRING = os.environ.get('SESSION_STRING')
TARGET_CHANNEL = int(os.environ.get('TARGET_CHANNEL'))

SOURCE_CHANNELS = [
    "@EL_King_4",
    "@TCLSyria",
    "@syrian_company_sy",
    "@hhhhhhhnmhossam",
    "@belleni",
    "@awladmahmoud5",
    "@msyrshop",
]

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def copy_recent_messages():
    """نسخ آخر 5 منشورات من كل قناة مصدر عند بدء التشغيل"""
    print("📡 جاري جلب آخر المنشورات من القنوات...")
    
    for channel in SOURCE_CHANNELS:
        try:
            # جلب آخر 5 منشورات من القناة
            messages = await client.get_messages(channel, limit=5)
            
            for msg in messages:
                try:
                    await client.send_message(TARGET_CHANNEL, msg)
                    print(f"✅ تم نسخ منشور قديم من {channel}")
                    await asyncio.sleep(1)  # تأخير بسيط
                except Exception as e:
                    print(f"❌ فشل نسخ منشور من {channel}: {e}")
                    
        except Exception as e:
            print(f"❌ خطأ في جلب المنشورات من {channel}: {e}")
    
    print("✅ انتهى نسخ آخر المنشورات")

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward_new(event):
    """نسخ المنشورات الجديدة فوراً"""
    try:
        await client.send_message(TARGET_CHANNEL, event.message)
        print(f"✅ تم نسخ منشور جديد")
    except Exception as e:
        print(f"❌ خطأ: {e}")

async def main():
    print("🚀 بوت نسخ العروض يعمل...")
    await client.start()
    print("✅ تم تسجيل الدخول بنجاح!")
    
    # نسخ آخر المنشورات أولاً
    await copy_recent_messages()
    
    print("🎯 جاهز لنسخ المنشورات الجديدة...")
    await client.run_until_disconnected()

asyncio.run(main())
