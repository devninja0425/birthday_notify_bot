from decouple import config
import logging

LOGFILE = 'bd.log'
logging.basicConfig(filename=LOGFILE,
                    level=logging.INFO,
                    format='%(asctime)s%(levelname)-8s%(message)',
                    datefmt='%Y-%M-%D %H:%M%:%S')

TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
DATABASE_NAME = config('DATABASE_NAME')