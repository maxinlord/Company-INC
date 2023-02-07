import logging
from aiogram import Bot, Dispatcher
import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import BotDB, path_db


BotDB = BotDB(path_db)
# BotDB = BotDB('C:\\Users\\Admin\Desktop\\MyProjects\\Company INC\\server.db')
# /Users/jcu/Documents/GitHub/Company-INC/server.db

# Configure logging

logging.basicConfig(level=logging.INFO)

# prerequisites
if not config.BOT_TOKEN:
    exit("No token provided")


# init
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
