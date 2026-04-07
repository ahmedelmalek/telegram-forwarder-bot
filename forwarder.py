import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
import os

API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
SESSION_STRING = os.environ.get('SESSION_STRING')
TARGET_CHANNEL = int(os.environ.get('TARGET_CHANNEL'))

# ==================== جميع القنوات ====================
SOURCE_CHANNELS = [
    # أجهزة كهربائية
    "@EL_King_4",
    "@TCLSyria",
    "@syrian_company_sy",
    "@hhhhhhhnmhossam",
    "@belleni",
    "@awladmahmoud5",
    "@msyrshop",
    # أزياء
    "@tagfashion",
    # أدوات منزلية
    "@magdyism",
    # كوبونات
    "@alcouponat1",
    # سفر
    "@zwaiatravel",
    # تقنية
    "@electromara1",
    "@vaasutechdeals",
]

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def join_all_channels():
    """طلب الانضمام إلى جميع القنوات"""
    print("\n📡 جاري طلب الانضمام إلى جميع القنوات...\n")
    
    for channel in SOURCE_CHANNELS:
        try:
            await client(JoinChannelRequest(channel))
            print(f"✅ تم الانضمام إلى {channel}")
        except Exception as e:
            error = str(e)
            if "USER_ALREADY_PARTICIPANT" in error:
                print(f"ℹ️ بالفعل عضو في {channel}")
            elif "Invite request sent" in error:
                print(f"📨 تم إرسال طلب انضمام إلى {channel} (في انتظار الموافقة)")
            elif "FLOOD_WAIT" in error:
                print(f"⚠️ انتظر قليلاً قبل الانضمام إلى {channel}")
            else:
                print(f"❌ فشل الانضمام إلى {channel}: {error[:60]}")
        
        await asyncio.sleep(1)  # تأخير بسيط بين الطلبات
    
    print("\n✅ اكتملت طلبات الانضمام\n")

async def main():
    print("🚀 بوت النسخ متعدد المجالات يعمل...")
    await client.start()
    print("✅ تم تسجيل الدخول بنجاح!")
    
    # طلب الانضمام إلى جميع القنوات
    await join_all_channels()
    
    print(f"📡 يتابع {len(SOURCE_CHANNELS)} قناة في مجالات مختلفة")
    print("🎯 جاهز لنسخ العروض الجديدة...")
    
    await client.run_until_disconnected()

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward_new(event):
    """نسخ المنشورات الجديدة فوراً"""
    try:
        await client.send_message(TARGET_CHANNEL, event.message)
        print(f"✅ تم نسخ منشور جديد")
    except Exception as e:
        print(f"❌ خطأ في النسخ: {e}")

asyncio.run(main())
