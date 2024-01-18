from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated
import asyncio

app = Client("my_account")

# Handle members joining the channel or group
async def on_join(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    await client.add_chat_members(chat_id, user_id)

# Handler for new chat members
@app.on_chat_member_updated(filters.chat_member_updated)
async def chat_members_updated(client, message: ChatMemberUpdated):
    if message.new_chat_members and message.new_chat_members[0].id == client.get_me().id:
        await on_join(client, message)

async def main():
    await app.start()
    await app.idle()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
