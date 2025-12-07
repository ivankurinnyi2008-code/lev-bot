import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import datetime
import sqlite3
import requests
from groq import Groq

# === ЗМІННІ (тепер тільки TELEGRAM_TOKEN) ===
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
CRYPTO_PAY_TOKEN = os.getenv('CRYPTO_PAY_TOKEN')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Groq з захистом від помилок
GROQ_WORKS = False
if GROQ_API_KEY and GROQ_API_KEY.startswith('gsk_'):
    try:
        groq_client = Groq(api_key=GROQ_API_KEY)
        GROQ_WORKS = True
    except:
        pass

# База
conn = sqlite3.connect('bot.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    language TEXT DEFAULT 'uk',
    messages_today INTEGER DEFAULT 0,
    last_message_date TEXT,
    subscribed_until TEXT
)
''')
conn.commit()

# Промпти (скорочую для економії місця, вставляй свої)
UK_PROMPT = "Ти — Лев, 28 років..."  # твій український промпт
RU_PROMPT = "Ты — Лев, 28 лет..."   # твій російський промпт

# === ФУНКЦІЇ ===
# (всі функції get_user_data, update_message_count, set_subscription, create_invoice, check_payment — залишаються як у тебе раніше)

# === ХЕНДЛЕРИ ===
# (всі хендлери /start, вибір мови, send_menu, оплата — як у тебе)

# === ГОЛОВНА ЛОГІКА ===
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    lang, msgs_today, is_sub = get_user_data(user_id)

    if not is_sub and msgs_today >= 5:
        send_menu(message)
        return

    prompt = UK_PROMPT if lang == 'uk' else RU_PROMPT

    if GROQ_WORKS:
        try:
            response = groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "system", "content": prompt}, {"role": "user", "content": message.text}],
                temperature=0.7,
                max_tokens=250
            )
            reply = response.choices[0].message.content.strip()
        except:
            reply = "AI тимчасово спить, але я тут. Пиши, розберемо по-людськи 😎"
    else:
        reply = "Привіт! Я Лев. Пиши що сталося — розберемо."

    bot.send_message(user_id, reply)
    if not is_sub:
        update_message_count(user_id)

print("Bot started! Лев онлайн 24/7")
bot.infinity_polling()
