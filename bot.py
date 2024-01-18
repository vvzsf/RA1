from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from motor.motor_asyncio import AsyncIOMotorClient  
from os import environ as env
import asyncio, datetime, time

ACCEPTED_TEXT = "<b> Hey {user}\n\nYour Request For {chat} Is Accepted ✅ </b> <b>Click To /start ♥️</b>,"
START_TEXT = "<b> Hai {}\n\nI am Auto Request Accept Bot With Working For All Channel. Add Me In Your Channel To Use </b>"
NAA_TEXT = "Hai"

API_ID = int(env.get('API_ID'))
API_HASH = env.get('API_HASH')
BOT_TOKEN = env.get('BOT_TOKEN')
DB_URL = env.get('DB_URL')
ADMINS = int(env.get('ADMINS'))
PICS = (env.get('PICS', 'https://graph.org/file/79c708cc8bcf16e88a2e9.jpg')).split()

Dbclient = AsyncIOMotorClient(DB_URL)
Cluster = Dbclient['Cluster0']
Data = Cluster['users']
Bot = Client(name='AutoAcceptBot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
      
@Bot.on_message(filters.command("start") & filters.private)                    
async def start_handler(c, m):
    user_id = m.from_user.id
    if not await Data.find_one({'id': user_id}): await Data.insert_one({'id': user_id})
    button = [[        
        InlineKeyboardButton('◤ ᴜᴘᴅᴀᴛᴇꜱ ◢', url='https://t.me/PanindiaFilmZ'),
        InlineKeyboardButton('◤ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ◢', url='https://t.me/BoTzUpdates0')
    ]]
    return await m.reply_text(text=START_TEXT.format(m.from_user.mention), disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(button))

@Bot.on_message(filters.command("naa") & filters.private)
async def naa_handler(c, m):
    await m.reply_photo(
        photo="https://graph.org/file/4c267929a2bf1f92088f4.jpg",
        caption="Hai")

@Bot.on_message(filters.command(["broadcast", "users"]) & filters.user(ADMINS))  
async def broadcast(c, m):
    if m.text == "/users":
        total_users = await Data.count_documents({})
        return await m.reply(f"Total Users: {total_users}")
    b_msg = m.reply_to_message
    sts = await m.reply_text("Broadcasting your messages...")
    users = Data.find({})
    total_users = await Data.count_documents({})
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    async for user in users:
        user_id = int(user['id'])
        try:
            await b_msg.copy(chat_id=user_id)
            success += 1
        except Exception as e:
            failed += 1
        done += 1
        if not done % 20:
            await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nFailed: {failed}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.delete()
    await m.reply_text(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nFailed: {failed}", quote=True)

@Bot.on_message(filters.channel & filters.incoming)
async def forward_messages(c, m):
    chat_id = m.chat.id
    user_id = m.from_user.id
    if await Data.find_one({'id': user_id}):
        try:
            await m.forward(chat_id=YOUR_DESTINATION_CHANNEL_ID)
        except Exception as e:
            print(e)

Bot.run()
