import logging, json, random
from datetime import datetime, time, timezone, timedelta

import telegram
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    update.message.reply_text('♥Просто насолоджуйсь сьогоднішнім днем.\n\n♦Якщо також хочеш бота, або маєш пропозиції щодо цього напиши мені\n>>> https://t.me/I_NANI_I\n\n‼ /stop - зупинити бота', disable_web_page_preview=True)

    # set time
    t = time(hour=7, tzinfo=timezone(timedelta(hours=3)))
    # t = time(hour=11, minute=30)

    # add a job
    if 'morning' not in context.chat_data:
        job = context.job_queue.run_daily(morning, t, context=update.message.chat_id)
        context.chat_data['morning'] = job

    # test job
    context.job_queue.run_once(morning, 1, context=update.message.chat_id)

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
    text = "♥Веселого ранку! | "

    # date
    text += datetime.now().strftime("%x") + "\n\n"

    # whether

    # dishes
    days = {
        "0": "monday",
        "1": "tuesday",
        "2": "wednesday",
        "3": "thursday",
        "4": "friday",
        "5": "saturday",
        "6": "sunday"
    }

    with open('meal_plan.json', encoding="utf8") as f:
        meals = json.load(f)
        rand = random.randint(0, len(meals)-1)

        text += "♦Страви на сьогодні♦\n\n♣Сніданок - %s\n♣Обід - %s\n♣Ввечеря - %s" % \
            tuple(["%s\n[%s]" % (i["title2"], i["title"]) for i in meals[rand]["week"][days[str(datetime.today().weekday())]]["meals"]])

    # quote

    context.bot.send_message(job.context, text=text)

def main(request=None):
    # take setup data
    with open('setup.json') as f:
        setup = json.load(f)
        token = setup['test_token']

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