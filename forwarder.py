import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
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
    """نسخ آخر 5 منشورات من كل قناة"""
    print("\n📡 جاري نسخ آخر المنشورات من القنوات...\n")
    
    for channel in SOURCE_CHANNELS:
        try:
            # جلب آخر 5 منشورات
            messages = await client.get_messages(channel, limit=5)
            count = 0
            
            for msg in messages:
                if msg:
                    await client.send_message(TARGET_CHANNEL, msg)
                    count += 1
                    print(f"✅ تم نسخ منشور {count}/5 من {channel}")
                    await asyncio.sleep(2)  # تأخير 2 ثانية بين كل منشور
            
            print(f"📊 اكتمل: {channel} → {count} منشورات\n")
            
        except Exception as e:
            print(f"❌ خطأ في {channel}: {e}")
    
    print("✅ انتهى نسخ آخر المنشورات!")

async def main():
    print("🚀 بوت النسخ يعمل...")
    await client.start()
    print("✅ تم تسجيل الدخول!")
    
    # طلب الانضمام إلى القنوات
    for channel in SOURCE_CHANNELS:
        try:
            await client(JoinChannelRequest(channel))
            print(f"✅ تم الانضمام إلى {channel}")
        except:
            pass
    
    # نسخ آخر 5 منشورات من كل قناة
    await copy_recent_messages()
    
    print("🎯 جاهز لنسخ المنشورات الجديدة...")
    await client.run_until_disconnected()

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward_new(event):
    """نسخ المنشورات الجديدة فوراً"""
    try:
        await client.send_message(TARGET_CHANNEL, event.message)
        print(f"✅ تم نسخ منشور جديد")
    except Exception as e:
        print(f"❌ خطأ: {e}")

asyncio.run(main())
