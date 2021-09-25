import logging
from telegram_handlers import updater
import telegram
from db import create_db_and_tables
from models import Birthday


def main():
    logging.info("migrating.....")
    create_db_and_tables()

    logging.info("starting the bot!")
    try:
        updater.start_polling()
        updater.idle()
    except telegram.error.TelegramError as e:
        logging.error(f"something went wrong! {e}")
        raise e
    logging.info("Bot shutting down. bye!")


if __name__ == "__main__":
    main()
