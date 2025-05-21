# bot.py

import telebot
from telebot import types
from config import BOT_TOKEN, DISPATCHER_CHAT_ID

bot = telebot.TeleBot(BOT_TOKEN)

# Словарь для временного хранения данных пользователя
user_data = {}

# Типы спецтехники
TYPES_OF_TECH = [
    "Экскаватор", "Самосвал", "Кран", "Мини-погрузчик",
    "Трактор", "Эвакуатор", "Вездеход", "Другое"
]

# Начало диалога
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_data[message.chat.id] = {}
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for tech in TYPES_OF_TECH:
        markup.add(tech)
    bot.send_message(message.chat.id, "👋 Привет! Выберите тип спецтехники:", reply_markup=markup)
    bot.register_next_step_handler(message, process_type_step)

# Шаг 1: Тип техники
def process_type_step(message):
    user_data[message.chat.id]['type'] = message.text
    bot.send_message(message.chat.id, "📍 Укажите адрес:")
    bot.register_next_step_handler(message, process_address_step)

# Шаг 2: Адрес
def process_address_step(message):
    user_data[message.chat.id]['address'] = message.text
    bot.send_message(message.chat.id, "📝 Опишите задачу:")
    bot.register_next_step_handler(message, process_description_step)

# Шаг 3: Описание задачи
def process_description_step(message):
    user_data[message.chat.id]['description'] = message.text
    bot.send_message(message.chat.id, "📞 Укажите ваш контактный телефон:")
    bot.register_next_step_handler(message, process_phone_step)

# Шаг 4: Телефон
def process_phone_step(message):
    user_data[message.chat.id]['phone'] = message.text

    data = user_data[message.chat.id]
    text = f"""
📩 *Новая заявка на спецтехнику*:

🔧 Тип техники: {data['type']}
🏠 Адрес: {data['address']}
📝 Задача: {data['description']}
📞 Телефон: {data['phone']}
"""

    bot.send_message(DISPATCHER_CHAT_ID, text, parse_mode='Markdown')
    bot.send_message(message.chat.id, "✅ Ваша заявка принята! С вами свяжутся в течение 5 минут.")

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
