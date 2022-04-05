import time
import asyncio
import aioschedule
from aiogram import executor
from db import BotDB
from all_function import rate_btc, rate_usd, verify
from dispatcher import dp
from handlers import *


BotDB = BotDB('/Users/jcu/Desktop/MyProjects/Company INC/server.db')

async def job_sec():
    pass

async def job_minute():
    date = time.strftime('%X').split(':')
    if date[2] == '00':
        rate_usd()
        rate_btc()
        await verify()
    else:
        pass


async def job_hour():
    date = time.strftime('%X').split(':')
    if date[1] == '00':
        pass
    else:
        pass


async def job_bonus():
    for i in BotDB.get_all('id_user'):
        bonus = BotDB.get(key='bonus',where='id_user',meaning=i)
        if bonus == 0:
            BotDB.updateN(key='bonus',where='id_user',meaning=i, num=1)


async def scheduler():
    aioschedule.every().day.at('18:00').do(job_bonus)
    aioschedule.every().day.at('00:00').do(job_bonus)
    aioschedule.every().day.at('06:00').do(job_bonus)
    aioschedule.every().day.at('12:00').do(job_bonus)
    aioschedule.every(1).seconds.do(job_minute)
    aioschedule.every(1).seconds.do(job_hour)
    aioschedule.every(1).seconds.do(job_sec)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(0.1)


async def on_startup(x):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except Exception as e:
        pass
