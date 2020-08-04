import logging
import json
from datetime import datetime, time, timezone, timedelta

import telegram
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, Dispatcher

with open('setup.json') as f:
    setup = json.load(f)
    bot = telegram.Bot(token=setup["token"])

dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

def start(update, context):
    update.message.reply_text('♥Просто насолоджуйсь сьогоднішнім днем.\n\n♦Якщо також хочеш бота, або маєш пропозиції щодо цього напиши мені\n>>> https://t.me/I_NANI_I\n\n‼ /stop - зупинити бота', disable_web_page_preview=True)

    # set time
    t = time(hour=7, tzinfo=timezone(timedelta(hours=3)))
    # t = time(hour=11, minute=30)

    # add a job
    if 'morning' not in context.chat_data:
        job = context.job_queue.run_daily(morning, t, context=update.message.chat_id)

        context.chat_data['morning'] = job

def stop(update, context):
    if 'morning' in context.chat_data:
        job = context.chat_data['morning']
        job.schedule_removal()
        del context.chat_data['morning']

    update.message.reply_text('♦Бот зупинений!\n‼ /start - запустити')

def echo(update, context):
    update.message.reply_text(update.message.text)

def main(request):
    
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # command handlers
        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(CommandHandler('stop', stop))

        # test handlers
        dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

        # start bot
        dispatcher.process_update(update)
    
    return "ok"