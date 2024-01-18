from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from pymongo import MongoClient
import os

# Read environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
DB_URL = os.environ.get('DB_URL')

# Initialize MongoDB connection
client = MongoClient(DB_URL)
db = client['mydatabase']
users_collection = db['users']

# Function to handle /start command
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Save user info to the database
    if not users_collection.find_one({'id': user_id}):
        users_collection.insert_one({'id': user_id})

    # Send a welcome message with buttons
    welcome_text = f"Welcome {update.message.from_user.mention_html()}!\n\nClick the buttons below:"
    keyboard = [
        [InlineKeyboardButton('Broadcast', callback_data='broadcast'),
         InlineKeyboardButton('Users Info', callback_data='users_info')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_html(
        text=welcome_text,
        reply_markup=reply_markup
    )

# Function to handle /broadcast command
def broadcast(update: Update, context: CallbackContext) -> None:
    # Implement your broadcast logic here
    context.bot.send_message(update.message.from_user.id, text="Broadcast button clicked!")

# Function to handle /users_info command
def users_info(update: Update, context: CallbackContext) -> None:
    # Retrieve and send users info
    total_users = users_collection.count_documents({})
    context.bot.send_message(update.message.from_user.id, text=f"Total Users: {total_users}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("broadcast", broadcast))
    dp.add_handler(CommandHandler("users_info", users_info))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
