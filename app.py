import os
import sys
import logging

import telegram
from telegram.ext import CommandHandler, Updater
from emoji import emojize

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger('app')

# Message cache
msg_cache = {}


def load_msg_cache(key, path):
    global msg_cache
    with open(path) as f:
        msg_cache[key] = emojize(f.read(4096), use_aliases=True)
    return msg_cache[key]


# Handler callbacks
def on_cmd_start(bot, update):
    bot.send_chat_action(
        chat_id=update.message.chat_id,
        action=telegram.ChatAction.TYPING
    )

    msg = msg_cache.get('start')
    if not msg:
        msg = load_msg_cache('start', 'msgs/start.html')
    bot.send_message(
        chat_id=update.message.chat_id,
        text=msg,
        parse_mode=telegram.ParseMode.HTML
    )


def on_cmd_list(bot, update):
    bot.send_chat_action(
        chat_id=update.message.chat_id,
        action=telegram.ChatAction.TYPING
    )
    
    msg = msg_cache.get('list')
    if not msg:
        msg = load_msg_cache('list', 'msgs/list.html')

    bot.send_message(
        chat_id=update.message.chat_id,
        text=msg,
        parse_mode=telegram.ParseMode.HTML
    )


def start_webook(updater):
    url_path = os.getenv('WEBHOOK_URL_PATH')
    app_url = os.getenv('APP_URL')
    listen = os.getenv('LISTEN', '0.0.0.0')
    port = int(os.getenv('PORT', 8080))

    if not url_path:
        logging.error("Missing WEBHOOK_URL_PATH environment variable")
        sys.exit(-1)
    if not app_url:
        logging.error("Missing APP_URL environment variable")
        sys.exit(-1)

    logger.info("Listening on %s:%d", listen, port)
    updater.start_webhook(
        listen=listen,
        port=port,
        url_path=url_path
    )
    updater.bot.set_webhook(app_url + url_path)
    updater.idle()


def start_updater(updater):
    stage = os.getenv("STAGE", "production")
    logging.info("Starting bot with STAGE=%s", stage)
    if stage == 'production':
        start_webook(updater)
    else:
        updater.start_polling()


def main():
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        logger.error("Missing BOT_TOKEN environment variable")
        sys.exit(-1)

    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    # Handlers
    start_handler = CommandHandler('start', on_cmd_start)
    list_handler = CommandHandler('list', on_cmd_list)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(list_handler)

    start_updater(updater)


if __name__ == '__main__':
    main()
