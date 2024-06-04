import telebot

from config import TELEGRAM_TOKEN


bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    text = (
        f"Привет! Я бот, который поможет тебе избежать пробок. "
        f"Отправь мне пункт назначения, и я помогу тебе объехать пробки."
    )
    bot.reply_to(message, text)


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()
