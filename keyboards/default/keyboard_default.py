from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from all_function import get_button
from db import BotDB

BotDB = BotDB('/Users/jcu/Desktop/MyProjects/Company INC/server.db')


def main_page():
    main_page = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_button('1')), KeyboardButton(text=get_button('2')), KeyboardButton(text=get_button('3'))
            ],
            [
                KeyboardButton(text=get_button('4')),KeyboardButton(text=get_button('5'))
            ],
            [
                KeyboardButton(text=get_button('6')), KeyboardButton(text=get_button('7')), KeyboardButton(text=get_button('8'))
            ],
            [
                KeyboardButton(text=get_button('9')), KeyboardButton(text=get_button('10'))
            ]
        ],
        resize_keyboard=True
    )
    return main_page


def exchange():
    exchange = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_button('2.1'))
            ],
            [
                KeyboardButton(text=get_button('2.2'))
            ]
        ],
        resize_keyboard=True
    )
    return exchange

def fields():
    fields = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_button('f1')),
                KeyboardButton(text=get_button('f2'))
            ],
            [
                KeyboardButton(text=get_button('f3'))
            ],
            [
                KeyboardButton(text=get_button('f4'))
            ]
        ],
        resize_keyboard=True
    )
    return fields


def types_it():
    types_it = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_button('f1.1'))
            ],
            [
                KeyboardButton(text=get_button('f1.2'))
            ],
            [
                KeyboardButton(text=get_button('*1'))
            ],
        ],
        resize_keyboard=True
    )
    return types_it


def types_product():
    types_product = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_button('f3.1')), KeyboardButton(text=get_button('f3.2'))
            ],
            [
                KeyboardButton(text=get_button('f3.3'))
            ],
            [
                KeyboardButton(text=get_button('f3.4')), KeyboardButton(text=get_button('f3.5'))
            ],
            [
                KeyboardButton(text=get_button('*1'))
            ],
        ],
        resize_keyboard=True
    )
    return types_product

def types_services():
    types_services = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_button('f2.1')), KeyboardButton(text=get_button('f2.2'))
            ],
            [
                KeyboardButton(text=get_button('f2.3')), KeyboardButton(text=get_button('f2.4'))
            ],
            [
                KeyboardButton(text=get_button('f2.5'))
            ],
            [
                KeyboardButton(text=get_button('*1'))
            ]
        ],
        resize_keyboard=True
    )
    return types_services


def types_blackgold():
    types_blackgold = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_button('f4.1')), KeyboardButton(text=get_button('f4.2'))
            ],
            [
                KeyboardButton(text=get_button('*1'))
            ]
        ],
        resize_keyboard=True
    )
    return types_blackgold

def company_dev_software():
    company_dev_software = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_button('8.1'))
            ],
            [
                KeyboardButton(text=get_button('8.2'))
            ],
            [
                KeyboardButton(text=get_button('8.3'))
            ],
            [
                KeyboardButton(text=get_button('8.4')), KeyboardButton(text=get_button('8.6'))
            ],
            [
                KeyboardButton(text=get_button('8.5')), KeyboardButton(text=get_button('*1'))
            ]
        ],
        resize_keyboard=True
    )
    return company_dev_software

def cds_upgrade():
    cds_upgrade = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_button('8.3.1'))
            ],
            [
                KeyboardButton(text=get_button('8.3.2'))
            ],
            [
                KeyboardButton(text=get_button('8.3.3'))
            ]
        ],
        resize_keyboard=True
    )
    return cds_upgrade

def user_setting():
    user_setting = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_button('10.1'))
            ],
            [
                KeyboardButton(text=get_button('10.2'))
            ],
            [
                KeyboardButton(text=get_button('10.3'))
            ],
            [
                KeyboardButton(text=get_button('*1'))
            ]
        ],
        resize_keyboard=True
    )
    return user_setting

def forbs():
    forbs = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_button('9.1'))
            ],
            [
                KeyboardButton(text=get_button('9.2'))
            ],
            [
                KeyboardButton(text=get_button('9.3'))
            ],
            [
                KeyboardButton(text=get_button('*1'))
            ]
        ],
        resize_keyboard=True
    )
    return forbs

def menu_stocks():
    menu_stocks = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_button('3.1')), KeyboardButton(text=get_button('3.3'))
            ],
            [
                KeyboardButton(text=get_button('3.2')), KeyboardButton(text=get_button('*1'))
            ]
        ],
        resize_keyboard=True
    )
    return menu_stocks


def cancel():
    cancel = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_button('*2'))
            ]
        ],
        resize_keyboard=True
    )
    return cancel

def cancel_answer():
    cancel_answer = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_button('*3'))
            ]
        ],
        resize_keyboard=True
    )
    return cancel_answer