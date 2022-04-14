import datetime
import random
import string
import types
from typing import List
from db import BotDB
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram import types
from dispatcher import bot
from all_states import Ban_User
import time
import re

BotDB = BotDB('/Users/jcu/Desktop/MyProjects/Company INC/server.db')



class User:

    def __init__(self, id_user):
        self.BotDB = BotDB
        
        self.id: int = id_user
        self.username: str = self.BotDB.get(key='username', where='id_user', meaning=self.id)
        self.name: str = self.BotDB.get(key='name', where='id_user', meaning=self.id)
    
    @property
    def get_company_name(self):
        return self.BotDB.get(key='name_company', where='id_company', meaning=self.id, table=self.get_type_of_activity)
    
    @property
    def get_nickname(self):
        return self.BotDB.get(key='nickname', where='id_user', meaning=self.id)
    
    @property
    def get_type_of_activity(self):
        return self.BotDB.get(key='type_of_activity', where='id_user', meaning=self.id)

    @property
    def get_rub(self):
        return self.BotDB.get(key='rub', where='id_user', meaning=self.id)
    
    @property
    def get_usd(self):
        return self.BotDB.get(key='usd', where='id_user', meaning=self.id)
    
    @property
    def get_btc(self):
        return self.BotDB.get(key='btc', where='id_user', meaning=self.id)


class DevSoftware:

    def __init__(self, id_company) -> None:
        self.user: User = User(id_company)
    
    def get_quantity_dev(self, dev: int):
        if int(dev) in [1, 2, 3]:
            return self.user.BotDB.get(key=f'quantity_dev_{dev}', where='id_company', meaning=self.user.id, table='dev_software')
    
    def get_quantity_buy_offices(self, office: int):
        return get_2dot_data(key=f'quantity_office_{office}', where='id_company', meaning=self.user.id, table='dev_software', meaning_data='1', get_data='buy')

    def get_quantity_rent_offices(self, office: int):
        return get_2dot_data(key=f'quantity_office_{office}', where='id_company', meaning=self.user.id, table='dev_software', meaning_data='1', get_data='rent')

    @property    
    def quantity_all_devs(self):
        return sum([self.get_quantity_dev(i) for i in range(1, 3+1)])
    
    @property
    def quantity_all_places(self):
        i = 1
        y = True
        places = 0
        while y:
            p = parse_2dot_data(key=f'quantity_office_{i}', where='id_company', meaning=self.user.id, table='dev_software')
            places += (p[1][1] + p[1][2]) * BotDB.vCollector(where='name', meaning=f'size_office_{i}', table='value_it')
            try:
                i+=1
                self.user.BotDB.vCollector(where='name', meaning=f'cost_office_{i}', table='value_it')
            except:
                y = False
        return places


# #########################################

def check_name_app(name_app):
    if name_app in BotDB.get_all('name_app', table='dev_software_apps'):
        return True
    return False

# #########################################

def one_pay(id_company):
    all_mark = 0
    total_income = 0
    all_dev = 0

    for i in range(1, 3+1):
        quantity_dev = BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software')
        all_dev += quantity_dev
        all_mark += quantity_dev * i
        total_income += quantity_dev * BotDB.vCollector(table='value_it', where='name', meaning=f'income_dev_{i}')

    percent_left = BotDB.vCollector(table='value_it', where='name', meaning='percent_one_pay_left')
    percent_right = BotDB.vCollector(table='value_it', where='name', meaning='percent_one_pay_right')
    true_perc = percent_right - percent_left
    average_mark = all_mark / all_dev
    x_perc = round(true_perc * average_mark / 3, 2)
    x_income = round((total_income * 60) * (percent_left + x_perc), 2)

    return x_income

def average_income_dev(id_company):
    total_income = 0
    all_dev = 0

    for i in range(1, 3+1):
        quantity_dev = BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software')
        all_dev += quantity_dev
        total_income += quantity_dev * BotDB.vCollector(table='value_it', where='name', meaning=f'income_dev_{i}')
    
    average_income = round(total_income/all_dev, 2)

    return average_income

def time_for_build(id_company):
    min = 0

    for i in range(1, 3+1):
        min += BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software') * (4-i)
    
    base_time = BotDB.vCollector(table='value_it', where='name', meaning='base_time_build_app')
    time_build = base_time + min 

    return time_build

# #########################################

def your_app_top(id_company):
    number_string = 1
    data = BotDB.get_alls_with_order(keys='id_company, name_app, one_pay, income', order='one_pay', table='dev_software_apps')
    for i in data:
        indx = data.index(i) + 1 if i[0] == id_company else 0
        if indx > BotDB.vCollector(where='name', meaning='quantity_top_apps', table='value_it'):
            d = {
                'number_string': number_string,
                'name_app': i[1],
                'one_pay': i[2],
                'income': i[3]
                }
            return get_text('template_string_end_top', format=True, d=d)
        elif indx == 0:
            number_string += 1
        else:
            return ''

def list_top_apps(id_company):
    number_string = 1
    t = ''
    for i in BotDB.get_alls_with_order(keys='id_company, name_app, one_pay, income', order='one_pay', table='dev_software_apps'):
        if number_string > BotDB.vCollector(where='name', meaning='quantity_top_apps', table='value_it'):
            break
        d = {
            'number_string': number_string,
            'name_app': i[1],
            'one_pay': shell_money(i[2]),
            'income': shell_money(i[3])
            }
        t += get_text('template_string_my_app', format=True, d=d) if i[0] == id_company else get_text('template_string_app', format=True, d=d)
        number_string += 1
    return t

def list_my_top_apps(id_company):
    number_string = 1
    t = ''
    for i in BotDB.get_alls_with_order(keys='id_company, name_app, one_pay, income', order='one_pay', table='dev_software_apps'):
        if i[0] == id_company:
            d = {
                'number_string': number_string,
                'name_app': i[1],
                'one_pay': shell_money(i[2]),
                'income': shell_money(i[3])
                }
            t += get_text('template_string_app', format=True, d=d)
            number_string += 1
    return t

def app_menu_data(id_company):
    all_income_apps = 0
    quantity_apps = 0
    d = {}
    time_left = ''
    for i in BotDB.get_alls_with_order(keys='id_company, done, income, quantity_min_build, date_reg', order='done', table='dev_software_apps'):
        all_income_apps += i[2] if i[0] == id_company else 0
        quantity_apps += 1 if i[0] == id_company else 0
        if i[1] == False and i[0] == id_company:
            date_reg = i[4]
            date_formatter = '%X %m/%d/%Y'
            future = datetime.datetime.strptime(date_reg, date_formatter) + datetime.timedelta(minutes=i[3])
            x = str(future - datetime.datetime.today()).split('.')[0]
            d = {'time_left': x}
            time_left = get_text('time_left_for_build_app', format=True, d=d)
    d = {
        'all_income_apps': shell_money(all_income_apps),
        'time_left': time_left,
        'quantity_apps': quantity_apps
        }
    return d
# #########################################

def calculate_pay_dev(quantity, salary_hour):
    min = int(time.strftime('%M'))
    min_job = 60 - min
    first_salary = round((min_job * salary_hour / 60) * quantity, 2) 
    return first_salary, min_job

def calculate_pay_rent(quantity, cost_rent_day):
    day = time.strftime('%d')
    month = time.strftime('%m')
    year = time.strftime('%Y')
    day = int(time.strftime('%d')) + 1 if datetime.datetime.strptime(f'19:00:00 {month}/{day}/{year}', '%H:%M:%S %m/%d/%Y') < datetime.datetime.today() else time.strftime('%d')
    t = datetime.datetime.strptime(f'19:00:00 {month}/{day}/{year}', '%H:%M:%S %m/%d/%Y') - datetime.datetime.today()
    min_rent = t.seconds // 60
    hours = min_rent // 60
    mins = 0 if min_rent % 60 + 1 == 60 else min_rent % 60 + 1 
    first_salary = round((min_rent * cost_rent_day / 1440) * quantity, 2) 
    return first_salary, hours, mins

# #########################################

def quantity_place_company(id_company):
    i = 1
    y = True
    places = 0
    while y:
        p = parse_2dot_data(key=f'quantity_office_{i}', where='id_company', meaning=id_company, table='dev_software')
        places += (p[1][1] + p[1][2]) * BotDB.vCollector(where='name', meaning=f'size_office_{i}', table='value_it')
        i+=1
        try:
            BotDB.vCollector(where='name', meaning=f'cost_office_{i}', table='value_it')
        except:
            y = False
    return places

def quantity_dev_company(id_company):
    return sum([BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software') for i in range(1, 3+1)])


def quantity_devices(id_company):
    i = 1
    ind = 0
    q_devices = 0
    y = True
    devices = ['screen', 'armchair', 'mouse', 'comp', 'keyboard', 'carpet']
    while y:
        device = devices[ind]
        data = parse_2dot_data(key=f'quantity_{device}', where='id_company', meaning=id_company, table='dev_software')
        ind_q = data[0].index('quantity')
        for i in data[1:]:
            q_devices += i[ind_q]
        try:
            ind += 1
            device = devices[ind]
        except:
            y = False
    return q_devices

def create_mat_percents(id_company):
    devices = ['screen', 'armchair', 'mouse', 'comp', 'keyboard', 'carpet']
    i = 1
    ind = 0
    y = True
    devices_k = []
    while y:
        device = devices[ind]
        q_device = parse_2dot_data(key=f'quantity_{device}', where='id_company', meaning=id_company, table='dev_software')[1:]
        q_devs = [BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software') for i in range(1, 3+1)]
        for i in q_device:
            s = []
            true_q_device = i[1]
            if i[0] > 1:
                u = 0
                for t in range(1, i[0]):
                    u += q_device[t-1][1] 
                s = [0]*u + s
            elif i[1] == 0:
                continue
            for j in q_devs:
                if j == 0:
                    continue
                elif i[1] >= j:
                    s += [1]*j
                    i[1] = i[1] - j
                    q_devs[q_devs.index(j)] = 0
                elif i[1] <= j:
                    s += [1]*i[1]
                    i[1] = 0
                    q_devs[q_devs.index(j)] = j - i[1]
                    s += [0]*(quantity_dev_company(id_company) - len(s))
                    break
            i[1] = true_q_device
            devices_k.append([f'{device}_{i[0]}'] + s)
        try:
            ind += 1
            device = devices[ind]
        except:
            y = False
    return devices_k


def count_percent_device(device_k, id_company):
    q_devs = [BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software') for i in range(1, 3+1)]
    dev_name = ['junior', 'middle', 'senior']
    percents = []
    for i in range(1, quantity_dev_company(id_company)+1):
        percent = 0
        for x in range(len(device_k)):
            if device_k[x][i] == 1:
                percent += BotDB.vCollector(where='name', meaning=f'percent_{device_k[x][0]}', table='value_it') 
        percents.append(round(percent, 2))
    text = ''
    u = 0
    for i in enumerate(q_devs):
        slice = percents[u:i[1]+u]
        for j in sorted(list(set(percents[u:i[1]+u])), reverse=False):
            d = {
                'dev': dev_name[i[0]],
                'quantity_same_percent': slice.count(j),
                'percent': shell_money(j*100)
                }
            text += get_text('template_string_count_percent_device', format=True, d=d)
        u += i[1]
    return text

# #########################################

def app_build(id_company):
    for i in BotDB.get_alls(keys='done, id_company, name_app', table='dev_software_apps'):
        if i[0] == 0 and i[1] == id_company:
            return True, i[2]
    return False, '-'

# #########################################

def get_button(unique_number) -> str:
    mode = BotDB.get(key='text_box1', where='name', meaning='program_mode_for_text', table='value_main')
    try:
        BotDB.get(key='name', where='number', meaning=unique_number, table='button_name')
    except:
        BotDB.add_new_button(unique_number)
    return f'({unique_number})\n\n' + BotDB.get(key='name', where='number', meaning=unique_number, table='button_name') if mode == 'on' else BotDB.get(key='name', where='number', meaning=unique_number, table='button_name')

def get_text(unique_name, d={}, format=True) -> str:
    mode = BotDB.get(key='text_box1', where='name', meaning='program_mode_for_text', table='value_main')
    try:
        text = BotDB.get(key='text_box1', where='name', meaning=unique_name, table='texts')
    except:
        BotDB.add_new_text(name=unique_name)
        text = BotDB.get(key='text_box1', where='name', meaning=unique_name, table='texts')
    text_true = text.format(**d) if format else text
    return f'({unique_name})\n\n' + text_true if mode == 'on' else text_true

def get_photo(unique_name) -> str:
    try:
        photo = BotDB.get(key='photo_id', where='name', meaning=unique_name, table='photos')
    except:
        photo = BotDB.get(key='photo_id', where='name', meaning='without_photo', table='photos')
    return photo

# #########################################

def create_2dot_data(table, key, where, meaning, headers=[], d=[]):
    get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
    h = ':'.join(headers)
    if get_data:
        get_data if h == get_data.split(',')[0] else h + get_data
    else:
        get_data = h + get_data
    s = ',' + ':'.join(d)
    adding = get_data.strip(',') + s
    BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=adding.strip(','))


def parse_2dot_data(table, key, where, meaning) -> List[list]: 
    get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
    l = get_data.split(',')
    l1 = []
    l2 = []
    for i in l:
        for x in i.split(':'):
            if x.isdigit() or isfloat(x):
                x = float(x) if isfloat(x) else int(x)
            l1.append(x)
        l2.append(l1)
        l1 = []
    return l2

def get_2dot_data(table, key, where, meaning, where_data: str = 'id', get_data: str = 'id', meaning_data: str = '0'):
    try:
        parse = parse_2dot_data(key=key, where=where, meaning=meaning, table=table)
        ind = parse[0].index(where_data)
        ind_get = parse[0].index(get_data)
    except Exception as e:
        return print('Ошибка!\nФункция: get_2dot_data') 
    for i in parse[1:]:
        if i[ind] == int(meaning_data):
            return i[ind_get]

def add_2dot_data(table, key, where, meaning, add, where_data: str = 'id', add_data: str = 'id', meaning_data: str = '0'):
    try:
        parse = parse_2dot_data(key=key, where=where, meaning=meaning, table=table)
        ind = parse[0].index(where_data)
        ind_add = parse[0].index(add_data)
    except Exception as e:
        return print('Ошибка!\nФункция: add_2dot_data') 
    s = ':'.join(parse[0])
    for i in parse[1:]:
        if str(i[ind]) == meaning_data:
            i[ind_add] = round(i[ind_add] + add, 2) if isfloat(str(i[ind_add])) else i[ind_add] + add
        s += ',' + ':'.join(list(map(lambda x: str(x), i)))
    BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=s.strip(','))


def delete_2dot_data(table, key, where, meaning, unique_value_data):
    get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
    l = get_data.split(',')
    headers = l[0]
    s = ''
    for i in l[1:]:
        if unique_value_data not in i:
            s += ',' + i
    s = headers + s
    BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=s.strip(','))


def update_item_2dot_data(table, key, where, meaning, item, where_data = 0, meaning_data = '0', change_index=0):
    get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
    l = get_data.split(',')
    s = ''
    for i in l:
        i = i.split(':')
        if i[where_data] == meaning_data:
            i[change_index] = item
        s += ',' + ':'.join(i)
    BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=s.strip(','))


def add_header_2dot_data(table, key, where, meaning, name_new_header):
    get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
    l = get_data.split(',')
    l_new = []
    l_new.append(l[0] + ':' + name_new_header)
    for i in l[1:]:
        l_new.append(i + ':0')
    BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=','.join(l_new))


def delete_header_2dot_data(table, key, where, meaning, name_header):
    try:
        get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
        l: list = get_data.split(',')
        ind = l[0].split(':').index(name_header)
    except Exception as e:
        return print('Ошибка!\nФункция: delete_header_2dot_data') 
    get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
    l: list = get_data.split(',')
    l_new = []
    ind = l[0].split(':').index(name_header)
    _: list = l[0].split(':')
    _.pop(ind)
    l_new.append(':'.join(_))
    for i in l[1:]:
        i = i.split(':')
        i.pop(ind)
        _ = ':'.join(i)
        l_new.append(_)
    BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=','.join(l_new))

# #########################################

def referrer_linc(id_user, bot_name='company_inc_game_bot'):
    '''Функция для создания реферральной ссылки юзера'''
    return f'http://t.me/{bot_name}?start={id_user}'

# #########################################

def last_tap(button='-', state=False): 
    def actual_dec(func):
        if state:
            async def wrapper(message: types.Message, state: FSMContext):
                if message.from_user.username != BotDB.get(key='username', where='id_user', meaning=message.from_user.id):
                    BotDB.updateT(key='username', where='id_user', meaning=message.from_user.id, text='@' + message.from_user.username)
                
                date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
                BotDB.updateT(key='last_tap', where='id_user', meaning=message.from_user.id, text=date)
                BotDB.add(key='count_tap', where='id_user', meaning=message.from_user.id, num=1)
                BotDB.add(table='click_button', key='amount_click', where='button', meaning=button, num=1)
                return await func(message, state)
        else:
            async def wrapper(message: types.Message):
                if message.from_user.username != BotDB.get(key='username', where='id_user', meaning=message.from_user.id):
                    BotDB.updateT(key='username', where='id_user', meaning=message.from_user.id, text='@' + message.from_user.username)
                
                date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
                BotDB.updateT(key='last_tap', where='id_user', meaning=message.from_user.id, text=date)
                BotDB.add(key='count_tap', where='id_user', meaning=message.from_user.id, num=1)
                BotDB.add(table='click_button', key='amount_click', where='button', meaning=button, num=1)
                return await func(message)
        return wrapper
    return actual_dec

def last_tap_call(button='-', state=False): 
    def actual_dec(func):
        if state:
            async def wrapper(call: CallbackQuery, state: FSMContext):
                if call.from_user.username != BotDB.get(key='username', where='id_user', meaning=call.from_user.id):
                    BotDB.updateT(key='username', where='id_user', meaning=call.from_user.id, text='@' + call.from_user.username)

                date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
                BotDB.updateT(key='last_tap', where='id_user', meaning=call.from_user.id, text=date)
                BotDB.add(key='count_tap', where='id_user', meaning=call.from_user.id, num=1)
                BotDB.add(table='click_button', key='amount_click', where='button', meaning=button, num=1)
                return await func(call, state)
        else:
            async def wrapper(call: CallbackQuery):
                if call.from_user.username != BotDB.get(key='username', where='id_user', meaning=call.from_user.id):
                    BotDB.updateT(key='username', where='id_user', meaning=call.from_user.id, text='@' + call.from_user.username)

                date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
                BotDB.updateT(key='last_tap', where='id_user', meaning=call.from_user.id, text=date)
                BotDB.add(key='count_tap', where='id_user', meaning=call.from_user.id, num=1)
                BotDB.add(table='click_button', key='amount_click', where='button', meaning=button, num=1)

                return await func(call)
        return wrapper
    return actual_dec

# #########################################

def clean_error_reg_company(id_user):
    # all_table=['dev_software','dev_game','farming','clothing_and_shoes','car_production','phone_production',
    # 'creating_food','restaurant','beauty_salon','tss','law_agency','private_clinic','fuel_production','oil_production']
    try:
        BotDB.delete(where='id_company', meaning=id_user, table=BotDB.get(key='type_of_activity',where='id_user', meaning=id_user))
    except Exception as e:
        print(e)

def check_emptys(id_user):
    try:
        answ =True if BotDB.get(key='nickname', where='id_user', meaning=id_user) == None or\
            BotDB.get(key='type_of_activity', where='id_user', meaning=id_user) == None or\
            BotDB.get(key='name_company', where='id_company', meaning=id_user, table=BotDB.get(key='type_of_activity', where='id_user', meaning=id_user)) == None else False
    except:
        answ = True
    return answ
        
def error_reg(func):
    async def wrapper(message: types.Message):
        if check_emptys(message.from_user.id):
            clean_error_reg_company(message.from_user.id)
            text1 = get_text('exist_user1', format=False)
            await message.answer(text1, reply_markup=ReplyKeyboardRemove())  
        else:
            return await func(message)
    return wrapper

def error_reg_call(func):
    async def wrapper(call: CallbackQuery):
        if check_emptys(call.from_user.id):
            clean_error_reg_company(call.from_user.id)
            text1 = get_text('exist_user1', format=False)
            await bot.send_(text1, reply_markup=ReplyKeyboardRemove())  
        else:
            return await func(call)
    return wrapper

# #########################################

def ban(state=False):
    def actdec(func):
        if state:
            async def wrapper(message: types.Message, state: FSMContext):
                if message.from_user.id in BotDB.get_all(key='id_user', table='black_list'):
                    await message.answer(get_text('ban_wrapper', format=False), reply_markup=ReplyKeyboardRemove()) 
                    await Ban_User.Q1.set()
                else:
                    return await func(message, state)
        else:
            async def wrapper(message: types.Message):
                if message.from_user.id in BotDB.get_all(key='id_user', table='black_list'):
                    await message.answer(get_text('ban_wrapper', format=False), reply_markup=ReplyKeyboardRemove()) 
                    await Ban_User.Q1.set()
                else:
                    return await func(message)
        return wrapper
    return actdec

def ban_call(state=False):
    def actdec(func):
        if state:
            async def wrapper(call: CallbackQuery, state: FSMContext):
                if call.from_user.id in BotDB.get_all(key='id_user', table='black_list'):
                    await bot.send_message(call.from_user.id, get_text('ban_wrapper', format=False), reply_markup=ReplyKeyboardRemove()) 
                    await Ban_User.Q1.set()
                else:
                    return await func(call, state)
        else:
            async def wrapper(call: CallbackQuery):
                if call.from_user.id in BotDB.get_all(key='id_user', table='black_list'):
                    await bot.send_message(call.from_user.id, get_text('ban_wrapper', format=False), reply_markup=ReplyKeyboardRemove()) 
                    await Ban_User.Q1.set()
                else:
                    return await func(call)
        return wrapper
    return actdec

# #########################################

def check_nickname(nickname):
    if nickname in BotDB.get_all('nickname'):
        return True
    return False

def clean_nickname(nickname):
    nickname = re.sub("[!\"#$%&'()*+,./\\\:;<=>?@[\]^`{|}~]", '', nickname)
    nickname = re.sub('[^\x00-\x7Fа-яА-ЯёЁ]', '', nickname)
    return nickname

def check_on_simbols(nickname):
    try:
        nickname1 = re.findall("[!\"#$%&'()*+,./\\\:;<=>?@[\]^`{|}~]", nickname)
        nickname2 = re.findall('[^\x00-\x7Fа-яА-ЯёЁ]', nickname)
        return len(nickname1)+len(nickname2)
    except:
        pass


# #########################################

def check_name_company(name_company):
    s = []
    all_table=['dev_software','farming','clothing_and_shoes','car_production','phone_production',
    'creating_food','restaurant','beauty_salon','tss','law_agency','private_clinic','fuel_production','oil_production']
    for i in all_table:
        s += BotDB.get_all('name_company', table=i)
    if name_company in s:
        return True
    return False

# #########################################

def get_your_stocks(id_user):
    t = ''
    number_string = 1
    parse = parse_2dot_data(table='users', key='briefcase', where='id_user', meaning=id_user)[1:]
    for x in parse:
        d = {
            'number_string': number_string,
            'id_company':shell_money(x[0], currency='id'),
            'name_company':x[1],
            'quantity_stocks':shell_money(x[2]),
            'price_buy': shell_money(x[3])
        }
        t += get_text('template_string_my_stocks', format=True, d=d)
        number_string += 1
    return t

def update_rating_stocks(id_company):
    rating = 0 
    for i in BotDB.get_all(key='id_user'):
        try:
            parse = parse_2dot_data(table='users', key='briefcase', where='id_user', meaning=i)
            for x in parse:
                if id_company in x:
                    rating += 1
        except Exception as e:
            pass
    BotDB.updateN(key='rating', where='id_company', meaning=id_company, table='stocks', num=rating)

def list_stocks(page=1):
    t = ''
    data = BotDB.get_alls_with_order('id_company, name_company, count_stocks_stay, price_one_stocks, piece_of_income, count_stocks, seller', order='rating', table='stocks')
    count_string = BotDB.vCollector(where='name', meaning='count_string_in_one_page_stocks', table='value_main')
    for i in list(data):
        if len(data)/BotDB.vCollector(where='name', meaning='count_string_in_one_page_stocks', table='value_main') >= 1:
            if i[2] > 0:
                if data.index(i) >= (page-1) * count_string and data.index(i)+1 <= page * count_string:
                    d = {
                        'id_company': shell_money(i[0], currency='id'),
                        'name_company': i[1],
                        'count_stocks_stay': shell_money(i[2]),
                        'price_one_stocks': shell_money(i[3]),
                        'percent': round(i[4]/i[5] * 100, 4),
                        'seller': BotDB.get(key='name_company', where='id_company', meaning=i[-1], table='stocks')
                        }
                    t += get_text('template_one_string_stocks', format=True, d=d) if i[-1] == i[0] else get_text('template_one_string_sell_stocks', format=True, d=d)
            else:
                data.remove(i)
        else:
            if i[2] > 0:
                d = {
                    'id_company': shell_money(i[0], currency='id'),
                    'name_company': i[1],
                    'count_stocks_stay': shell_money(i[2]),
                    'price_one_stocks': shell_money(i[3]),
                    'percent': round(i[4]/i[5] * 100, 4),
                    'seller': BotDB.get(key='name_company', where='id_company', meaning=i[-1], table='stocks')
                    }
                t += get_text('template_one_string_stocks', format=True, d=d) if i[-1] == 0 else get_text('template_one_string_sell_stocks', format=True, d=d)
            else:
                data.remove(i)

    return t.strip('\n')


# #########################################

def available(id_user, price_item, currency='rub'):
    quantity_money = BotDB.get(key=currency, where='id_user', meaning=id_user)
    quantity_available = quantity_money // price_item
    return quantity_available
# #########################################

def shell_money(quantity_money, currency='usd'):
    quantity_money = round(quantity_money, 2)
    if currency == 'id':
        return '<code>{}</code>'.format(quantity_money)
    elif isfloat(str(quantity_money)):
        if float(quantity_money) % 1 == 0:
            return '<code>{:,}</code>'.format(int(quantity_money))
        return '<code>{:,.2f}</code>'.format(float(quantity_money)) if currency == 'usd' else '<code>{:,.5f}</code>'.format(float(quantity_money))
    else:
        return '<code>{:,}</code>'.format(int(quantity_money))

def cleannum(numb):
    numb = re.sub("[!\"#$%&'()*+,/\\\:;<=>?@[\]^`{|}~]", '', numb)
    numb = re.sub('[^\x00-\x7F]', '', numb)
    numb = re.sub('[а-яА-ЯёЁ]', '', numb)
    numb = re.sub('[A-Za-z]', '', numb)
    clean_num = re.findall("^[-+]?[0-9]*[.,]?[0-9]+(?:[eE][-+]?[0-9]+)?$", numb)
    try:
        return clean_num[0]
    except: return ' ' 


def currency_calculation(money, what_calculate='rub_in_usd', currency='rate_usd'):
    '''Конвертирует валюты'''
    rate = BotDB.vCollector(table='value_main', where='name', meaning=currency)
    if what_calculate == 'rub_in_usd':
        result = round(money / rate, 2)
    elif what_calculate == 'usd_in_btc':
        result = round(money / rate, 5)
    elif what_calculate == 'usd_in_rub':
        result = int(money * rate)
    elif what_calculate == 'btc_in_usd':
        result = round(money * rate,2)
    return result

# #########################################

def isfloat(num):
    if num.isdigit():
        return False
    else:
        try:
            float(num)
            return True
        except:
            return False

# #########################################

def get_minpercent(type_money,update=False) -> int:

    users = BotDB.get_all('id_user')
    type_average_percent = type_money + '_average_percent'
    all_average_percent =  BotDB.get_all(type_average_percent)
    sum_perc = 0

    for i in all_average_percent:
        idx = all_average_percent.index(i)
        if i:
            list_minpercent = [i for i in i.split(';') if i]
            sum_perc = 0
            text_box = []
            for i in list_minpercent:
                list_box = i.split(',')
                percent = float(list_box[1])
                min = int(list_box[0])
                if min == 0:
                    text_box.append('')
                else:
                    sum_perc += percent
                    text_box.append(f'{min-1},{percent}')
            if update:
                text_box = [i for i in text_box if i != '']
                text = ';'.join(text_box)
                BotDB.updateT(key=type_average_percent, where='id_user', meaning=users[idx], text=text)

    return sum_perc

def check_graf_rate(dimension):
    '''Проверяет кол-во записей курсов usd and btc в БД, если оно превышает установленую размерность, тогда самая старая запись удаляется'''
    result_usd, result_btc = BotDB.get_all('id','graf_rate_usd'), BotDB.get_all('id','graf_rate_btc')
    if len(result_usd) > dimension:
        BotDB.delete('id', result_usd[0], 'graf_rate_usd')
    elif len(result_btc) > dimension:
        BotDB.delete('id', result_btc[0], 'graf_rate_btc')


def add_minperc(id_user, type_money, percent, min=15):
    type_average_percent = type_money + '_average_percent'
    text = f';{min},{percent}'
    old_text = BotDB.get(key=type_average_percent, where='id_user', meaning=id_user)
    BotDB.updateT(key=type_average_percent, where='id_user', meaning=id_user, text=old_text+text) 


def exchange_balans(id_user, count_money, type_currency='rate_usd'):
    dimension_graf_rate = BotDB.vCollector(table='value_main', where='name', meaning='dimension_graf_rate') #размерность данных для графика
    
    abs_money = abs(count_money) #берем по модулю наши деньги
    
    ratio = BotDB.vCollector(table='value_main', where='name', meaning=f'ratio_exchange')  #коеффициент скорости изменения курса
    all_money_people = BotDB.get_all(type_currency.split('_')[1]) #получаем все имеющиеся деньги указоного типа от всех юзеров
    
    if count_money > 0:
        rate_currency = BotDB.vCollector(table='value_main', where='name', meaning=type_currency)
        percent_decimal = round((abs_money / (sum(all_money_people) + abs_money)) / ratio, 4) #получаем десятичный процент, формула = наши_деньги / деньги_всех + наши_деньги / коеффициент скорости изменения курса
        percent = percent_decimal * 100 #получаем проценты
        add_minperc(id_user,type_currency.split('_')[1],percent,ratio-1) #записываем их в БД 

        type_rate_now_text = type_currency + '_now' #генерируем нужные нам текста для обращения в БД
        type_percent_text = 'perc_' + type_currency.split('_')[1] 
        type_graf_rate_text = 'graf_rate_' + type_currency.split('_')[1] 
        
        sum_percent_decimal = get_minpercent(type_currency.split('_')[1]) / 100

        currency = rate_currency + sum_percent_decimal * rate_currency #просчитываем курс учитывая проценты
        BotDB.updateN(table='value_main', key='main_num', where='name', meaning=type_currency, num=round(currency, 2)) #записываем в БД текущий курс
        
        date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
        percent_to_text = f"{sum_percent_decimal * 100}"
      
        BotDB.cur.execute(f'INSERT INTO "{type_graf_rate_text}" (time_update, {type_currency}, {type_percent_text}, {type_rate_now_text}) VALUES (?,?,?,?)',(date, rate_currency, percent_to_text, round(currency, 2)))
        BotDB.conn.commit()
    else:
        percent = round((abs_money / (sum(all_money_people) + abs_money)) / ratio, 4) * 100
        add_minperc(id_user,type_currency.split('_')[1],-percent,ratio) #записываем их в БД 
    
    check_graf_rate(dimension_graf_rate)

# #########################################

def taG():
    tagg = ''
    all = string.digits + string.ascii_letters
    for i in range(0, 10):
        a = random.choice(all)
        tagg += a
    return tagg

# #########################################

def emodziside(num):
    plus = BotDB.get(key='text_box1', where='name', meaning='plus', table='value_main')
    minus = BotDB.get(key='text_box1', where='name', meaning='minus', table='value_main')
    return plus if num > 0 else minus

def get_text(unique_name, d={}, format=True) -> str:
    mode = BotDB.get(key='text_box1', where='name', meaning='program_mode_for_text', table='value_main')
    try:
        text = BotDB.get(key='text_box1', where='name', meaning=unique_name, table='texts')
    except:
        BotDB.add_new_text(name=unique_name)
        text = BotDB.get(key='text_box1', where='name', meaning=unique_name, table='texts')
    text_true = text.format(**d) if format else text
    return f'({unique_name})\n\n' + text_true if mode == 'on' else text_true


def check_graf_rate(dimension):
    '''Проверяет кол-во записей курсов usd and btc в БД, если оно превышает установленую размерность, тогда самая старая запись удаляется'''
    result_usd, result_btc = BotDB.get_all('id','graf_rate_usd'), BotDB.get_all('id','graf_rate_btc')
    if len(result_usd) > dimension:
        BotDB.delete('id', result_usd[0], 'graf_rate_usd')
    elif len(result_btc) > dimension:
        BotDB.delete('id', result_btc[0], 'graf_rate_btc')
    else:
        pass

def get_minpercent(type_money,update=False) -> int:

    users = BotDB.get_all('id_user')
    type_average_percent = type_money + '_average_percent'
    all_average_percent =  BotDB.get_all(type_average_percent)
    sum_perc = 0

    for i in all_average_percent:
        idx = all_average_percent.index(i)
        if i:
            list_minpercent = [i for i in i.split(';') if i]
            sum_perc = 0
            text_box = []
            for i in list_minpercent:
                list_box = i.split(',')
                percent = float(list_box[1])
                min = int(list_box[0])
                if min == 0:
                    text_box.append('')
                else:
                    sum_perc += percent
                    text_box.append(f'{min-1},{percent}')
            if update:
                text_box = [i for i in text_box if i != '']
                text = ';'.join(text_box)
                BotDB.updateT(key=type_average_percent, where='id_user', meaning=users[idx], text=text)
        else:
            pass

    return sum_perc

def rate_usd():
    dimension_graf_rate = BotDB.vCollector(table='value_main', where='name', meaning='dimension_graf_rate')

    usd = BotDB.vCollector(table='value_main', where='name', meaning='rate_usd')
    sum_perc_decimal = get_minpercent('usd') / 100

    random_perc_decimal = round(random.uniform(-1, 1), 2) / 100
    
    full_perc_decimal = random_perc_decimal + sum_perc_decimal
    abs_full_perc_decimal = abs(full_perc_decimal)

    if full_perc_decimal > 0:
        usd_now = usd * full_perc_decimal + usd
    else:
        usd_now = usd - usd * abs_full_perc_decimal
    
    text = f"{full_perc_decimal * 100}"
    
    get_minpercent('usd',True)

    BotDB.updateN(table='value_main', key='main_num', where='name', meaning='rate_usd', num=round(usd_now, 2))  
    date = time.strftime('%X') + time.strftime(' %m/%d/%Y')  
    BotDB.cur.execute(
        f'INSERT INTO graf_rate_usd (time_update, rate_usd, perc_usd, rate_usd_now) VALUES (?,?,?,?)',(date, usd, text, round(usd_now, 2)))
    BotDB.conn.commit()

    check_graf_rate(dimension_graf_rate)



def rate_btc():
    dimension_graf_rate = BotDB.vCollector(table='value_main', where='name', meaning='dimension_graf_rate')

    btc = BotDB.vCollector(table='value_main', where='name', meaning='rate_btc')
    sum_perc_decimal = get_minpercent('btc') / 100

    random_perc_decimal = round(random.uniform(-1, 1), 2) / 100
    
    full_perc_decimal = random_perc_decimal + sum_perc_decimal
    abs_full_perc_decimal = abs(full_perc_decimal)

    if full_perc_decimal > 0:
        btc_now = btc * full_perc_decimal + btc
    else:
        btc_now = btc - btc * abs_full_perc_decimal
    
    text = f"{full_perc_decimal * 100}"
    
    get_minpercent('btc',True)

    BotDB.updateN(table='value_main', key='main_num', where='name', meaning='rate_btc', num=round(btc_now, 2))  
    date = time.strftime('%X') + time.strftime(' %m/%d/%Y')  
    BotDB.cur.execute(
        f'INSERT INTO graf_rate_btc (time_update, rate_btc, perc_btc, rate_btc_now) VALUES (?,?,?,?)',(date, btc, text, round(btc_now, 2)))
    BotDB.conn.commit()

    check_graf_rate(dimension_graf_rate)


async def verify():
    data = BotDB.get_alls('id_user, referrer, count_tap, date_reg, verify')
    for i in data:
        verife_date = datetime.datetime.today() > datetime.datetime.strptime(i[3], '%H:%M:%S %m/%d/%Y') + datetime.timedelta(days=3)
        if i[1] != 0 and i[2] >= 50 and verife_date and i[4] == 0:
            award_referral = BotDB.vCollector(table='value_main', where='name', meaning='award_referral')
            award_referrer = BotDB.vCollector(table='value_main', where='name', meaning='award_referrer')
            # обновляем статус верификации
            BotDB.updateN(key='verify', where='id_user', meaning=i[0], num=1)
            # отправляем сообщение пользователю о том, что он прошел верефикацию успешно
            await bot.send_message(i[0], get_text('verify_ referral', format=False))
            # начисляем бонус за положительный статус верификации реффералу
            BotDB.add(key='usd', where='id_user', meaning=i[0], num=award_referral)
            # отправляем сообщение человеку, который сделал инвайт 
            await bot.send_message(i[1], get_text('verify_referrer', format=False))
            # начисляем бонус рефферу за положительный статус верификации у рефферала
            BotDB.add(key='usd', where='id_user', meaning=i[1], num=award_referrer)
