import asyncio
from telethon import TelegramClient, events
import os

# قراءة البيانات من الأسرار
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
phone = os.environ.get('PHONE')

TARGET_CHANNEL = -1003624571276

SOURCE_CHANNELS = [
    "@EL_King_4",
    "@TCLSyria",
    "@syrian_company_sy",
    "@hhhhhhhnmhossam",
    "@belleni",
    "@awladmahmoud5",
    "@msyrshop",
]

client = TelegramClient("forwarder", api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward(event):
    try:
        await client.send_message(TARGET_CHANNEL, event.message)
        print(f"✅ تم النسخ")
    except Exception as e:
        print(f"❌ خطأ: {e}")

async def main():
    print("🚀 البوت يعمل...")
    await client.start(phone)
    await client.run_until_disconnected()

asyncio.run(main())
