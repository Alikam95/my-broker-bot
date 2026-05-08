import os
import telebot

# Берем только токен Телеграма
TG_TOKEN = os.getenv('TG_TOKEN')

bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Олег, привет! Я живой! Теперь я работаю на Railway.")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, f"Ты написал: {message.text}. Я тебя слышу!")

print("Бот запускается...")
bot.polling(none_stop=True)
