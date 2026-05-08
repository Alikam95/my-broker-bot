import os
import telebot
from binance.client import Client
import google.generativeai as genai

# Забираем ключи из настроек Railway
TG_TOKEN = os.getenv('TG_TOKEN')
B_API = os.getenv('B_API')
B_SECRET = os.getenv('B_SECRET')
# Если используешь Gemini, добавь переменную GEMINI_KEY или вставь ключ ниже
GEMINI_KEY = os.getenv('GEMINI_KEY', 'ТВОЙ_КЛЮЧ_GEMINI_ЕСЛИ_ЕСТЬ')

# Настройка бота и ИИ
bot = telebot.TeleBot(TG_TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# Пробуем подключить Binance
try:
    binance_client = Client(B_API, B_SECRET)
    # Проверка связи
    binance_client.get_account_api_trading_status()
    print("Binance подключен успешно!")
    binance_ready = True
except Exception as e:
    print(f"Ошибка Binance: {e}")
    print("Бот запущен в режиме чата без биржи.")
    binance_ready = False

@bot.message_handler(commands=['start'])
def start(message):
    status = "✅ Биржа подключена" if binance_ready else "⚠️ Работаю без биржи (ограничение сети)"
    bot.reply_to(message, f"Привет! Я твой торговый ассистент.\nСтатус: {status}\nЧем могу помочь?")

@bot.message_handler(commands=['balance'])
def balance(message):
    if not binance_ready:
        bot.reply_to(message, "Извини, из-за ограничений хостинга я не могу дотянуться до Binance. Проверь баланс в приложении.")
        return
    
    try:
        acc = binance_client.get_account()
        balances = [f"{b['asset']}: {b['free']}" for b in acc['balances'] if float(b['free']) > 0]
        bot.reply_to(message, "Твой баланс:\n" + "\n".join(balances))
    except:
        bot.reply_to(message, "Не удалось получить баланс.")

@bot.message_handler(func=lambda m: True)
def chat(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except:
        bot.reply_to(message, "Я тебя слышу, но мой 'мозг' (ИИ) пока не настроен. Просто скажи привет!")

print("Запуск бота...")
bot.polling(none_stop=True)
