import logging
import csv
from datetime import datetime
import calendar
from telegram import Update
import config
from telegram.ext import (Updater, CallbackContext, CommandHandler,
                          MessageHandler, Filters)

from repository import create_birthday, get_all_birthdays_the_month

updater = Updater(config.TELEGRAM_BOT_TOKEN)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=("just export .csv file and i will tell u when \n"
              "\t\t\tNotice\t\t\t\n"
              "full_name,month,day"))


def import_dot_csv_file(update: Update, context: CallbackContext) -> None:
    #download the csv file
    file_id = update.message.document.file_id
    context.bot.get_file(file_id).download('bd.csv')
    #store the  bd.csv file data into the db
    path = "bd.csv"
    file = open(path, 'r')
    reader = csv.reader(file)
    header = next(reader)
    data = [line for line in reader]
    payload = []
    for i in data:
        x = {header[0]: i[0], header[1]: i[1], header[2]: i[2]}
        payload.append(x)
    create_birthday(payload)
    #start the scheduler to run daily
    # context.job_queue.run_repeating(callback=notify,
    #                                 interval=30,
    #                                 context=update.effective_chat.id)
    context.job_queue.run_daily(callback=notify,context=update.effective_chat.id)


def error_handler(update, context):
    """Handles errors we get while executing commands."""
    logging.error(msg="Something went wrong when trying to handle an update.",
                  exc_info=context.error)


def notify(context) -> None:
    """
    return list of birthday for today
    """
    #Read the database to get today birthdays
    today = datetime.today()
    birthdays_this_month = get_all_birthdays_the_month(today)
    birthdays = []
    #See if today is a birthday.
    for birthday in birthdays_this_month:
        if today.day == birthday.day:
            birthdays.append(birthday)
        # Handle leap years
        if (today.month == 2 and today.day == 28
                and (not calendar.isleap(today.year)) and birthday.day == 29):
            birthdays.append(birthday)
    message = "We've got some birthdays!\n\n" + "\n\n".join(
        f"{bday}" for bday in birthdays)
    ctx = context.job.context
    context.bot.send_message(chat_id=ctx, text=message)


#handle registration
START_HANDLER = CommandHandler('start', start)
CSV_HANDLER = MessageHandler(Filters.document.file_extension('csv'),
                             import_dot_csv_file)

handlers = [START_HANDLER, CSV_HANDLER]
for i in handlers:
    dispatcher.add_handler(i)

dispatcher.add_error_handler(error_handler)