from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
from db import BotDB, path_db
from aiogram.utils.callback_data import CallbackData
from all_function import emodzi_active_item, get_button, get_inventory_with_items, get_text, parse_2dot_data

BotDB = BotDB(path_db)


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
            InlineKeyboardButton(text=get_button('i2.1'), callback_data='rub_usd'),
            InlineKeyboardButton(text=get_button('i2.2'), callback_data='usd_rub'),
            InlineKeyboardButton(text=get_button('i2.3'), callback_data='usd_btc')
        ],
        [
            InlineKeyboardButton(text=get_button('i2.4'), callback_data='btc_usd'),
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
            InlineKeyboardButton(text=get_button('i8.5.1'), callback_data=f'device_item:1'), InlineKeyboardButton(text=get_button('i8.5.2'), callback_data=f'device_item:2')          
        ],
        [
            InlineKeyboardButton(text=get_button('i8.5.3'), callback_data=f'device_item:3'), InlineKeyboardButton(text=get_button('i8.5.4'), callback_data=f'device_item:4')    
        ],
        [
            InlineKeyboardButton(text=get_button('i8.5.5'), callback_data=f'device_item:5'), InlineKeyboardButton(text=get_button('i8.5.6'), callback_data=f'device_item:6')
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

def create_app():
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


def create_stocks():
    create_stocks =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i3.2.1'), callback_data=f'stocks:create_stocks')
        ]
    ])
    return create_stocks

def split_stocks():
    split_stocks =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i3.2.2'), callback_data=f'stocks:extend_quantity_stocks')
        ]
    ])
    return split_stocks

def poll_extend_stocks(id_stocks):
    poll_extend_stocks =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i3.2.4'), callback_data=f'stocks:poll:yes:{id_stocks}'), InlineKeyboardButton(text=get_button('i3.2.5'), callback_data=f'stocks:poll:no:{id_stocks}')
        ]
    ])
    return poll_extend_stocks


def confirm_extension():
    confirm_extension =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i3.2.3'), callback_data=f'stocks:confirm_extension')
        ]
    ])
    return confirm_extension


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


def trends_menu_():
    buy_stocks =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i5.1'), callback_data=f'trends:voting')
        ]
    ])
    return buy_stocks

def all_voting_company(id_company):
    all_voting_company = InlineKeyboardMarkup(row_width=2)
    for i in parse_2dot_data(table='value_main', key='text_box1', where='name', meaning='all_companys')[1:]:
        all_voting_company.insert(InlineKeyboardButton(text=i[0], callback_data=f'trends:{i[1]}'))
    all_voting_company.add(InlineKeyboardButton(text=get_button('i6.1.2'), callback_data='trends:back'))
    return all_voting_company

def item_shop_menu(item_name):
    item_menu =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('i10.1.0'), callback_data=f'item_shop:buy:{item_name}'), InlineKeyboardButton(text=get_button('*1'), callback_data=f'item_shop:back')
        ]
    ])
    return item_menu

def create_items_keyboard():
    items = BotDB.get_alls(table='items', keys='name, type_add')
    items_keyboard = InlineKeyboardMarkup()
    for i in items:
        if i[1] == 'once':
            continue
        name_button = get_text(f'{i[0]}_name', format=False)
        items_keyboard.insert(InlineKeyboardButton(text=name_button, callback_data=f'item_shop_name:{i[0]}'))
    return items_keyboard

def create_inventory_items_keyboard(id_user):
    items = get_inventory_with_items(id_user)
    items_keyboard = InlineKeyboardMarkup(row_width=1)
    for i in items:
        status = items[i]['activated']
        name_button = items[i]['item_name'] + ' ' + emodzi_active_item(status)
        
        items_keyboard.insert(InlineKeyboardButton(text=name_button, callback_data=f'item_inventory_name:{i}:activated:{status}'))
    return items_keyboard


def item_inventory_menu(item_name, activated):
    activated = str(activated)
    items_keyboard = InlineKeyboardMarkup(row_width=1)
    if activated == '0':
        items_keyboard.insert(InlineKeyboardButton(text=get_button('activated.name_to_change!'), callback_data=f'item_inventory_adg:activated:{item_name}'))
    elif activated == '1': 
        items_keyboard.insert(InlineKeyboardButton(text=get_button('deactivated.name_to_change!'), callback_data=f'item_inventory_adg:deactivated:{item_name}'))
    elif activated == '2':
        items_keyboard.insert(InlineKeyboardButton(text=get_button('gift.name_to_change!'), callback_data=f'item_inventory_adg:gift:{item_name}'))

    items_keyboard.insert(InlineKeyboardButton(text=get_button('*1'), callback_data=f'item_inventory:back'))
    return items_keyboard


def item_inventory_gift_menu(item_name):
    item_menu_gift =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_button('gift.name_to_change!'), callback_data=f'item_menu_gift:{item_name}')
        ],
        [
             InlineKeyboardButton(text=get_button('*1'), callback_data=f'item_inventory:back')
        ]
    ])
    return item_menu_gift

def get_files_k():
    table_names = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", BotDB.conn)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for table in table_names['name']:  
        keyboard.insert(InlineKeyboardButton(text=table, callback_data=f'name_table:{table}'))
    return keyboard