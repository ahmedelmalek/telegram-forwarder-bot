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

# =============== هاشتاجات مضبوطة حسب اليوم ===============

def get_hashtags():
    """هاشتاجات حسب اليوم باللغة العربية"""
    now = datetime.now()
    day = now.strftime("%A")
    
    # الأيام بالعربية
    arabic_days = {
        "Monday": "الاثنين",
        "Tuesday": "الثلاثاء", 
        "Wednesday": "الأربعاء",
        "Thursday": "الخميس",
        "Friday": "الجمعة",
        "Saturday": "السبت",
        "Sunday": "الأحد"
    }
    
    day_ar = arabic_days.get(day, "")
    
    # هاشتاجات حسب اليوم
    if day == "Saturday":
        return f"#عروض_السبت #تخفيضات_السبت #اجهزة_كهربائية #عروض"
    elif day == "Sunday":
        return f"#عروض_الأحد #كوبونات_الأحد #خصومات #تسوق"
    elif day == "Monday":
        return f"#عروض_الاثنين #الكترونيات #تخفيضات_الاثنين"
    elif day == "Tuesday":
        return f"#عروض_الثلاثاء #صفقات #تخفيضات"
    elif day == "Wednesday":
        return f"#عروض_الأربعاء #خصم_الأربعاء #بيعتك"
    elif day == "Thursday":
        return f"#عروض_الخميس #تخفيضات_الخميس #عروض_نهاية_الاسبوع"
    elif day == "Friday":
        return f"#جمعة_البيعتك #عروض_الجمعة #تخفيضات_الجمعة #عروض_الجمعة_البيضاء"
    else:
        return "#عروض #تخفيضات #اجهزة_كهربائية"

# =============== تنسيق المنشور مع صورة ===============

async def copy_message_with_image(msg, channel_name):
    """نسخ المنشور مع الصورة والنص والهاشتاجات"""
    try:
        # النص الأصلي + الهاشتاجات
        new_text = ""
        if msg.text:
            new_text = msg.text + f"\n\n🔥 *عرض حصري من {channel_name}* 🔥\n\n"
        else:
            new_text = f"🔥 *عرض حصري من {channel_name}* 🔥\n\n"
        
        new_text += f"---\n✅ *لمتابعة أحدث العروض يومياً*\n🔗 @AhmedElectroShop\n\n{get_hashtags()}"
        
        # إذا كان فيه صورة
        if msg.photo:
            await client.send_file(
                TARGET_CHANNEL,
                msg.photo,
                caption=new_text,
                parse_mode='markdown'
            )
            print(f"✅ تم نسخ منشور (مع صورة) من {channel_name}")
        # إذا كان فيه فيديو
        elif msg.video:
            await client.send_file(
                TARGET_CHANNEL,
                msg.video,
                caption=new_text,
                parse_mode='markdown'
            )
            print(f"✅ تم نسخ منشور (مع فيديو) من {channel_name}")
        # نص فقط
        elif msg.text:
            await client.send_message(
                TARGET_CHANNEL,
                new_text,
                parse_mode='markdown'
            )
            print(f"✅ تم نسخ منشور (نص فقط) من {channel_name}")
            
    except Exception as e:
        print(f"❌ خطأ في نسخ منشور من {channel_name}: {e}")

# =============== المهام ===============

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def copy_recent_messages():
    """نسخ آخر 3 منشورات من كل قناة (بالصور)"""
    print("\n📡 جاري نسخ آخر المنشورات...\n")
    
    for channel in SOURCE_CHANNELS:
        try:
            messages = await client.get_messages(channel, limit=3)
            count = 0
            
            for msg in messages:
                if msg:
                    await copy_message_with_image(msg, channel)
                    count += 1
                    await asyncio.sleep(2)
            
            print(f"📊 اكتمل: {channel} → {count} منشورات\n")
        except Exception as e:
            print(f"❌ خطأ في {channel}: {e}")

async def send_tip():
    """إرسال نصيحة شراء كل 6 ساعات"""
    tips = [
        "💡 *نصيحة اليوم:* قارن الأسعار بين 3 متاجر قبل الشراء",
        "💡 *نصيحة:* اشترِ الأجهزة في عروض الجمعة البيضاء لتوفير 30-50%",
        "💡 *نصيحة:* الأجهزة الموفرة للطاقة توفر 40% في فاتورة الكهرباء",
    ]
    import random
    while True:
        try:
            tip = random.choice(tips) + f"\n\n{get_hashtags()}"
            await client.send_message(TARGET_CHANNEL, tip, parse_mode='markdown')
            print("✅ تم إرسال نصيحة شراء")
            await asyncio.sleep(21600)  # 6 ساعات
        except Exception as e:
            print(f"❌ خطأ: {e}")
            await asyncio.sleep(21600)

async def auto_promote():
    """ترويج تلقائي كل ساعتين"""
    while True:
        try:
            promo = f"""
🎯 *قناتك الأولى للعروض والتخفيضات* 🎯

✅ عروض حصرية يومياً
✅ أقل الأسعار في السوق
✅ كوبونات خصم فعالة

🔗 @AhmedElectroShop

{get_hashtags()}
"""
            await client.send_message(TARGET_CHANNEL, promo, parse_mode='markdown')
            print("✅ تم إرسال ترويج")
            await asyncio.sleep(7200)  # ساعتين
        except Exception as e:
            print(f"❌ خطأ: {e}")
            await asyncio.sleep(7200)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward_new(event):
    """نسخ المنشورات الجديدة فوراً (بالصور)"""
    try:
        await copy_message_with_image(event.message, str(event.chat_id))
    except Exception as e:
        print(f"❌ خطأ في النسخ الفوري: {e}")

async def main():
    print("🚀 بوت الصور والهاشتاجات يعمل...")
    await client.start()
    
    # ✅ تثبيت الجلسة
    me = await client.get_me()
    print(f"✅ تم تسجيل الدخول كـ: {me.first_name}")
    
    # الانضمام إلى القنوات
    for channel in SOURCE_CHANNELS:
        try:
            await client(JoinChannelRequest(channel))
            print(f"✅ تم الانضمام إلى {channel}")
        except Exception as e:
            print(f"⚠️ مشكلة في {channel}")
    
    # نسخ آخر المنشورات
    await copy_recent_messages()
    
    # بدء المهام التلقائية
    asyncio.create_task(auto_promote())
    asyncio.create_task(send_tip())
    
    print(f"🎯 جاهز لنسخ المنشورات الجديدة...")
    print(f"📅 اليوم: {datetime.now().strftime('%A')} → {get_hashtags()}")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
