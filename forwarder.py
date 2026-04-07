import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
import os
from datetime import datetime
import calendar

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

# هاشتاجات حسب اليوم
def get_hashtags():
    day = datetime.now().strftime("%A")
    hashtags = {
        "Saturday": "#عروض_السبت #اجهزة_كهربائية #تخفيضات",
        "Sunday": "#كوبونات #خصومات_الأحد #عروض_خاصة",
        "Monday": "#الكترونيات #عروض_الاثنين #تسوق_اونلاين",
        "Tuesday": "#عروض_الثلاثاء #تخفيضات #صفقات",
        "Wednesday": "#عروض_خاصة #خصم_الاربعاء #بيعتك",
        "Thursday": "#تخفيضات_الخميس #عروض_نهاية_الاسبوع",
        "Friday": "#جمعة_البيعتك #عروض_الجمعة #عروض_الجمعة_البيضاء"
    }
    return hashtags.get(day, "#عروض #تخفيضات #اجهزة_كهربائية")

# تنسيق المنشورات
def format_post(text):
    return f"""
🔥 *عرض حصري* 🔥

{text}

---
✅ *لمتابعة أحدث العروض يومياً*
🔗 @AhmedElectroShop

{get_hashtags()}
"""

# نصائح الشراء
TIPS = [
    "💡 *نصيحة اليوم:* قارن الأسعار بين 3 متاجر قبل الشراء",
    "💡 *نصيحة:* اشترِ الأجهزة في عروض الجمعة البيضاء لتوفير 30-50%",
    "💡 *نصيحة:* الأجهزة الموفرة للطاقة توفر 40% في فاتورة الكهرباء",
    "💡 *نصيحة:* اقرأ التقييمات قبل شراء أي جهاز",
    "💡 *نصيحة:* تأكد من الضمان وخدمة ما بعد البيع",
]

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def copy_recent_messages():
    """نسخ آخر المنشورات مع تنسيق وهاشتاجات"""
    print("\n📡 جاري نسخ آخر المنشورات...\n")
    
    for channel in SOURCE_CHANNELS:
        try:
            messages = await client.get_messages(channel, limit=3)
            count = 0
            
            for msg in messages:
                if msg and msg.text:
                    formatted = format_post(msg.text)
                    await client.send_message(TARGET_CHANNEL, formatted)
                    count += 1
                    print(f"✅ تم نسخ منشور من {channel}")
                    await asyncio.sleep(2)
            
            print(f"📊 اكتمل: {channel} → {count} منشورات\n")
        except Exception as e:
            print(f"❌ خطأ في {channel}: {e}")

async def send_tip():
    """إرسال نصيحة شراء بشكل دوري"""
    import random
    while True:
        try:
            tip = random.choice(TIPS)
            await client.send_message(TARGET_CHANNEL, tip)
            print("✅ تم إرسال نصيحة شراء")
            await asyncio.sleep(21600)  # كل 6 ساعات
        except Exception as e:
            print(f"❌ خطأ في نصيحة: {e}")
            await asyncio.sleep(21600)

async def auto_promote():
    """ترويج تلقائي للقناة"""
    while True:
        try:
            promo = f"""
🎯 *قناتك الأولى للعروض والتخفيضات* 🎯

✅ عروض حصرية يومية
✅ أقل الأسعار في السوق
✅ كوبونات خصم فعالة

🔗 @AhmedElectroShop

{get_hashtags()}
"""
            await client.send_message(TARGET_CHANNEL, promo)
            print("✅ تم إرسال ترويج")
            await asyncio.sleep(7200)  # كل ساعتين
        except Exception as e:
            print(f"❌ خطأ في الترويج: {e}")
            await asyncio.sleep(7200)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward_new(event):
    """نسخ المنشورات الجديدة مع تنسيق"""
    try:
        if event.message.text:
            formatted = format_post(event.message.text)
            await client.send_message(TARGET_CHANNEL, formatted)
            print(f"✅ تم نسخ منشور جديد مع تنسيق")
    except Exception as e:
        print(f"❌ خطأ: {e}")

async def main():
    print("🚀 بوت الترويج التلقائي يعمل...")
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
    
    # بدء المهام التلقائية
    asyncio.create_task(auto_promote())
    asyncio.create_task(send_tip())
    
    print("🎯 جاهز لنسخ المنشورات الجديدة والترويج...")
    await client.run_until_disconnected()

asyncio.run(main())
