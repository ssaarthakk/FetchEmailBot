from nfemail import read_emails
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("BOT_API_KEY")

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am HouseholdNF Bot.🤖\n
I am here to fetch the latest email sent to the email provided by you.\
""")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    reply_message = bot.reply_to(message, "Please wait...")
    nfsubject, nfbody = read_emails(message.text)
    bot.edit_message_text(chat_id=reply_message.chat.id, message_id=reply_message.message_id, text=f"Subject: {nfsubject}\n\nBody: {nfbody}")

bot.infinity_polling()