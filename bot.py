import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os

api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
session_string = os.environ.get('SESSION_STRING')
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

client = TelegramClient(StringSession(session_string), api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward(event):
    try:
        await client.send_message(TARGET_CHANNEL, event.message)
        print("✅ تم النسخ")
    except Exception as e:
        print(f"❌ خطأ: {e}")

async def main():
    print("🚀 البوت يعمل...")
    await client.start()
    await client.run_until_disconnected()

asyncio.run(main())
