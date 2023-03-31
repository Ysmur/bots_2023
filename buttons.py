import os
import random
from datetime import datetime

from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from dotenv import load_dotenv
# from config import BOT_TOKEN

# Запускаем логгирование
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
# )
#
# logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

base_keyboard = [['/dice', '/timer']]
base_markup = ReplyKeyboardMarkup(base_keyboard, one_time_keyboard=False)

dice_keyboard = [['/one_dice', '/two_dices'],
                      ['/one_20_dice', '/back']]
dice_markup = ReplyKeyboardMarkup(dice_keyboard, one_time_keyboard=False)

closes_keyboard = [['/close']]
closes_markup = ReplyKeyboardMarkup(closes_keyboard, one_time_keyboard=False)

async def start(update, context):
    await update.message.reply_text(
        "Я бот-помощник для настольных игр",
        reply_markup=base_markup
    )

async def help(update, context):
    await update.message.reply_text(
        "Я бот-помощник для настольных игр.")

# управление кубиком
async def dice(update, context):
    await update.message.reply_text(
        "Выбирай",
        reply_markup=dice_markup
    )

async def one_dice(update, context):
    num = random.randint(1, 6)
    await update.message.reply_text(num)

# управление таймером
async def set_timer(update, context, time):
    chat_id = update.effective_message.chat_id

    job = context.job_queue.run_once(task,
                                     time,
                                     chat_id=chat_id,
                                     name=str(chat_id),
                                     data=time)
    context.chat_data['job'] = job


async def task(context):
    time = context.chat_data['job'].data
    print(time)
    await context.bot.send_message(context.job.chat_id,
                                   text=f'{time} cek',
                                   reply_markup=dice_markup)


async def timer(update, context):
    text = 'Установить таймер на 10 сек'
    await set_timer(update, context, 10)
    await update.message.reply_text(text,
                                    reply_markup=closes_markup)



async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler("one_dice", one_dice))
    application.add_handler(CommandHandler("two_dices", timer))
    application.add_handler(CommandHandler("back", start))
    application.add_handler(CommandHandler("timer", timer))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.run_polling()


if __name__ == '__main__':
    main()