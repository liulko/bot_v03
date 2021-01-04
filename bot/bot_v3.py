import telebot
from telebot import types

#partickbestbot 1536137051:AAFs12zVogqTkAEwJypkLRlJtNss1nYBj8M
bot = telebot.TeleBot("1536137051:AAFs12zVogqTkAEwJypkLRlJtNss1nYBj8M")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)