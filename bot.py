import os
import telebot
import logging

logging.basicConfig(level=logging.INFO)

try:
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN не знайдено! Перевір Environment на Render")

    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=['start', 'help'])
    def start(message):
        bot.reply_to(message, "Привіт! Бот працює!\nТи вже на фініші, брате!")

    @bot.message_handler(func=lambda message: True)
    def echo(message):
        bot.reply_to(message, "Бот живий! Скоро буде повна версія з Groq і CryptoPay")

    print("Bot started! Бот успішно запущено і слухає повідомлення")
    bot.infinity_polling()

except Exception as e:
    print("КРИТИЧНА ПОМИЛКА ЗАПУСКУ:", e)
    logging.error("Помилка:", exc_info=True)
    raise
