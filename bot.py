import telebot
from telebot import types
import google.generativeai as genai
from binance.client import Client

# Твои ключи
TG_TOKEN = '8628144206:AAH4ZLIzvWO9oiFEiBHUpM4MGzvpYJCxyNc'
G_KEY = 'AIzaSyAjN258DeD_un-pHVhXyXZsBB-2NL8NG6Y'
B_API = 't91LXupGkuQHOFkmwyxJCJceSLQybgqwUF2QaUcPTVAJdw2E6OWwj3Ji5U5j8bnq'
B_SECRET = '1TdBPc1W3HTov15oeQmFNreHe852muuAvUqPQKtbYSC54aYkJtWhiLNNyYHj8sO7'

bot = telebot.TeleBot(TG_TOKEN)
binance_client = Client(B_API, B_SECRET)
genai.configure(api_key=G_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Баланс", "💬 Чат с Брокером")
    bot.send_message(message.chat.id, "🚀 Брокер запущен на Railway!", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle(message):
    if message.text == "💰 Баланс":
        bot.send_message(message.chat.id, "Связываюсь с биржей Binance...")
        try:
            acc = binance_client.get_account()
            # Упрощенный вывод для теста
            bot.send_message(message.chat.id, "Доступ к балансу получен!")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка Binance: {e}")
    else:
        try:
            res = model.generate_content(message.text)
            bot.send_message(message.chat.id, res.text)
        except:
            bot.send_message(message.chat.id, "Брокер задумался, попробуй еще раз.")

bot.polling(none_stop=True)
