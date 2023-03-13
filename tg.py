import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Updater, Filters, MessageHandler
from db import select_tasks, select_tags_uniq

load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')


def start(update, context):
    chat = update.effective_chat
    tags_uniq = select_tags_uniq(HOST, USER, PASSWORD, DB_NAME)
    tags_uniq_mes = '\n'.join(map(lambda elem: elem[0], tags_uniq))
    context.bot.send_message(
        chat_id=chat.id,
        text=(
            'Введите тему и сложность в формате: тема-сложность.\n'
            'Например: математика-800.\n'
            f'У нас есть задачи по темам:\n'
            f'{tags_uniq_mes}'
        )
    )


def get_tasks(update, context):
    tag = update.message.text.split('-')[0].lower()
    complexity = update.message.text.split('-')[1]
    select = select_tasks(HOST, USER, PASSWORD, DB_NAME, tag, complexity)
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='\n'.join(map(lambda elem: elem[0], select))
    )


def get_error(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='Пожалуйста, проверьте правильность указания темы и сложности'
    )


def main():
    updater = Updater(token=TELEGRAM_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(r'^[А-Яа-я]+-[\d]+'),
            get_tasks
        )
    )
    updater.dispatcher.add_handler(MessageHandler(Filters.text, get_error))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
