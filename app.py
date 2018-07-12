import os
import sys
import logging

from telegram.ext import CommandHandler, Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger('app')


def main():
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        logger.error("Missing BOT_TOKEN environment variable")
        sys.exit(-1)

    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    # Command handlers
    start_handler = CommandHandler('start', on_cmd_start)
    list_handler = CommandHandler('list', on_cmd_list)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(list_handler)

    start_updater(updater)


def start_updater(updater):
    stage = os.getenv("STAGE", "production")
    logging.info("Starting bot with STAGE=%s", stage)
    if stage == 'production':
        url_path = os.getenv('WEBHOOK_URL_PATH')
        app_url = os.getenv('APP_URL')
        if not url_path:
            logging.error("Missing WEBHOOK_URL_PATH environment variable")
            sys.exit(-1)
        if not app_url:
            logging.error("Missing APP_URL environment variable")
            sys.exit(-1)

        updater.start_webhook(
            listen='0.0.0.0',
            port=443,
            url_path=url_path
        )
        updater.bot.set_webhook(app_url + '/' + url_path)
        updater.idle()

    else:
        updater.start_polling()


def on_cmd_start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hi"
    )


def on_cmd_list(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="List"
    )


if __name__ == '__main__':
    main()
