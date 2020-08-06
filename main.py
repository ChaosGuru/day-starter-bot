import logging
import json
from datetime import time, timezone, timedelta

import telegram
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    update.message.reply_text('♥Просто насолоджуйсь сьогоднішнім днем.\n\n♦Якщо також хочеш бота, або маєш пропозиції щодо цього напиши мені\n>>> https://t.me/I_NANI_I\n\n‼ /stop - зупинити бота', disable_web_page_preview=True)

    # set time
    t = time(hour=14, minute=47, tzinfo=timezone(timedelta(hours=3)))
    # t = time(hour=11, minute=30)

    # add a job
    if 'morning' not in context.chat_data:
        job = context.job_queue.run_daily(morning, t, context=update.message.chat_id)
        context.chat_data['morning'] = job

    # add test job
    if 'test' in context.chat_data:
        context.chat_data['test'].schedule_removal()
        del context.chat_data['test']
    
    test_job = context.job_queue.run_once(morning, 3, context=update.message.chat_id)
    context.chat_data['test'] = test_job

def stop(update, context):
    if 'morning' in context.chat_data:
        job = context.chat_data['morning']
        job.schedule_removal()
        del context.chat_data['morning']

    update.message.reply_text('♦Бот зупинений!\n‼ /start - запустити')

def echo(update, context):
    update.message.reply_text(update.message.text)

def morning(context):
    logging.info("Morning job run.")

    job = context.job
    text = "Доброго ранку!\n\n"

    # date

    # whether

    # dishes
    with open('dishes.json') as f:
        pass

    # quote

    context.bot.send_message(job.context, text=text)

def main(request=None):
    # take setup data
    with open('setup.json') as f:
        setup = json.load(f)
        token = setup['token']

    # setup updater
    updater = Updater(token=token, use_context=True)
    disp = updater.dispatcher

    # command handlers
    disp.add_handler(CommandHandler('start', start))
    disp.add_handler(CommandHandler('stop', stop))

    # test handlers
    disp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    # start bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

# TODO: add job serilization https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#save-and-load-jobs-using-pickle
#       finish morning job