from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db import BotDB
from aiogram.utils.callback_data import CallbackData
from all_function import get_button

BotDB = BotDB('/Users/jcu/Desktop/MyProjects/Company INC/server.db')

# leftright = CallbackData('side','postfix', 'index')

def changes_nickname():
    changes_nickname =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i10.2.1'), callback_data='support:change_nickname')
        ]
    ])
    return changes_nickname

def give_an_answer(tag_question):
    give_an_answer =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i10.3.2'), callback_data=f'give_an_answer:{tag_question}')
        ]
    ])
    return give_an_answer

def i_am_take(tag_question):
    i_am_take =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i10.3.1'), callback_data=f'i_am_take:{tag_question}')
        ]
    ])
    return i_am_take


def get_items():
    get_items =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('c1.i1'), callback_data=f'parse_items')
        ]
    ])
    return get_items


def update_and_convert():
    update_and_convert = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i2.1'), callback_data='ru'),
            InlineKeyboardButton(text=get_button('i2.2'), callback_data='ur'),
            InlineKeyboardButton(text=get_button('i2.3'), callback_data='ub')
        ],
        [
            InlineKeyboardButton(text=get_button('i2.4'), callback_data='bu'),
            InlineKeyboardButton(text=get_button('i2.5'), callback_data='update')
        ]
    ])
    return update_and_convert

def hire_dev(index):
    hire_dev =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i8.4.1'), callback_data=f'hire:dev:{index}')
        ],
        [
            InlineKeyboardButton(text=get_button('i8.4.4'), callback_data=f'dismiss:dev:{index}'),InlineKeyboardButton(text=get_button('i8.4.2'), callback_data=f'left:dev:{index}'), InlineKeyboardButton(text=get_button('i8.4.3'), callback_data=f'right:dev:{index}')
        ]
    ])
    return hire_dev

def office_dev(index):
    office_dev =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i8.6.6'), callback_data=f'stoprent:office:{index}'),        
        ],
        [
            InlineKeyboardButton(text=get_button('i8.6.1'), callback_data=f'buy:office:{index}'), InlineKeyboardButton(text=get_button('i8.6.2'), callback_data=f'rent:office:{index}')          
        ],
        [
            InlineKeyboardButton(text=get_button('i8.6.3'), callback_data=f'sell:office:{index}'), InlineKeyboardButton(text=get_button('i8.6.4'), callback_data=f'left:office:{index}'), InlineKeyboardButton(text=get_button('i8.6.5'), callback_data=f'right:office:{index}')
        ]
    ])
    return office_dev


def device():
    device =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i8.5.1'), callback_data=f'device_item:screen'), InlineKeyboardButton(text=get_button('i8.5.2'), callback_data=f'device_item:keyboard')          
        ],
        [
            InlineKeyboardButton(text=get_button('i8.5.3'), callback_data=f'device_item:mouse'), InlineKeyboardButton(text=get_button('i8.5.4'), callback_data=f'device_item:carpet')    
        ],
        [
            InlineKeyboardButton(text=get_button('i8.5.5'), callback_data=f'device_item:comp'), InlineKeyboardButton(text=get_button('i8.5.6'), callback_data=f'device_item:armchair')
        ]
    ])
    return device

def device_menu(device, index):
    device_menu =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('ii8.5.1'), callback_data=f'buy:device:{device}:{index}'), InlineKeyboardButton(text=get_button('ii8.5.2'), callback_data=f'sell:device:{device}:{index}')         
        ],
        [
            InlineKeyboardButton(text=get_button('ii8.5.3'), callback_data=f'device:back'), InlineKeyboardButton(text=get_button('ii8.5.4'), callback_data=f'left:device:{index}'), InlineKeyboardButton(text=get_button('ii8.5.5'), callback_data=f'right:device:{index}')
        ]
    ])
    return device_menu

def test_viev():
    test_viev =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Купить', callback_data=f'any'), InlineKeyboardButton(text='Продать', callback_data=f'any')         
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=f'any'), InlineKeyboardButton(text='⬅️', callback_data=f'any'), InlineKeyboardButton(text='➡️', callback_data=f'any')
        ]
    ])
    return test_viev

def create_first_app():
    create_first_app =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i8.1.3'), callback_data=f'app:create_app')
        ]
    ])
    return create_first_app


def menu_apps():
    menu_apps =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i8.1.1'), callback_data=f'app:top_apps')         
        ],
        [
            InlineKeyboardButton(text=get_button('i8.1.2'), callback_data=f'app:my_top_apps')   
        ],
        [
            InlineKeyboardButton(text=get_button('i8.1.3'), callback_data=f'app:create_app')
        ]
    ])
    return menu_apps

def app_back():
    app_back =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i8.1.4'), callback_data=f'app:back')
        ]
    ])
    return app_back

def menu_data_centre():
    menu_data_centre =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i8.2.1'), callback_data=f'data_centre:home')         
        ],
        [
            InlineKeyboardButton(text=get_button('i8.2.2'), callback_data=f'data_centre:foreign')   
        ]
    ])
    return menu_data_centre

def data_centre_open_back(place):
    data_centre_open_back =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i8.2.3'), callback_data=f'data_centre:open:{place}'), InlineKeyboardButton(text=get_button('i8.2.4'), callback_data=f'data_centre:back')
        ]
    ])
    return data_centre_open_back

def menu_briefcase():
    menu_briefcase =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i3.3.1'), callback_data=f'briefcase:sell_stocks')         
        ]
    ])
    return menu_briefcase

def menu_marketing_lab():
    menu_marketing_lab =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i8.3.1'), callback_data=f'marketing_lab:simple')         
        ],
        [
            InlineKeyboardButton(text=get_button('i8.3.2'), callback_data=f'marketing_lab:hard')   
        ]
    ])
    return menu_marketing_lab

def marketing_lab_open_back(type):
    data_centre_open_back =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i8.3.3'), callback_data=f'marketing_lab:study:{type}'), InlineKeyboardButton(text=get_button('i8.3.4'), callback_data=f'marketing_lab:back')
        ]
    ])
    return data_centre_open_back


def create_first_stocks():
    create_first_stocks =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i3.2.1'), callback_data=f'stocks:create_first_stocks')
        ]
    ])
    return create_first_stocks


def back_forward_page_stocks(page):
    back_forward_page_stocks =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i3.1.3'), callback_data=f'stocks:buy')
        ],
        [
            InlineKeyboardButton(text=get_button('i3.1.1'), callback_data=f'stocks:back:{page}'), InlineKeyboardButton(text=get_button('i3.1.2'), callback_data=f'stocks:forward:{page}')
        ]
    ])
    return back_forward_page_stocks

def back_page_stocks(page):
    back_page_stocks =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i3.1.3'), callback_data=f'stocks:buy'), InlineKeyboardButton(text=get_button('i3.1.1'), callback_data=f'stocks:back:{page}')
        ]
    ])
    return back_page_stocks

def forward_page_stocks(page):
    forward_page_stocks =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i3.1.3'), callback_data=f'stocks:buy'), InlineKeyboardButton(text=get_button('i3.1.2'), callback_data=f'stocks:forward:{page}')
        ]
    ])
    return forward_page_stocks

def buy_stocks():
    buy_stocks =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i3.1.3'), callback_data=f'stocks:buy')
        ]
    ])
    return buy_stocks