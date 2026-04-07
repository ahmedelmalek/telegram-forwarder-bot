from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio

API_ID = 37398537
API_HASH = "0936672f2e8f776a21727c69b16ad6ff"

async def main():
    print("جارٍ إنشاء جلسة جديدة...")
    async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        await client.start()
        session_string = client.session.save()
        print("\n✅ الجلسة الجديدة:\n")
        print(session_string)

if __name__ == "__main__":
    asyncio.run(main())
