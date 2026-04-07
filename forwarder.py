import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
import os

API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
SESSION_STRING = os.environ.get('SESSION_STRING')
TARGET_CHANNEL = int(os.environ.get('TARGET_CHANNEL'))

# قنوات المصدر (العروض)
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

async def request_join_all():
    """يطلب الانضمام إلى جميع القنوات"""
    print("📡 جاري طلب الانضمام إلى القنوات...")
    
    for channel in SOURCE_CHANNELS:
        try:
            entity = await client.get_entity(channel)
            await client(JoinChannelRequest(entity))
            print(f"✅ تم الانضمام إلى {channel}")
        except Exception as e:
            error_msg = str(e)
            if "USER_ALREADY_PARTICIPANT" in error_msg:
                print(f"ℹ️ أنت بالفعل عضو في {channel}")
            elif "FLOOD_WAIT" in error_msg:
                print(f"⚠️ انتظر قليلاً قبل محاولة الانضمام إلى {channel}")
            elif "Invite request sent" in error_msg:
                print(f"📨 تم إرسال طلب انضمام إلى {channel} (في انتظار الموافقة)")
            else:
                print(f"❌ فشل طلب الانضمام إلى {channel}: {error_msg[:100]}")

async def copy_recent_messages():
    """نسخ آخر المنشورات من القنوات"""
    print("📡 جاري جلب آخر المنشورات...")
    
    for channel in SOURCE_CHANNELS:
        try:
            messages = await client.get_messages(channel, limit=3)
            for msg in messages:
                try:
                    await client.send_message(TARGET_CHANNEL, msg)
                    print(f"✅ تم نسخ منشور من {channel}")
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"❌ فشل نسخ منشور من {channel}: {e}")
        except Exception as e:
            print(f"❌ لا يمكن الوصول إلى {channel}: {e}")

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward_new(event):
    """نسخ المنشورات الجديدة فوراً"""
    try:
        await client.send_message(TARGET_CHANNEL, event.message)
        print(f"✅ تم نسخ منشور جديد")
    except Exception as e:
        print(f"❌ خطأ: {e}")

async def main():
    print("🚀 بوت النسخ يعمل...")
    await client.start()
    print("✅ تم تسجيل الدخول بنجاح!")
    
    # طلب الانضمام إلى جميع القنوات
    await request_join_all()
    
    # انتظار 5 ثوانٍ للتأكد
    await asyncio.sleep(5)
    
    # محاولة نسخ آخر المنشورات
    await copy_recent_messages()
    
    print("🎯 جاهز لنسخ المنشورات الجديدة...")
    await client.run_until_disconnected()

asyncio.run(main())
