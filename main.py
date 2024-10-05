import telebot
import json
from telebot import types

API_TOKEN = '7840425281:AAGAAlF80ZpDPZVcnK87PHMJiJ6KcHLiAMQ'
bot = telebot.TeleBot(API_TOKEN)

# Шлях до файлу з балансами користувачів
BALANCE_FILE = 'user_balances.json'

# Функція для зчитування балансів з файлу
def load_balances():
    try:
        with open(BALANCE_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Функція для збереження балансів у файл
def save_balances(balances):
    with open(BALANCE_FILE, 'w') as file:
        json.dump(balances, file)

# Команда для оновлення балансу
@bot.message_handler(func=lambda message: message.text.startswith('/update_balance'))
def update_balance(message):
    try:
        parts = message.text.split()
        if len(parts) == 3:
            user_id = parts[1]
            new_balance = int(parts[2])
            user_balances = load_balances()
            user_balances[user_id] = new_balance
            save_balances(user_balances)
            bot.send_message(message.chat.id, f"Баланс оновлено до: {new_balance}")
        else:
            bot.send_message(message.chat.id, "Невірний формат команди. Використовуйте: /update_balance <user_id> <balance>")
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Невірний формат команди.")

# Старт бота
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user.first_name  # Отримаємо ім'я користувача

    # Створення тексту вітання з персоналізацією
    text = f"Привіт, {user}! Радий вітати тебе в нашому казино. \n" \
          "Натисни кнопку нижче, щоб відкрити веб-версію казино і розпочати гру."

    

    # Створення кнопки для відкриття Web Mini App через WebAppInfo
    markup = types.InlineKeyboardMarkup()
    web_app_url = "https://oleksandr38kebab342.github.io/casino.io/"  # Замініть на URL вашого веб-міні-додатку
    btn = types.InlineKeyboardButton(
        text="🎰 Відкрити веб-казино",
        web_app=types.WebAppInfo(url=web_app_url)  # Веб-додаток у Telegram
    )
    markup.add(btn)
    bot.send_message(message.chat.id, text, reply_markup=markup)
bot.polling()
