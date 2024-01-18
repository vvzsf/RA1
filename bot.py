from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from pymongo import MongoClient
import os

# Read environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
DB_URL = os.environ.get('DB_URL')
OWNER_USER_ID = os.environ.get('OWNER_USER_ID')  # Add this line to get the owner's user ID

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

    # Send a welcome image and message
    welcome_text = "Welcome to the community! We're glad to have you on board."
    welcome_image_url = "https://graph.org/file/79c708cc8bcf16e88a2e9.jpg"  # Replace with your image URL

    update.message.reply_photo(
        photo=welcome_image_url,
        caption=welcome_text
    )

    # Notify the user about the request acceptance if the owner
    if user_id == OWNER_USER_ID:
        update.message.reply_text("Your join request has been automatically accepted!")

# Function to handle /broadcast command
def broadcast(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Check if the user is the owner
    if user_id == OWNER_USER_ID:
        # Implement your broadcast logic here
        context.bot.send_message(user_id, text="Broadcasting message to all users!")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# Function to handle /users_status command
def users_status(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Check if the user is the owner
    if user_id == OWNER_USER_ID:
        # Retrieve and send users status
        total_users = users_collection.count_documents({})
        context.bot.send_message(user_id, text=f"Total Users: {total_users}")
    else:
        update.message.reply_text("You are not authorized to use this command.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("broadcast", broadcast))
    dp.add_handler(CommandHandler("users_status", users_status))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
