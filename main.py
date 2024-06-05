import telebot

from config import TELEGRAM_TOKEN


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
    user_addresses[user_id]['job'] = job_address

    chat_id = message.chat.id
    bot.send_message(chat_id, 'Спасибо. Информация сохранена.')
    print(user_addresses)


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()
