from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from motor.motor_asyncio import AsyncIOMotorClient
from os import environ as env

# Read environment variables
API_ID = int(env.get('API_ID'))
API_HASH = env.get('API_HASH')
BOT_TOKEN = env.get('BOT_TOKEN')
DB_URL = env.get('DB_URL')

# Initialize MongoDB connection
Dbclient = AsyncIOMotorClient(DB_URL)
Cluster = Dbclient['Cluster0']
Data = Cluster['users']

# Initialize Pyrogram Client
Bot = Client(
    'AutoRequestBot',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


@Bot.on_chat_join_request()
async def request_handler(_, request):
    user_id = request.from_user.id
    chat_id = request.chat.id

    # Automatically approve the join request
    await Bot.approve_chat_join_request(chat_id, user_id)

    # Save user info to the database
    if not await Data.find_one({'id': user_id}):
        await Data.insert_one({'id': user_id})

    # Send a welcome message with buttons
    welcome_text = f"Welcome {request.from_user.mention}!\n\nClick the buttons below:"
    keyboard = [
        [
            InlineKeyboardButton('Broadcast', callback_data='broadcast'),
            InlineKeyboardButton('Users Info', callback_data='users_info')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await request.reply_text(
        text=welcome_text,
        reply_markup=reply_markup
    )


@Bot.on_callback_query()
async def callback_handler(_, callback):
    user_id = callback.from_user.id

    # Handle button callbacks
    if callback.data == 'broadcast':
        # Implement your broadcast logic here
        await callback.answer("Broadcast button clicked!")

    elif callback.data == 'users_info':
        # Retrieve and send users info
        total_users = await Data.count_documents({})
        await callback.answer(f"Total Users: {total_users}")

# Run the bot
Bot.run()
      
