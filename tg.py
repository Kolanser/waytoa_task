import logging
import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Updater, Filters, MessageHandler
from db import select_tasks

load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

UPDATER = Updater(token=TELEGRAM_TOKEN)


def start(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=(
            'Введите тему и сложность в формате: тема-сложность.'
            ' Например: математика-800.'
        )
    )


def get_tasks(update, context):
    host = os.getenv('HOST')
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    db_name = os.getenv('DB_NAME')
    tag = update.message.text.split('-')[0]
    complexity = update.message.text.split('-')[1]
    select = select_tasks(host, user, password, db_name, tag, complexity)
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='\n'.join(map(lambda elem: elem[0], select))
    )


def main():
    UPDATER.dispatcher.add_handler(CommandHandler('start', start))
    UPDATER.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(r'^[а-я]+-[\d]+'),
            get_tasks
        )
    )
    UPDATER.start_polling()
    UPDATER.idle()


if __name__ == '__main__':
    main()
