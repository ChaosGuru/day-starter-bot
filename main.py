import logging
import json

from telegram.ext import Updater, CommandHandler

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def main():
    # take setup data
    with open('setup.json') as f:
        setup = json.load(f)
        token = setup['token']

    # setup updater
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # command handlers

if __name__ == '__main__':
    main()