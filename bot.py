import asyncio
import time

import aioschedule
from aiogram import executor

from all_function import (check_apps_done, income_dev_software, rate_currency, rent_office,
                          salary_dev, verify)
from dispatcher import BotDB, dp
from handlers import *


async def job_sec():
    pass

async def job_minute():
    date = time.strftime('%X').split(':')
    if date[2] == '00':
        rate_currency()
        await verify()
        [BotDB.add(key='rub', where='id_user', meaning=i, num=income_dev_software(i)) for i in
         BotDB.get_all('id_company', 'dev_software')]
        check_apps_done()
    else:
        pass


async def job_hour():
    date = time.strftime('%X').split(':')
    if date[1] == '00':
        [BotDB.add(key='rub', where='id_user', meaning=i, num=-salary_dev(i)) for i in
         BotDB.get_all('id_company', 'dev_software')]
    else:
        pass


async def job_take_rent():
    [BotDB.add(key='rub', where='id_user', meaning=i, num=-rent_office(i)) for i in
     BotDB.get_all('id_company', 'dev_software')]


async def job_bonus():
    for i in BotDB.get_all('id_user'):
        bonus = BotDB.get(key='bonus', where='id_user', meaning=i)
        if bonus == 0:
            BotDB.updateN(key='bonus', where='id_user', meaning=i, num=1)


async def scheduler():
    aioschedule.every().day.at('18:00').do(job_bonus)
    aioschedule.every().day.at('00:00').do(job_bonus)
    aioschedule.every().day.at('06:00').do(job_bonus)
    aioschedule.every().day.at('12:00').do(job_bonus)
    aioschedule.every().day.at('19:00').do(job_take_rent)
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
        executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
    except Exception as e:
        pass
