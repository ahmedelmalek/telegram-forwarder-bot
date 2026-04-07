import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
import os
from datetime import datetime

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

# الهاشتاجات المضافة تلقائياً
HASHTAGS = """
#عروض #تخفيضات #اجهزة_كهربائية #خصومات #تسوق_اونلاين 
#صفقات #الكترونيات #بيعتك #تخفيضات_اليوم #عروض_خاصة
"""

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def copy_recent_messages():
    """نسخ آخر 5 منشورات من كل قناة مع إضافة هاشتاجات"""
    print("\n📡 جاري نسخ آخر المنشورات...\n")
    
    for channel in SOURCE_CHANNELS:
        try:
            messages = await client.get_messages(channel, limit=5)
            count = 0
            
            for msg in messages:
                if msg:
                    # إضافة الهاشتاجات للمنشور
                    if msg.text:
                        new_text = msg.text + "\n\n" + HASHTAGS
                        msg.text = new_text
                    
                    await client.send_message(TARGET_CHANNEL, msg)
                    count += 1
                    print(f"✅ تم نسخ منشور {count}/5 من {channel}")
                    await asyncio.sleep(2)
            
            print(f"📊 اكتمل: {channel} → {count} منشورات\n")
        except Exception as e:
            print(f"❌ خطأ في {channel}: {e}")
    
    print("✅ انتهى نسخ المنشورات مع الهاشتاجات!")

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward_new(event):
    """نسخ المنشورات الجديدة مع إضافة هاشتاجات"""
    try:
        msg = event.message
        if msg.text:
            new_text = msg.text + "\n\n" + HASHTAGS
            msg.text = new_text
        await client.send_message(TARGET_CHANNEL, msg)
        print(f"✅ تم نسخ منشور جديد مع هاشتاجات")
    except Exception as e:
        print(f"❌ خطأ: {e}")

async def auto_promote():
    """الترويج التلقائي للقناة"""
    while True:
        try:
            # رسالة ترويجية تظهر كل ساعة
            promo_message = f"""
🔥 *عروض حصرية يومية* 🔥

📢 قناة متخصصة في أحدث العروض والتخفيضات على:
• الأجهزة الكهربائية
• الإلكترونيات
• أدوات منزلية
• كوبونات خصم

{HASHTAGS}

🔗 اشترك الآن: https://t.me/AhmedElectroShop
"""
            await client.send_message(TARGET_CHANNEL, promo_message)
            print("✅ تم إرسال رسالة ترويجية")
            
            # انتظر ساعة قبل إرسال الترويج التالي
            await asyncio.sleep(3600)
            
        except Exception as e:
            print(f"❌ خطأ في الترويج: {e}")
            await asyncio.sleep(3600)

async def main():
    print("🚀 بوت النسخ مع الترويج التلقائي يعمل...")
    await client.start()
    print("✅ تم تسجيل الدخول!")
    
    # الانضمام إلى القنوات
    for channel in SOURCE_CHANNELS:
        try:
            await client(JoinChannelRequest(channel))
            print(f"✅ تم الانضمام إلى {channel}")
        except:
            pass
    
    # نسخ آخر المنشورات
    await copy_recent_messages()
    
    # بدء الترويج التلقائي
    asyncio.create_task(auto_promote())
    
    print("🎯 جاهز لنسخ المنشورات الجديدة والترويج التلقائي...")
    await client.run_until_disconnected()

asyncio.run(main())
