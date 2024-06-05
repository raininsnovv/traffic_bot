from telebot.types import ReplyKeyboardMarkup
import requests
from sqlalchemy import text
import telebot

from config import TELEGRAM_TOKEN, DISTANCE_BASE_URL, DISTANCE_MATRIX_KEY
from db_connect import db

from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = KeyboardButton('Получить время в пути')
    markup.add(button)
    return markup


bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_addresses = {}


@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    text = (
        f"Привет! Я бот, который поможет тебе избежать пробок. "
        f"Отправь мне пункт назначения, и я помогу тебе объехать пробки."
    )
    bot.reply_to(message, text)
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Введите адрес вашего дома')
    bot.register_next_step_handler(msg, get_user_address_home)


def get_user_address_home(message):
    user_id = message.from_user.id
    home_address = message.text
    user_addresses[user_id] = {
        'home': home_address
    }

    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Введите адрес вашей работы')
    bot.register_next_step_handler(msg, get_user_address_job)


def get_user_address_job(message):
    user_id = message.from_user.id
    job_address = message.text
    home_address = user_addresses[user_id]['home']
    db.execute(
        text(
            f"INSERT INTO addresses (user_id, home, job) "
            f"VALUES ('{user_id}', '{home_address}', '{job_address}');"
        )
    )

    db.commit()

    chat_id = message.chat.id
    msg_text = (
        f'Спасибо. Информация сохранена.'
        f'Нажмите на кнопку "Получить время в пути".'
    )
    bot.send_message(chat_id, msg_text, reply_markup=keyboard())


@bot.message_handler(func=lambda message: True)
def get_info(message):
    if message.text == 'Получить время в пути':
        user_id = message.from_user.id
        user_data = db.execute(
            text(
                f"SELECT * "
                f"FROM addresses "
                f"WHERE user_id == {user_id};"
            )
        ).first()

        query_params = {
            'key': DISTANCE_MATRIX_KEY,
            'origins': user_data.home,
            'destinations': user_data.job,
        }

        response = requests.get(DISTANCE_BASE_URL, params=query_params)
        if response.status_code == 200:
            data = response.json()
            origin = data.get('origin_addresses')[0]
            destination = data.get('destination_addresses')[0]
            try:
                duration = data['rows'][0]['elements'][0]['duration']['text']
            except KeyError:
                pass
            msg_text = f'Время в пути из {origin} в {
                destination} занимает {duration}'
            bot.reply_to(message, msg_text, reply_markup=keyboard())


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()
