
import datetime
from itertools import count
from pprint import pprint
import random
import string
import types
from typing import List, Tuple, Union
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from dispatcher import bot, BotDB
from aiogram import types
from all_states import Ban_User
import time
import re


# #########################################

def check_name_app(name_app):
    if name_app in BotDB.get_all('name_app', table='dev_software_apps'):
        return True
    return False

# #########################################

def one_pay_app(id_company):
    all_mark = 0
    total_income = 0
    all_dev = quantity_devs_company(id_company)
    device_k = create_mat_percents(id_company)
    
    for j in range(1, 3+1):
        quantity_dev = BotDB.get(key=f'quantity_dev_{j}', where='id_company', meaning=id_company, table='dev_software')
        all_mark += quantity_dev * j
        for i in count_percent_device(device_k, id_company, viev=False):
            income_dev = BotDB.vCollector(table='value_it', where='name', meaning=f'income_dev_{j}')
            total_income += ((1 + i['percent']) * income_dev) * i['quantity_same_percent'] if i['dev'] == j else 0


    percent_left = BotDB.vCollector(table='value_it', where='name', meaning='percent_one_pay_left')
    percent_right = BotDB.vCollector(table='value_it', where='name', meaning='percent_one_pay_right')
    true_perc = percent_right - percent_left
    average_mark = all_mark / all_dev
    x_perc = round(true_perc * average_mark / 3, 2)
    x_income = round((total_income * 60) * (percent_left + x_perc), 2)

    return x_income

def infinity_income_app(id_company):
    total_income = 0
    all_dev = quantity_devs_company(id_company)
    device_k = create_mat_percents(id_company)

    for j in range(1, 3+1):
        for i in count_percent_device(device_k, id_company, viev=False):
            income_dev = BotDB.vCollector(table='value_it', where='name', meaning=f'income_dev_{j}')
            total_income += ((1 + i['percent']) * income_dev) * i['quantity_same_percent'] if i['dev'] == j else 0
    
    average_income = round(total_income/all_dev, 2)

    return average_income

def time_for_build(id_company):
    min = sum([BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software') * (4-i) for i in range(1, 3+1)])
    
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
            'one_pay': shell_num(i[2]),
            'income': shell_num(i[3])
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
                'one_pay': shell_num(i[2]),
                'income': shell_num(i[3])
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
        'all_income_apps': shell_num(all_income_apps),
        'time_left': time_left,
        'quantity_apps': quantity_apps
        }
    return d
# #########################################

def calculate_pay_dev(quantity: int, salary_hour: Union[int, float]):
    min = int(time.strftime('%M'))
    min_job = 60 - min
    first_salary = round((min_job * salary_hour / 60) * quantity, 2) 
    return first_salary, min_job

def calculate_pay_rent(quantity: int, cost_rent_day: Union[int, float]) -> Tuple[Union[int, float], int, int]:
    day, month, year  = time.strftime('%d'), time.strftime('%m'), time.strftime('%Y')
    day = int(time.strftime('%d')) + 1 if datetime.datetime.strptime(f'19:00:00 {month}/{day}/{year}', '%H:%M:%S %m/%d/%Y') < datetime.datetime.today() else time.strftime('%d')
    t = datetime.datetime.strptime(f'19:00:00 {month}/{day}/{year}', '%H:%M:%S %m/%d/%Y') - datetime.datetime.today()
    min_rent = t.seconds // 60
    hours = min_rent // 60
    mins = 0 if min_rent % 60 + 1 == 60 else min_rent % 60 + 1 
    first_salary = round((min_rent * cost_rent_day / (24 * 60)) * quantity, 2) 
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

def quantity_devs_company(id_company):
    return sum([BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software') for i in range(1, 3+1)])


def quantity_devices(id_company):
    i = 1
    ind = 1
    q_devices = 0
    y = True
    while y:
        data = parse_2dot_data(key=f'quantity_device_{ind}', where='id_company', meaning=id_company, table='dev_software')
        ind_q = data[0].index('quantity')
        for i in data[1:]:
            q_devices += i[ind_q]
        try:
            ind += 1
            BotDB.get(table='dev_software', key=f'quantity_device_{ind}', where='id_company', meaning=id_company)
        except:
            y = False
    return q_devices

def create_mat_percents(id_company):
    i = 1
    ind = 1
    y = True
    devices_k = []
    while y:
        q_device = parse_2dot_data(key=f'quantity_device_{ind}', where='id_company', meaning=id_company, table='dev_software')[1:]
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
                    s += [0]*(quantity_devs_company(id_company) - len(s))
                    break
            i[1] = true_q_device
            devices_k.append([f'{ind}_{i[0]}'] + s)
        try:
            ind += 1
            BotDB.get(table='dev_software', key=f'quantity_device_{ind}', where='id_company', meaning=id_company)
        except:
            y = False
    # pprint(devices_k, width=300)
    return devices_k


def count_percent_device(device_k, id_company, viev=True):
    q_devs = [BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software') for i in range(1, 3+1)]
    dev_name = ['junior', 'middle', 'senior']
    percents = []
    for i in range(1, quantity_devs_company(id_company)+1):
        percent = 0
        for x in range(len(device_k)):
            if device_k[x][i] == 1:
                percent += BotDB.vCollector(where='name', meaning=f'percent_device_{device_k[x][0]}', table='value_it') 
        percents.append(round(percent, 2))
    text = ''
    l = []
    u = 0
    for i in enumerate(q_devs):
        slice = percents[u:i[1]+u]
        for j in sorted(list(set(percents[u:i[1]+u])), reverse=False):
            d = {
                'dev': dev_name[i[0]],
                'quantity_same_percent': slice.count(j),
                'percent': shell_num(j*100)
                }
            if viev:
                text += get_text('template_string_count_percent_device', format=True, d=d)
            else:
                d = {
                'dev': i[0]+1,
                'quantity_same_percent': slice.count(j),
                'percent': j
                }
                l.append(d)
        u += i[1]
    if viev:
        return text
    return l

# #########################################

def app_build(id_company: int) -> Tuple[bool, str]:
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

def create_2dot_data(table, key, where, meaning, d=[]):
    get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table).strip(',')
    s = ',' + ':'.join(list(map(lambda x: str(x), d)))
    adding = get_data + s
    BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=adding)


def parse_2dot_data(table, key, where, meaning) -> List[list]: 
    get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table).strip(',')
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
        parse = parse_2dot_data(key=key, where=where, meaning=meaning, table=table).strip(',')
        ind = parse[0].index(where_data)
        ind_get = parse[0].index(get_data)
    except Exception as e:
        return print('????????????!\n??????????????: get_2dot_data') 
    for i in parse[1:]:
        if str(i[ind]) == str(meaning_data):
            return i[ind_get]

def add_2dot_data(table, key, where, meaning, add, where_data: str = 'id', add_data: str = 'id', meaning_data: str = '0'):
    try:
        parse = parse_2dot_data(key=key, where=where, meaning=meaning, table=table).strip(',')
        ind = parse[0].index(where_data)
        ind_add = parse[0].index(add_data)
    except Exception as e:
        return print('????????????!\n??????????????: add_2dot_data') 
    s = ':'.join(parse[0])
    for i in parse[1:]:
        if str(i[ind]) == meaning_data:
            i[ind_add] = round(i[ind_add] + add, 2) if isfloat(str(i[ind_add])) else i[ind_add] + add
        s += ',' + ':'.join(list(map(lambda x: str(x), i)))
    BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=s.strip(','))


def delete_2dot_data(table, key, where, meaning, unique_value_data):
    get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table).strip(',')
    l = get_data.split(',')
    headers = l[0]
    s = ''
    for i in l[1:]:
        if unique_value_data not in i:
            s += ',' + i
    s = headers + s
    BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=s.strip(','))


def update_item_2dot_data(table, key, where, meaning, item, where_data = 0, meaning_data = '0', change_index=0):
    get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table).strip(',')
    l = get_data.split(',')
    s = ''
    for i in l:
        i = i.split(':')
        if i[where_data] == meaning_data:
            i[change_index] = item
        s += ',' + ':'.join(i)
    BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=s.strip(','))


def add_header_2dot_data(table, key, where, meaning, name_new_header):
    get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table).strip(',')
    l = get_data.split(',')
    l_new = []
    l_new.append(l[0] + ':' + name_new_header)
    for i in l[1:]:
        l_new.append(i + ':0')
    BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=','.join(l_new))


def delete_header_2dot_data(table, key, where, meaning, name_header):
    try:
        get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table).strip(',')
        l: list = get_data.split(',')
        ind = l[0].split(':').index(name_header)
    except Exception as e:
        return print('????????????!\n??????????????: delete_header_2dot_data') 
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
    '''?????????????? ?????? ???????????????? ???????????????????????? ???????????? ??????????'''
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

def error_reg(state=False):      
    def wrapper1(func):
        if state:
            async def wrapper2(message: types.Message, state: FSMContext):
                if check_emptys(message.from_user.id):
                    clean_error_reg_company(message.from_user.id)
                    text1 = get_text('exist_user1', format=False)
                    await message.answer(text1, reply_markup=ReplyKeyboardRemove())  
                else:
                    return await func(message, state)
        else:
            async def wrapper2(message: types.Message):
                if check_emptys(message.from_user.id):
                    clean_error_reg_company(message.from_user.id)
                    text1 = get_text('exist_user1', format=False)
                    await message.answer(text1, reply_markup=ReplyKeyboardRemove())  
                else:
                    return await func(message)
        return wrapper2
    return wrapper1

def error_reg_call(state=False):
    def wrapper1(func):
        if state:
            async def wrapper2(call: CallbackQuery, state: FSMContext):
                if check_emptys(call.from_user.id):
                    clean_error_reg_company(call.from_user.id)
                    text1 = get_text('exist_user1', format=False)
                    await bot.send_message(text1, reply_markup=ReplyKeyboardRemove())  
                else:
                    return await func(call, state)
        else:
            async def wrapper2(call: CallbackQuery):
                if check_emptys(call.from_user.id):
                    clean_error_reg_company(call.from_user.id)
                    text1 = get_text('exist_user1', format=False)
                    await bot.send_message(text1, reply_markup=ReplyKeyboardRemove())  
                else:
                    return await func(call)
        return wrapper2
    return wrapper1

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
    nickname = re.sub('[^\x00-\x7F??-????-??????]', '', nickname)
    return nickname

def check_on_simbols(nickname):
    try:
        nickname1 = re.findall("[!\"#$%&'()*+,./\\\:;<=>?@[\]^`{|}~]", nickname)
        nickname2 = re.findall('[^\x00-\x7F??-????-??????]', nickname)
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

def i_have_stocks(id_user: int) -> bool:
    try:
        parse_2dot_data(table='users', key='briefcase', where='id_user', meaning=id_user)[1]
        return True
    except:
        return False

def get_quantity_stocks_currently(id_stocks: int) -> int:
    data = BotDB.get_alls(keys='seller, id_stocks, quantity_stocks', table='stocks')
    return int([i[2] for i in data if i[0] == i[1]][0])


def stocks_exist(id_company: int) -> bool:
    if int(BotDB.get(key='count_make_stocks', where='id_user', meaning=id_company)) == 0:
        return False
    return True

def get_your_stocks(id_user):
    t = ''
    number_string = 1
    parse = parse_2dot_data(table='users', key='briefcase', where='id_user', meaning=id_user)[1:]
    for x in parse:
        d = {
            'id_slot': shell_num(x[0], signs=False),
            'number_string': number_string,
            'name_company':x[2],
            'quantity_stocks':shell_num(x[3]),
            'price_buy': shell_num(x[4])
        }
        t += get_text('template_string_my_stocks', format=True, d=d)
        number_string += 1
    return t

def update_rating_stocks(id_slot):
    rating = 0 
    for i in BotDB.get_all(key='id_user'):
        try:
            parse = parse_2dot_data(table='users', key='briefcase', where='id_user', meaning=i)[1:]
            for x in parse:
                if id_slot in x:
                    rating += 1
        except Exception as e:
            pass
    BotDB.updateN(key='rating', where='id_slot', meaning=id_slot, table='stocks', num=rating)

def list_stocks(page=1):
    t = ''
    data = [i for i in BotDB.get_alls_with_order('id_slot, id_stocks, quantity_stocks, price_one_stock, percent_of_income, seller', order='rating', table='stocks') if i[1] > 0]
    count_string = BotDB.vCollector(where='name', meaning='count_string_in_one_page_stocks', table='value_main')
    for i in list(data):
        if (len(data) / count_string) >= 1:
            if (page-1) * count_string <= data.index(i) < page * count_string:
                quantity_stocks = BotDB.get(key='count_make_stocks', where='id_user', meaning=i[1])
                percent = round(float((i[4]/quantity_stocks) * 100), 6)
                signs = len(str(percent).strip('0').split('.')[1])
                type_of_a = BotDB.get(key='type_of_activity', where='id_user', meaning=i[1])
                d = {
                    'id_slot': shell_num(i[0], signs=False),
                    'name_seller': BotDB.get(key='nickname', where='id_user', meaning=i[-1]),
                    'quantity_stocks': shell_num(i[2]),
                    'price_one_stock': shell_num(i[3]),
                    'percent': shell_num(percent, q_signs_after_comma=signs),
                    'name_company': BotDB.get(key='name_company', where='id_company', meaning=i[1], table=type_of_a)
                    }
                t += get_text('template_one_string_stocks', format=True, d=d) if i[-1] == i[1] else get_text('template_one_string_sell_stocks', format=True, d=d)
        else:
            print(5)
            percent = round(float((i[4]/i[2]) * 100), 6)
            signs = len(str(percent).strip('0').split('.')[1])
            type_of_a = BotDB.get(key='type_of_activity', where='id_user', meaning=i[1])
            d = {
                'id_slot': shell_num(i[0], signs=False),
                'name_seller': BotDB.get(key='nickname', where='id_user', meaning=i[-1]),
                'quantity_stocks': shell_num(i[2]),
                'price_one_stock': shell_num(i[3]),
                'percent': shell_num(percent, q_signs_after_comma=signs),
                'name_company': BotDB.get(key='name_company', where='id_company', meaning=i[1], table=type_of_a)
                }
            t += get_text('template_one_string_stocks', format=True, d=d) if i[-1] == i[1] else get_text('template_one_string_sell_stocks', format=True, d=d)

    return t.strip('\n')

# #########################################

def available(id_user: int, price_item: Union[int, float], currency: str ='rub'):
    quantity_money = BotDB.get(key=currency, where='id_user', meaning=id_user)
    quantity_available = quantity_money // price_item
    return quantity_available
# #########################################

def shell_num(num: Union[int, float], q_signs_after_comma: int = 2, signs: bool =True) -> str:
    if signs:
        num = round(num, q_signs_after_comma)
        if isfloat(str(num)):
            if float(num) % 1 != 0:
                return '<code>{:,.{}f}</code>'.format(float(num), q_signs_after_comma) 
        return '<code>{:,}</code>'.format(int(num))
    return '<code>{}</code>'.format(num)

def cleannum(numb: str) -> str:
    numb = re.sub("[!\"#$%&'()*+,/\\\:;<=>?@[\]^`{|}~]", '', numb)
    numb = re.sub('[^\x00-\x7F]', '', numb)
    numb = re.sub('[??-????-??????]', '', numb)
    numb = re.sub('[A-Za-z]', '', numb)
    clean_num = re.findall("^[-+]?[0-9]*[.,]?[0-9]+(?:[eE][-+]?[0-9]+)?$", numb)
    try:
        return clean_num[0]
    except: return ' ' 


def currency_calculation(money: Union[int, float], what_calculate: str ='rub_in_usd', currency: str ='rate_usd') -> Tuple[float, float]:
    '''???????????????????????? ????????????'''
    rate = BotDB.vCollector(table='value_main', where='name', meaning=currency)
    if what_calculate == 'rub_in_usd':
        result = round(money / rate, 2)
    elif what_calculate == 'usd_in_btc':
        result = round(money / rate, 5)
    elif what_calculate == 'usd_in_rub':
        result = round(money * rate, 2)
    elif what_calculate == 'btc_in_usd':
        result = round(money * rate, 2)
    return result, rate

# #########################################

def isfloat(num: str) -> bool:
    if num.isdigit():
        return False
    else:
        try:
            float(num)
            return True
        except:
            return False


# #########################################

def check_graf_rate(dimension):
    '''?????????????????? ??????-???? ?????????????? ???????????? usd and btc ?? ????, ???????? ?????? ?????????????????? ???????????????????????? ??????????????????????, ?????????? ?????????? ???????????? ???????????? ??????????????????'''
    result_usd, result_btc = BotDB.get_all('id','graf_rate_usd'), BotDB.get_all('id','graf_rate_btc')
    if len(result_usd) > dimension:
        BotDB.delete('id', result_usd[0], 'graf_rate_usd')
    elif len(result_btc) > dimension:
        BotDB.delete('id', result_btc[0], 'graf_rate_btc')


def update_carrency_influence(random_percent_usd=0, random_percent_btc=0):
    sum_percent_decimal_usd = 0
    sum_percent_decimal_btc = 0
    users_id= BotDB.get_all(key='id_user')
    rate_usd = BotDB.vCollector(table='value_main', where='name', meaning='rate_usd')
    rate_btc = BotDB.vCollector(table='value_main', where='name', meaning='rate_btc')
    for i in users_id:
        for j in parse_2dot_data(table='users', key='average_percent_influences', where='id_user', meaning=i)[1:]:
            try:
                j[3]
            except:
                break
            if j[2] == 0:
                delete_2dot_data(table='users', key='average_percent_influences', where='id_user', meaning=i, unique_value_data=j[0])
                continue
            elif j[1] == 'rate_usd':
                sum_percent_decimal_usd += j[3]
                add_2dot_data(table='users', key='average_percent_influences', where='id_user', meaning=i, meaning_data=str(j[0]), add_data='min', add=-1)
                continue
            sum_percent_decimal_btc += j[3]
            add_2dot_data(table='users', key='average_percent_influences', where='id_user', meaning=i, meaning_data=str(j[0]), add_data='min', add=-1)

    usd = (1 + random_percent_usd + sum_percent_decimal_usd) * rate_usd  #???????????????????????? ???????? ???????????????? ????????????????
    btc = (1 + random_percent_btc + sum_percent_decimal_btc) * rate_btc 
    d = {'rate_usd': [usd, random_percent_usd + sum_percent_decimal_usd, rate_usd], 'rate_btc': [btc, random_percent_btc + sum_percent_decimal_btc, rate_btc]}
    for i in d: 
        BotDB.updateN(table='value_main', key='main_num', where='name', meaning=i, num=round(d[i][0], 2))
        tag = taG(len=12)
        BotDB.updateT(key='text_box2', where='name', meaning=f'{i}_unique_id', text=tag, table='value_main')
        sum_percent_decimal = d[i][1]
        rate = d[i][2]
        
        _ = i.split('_')[1]

        type_rate_now_text = i + '_now' #???????????????????? ???????????? ?????? ???????????? ?????? ?????????????????? ?? ????
        type_percent_text = 'perc_' + _
        type_graf_rate_text = 'graf_rate_' + _
        

        date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
        percent_to_text = f"{sum_percent_decimal * 100}"
        
        BotDB.cur.execute(f'INSERT INTO "{type_graf_rate_text}" (id, time_update, {i}, {type_percent_text}, {type_rate_now_text}) VALUES (?,?,?,?,?)',(tag, date, rate, percent_to_text, round(d[i][0], 2)))
        BotDB.conn.commit() 
    dimension_graf_rate = BotDB.vCollector(table='value_main', where='name', meaning='dimension_graf_rate')  
    check_graf_rate(dimension_graf_rate)


def exchange_balans(id_user: int, count_money: Union[int, float], type_currency: str ='rate_usd'):
    dimension_graf_rate = BotDB.vCollector(table='value_main', where='name', meaning='dimension_graf_rate') #?????????????????????? ???????????? ?????? ??????????????
    
    abs_money = abs(count_money) #?????????? ???? ???????????? ???????? ????????????
    
    ratio = BotDB.vCollector(table='value_main', where='name', meaning=f'ratio_exchange')  #?????????????????????? ???????????????? ?????????????????? ??????????
    all_money_people = BotDB.get_all(type_currency.split('_')[1]) #???????????????? ?????? ?????????????????? ???????????? ?????????????????? ???????? ???? ???????? ????????????
    
    if count_money > 0:
        percent_decimal = round((abs_money / (sum(all_money_people) + abs_money)) / ratio, 6) #???????????????? ???????????????????? ??????????????, ?????????????? = ????????_???????????? / ????????????_???????? + ????????_???????????? / ?????????????????????? ???????????????? ?????????????????? ??????????
        if percent_decimal != 0:
            create_2dot_data(table='users', key='average_percent_influences', where='id_user', meaning=id_user, d=[taG(), type_currency, 15, percent_decimal]) #???????????????????? ???? ?? ???? 
            update_carrency_influence()
    else:
        percent_decimal = round((abs_money / (sum(all_money_people) + abs_money)) / ratio, 6)
        if percent_decimal != 0:
            create_2dot_data(table='users', key='average_percent_influences', where='id_user', meaning=id_user, d=[taG(), type_currency, 15, -percent_decimal]) #???????????????????? ???? ?? ???? 
    check_graf_rate(dimension_graf_rate)


def rate_currency():
    dimension_graf_rate = BotDB.vCollector(table='value_main', where='name', meaning='dimension_graf_rate')

    random_perc_usd = round(random.uniform(-1, 1), 2) / 100
    random_perc_btc = round(random.uniform(-1, 1), 2) / 100
    update_carrency_influence(random_perc_usd, random_perc_btc)

    check_graf_rate(dimension_graf_rate)

# #########################################

def taG(len=10):
    tagg = ''
    all = string.digits + string.ascii_letters
    for i in range(0, len):
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


async def verify():
    data = BotDB.get_alls('id_user, referrer, count_tap, date_reg, verify')
    for i in data:
        verife_date = datetime.datetime.today() > datetime.datetime.strptime(i[3], '%H:%M:%S %m/%d/%Y') + datetime.timedelta(days=3)
        if i[1] != 0 and i[2] >= 50 and verife_date and i[4] == 0:
            award_referral = BotDB.vCollector(table='value_main', where='name', meaning='award_referral')
            award_referrer = BotDB.vCollector(table='value_main', where='name', meaning='award_referrer')
            # ?????????????????? ???????????? ??????????????????????
            BotDB.updateN(key='verify', where='id_user', meaning=i[0], num=1)
            # ???????????????????? ?????????????????? ???????????????????????? ?? ??????, ?????? ???? ???????????? ?????????????????????? ??????????????
            await bot.send_message(i[0], get_text('verify_??referral', format=False))
            # ?????????????????? ?????????? ???? ?????????????????????????? ???????????? ?????????????????????? ??????????????????
            BotDB.add(key='usd', where='id_user', meaning=i[0], num=award_referral)
            # ???????????????????? ?????????????????? ????????????????, ?????????????? ???????????? ???????????? 
            await bot.send_message(i[1], get_text('verify_referrer', format=False))
            # ?????????????????? ?????????? ?????????????? ???? ?????????????????????????? ???????????? ?????????????????????? ?? ??????????????????
            BotDB.add(key='usd', where='id_user', meaning=i[1], num=award_referrer)
