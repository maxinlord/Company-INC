import datetime
from decimal import Decimal
import random
import re
import string
import time
import types
from typing import List, Tuple, Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import ReplyKeyboardRemove

from all_states import Ban_User, Tech_Break
from dispatcher import bot, BotDB


# #########################################

def check_name_app(name_app):
    return name_app in BotDB.get_all('name_app', table='dev_software_apps')


# #########################################

def get_date_now(ymd=True, h=True, m=True, s=True, sep1=':', sep2='/'):
    result = ''
    if h:
        result += '%H:'
    if m:
        result += '%M:'
    if s:
        result += '%S'
    result = result.strip(':').replace(':', sep1)
    if ymd:
        result += ' %m/%d/%Y'.replace('/', sep2)
    return str(datetime.datetime.now().strftime(result.strip(' ')))

# #########################################

def get_weight(id_user, name_weight):
    ratio = get_2dot_data(table='weights', key='user_weights', where='id_user', meaning=id_user,
                          where_data='name_weight', meaning_data=name_weight, get_data='wRatio')
    plus = get_2dot_data(table='weights', key='user_weights', where='id_user', meaning=id_user,
                         where_data='name_weight', meaning_data=name_weight, get_data='wPlus')
    return (ratio, plus) if ratio else (1, 0)


# ########################################

def one_pay_app(id_company):
    all_mark = 0
    total_income = 0
    all_dev = quantity_devs_company(id_company)
    device_k = create_mat_percents(id_company)
    data_centre_h, data_centre_f = [
        get_2dot_data(table='dev_software', key='data_centre', where='id_company', meaning=id_company, meaning_data='1',
                      get_data=i) for i in ['home', 'foreign']]
    d = {'percent_datacentre_home_infinitypay': data_centre_h,
         'percent_datacentre_foreign_infinitypay': data_centre_f}
    percent_h, percent_f = [
        BotDB.vCollector(wNum=get_weight(id_company, i), table='value_it', where='name', meaning=i) * d[i] for i in d]

    for j in range(1, 3 + 1):
        quantity_dev = BotDB.get(
            key=f'quantity_dev_{j}', where='id_company', meaning=id_company, table='dev_software')
        all_mark += quantity_dev * j
        for i in count_percent_device(device_k, id_company, viev=False):
            income_dev = BotDB.vCollector(wNum=get_weight(id_company, f'income_dev_{j}'), table='value_it',
                                          where='name', meaning=f'income_dev_{j}')
            total_income += (((1 + i['percent']) * income_dev) * (1 + percent_f + percent_h)) * i[
                'quantity_same_percent'] if i['dev'] == j else 0

    percent_left = BotDB.vCollector(wNum=get_weight(id_company, 'percent_one_pay_left'), table='value_it', where='name',
                                    meaning='percent_one_pay_left')
    percent_right = BotDB.vCollector(wNum=get_weight(id_company, 'percent_one_pay_right'), table='value_it',
                                     where='name', meaning='percent_one_pay_right')
    true_perc = percent_right - percent_left
    average_mark = all_mark / all_dev
    x_perc = round(true_perc * average_mark / 3, 2)
    x_income = round((total_income * 60) * (percent_left + x_perc), 2)

    return x_income


def infinity_income_app(id_company):
    total_income = 0
    all_dev = quantity_devs_company(id_company)
    device_k = create_mat_percents(id_company)
    data_centre_h, data_centre_f = [
        get_2dot_data(table='dev_software', key='data_centre', where='id_company', meaning=id_company, meaning_data='1',
                      get_data=i) for i in ['home', 'foreign']]
    d = {'percent_datacentre_home_infinitypay': data_centre_h,
         'percent_datacentre_foreign_infinitypay': data_centre_f}
    percent_h, percent_f = [
        BotDB.vCollector(wNum=get_weight(id_company, i), table='value_it', where='name', meaning=i) * d[i] for i in d]

    print(count_percent_device(device_k, id_company, viev=False))

    for j in range(1, 3 + 1):
        for i in count_percent_device(device_k, id_company, viev=False):
            income_dev = BotDB.vCollector(wNum=get_weight(id_company, f'income_dev_{j}'), table='value_it',
                                          where='name', meaning=f'income_dev_{j}')
            total_income += (((1 + i['percent']) * income_dev) * (1 + percent_f + percent_h)) * i[
                'quantity_same_percent'] if i['dev'] == j else 0

    average_income = round(total_income / all_dev, 2)

    return average_income


def time_for_build(id_company):  # sourcery skip: avoid-builtin-shadow
    min = sum(
        [BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software') * (4 - i) for
         i in range(1, 3 + 1)])

    base_time = BotDB.vCollector(wNum=get_weight(id_company, 'base_time_build_app'), table='value_it', where='name',
                                 meaning='base_time_build_app')
    time_build = base_time + min

    return time_build


# #########################################

def your_app_top(id_company):
    number_string = 1
    data = BotDB.get_alls_with_order(keys='id_company, name_app, one_pay, income', order='one_pay',
                                     table='dev_software_apps')
    for i in data:
        indx = data.index(i) + 1 if i[0] == id_company else 0
        if indx > BotDB.vCollector(wNum=get_weight(id_company, 'quantity_top_apps'), where='name',
                                   meaning='quantity_top_apps', table='value_it'):
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
    for i in BotDB.get_alls_with_order(keys='id_company, name_app, one_pay, income', order='one_pay',
                                       table='dev_software_apps'):
        if number_string > BotDB.vCollector(wNum=get_weight(id_company, 'quantity_top_apps'), where='name',
                                            meaning='quantity_top_apps', table='value_it'):
            break
        d = {
            'number_string': number_string,
            'name_app': i[1],
            'one_pay': shell_num(i[2]),
            'income': shell_num(i[3])
        }
        t += get_text('template_string_my_app', format=True, d=d) if i[0] == id_company else get_text(
            'template_string_app', format=True, d=d)
        number_string += 1
    return t


def list_my_top_apps(id_company):
    number_string = 1
    t = ''
    for i in BotDB.get_alls_with_order(keys='id_company, name_app, one_pay, income', order='one_pay',
                                       table='dev_software_apps'):
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
    for i in BotDB.get_alls_with_order(keys='id_company, done, income, quantity_min_build, date_reg', order='done',
                                       table='dev_software_apps'):
        all_income_apps += i[2] if i[0] == id_company and i[1] == 1 else 0
        quantity_apps += 1 if i[0] == id_company and i[1] == 1 else 0
        if i[1] == 0 and i[0] == id_company:
            date_reg = i[4]
            date_formatter = '%X %m/%d/%Y'
            future = datetime.datetime.strptime(
                date_reg, date_formatter) + datetime.timedelta(minutes=i[3])
            x = str(future - datetime.datetime.now()).split('.')[0]
            d = {'time_left': x}
            time_left = get_text('time_left_for_build_app', format=True, d=d)
    d = {
        'all_income_apps': shell_num(all_income_apps),
        'time_left': time_left,
        'quantity_apps': quantity_apps
    }
    return d

# #########################################


def check_apps_done():
    for i in BotDB.get_alls_with_order(keys='id_company, done, date_reg, quantity_min_build', order='done',
                                       table='dev_software_apps'):
        if i[1] == 1:
            continue
        date_reg = i[2]
        date_formatter = '%X %m/%d/%Y'
        future = datetime.datetime.strptime(
            date_reg, date_formatter) + datetime.timedelta(minutes=i[3])
        if datetime.datetime.now() >= future:
            BotDB.updateN(key='done', where='id_company',
                          meaning=i[0], num=1, table='dev_software_apps')


# #########################################

def calculate_pay_dev(quantity: int, salary_hour: Union[int, float]):
    # sourcery skip: avoid-builtin-shadow
    min = int(time.strftime('%M'))
    min_job = 60 - min
    first_salary = round((min_job * salary_hour / 60) * quantity, 2)
    return first_salary, min_job


def calculate_pay_rent(quantity: int, cost_rent_day: Union[int, float]) -> Tuple[Union[int, float], int, int]:
    day, month, year = time.strftime(
        '%d'), time.strftime('%m'), time.strftime('%Y')
    day = int(time.strftime('%d')) + 1 if datetime.datetime.strptime(f'19:00:00 {month}/{day}/{year}', '%H:%M:%S %m/%d/%Y') < datetime.datetime.now() else time.strftime('%d')

    t = datetime.datetime.strptime(f'19:00:00 {month}/{day}/{year}', '%H:%M:%S %m/%d/%Y') - datetime.datetime.now()

    min_rent = t.seconds // 60
    hours = min_rent // 60
    mins = 0 if min_rent % 60 == 59 else min_rent % 60 + 1
    first_salary = round((min_rent * cost_rent_day / (24 * 60)) * quantity, 2)
    return first_salary, hours, mins


# #########################################

def quantity_place_company(id_company):
    i = 1
    y = True
    places = 0
    while y:
        p = parse_2dot_data(
            key=f'quantity_office_{i}', where='id_company', meaning=id_company, table='dev_software')
        places += (p[1][1] + p[1][2]) * BotDB.vCollector(wNum=get_weight(id_company, f'size_office_{i}'), where='name',
                                                         meaning=f'size_office_{i}', table='value_it')
        i += 1
        try:
            BotDB.vCollector(wNum=get_weight(id_company, f'cost_office_{i}'), where='name', meaning=f'cost_office_{i}',
                             table='value_it')
        except:
            y = False
    return places


def quantity_devs_company(id_company):
    return sum(BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software') for i in range(1, 3 + 1))


def quantity_devices(id_company):
    i = 1
    ind = 1
    q_devices = 0
    y = True
    while y:
        data = parse_2dot_data(key=f'quantity_device_{ind}', where='id_company', meaning=id_company,
                               table='dev_software')
        ind_q = data[0].index('quantity')
        for i in data[1:]:
            q_devices += i[ind_q]
        try:
            ind += 1
            BotDB.get(table='dev_software',
                      key=f'quantity_device_{ind}', where='id_company', meaning=id_company)
        except:
            y = False
    return q_devices


def create_mat_percents(id_company):
    i = 1
    ind = 1
    y = True
    devices_k = []
    while y:
        q_device = parse_2dot_data(key=f'quantity_device_{ind}', where='id_company', meaning=id_company,
                                   table='dev_software')[1:]
        q_devs = [BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software') for i
                  in range(1, 3 + 1)]
        for i in q_device:
            s = []
            true_q_device = i[1]
            if i[0] > 1:
                u = sum(q_device[t - 1][1] for t in range(1, i[0]))
                s = [0] * u + s
            elif i[1] == 0:
                continue
            for j in q_devs:
                if j == 0:
                    continue
                elif i[1] >= j:
                    s += [1] * j
                    i[1] = i[1] - j
                    q_devs[q_devs.index(j)] = 0
                elif i[1] <= j:
                    s += [1] * i[1]
                    i[1] = 0
                    q_devs[q_devs.index(j)] = j - i[1]
                    s += [0] * (quantity_devs_company(id_company) - len(s))
                    break
            i[1] = true_q_device
            devices_k.append([f'{ind}_{i[0]}'] + s)
        try:
            ind += 1
            BotDB.get(table='dev_software',
                      key=f'quantity_device_{ind}', where='id_company', meaning=id_company)
        except:
            y = False
    # pprint(devices_k, width=300)
    return devices_k


def count_percent_device(device_k, id_company, viev=True):
    # sourcery skip: avoid-builtin-shadow
    q_devs = [BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software') for i in
              range(1, 3 + 1)]
    dev_name = ['junior', 'middle', 'senior']
    percents = []
    for i in range(1, quantity_devs_company(id_company) + 1):
        percent = sum(BotDB.vCollector(wNum=get_weight(
            id_company, f'percent_device_{device_k[x][0]}'), where='name', meaning=f'percent_device_{device_k[x][0]}', table='value_it') for x in range(len(device_k)) if device_k[x][i] == 1)

        percents.append(round(percent, 2))
    text = ''
    l = []
    u = 0
    for i in enumerate(q_devs):
        slice = percents[u:i[1] + u]
        for j in sorted(list(set(percents[u:i[1] + u])), reverse=False):
            d = {
                'dev': dev_name[i[0]],
                'quantity_same_percent': slice.count(j),
                'percent': shell_num(j * 100)
            }
            if viev:
                text += get_text('template_string_count_percent_device',
                                 format=True, d=d)
            else:
                d = {
                    'dev': i[0] + 1,
                    'quantity_same_percent': slice.count(j),
                    'percent': j
                }
                l.append(d)
        u += i[1]
    return text if viev else l


# #########################################

def app_build(id_company: int) -> Tuple[bool, str]:
    for i in BotDB.get_alls(keys='done, id_company, name_app', table='dev_software_apps'):
        if i[0] == 0 and i[1] == id_company:
            return True, i[2]
    return False, '-'


# #########################################

def get_button(unique_number, d=None, format=False) -> str:
    if d is None:
        d = {}
    mode = BotDB.get(key='text_box1', where='name',
                     meaning='program_mode_for_text', table='value_main')
    try:
        text = BotDB.get(key='name', where='number',
                         meaning=unique_number, table='button_name')
    except:
        BotDB.add_new_button(unique_number)
        text = BotDB.get(key='name', where='name',
                         meaning=unique_number, table='button_name')
    text_true = text.format(**d) if format else text
    return f'({unique_number})\n\n{text_true}' if mode == 'on' else text_true


def get_text(unique_name, d=None, format=True) -> str:
    if d is None:
        d = {}
    mode = BotDB.get(key='text_box1', where='name',
                     meaning='program_mode_for_text', table='value_main')
    try:
        text = BotDB.get(key='text_box1', where='name',
                         meaning=unique_name, table='texts')
    except:
        BotDB.add_new_text(name=unique_name)
        text = BotDB.get(key='text_box1', where='name',
                         meaning=unique_name, table='texts')
    text_true = text.format(**d) if format else text
    return f'({unique_name})\n\n{text_true}' if mode == 'on' else text_true


def get_photo(unique_name) -> str:
    try:
        photo = BotDB.get(key='photo_id', where='name',
                          meaning=unique_name, table='photos')
    except:
        photo = BotDB.get(key='photo_id', where='name',
                          meaning='without_photo', table='photos')
    return photo


# #########################################

def create_2dot_data(table, key, where, meaning, d=None):
    if d is None:
        d = []
    get_data = BotDB.get(key=key, where=where,
                         meaning=meaning, table=table).strip(',')
    s = ',' + ':'.join(list(map(lambda x: str(x), d)))
    adding = get_data + s
    BotDB.updateT(key=key, where=where, meaning=meaning,
                  table=table, text=adding)


def parse_2dot_data(table, key, where, meaning) -> List[list]:
    get_data = BotDB.get(key=key, where=where,
                         meaning=meaning, table=table).strip(',')
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
        return
    for i in parse[1:]:
        if str(i[ind]) == meaning_data:
            return i[ind_get]


def add_2dot_data(table, key, where, meaning, add, where_data: str = 'id', add_data: str = 'id',
                  meaning_data: str = '0'):
    try:
        parse = parse_2dot_data(key=key, where=where,
                                meaning=meaning, table=table)
        ind = parse[0].index(where_data)
        ind_add = parse[0].index(add_data)
    except Exception as e:
        return
    s = ':'.join(parse[0])
    for i in parse[1:]:
        if str(i[ind]) == meaning_data:
            i[ind_add] = round(
                i[ind_add] + add, 2) if isfloat(str(i[ind_add])) else i[ind_add] + add
        s += ',' + ':'.join(list(map(lambda x: str(x), i)))
    BotDB.updateT(key=key, where=where, meaning=meaning,
                  table=table, text=s.strip(','))


def delete_2dot_data(table, key, where, meaning, unique_value_data):
    get_data = BotDB.get(key=key, where=where,
                         meaning=meaning, table=table).strip(',')
    l = get_data.split(',')
    headers = l[0]
    s = ''.join(f',{i}' for i in l[1:] if unique_value_data not in i)
    s = headers + s
    BotDB.updateT(key=key, where=where, meaning=meaning,
                  table=table, text=s.strip(','))


def update_2dot_data(table, key, where, meaning, num, where_data='id', meaning_data='0', update_data='id'):
    try:
        parse = parse_2dot_data(key=key, where=where,
                                meaning=meaning, table=table)
        ind = parse[0].index(where_data)
        ind_update = parse[0].index(update_data)
    except Exception as e:
        return
    s = ':'.join(parse[0])
    for i in parse[1:]:
        if str(i[ind]) == meaning_data:
            i[ind_update] = num
        s += ',' + ':'.join(list(map(lambda x: str(x), i)))
    BotDB.updateT(key=key, where=where, meaning=meaning,
                  table=table, text=s.strip(','))


def add_header_2dot_data(table, key, where, meaning, name_new_header, ):
    get_data = BotDB.get(key=key, where=where,
                         meaning=meaning, table=table).strip(',')
    l = get_data.split(',')
    l_new = [f'{l[0]}:{name_new_header}']
    l_new.extend(f'{i}:0' for i in l[1:])
    BotDB.updateT(key=key, where=where, meaning=meaning,
                  table=table, text=','.join(l_new))


def delete_header_2dot_data(table, key, where, meaning, name_header):
    try:
        get_data = BotDB.get(key=key, where=where,
                             meaning=meaning, table=table).strip(',')
        l: list = get_data.split(',')
        ind = l[0].split(':').index(name_header)
    except Exception as e:
        return
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
    BotDB.updateT(key=key, where=where, meaning=meaning,
                  table=table, text=','.join(l_new))


# #########################################

def referrer_linc(id_user, bot_name='company_inc_game_bot'):
    '''Функция для создания реферральной ссылки юзера'''
    return f'http://t.me/{bot_name}?start={id_user}'


# #########################################

def last_tap(button='-', state=False):
    def actual_dec(func):
        if state:
            async def wrapper(message: types.Message, state: FSMContext):
                try:
                    if message.from_user.username != BotDB.get(key='username', where='id_user',
                                                               meaning=message.from_user.id):
                        BotDB.updateT(key='username', where='id_user',
                                      meaning=message.from_user.id, text=f'@{message.from_user.username}')

                    date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
                    BotDB.updateT(key='last_tap', where='id_user',
                                  meaning=message.from_user.id, text=date)
                    BotDB.add(key='count_tap', where='id_user',
                              meaning=message.from_user.id, num=1)
                except:
                    pass
                BotDB.add(table='click_button', key='amount_click',
                          where='button', meaning=button, num=1)
                return await func(message, state)

        else:
            async def wrapper(message: types.Message):
                try:
                    if message.from_user.username != BotDB.get(key='username', where='id_user',
                                                               meaning=message.from_user.id):
                        BotDB.updateT(key='username', where='id_user',
                                      meaning=message.from_user.id, text=f'@{message.from_user.username}')

                    date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
                    BotDB.updateT(key='last_tap', where='id_user',
                                  meaning=message.from_user.id, text=date)
                    BotDB.add(key='count_tap', where='id_user',
                              meaning=message.from_user.id, num=1)
                except:
                    pass
                BotDB.add(table='click_button', key='amount_click',
                          where='button', meaning=button, num=1)
                return await func(message)

        return wrapper

    return actual_dec


def last_tap_call(button='-', state=False):
    def actual_dec(func):
        if state:
            async def wrapper(call: CallbackQuery, state: FSMContext):
                try:
                    if call.from_user.username != BotDB.get(key='username', where='id_user', meaning=call.from_user.id):
                        BotDB.updateT(key='username', where='id_user', meaning=call.from_user.id, text=f'@{call.from_user.username}')

                    date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
                    BotDB.updateT(key='last_tap', where='id_user',
                                  meaning=call.from_user.id, text=date)
                    BotDB.add(key='count_tap', where='id_user',
                              meaning=call.from_user.id, num=1)
                except:
                    pass
                BotDB.add(table='click_button', key='amount_click',
                          where='button', meaning=button, num=1)
                return await func(call, state)

        else:
            async def wrapper(call: CallbackQuery):
                try:
                    if call.from_user.username != BotDB.get(key='username', where='id_user', meaning=call.from_user.id):
                        BotDB.updateT(key='username', where='id_user', meaning=call.from_user.id, text=f'@{call.from_user.username}')

                    date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
                    BotDB.updateT(key='last_tap', where='id_user',
                                  meaning=call.from_user.id, text=date)
                    BotDB.add(key='count_tap', where='id_user',
                              meaning=call.from_user.id, num=1)
                except:
                    pass
                BotDB.add(table='click_button', key='amount_click',
                          where='button', meaning=button, num=1)

                return await func(call)

        return wrapper

    return actual_dec


# #########################################

def clean_error_reg_company(id_user):
    # all_table=['dev_software','dev_game','farming','clothing_and_shoes','car_production','phone_production',
    # 'creating_food','restaurant','beauty_salon','tss','law_agency','private_clinic','fuel_production','oil_production']
    try:
        BotDB.delete(where='id_company', meaning=id_user,
                     table=BotDB.get(key='type_of_activity', where='id_user', meaning=id_user))
    except Exception as e:
        print(e)


def check_emptys(id_user):
    try:
        answ = BotDB.get(key='nickname', where='id_user', meaning=id_user) is None or BotDB.get(key='type_of_activity', where='id_user', meaning=id_user) is None or BotDB.get(
            key='name_company', where='id_company', meaning=id_user, table=BotDB.get(key='type_of_activity', where='id_user', meaning=id_user)) is None

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
                    mes = BotDB.get(key='message_why', where='id_user', meaning=message.from_user.id,
                                    table='black_list')
                    await message.answer(get_text('ban_wrapper', format=True, d={'message_why': mes}),
                                         reply_markup=ReplyKeyboardRemove())
                    await Ban_User.Q1.set()
                else:
                    return await func(message, state)
        else:
            async def wrapper(message: types.Message):
                if message.from_user.id in BotDB.get_all(key='id_user', table='black_list'):
                    mes = BotDB.get(key='message_why', where='id_user', meaning=message.from_user.id,
                                    table='black_list')
                    await message.answer(get_text('ban_wrapper', format=True, d={'message_why': mes}),
                                         reply_markup=ReplyKeyboardRemove())
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
                    mes = BotDB.get(key='message_why', where='id_user',
                                    meaning=call.from_user.id, table='black_list')
                    await bot.send_message(call.from_user.id,
                                           get_text('ban_wrapper', format=True, d={
                                                    'message_why': mes}),
                                           reply_markup=ReplyKeyboardRemove())
                    await Ban_User.Q1.set()
                else:
                    return await func(call, state)
        else:
            async def wrapper(call: CallbackQuery):
                if call.from_user.id in BotDB.get_all(key='id_user', table='black_list'):
                    mes = BotDB.get(key='message_why', where='id_user',
                                    meaning=call.from_user.id, table='black_list')
                    await bot.send_message(call.from_user.id,
                                           get_text('ban_wrapper', format=True, d={
                                                    'message_why': mes}),
                                           reply_markup=ReplyKeyboardRemove())
                    await Ban_User.Q1.set()
                else:
                    return await func(call)
        return wrapper

    return actdec

# #########################################


def tech_break(state=False):
    def actdec(func):
        if state:
            async def wrapper(message: types.Message, state: FSMContext):
                if BotDB.get(key='text_box1', where='name', meaning='tech_break', table='value_main') == 'off' or \
                        message.from_user.id == 474701274:
                    return await func(message, state)
                await message.answer(get_text('tech_break', format=False), reply_markup=ReplyKeyboardRemove())
                await Tech_Break.Q1.set()
        else:
            async def wrapper(message: types.Message):
                if BotDB.get(key='text_box1', where='name', meaning='tech_break', table='value_main') == 'off' or \
                        message.from_user.id == 474701274:
                    return await func(message)
                await message.answer(get_text('tech_break', format=False), reply_markup=ReplyKeyboardRemove())
                await Tech_Break.Q1.set()
        return wrapper

    return actdec


def tech_break_call(state=False):
    def actdec(func):
        if state:
            async def wrapper(call: CallbackQuery, state: FSMContext):
                if BotDB.get(key='text_box1', where='name', meaning='tech_break', table='value_main') == 'off' or \
                        call.from_user.id == 474701274:
                    return await func(call, state)
                await call.answer(get_text('tech_break', format=False), reply_markup=ReplyKeyboardRemove())
                await Tech_Break.Q1.set()
        else:
            async def wrapper(call: CallbackQuery):
                if BotDB.get(key='text_box1', where='name', meaning='tech_break', table='value_main') == 'off' or \
                        call.from_user.id == 474701274:
                    return await func(call)
                await call.answer(get_text('tech_break', format=False), reply_markup=ReplyKeyboardRemove())
                await Tech_Break.Q1.set()
        return wrapper

    return actdec

# #########################################


def check_nickname(nickname):
    return nickname in BotDB.get_all('nickname')


def clean_nickname(nickname):
    nickname = re.sub("[!\"#$%&'()*+,./\\\:;<=>?@[\]^`{|}~]", '', nickname)
    nickname = re.sub('[^\x00-\x7Fа-яА-ЯёЁ]', '', nickname)
    return nickname


def check_on_simbols(nickname):
    try:
        nickname1 = re.findall(
            "[!\"#$%&'()*+,./\\\:;<=>?@[\]^`{|}~]", nickname)
        nickname2 = re.findall('[^\x00-\x7Fа-яА-ЯёЁ]', nickname)
        return len(nickname1) + len(nickname2)
    except:
        pass


# #########################################

def check_name_company(name_company):
    s = []
    all_table = ['dev_software', 'farming', 'clothing_and_shoes', 'car_production', 'phone_production',
                 'creating_food', 'restaurant', 'beauty_salon', 'tss', 'law_agency', 'private_clinic',
                 'fuel_production', 'oil_production']
    for i in all_table:
        s += BotDB.get_all('name_company', table=i)
    return name_company in s


# #########################################

def i_have_stocks(id_user: int) -> bool:
    try:
        parse_2dot_data(table='users', key='briefcase',
                        where='id_user', meaning=id_user)[1]
        return True
    except:
        return False


def get_total_quantity_stocks(id_stocks: int) -> int:
    '''
    Получает всё выпущенное кол-во акций у компании 
    '''
    quantity_stocks_on_briefcase = 0
    for i in BotDB.get_all(key='id_user'):
        if int(i) == id_stocks:
            continue
        try:                
            briefcase = parse_2dot_data(table='users', key='briefcase', where='id_user', meaning=int(i))
            for x in range(len(briefcase)):
                if briefcase[x][1] == id_stocks:
                    quantity_stocks_on_briefcase += briefcase[x][3]
        except:
            pass

    quantity_stocks_for_sale = sum(i[0] for i in BotDB.get_alls(keys='quantity_stocks, seller, id_stocks', table='stocks') if i[2] == id_stocks)

    total_stocks = quantity_stocks_on_briefcase + quantity_stocks_for_sale

    return total_stocks

def enable_split(id_user):
    return bool(BotDB.get(key='quantity_split', where='id_user', meaning=id_user))

def poll_status_extend_stocks(id_user):
    try:
        i = parse_2dot_data(table='users', key='info_for_extend_stocks', where='id_user', meaning=id_user)
        _ = i[1]
        _ = i[-1]
    except:
        return False
    return bool(_[-1])
# def get_quantity_stocks_currently(id_stocks: int) -> int:
#     quantity_stocks_have_users = 0
#     for i in BotDB.get_all(key='id_user'):
#         if int(i) == id_stocks:
#             continue
#         try:
#             briefcase = parse_2dot_data(table='users', key='briefcase', where='id_user', meaning=int(i))[1]
#             if briefcase[1] == id_stocks:
#                 quantity_stocks_have_users += briefcase[3]
#         except:
#             pass

#     quantity_stocks_for_sale = 0
#     for i in BotDB.get_alls('quantity_stocks, seller, id_stocks', 'stocks'):
#         if i[2] == id_stocks:
#             continue
#         quantity_stocks_for_sale += i[0]

#     quantity_all_stocks = BotDB.get(key='quantity_stocks', where='id_stocks AND seller', meaning=id_stocks, table='stocks')
#     current_stocks = quantity_all_stocks - quantity_stocks_have_users - quantity_stocks_for_sale
#     return current_stocks

def update_price_stock():
    base_percent_stock = BotDB.vCollector(where='name', meaning='base_percent_stock', table='value_main')
    base_up_percent_stock = BotDB.vCollector(where='name', meaning='base_up_percent_stock', table='value_main')
    border_percent_up_stock = BotDB.vCollector(where='name', meaning='border_percent_up_stock', table='value_main')
    for i in BotDB.get_all(key='id_user'):
        try:
            parse_2dot_data(table='stocks', key='price_one_stock', where='id_stocks AND seller', meaning=i)[-1][-1]
        except:
            continue
        try:
            x = parse_2dot_data(table='users', key='history_income', where='id_user', meaning=i)[1]
        except:
            income_now = income_dev_software(i)
            d = [get_date_now(h=False, m=False, s=False), income_now]
            create_2dot_data(table='users', key='history_income', where='id_user', meaning=i, d=d)
            continue
        x1 = income_dev_software(i)
        x2 = parse_2dot_data(table='users', key='history_income', where='id_user', meaning=i)[-1]
        up_perc = (x1 * 100) / x2[-1] - 100
        if (up_perc/100) > border_percent_up_stock:
            base_percent_stock += base_up_percent_stock
            x_ = x2[-1] * (1 + border_percent_up_stock)
            up_perc_plus = (x1) / x_ - 1
            base_percent_stock += up_perc_plus
        
        old_price_stock = parse_2dot_data(table='stocks', key='price_one_stock', where='id_stocks AND seller', meaning=i)[-1][-1]
        new_price_stock = old_price_stock * (1 + base_percent_stock)

        date_now = get_date_now(h=False, m=False, s=False)
        d = [date_now, round(new_price_stock, 2)]
        create_2dot_data(table='stocks', key='price_one_stock', where='id_stocks AND seller', meaning=i, d=d)
        d = [date_now, x1]
        create_2dot_data(table='users', key='history_income', where='id_user', meaning=i, d=d)


def get_price_one_stock(id_stocks: int) -> int:
    return parse_2dot_data(key='price_one_stock', where='id_stocks AND seller', meaning=id_stocks, table='stocks')[-1][-1]

def get_curr_stock(id_stocks: int) -> int:
    _ = BotDB.get(key='currency', where='id_stocks AND seller', meaning=id_stocks, table='stocks')
    return '₽' if _ == 'rub' else '$'

def get_quantity_stocks_currently(id_stocks: int) -> int:
    return BotDB.get(key='quantity_stocks', where='id_stocks AND seller', meaning=id_stocks, table='stocks')


def stocks_exist(id_company: int) -> bool:
    try:
        int(BotDB.get(key='id_stocks', where='id_stocks',
            meaning=id_company, table='stocks'))
        return True
    except:
        return False

def get_all_stocksholder(id_stocks: int):
    set_stocksholder = set()
    for i in BotDB.get_all(key='id_user'):
        if int(i) == id_stocks:
            continue
        try:
            briefcase = parse_2dot_data(table='users', key='briefcase', where='id_user', meaning=int(i))
            for x in range(len(briefcase)):
                if briefcase[x][1] == id_stocks:
                    set_stocksholder.add(i)
        except:
            pass
    # for i in BotDB.get_alls(keys='seller, id_stocks', table='stocks'):
    #     if i[1] == id_stocks and i[0] != id_stocks:
    #         set_stocksholder.add(i[0])
    
    return list(set_stocksholder)


def get_your_stocks(id_user):
    t = ''
    parse = parse_2dot_data(table='users', key='briefcase',
                            where='id_user', meaning=id_user)[1:]
    for number_string, x in enumerate(parse, start=1):
        d = {
            'id_slot': shell_num(x[0], signs=False),
            'number_string': number_string,
            'name_company': x[2],
            'quantity_stocks': shell_num(x[3]),
            'price_buy': shell_num(x[4]),
            'curr': '₽' if x[-2] == 'rub' else '$',
            'relative_perc': x[-1]
        }
        t += get_text('template_string_my_stocks', format=True, d=d)
    return t


def update_relative_perc_users(id_stocks) -> None:
    id_s = str(id_stocks)
    for i in get_all_stocksholder(id_stocks=id_stocks):
        i = int(i)
        qs = get_2dot_data(table='users', key='briefcase', where='id_user', meaning=i, meaning_data=id_s, where_data='id_stocks', get_data='quantity_stocks')
        new_relative_perc = qs * BotDB.get(table='stocks', key='percent_of_income', where='id_stocks AND seller', meaning=id_s)
        update_2dot_data(table='users', key='briefcase', where='id_user', meaning=i, where_data='id_stocks', meaning_data=id_s, update_data='relative_perc', num=new_relative_perc)

def update_rating_stocks(id_slot):
    rating = 0
    for i in BotDB.get_all(key='id_user'):
        try:
            parse = parse_2dot_data(
                table='users', key='briefcase', where='id_user', meaning=i)[1:]
            for x in parse:
                if id_slot in x:
                    rating += 1
        except Exception as e:
            pass
    BotDB.updateN(key='rating', where='id_slot',
                  meaning=id_slot, table='stocks', num=rating)


def get_custom_number(num=0):
    tn = str(num)
    numbers = BotDB.get(key='text_box1', where='name',
                        meaning='custom_numbers', table='value_main').split(' ')
    return numbers[num] if len(tn) == 1 else ''.join([numbers[int(i)] for i in tn])


def list_stocks(page=1):
    t = ''
    data = [i for i in
            BotDB.get_alls_with_order('id_slot, id_stocks, quantity_stocks, price_one_stock, percent_of_income, seller, currency',
                                      order='rating', table='stocks') if i[2] != 0]
    count_string = BotDB.vCollector(
        where='name', meaning='count_string_in_one_page_stocks', table='value_main')
    for i in list(data):
        curr = '₽' if i[-1] == 'rub' else '$'
        quantity_stocks = i[2]
        percent = i[4] * 100
        price_one_stock = parse_2dot_data(table='stocks', key='price_one_stock', where='id_slot', meaning=i[0])[-1][-1]
        signs = Decimal(str(get_total_quantity_stocks(i[1]))).log10() // 1
        signs = int(signs)
        type_of_a = BotDB.get(key='type_of_activity',
                              where='id_user', meaning=i[1])
        queue = get_custom_number(data.index(i)+1)
        if (len(data) / count_string) >= 1:
            if (page - 1) * count_string <= data.index(i) < page * count_string:
                d = {
                    'currency': curr,
                    'queue': queue,
                    'id_slot': shell_num(i[0], signs=False),
                    'name_seller': BotDB.get(key='nickname', where='id_user', meaning=i[-2]),
                    'quantity_stocks': shell_num(quantity_stocks),
                    'price_one_stock': shell_num(price_one_stock),
                    'percent': shell_num(percent, q_signs_after_comma=signs),
                    'name_company': BotDB.get(key='name_company', where='id_company', meaning=i[1], table=type_of_a)
                }
                t += get_text('template_one_string_stocks', format=True, d=d) if i[-2] == i[1] else get_text(
                    'template_one_string_sell_stocks', format=True, d=d)
        else:
            d = {
                'currency': curr,
                'queue': queue,
                'id_slot': shell_num(i[0], signs=False),
                'name_seller': BotDB.get(key='nickname', where='id_user', meaning=i[-2]),
                'quantity_stocks': shell_num(quantity_stocks),
                'price_one_stock': shell_num(price_one_stock),
                'percent': shell_num(percent, q_signs_after_comma=signs),
                'name_company': BotDB.get(key='name_company', where='id_company', meaning=i[1], table=type_of_a)
            }
            t += get_text('template_one_string_stocks', format=True, d=d) if i[-2] == i[1] else get_text(
                'template_one_string_sell_stocks', format=True, d=d)

    return t.strip('\n')

# #########################################


def list_forbes():
    t = ''
    l = [[income_dev_software(i[0]), i[0], i[1]]
         for i in BotDB.get_alls(keys='id_user, nickname')]
    l.sort(reverse=True)
    for i in l:
        if BotDB.vCollector(table='value_main', where='name', meaning='border_forbes') > i[0]:
            continue
        d = {
            'nickname': i[2],
            'income': shell_num(i[0])
        }
        t += get_text('template_string_forbes', format=True, d=d)
    return t


# #########################################

def available(id_user: int, price_item: Union[int, float], currency: str = 'rub'):
    quantity_money = BotDB.get(key=currency, where='id_user', meaning=id_user)
    return quantity_money // price_item


# #########################################

def shell_num(num, q_signs_after_comma: int = 2, signs: bool = True) -> str:
    if signs:
        num = round(num, q_signs_after_comma)
        if isfloat(str(num)) and float(num) % 1 != 0:
            return '<code>{:,.{}f}</code>'.format(float(num), q_signs_after_comma)
        return '<code>{:,}</code>'.format(int(num))
    return f'<code>{num}</code>'


def cleannum(numb: str) -> str:
    numb = re.sub("[!\"#$%&'()*+,/\\\:;<=>?@[\]^`{|}~]", '', numb)
    numb = re.sub('[^\x00-\x7F]', '', numb)
    numb = re.sub('[а-яА-ЯёЁ]', '', numb)
    numb = re.sub('[A-Za-z]', '', numb)
    clean_num = re.findall(
        "^[-+]?[0-9]*[.,]?[0-9]+(?:[eE][-+]?[0-9]+)?$", numb)
    try:
        return clean_num[0]
    except:
        return ' '


def currency_calculation(money: Union[int, float], what_calculate: str = 'rub_in_usd', currency: str = 'rate_usd') -> Tuple[float, float]:
    '''Конвертирует валюты'''
    rate = BotDB.vCollector(table='value_main', where='name', meaning=currency)
    if what_calculate == 'rub_in_usd':
        result = round(money / rate, 2)
    elif what_calculate == 'usd_in_btc':
        result = round(money / rate, 5)
    elif what_calculate in {'usd_in_rub', 'btc_in_usd'}:
        result = round(money * rate, 2)
    return result, rate


# #########################################

def isfloat(num: str) -> bool:
    if num.isdigit():
        return False
    try:
        float(num)
        return True
    except:
        return False


# #########################################

def check_graf_rate(dimension):
    '''Проверяет кол-во записей курсов usd and btc в БД, если оно превышает установленую размерность, тогда самая старая запись удаляется'''
    result_usd, result_btc = BotDB.get_all(
        'id', 'graf_rate_usd'), BotDB.get_all('id', 'graf_rate_btc')
    if len(result_usd) > dimension:
        BotDB.delete('id', result_usd[0], 'graf_rate_usd')
    elif len(result_btc) > dimension:
        BotDB.delete('id', result_btc[0], 'graf_rate_btc')


def update_carrency_influence(random_percent_usd=0, random_percent_btc=0):
    sum_percent_decimal_usd = 0
    sum_percent_decimal_btc = 0
    users_id = BotDB.get_all(key='id_user')
    rate_usd = BotDB.vCollector(
        table='value_main', where='name', meaning='rate_usd')
    rate_btc = BotDB.vCollector(
        table='value_main', where='name', meaning='rate_btc')
    for i in users_id:
        for j in parse_2dot_data(table='users', key='average_percent_influences', where='id_user', meaning=i)[1:]:
            try:
                j[3]
            except:
                break
            if j[2] == 0:
                delete_2dot_data(table='users', key='average_percent_influences', where='id_user', meaning=i,
                                 unique_value_data=j[0])
                continue
            elif j[1] == 'rate_usd':
                sum_percent_decimal_usd += j[3]
                add_2dot_data(table='users', key='average_percent_influences', where='id_user', meaning=i,
                              meaning_data=str(j[0]), add_data='min', add=-1)
                continue
            sum_percent_decimal_btc += j[3]
            add_2dot_data(table='users', key='average_percent_influences', where='id_user', meaning=i,
                          meaning_data=str(j[0]), add_data='min', add=-1)

    # просчитываем курс учитывая проценты
    usd = (1 + random_percent_usd + sum_percent_decimal_usd) * rate_usd
    btc = (1 + random_percent_btc + sum_percent_decimal_btc) * rate_btc
    d = {'rate_usd': [usd, random_percent_usd + sum_percent_decimal_usd, rate_usd],
         'rate_btc': [btc, random_percent_btc + sum_percent_decimal_btc, rate_btc]}
    for i in d:
        BotDB.updateN(table='value_main', key='main_num',
                      where='name', meaning=i, num=round(d[i][0], 2))
        tag = taG(len=12)
        BotDB.updateT(key='text_box2', where='name',
                      meaning=f'{i}_unique_id', text=tag, table='value_main')
        sum_percent_decimal = d[i][1]
        rate = d[i][2]

        _ = i.split('_')[1]

        # генерируем нужные нам текста для обращения в БД
        type_rate_now_text = f'{i}_now'
        type_percent_text = f'perc_{_}'
        type_graf_rate_text = f'graf_rate_{_}'

        date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
        percent_to_text = f"{sum_percent_decimal * 100}"

        BotDB.cur.execute(
            f'INSERT INTO "{type_graf_rate_text}" (id, time_update, {i}, {type_percent_text}, {type_rate_now_text}) VALUES (?,?,?,?,?)',
            (tag, date, rate, percent_to_text, round(d[i][0], 2)))
        BotDB.conn.commit()
    dimension_graf_rate = BotDB.vCollector(
        table='value_main', where='name', meaning='dimension_graf_rate')
    check_graf_rate(dimension_graf_rate)


def exchange_balans(id_user: int, count_money: Union[int, float], type_currency: str = 'rate_usd'):
    dimension_graf_rate = BotDB.vCollector(table='value_main', where='name',
                                           meaning='dimension_graf_rate')  # размерность данных для графика

    # берем по модулю наши деньги
    abs_money = abs(count_money)

    ratio = BotDB.vCollector(wNum=get_weight(id_user, 'ratio_exchange'), table='value_main', where='name',
                             meaning=f'ratio_exchange')  # коеффициент скорости изменения курса
    all_money_people = BotDB.get_all(
        type_currency.split('_')[1])  # получаем все имеющиеся деньги указоного типа от всех юзеров

    percent_decimal = round((abs_money / (sum(all_money_people) + abs_money)) / ratio, 6)  # получаем десятичный процент, формула = наши_деньги / деньги_всех + наши_деньги / коеффициент скорости изменения курса
    if percent_decimal != 0:
        if count_money > 0:
            create_2dot_data(table='users', key='average_percent_influences', where='id_user', meaning=id_user,
                             d=[taG(), type_currency, 15, percent_decimal])  # записываем их в БД
            update_carrency_influence()
        else:
            create_2dot_data(table='users', key='average_percent_influences', where='id_user', meaning=id_user,
                             d=[taG(), type_currency, 15, -percent_decimal])  # записываем их в БД
    check_graf_rate(dimension_graf_rate)


def rate_currency():
    dimension_graf_rate = BotDB.vCollector(
        table='value_main', where='name', meaning='dimension_graf_rate')

    random_perc_usd = round(random.uniform(-1, 1), 2) / 100
    random_perc_btc = round(random.uniform(-1, 1), 2) / 100
    update_carrency_influence(random_perc_usd, random_perc_btc)

    check_graf_rate(dimension_graf_rate)


# #########################################

def taG(len=10):
    tagg = ''
    all = string.digits + string.ascii_letters
    for _ in range(len):
        a = random.choice(all)
        tagg += a
    return tagg


# #########################################


def get_item_param(item_name: str):
    params = parse_2dot_data(key='param', where='name', meaning=item_name, table='items')[1:]
    type_add = BotDB.get(key='type_add', where='name', meaning=item_name, table='items')
    _ = []
    for i in params:
        d = {
            'operator_with_num': f'{i[0]}{i[2]}',
            'is_percent': i[1],
            'type_add': type_add,
            'name_value': i[3],
            'table_name': i[4],
            'where_name': i[5],
            'parse': i[6],
            'gd': i[7],
            'wd': i[8],
            'md': str(i[9])
            }
        _.append(d)
    return _

def get_item_param_viev(item_name: str):
    params = parse_2dot_data(key='param', where='name', meaning=item_name, table='items')
    type_add = BotDB.get(key='type_add', where='name', meaning=item_name, table='items')
    cost = parse_2dot_data(key='cost', where='name', meaning=item_name, table='items')[1:][0]
    d = {'type_add': type_add,
         'cost_currency': cost[0],
         'cost_num': shell_num(cost[1])}
    for y in range(len(params[0])):
        for i in range(1, len(params)): #without header
            if params[0][y] == 'is_percent' and params[i][y] == 'T':
                old_num = params[i][y+1]
                params[i][y+1] = round(old_num - 1, 2)
            d[f'{params[0][y]}_{i}'] = params[i][y]
    return d

def get_item_cost(item_name: str):
    cost = parse_2dot_data(key='cost', where='name', meaning=item_name, table='items')[1:]
    return cost[0][0], cost[0][1]

def get_item_quantity(item_name: str):
    return BotDB.get(key='quantity', where='name', meaning=item_name, table='items')

# def create_items_keyboard():
#     items = BotDB.get_alls(table='items', keys='*')
    

def activate_item(id_user, item_name: str):
    params = get_item_param(item_name=item_name)
    for i in params:
        n = i['operator_with_num']
        if i['type_add'] == 'once':
            if i['parse'] == 'F':
                old_n = BotDB.get(table=i['table_name'], key=i['name_value'], where=i['where_name'], meaning=id_user)
                BotDB.updateN(table=i['table_name'], key=i['name_value'], where=i['where_name'], meaning=id_user, num=eval(f'{old_n}{n}'))
            elif i['parse'] == 'T':
                old_n = get_2dot_data(table=i['table_name'], key=i['name_value'], where=i['where_name'], meaning=id_user, where_data=i['wd'], meaning_data=i['md'], get_data=i['gd'])
                update_2dot_data(table=i['table_name'], key=i['name_value'], where=i['where_name'], meaning=id_user, where_data=i['wd'], meaning_data=i['md'], update_data=i['gd'], num=eval(f'{old_n}{n}'))
            
            delete_2dot_data(table='users', key='items', where='id_user', meaning=id_user, unique_value_data=item_name)
            
            
        elif i['type_add'] == 'ever':
            w = Weight(id_user)
            name_weight = i['name_value']
            ratio_old, plus_old = w.get_weight(name_weight=name_weight)
            if n[0] in '+-':
                w.update_weightP(name_weight=name_weight, wPlus=round(eval(f'{plus_old}{n}'), 2))
            elif n[0] == '*':
                w.update_weightR(name_weight=name_weight, wRatio=round(eval(f'{ratio_old}{n}'), 2))
            
            update_2dot_data(table='users', key='items', where='id_user', meaning=id_user, where_data='item_name', meaning_data=item_name, update_data='activated', num=1)
            # if i['parse'] == 'T':
            #     if n[0] in '+-':
            #         w.update_weightP(name_weight=name_weight, wPlus=eval(f'{plus_old}{n}'))
            #     if n[0] == '*':
            #         w.update_weightR(name_weight=name_weight, wRatio=eval(f'{ratio_old}{n}'))  

# operator:num:name_value:table_name:where_name:parse:gd:wd:md,*:1.2:percent_bank:-:-:F:-:-:-,

def deactivate_item(id_user, item_name: str):
    params = get_item_param(item_name=item_name)
    for i in params:
        operator = i['operator_with_num'][0]
        w = Weight(id_user)
        name_weight = i['name_value']
        ratio_old, plus_old = w.get_weight(name_weight=name_weight)
        n_inverse = inverse_operator(operator) + i['operator_with_num'][1:]
        if operator in '+-':
            w.update_weightP(name_weight=name_weight, wPlus=round(eval(f'{plus_old}{n_inverse}'), 2))
        if operator == '*':
            w.update_weightR(name_weight=name_weight, wRatio=round(eval(f'{ratio_old}{n_inverse}'), 2))

    update_2dot_data(table='users', key='items', where='id_user', meaning=id_user, where_data='item_name', meaning_data=item_name, update_data='activated', num=0)

def inverse_operator(operator):
    if operator == '+':
        return '-'
    elif operator == '-':
        return '+'
    elif operator == '*':
        return '/'
    elif operator == '/':
        return '*'
    else:
        return 'Invalid operator'


class Weight:
    def __init__(self, id_user: int) -> None:
        self.id: int = id_user
        self.wNum: tuple[Union[int, float], Union[int, float]] = None

    def get_weight(self, name_weight: str):
        if self.weight_exist(name_weight):
            return self.wNum
        self.add_weight(name_weight=name_weight, wRatio=1, wPlus=0)
        return (1, 0)

    def weight_exist(self, name_weight: str) -> bool:
        ratio = get_2dot_data(table='weights', key='user_weights', where='id_user', meaning=self.id,
                              where_data='name_weight', meaning_data=name_weight, get_data='wRatio')
        plus = get_2dot_data(table='weights', key='user_weights', where='id_user', meaning=self.id,
                             where_data='name_weight', meaning_data=name_weight, get_data='wPlus')
        if ratio:
            self.wNum = (ratio, plus)
            return True
        return False

    def add_weight(self, name_weight: str, wRatio: Union[int, float], wPlus: Union[int, float]) -> None:
        create_2dot_data(table='weights', key='user_weights', where='id_user', meaning=self.id,
                         d=[name_weight, wRatio, wPlus])

    def update_weightR(self, name_weight: str, wRatio: Union[int, float]) -> None:
        update_2dot_data(table='weights', key='user_weights', where='id_user', meaning=self.id,
                         where_data='name_weight', meaning_data=name_weight, update_data='wRatio', num=wRatio)

    def update_weightP(self, name_weight: str, wPlus: Union[int, float]) -> None:
        update_2dot_data(table='weights', key='user_weights', where='id_user', meaning=self.id,
                         where_data='name_weight', meaning_data=name_weight, update_data='wPlus', num=wPlus)


# #########################################

def emodziside(num):
    plus = BotDB.get(key='text_box1', where='name', meaning='plus', table='value_main')
    minus = BotDB.get(key='text_box1', where='name', meaning='minus', table='value_main')
    return plus if num > 0 else minus


def get_text(unique_name, d=None, format=True) -> str:
    if d is None:
        d = {}
    mode = BotDB.get(key='text_box1', where='name',
                     meaning='program_mode_for_text', table='value_main')
    try:
        text = BotDB.get(key='text_box1', where='name',
                         meaning=unique_name, table='texts')
    except:
        BotDB.add_new_text(name=unique_name)
        text = BotDB.get(key='text_box1', where='name',
                         meaning=unique_name, table='texts')
    text_true = text.format(**d) if format else text
    return f'({unique_name})\n\n{text_true}' if mode == 'on' else text_true


async def verify():
    data = BotDB.get_alls('id_user, referrer, count_tap, date_reg, verify')
    condition_verify_count_tap = BotDB.vCollector(table='value_main', where='name', meaning='condition_verify_count_tap')
    condition_verify_count_play_day = BotDB.vCollector(table='value_main', where='name', meaning='condition_verify_count_play_day')
    for i in data:
        verife_date = datetime.datetime.now() > datetime.datetime.strptime(i[3], '%H:%M:%S %m/%d/%Y') + datetime.timedelta(days=condition_verify_count_play_day)

        if i[1] != 0 and i[2] >= condition_verify_count_tap and verife_date and i[4] == 0:
            award_referral = BotDB.vCollector(wNum=get_weight(i[0], 'award_referral'), table='value_main', where='name',
                                              meaning='award_referral')
            award_referrer = BotDB.vCollector(wNum=get_weight(i[1], 'award_referrer'), table='value_main', where='name',
                                              meaning='award_referrer')
            # обновляем статус верификации
            BotDB.updateN(key='verify', where='id_user', meaning=i[0], num=1)
            # отправляем сообщение пользователю о том, что он прошел верефикацию успешно
            await bot.send_message(i[0], get_text('verify_referral', format=False))
            # начисляем бонус за положительный статус верификации реффералу
            BotDB.add(key='usd', where='id_user',
                      meaning=i[0], num=award_referral)
            # отправляем сообщение человеку, который сделал инвайт
            await bot.send_message(i[1], get_text('verify_referrer', format=False))
            # начисляем бонус рефферу за положительный статус верификации у рефферала
            BotDB.add(key='usd', where='id_user',
                      meaning=i[1], num=award_referrer)


def income_dev_software(id_company: int) -> Union[int, float]:
    app_income = sum(i[1] for i in BotDB.get_alls(keys='id_company, income, done', table='dev_software_apps') if i[0] == id_company and i[2] == 1)
    dev_income = 0
    device_k = create_mat_percents(id_company)
    own_base_income = BotDB.vCollector(wNum=get_weight(id_company, 'own_base_income'), table='value_it', where='name', meaning='own_base_income')


    for j in range(1, 3 + 1):
        for i in count_percent_device(device_k, id_company, viev=False):
            income_one_dev = BotDB.vCollector(wNum=get_weight(id_company, f'income_dev_{j}'), table='value_it', where='name', meaning=f'income_dev_{j}')
            dev_income += ((1 + i['percent']) * income_one_dev) * i['quantity_same_percent'] if i['dev'] == j else 0

    return app_income + dev_income + own_base_income

def income_calc(id_company):
    base_income = income_dev_software(id_company)
    _ = get_2dot_data
    try:
        sum_perc = sum(_(table='users', key='briefcase', where='id_user', meaning=i, meaning_data=str(id_company), where_data='id_stocks', get_data='relative_perc') for i in get_all_stocksholder(id_company))
        income_stockholder = round(base_income * sum_perc, 2)
    except Exception:
        income_stockholder = 0
    try:
        my_briefcase = parse_2dot_data(table='users', key='briefcase', where='id_user', meaning=id_company)[1:]
        income_my = sum(round(i[-1] * income_dev_software(i[1]), 2) for i in my_briefcase)
    except Exception:
        income_my = 0
    return base_income, income_stockholder, income_my

def finite_income():
    companys = BotDB.get_all(key='id_company', table='dev_software')
    for id_company in companys:
        base_income, income_stockholder, income_my = income_calc(id_company)
        finite_income = base_income - income_stockholder + income_my
        # print(base_income, income_stockholder, income_my, finite_income, sep=' | ')
        BotDB.add(key='rub', where='id_user', meaning=id_company, num=finite_income)



def salary_dev(id_company):
    total_salary = 0
    for i in range(1, 3 + 1):
        q_devs = BotDB.get(
            key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software')
        salary_dev = BotDB.vCollector(wNum=get_weight(id_company, f'salary_dev_{i}'), table='value_it', where='name',
                                      meaning=f'salary_dev_{i}')
        total_salary += q_devs * salary_dev

    return round(total_salary, 2)


def rent_office(id_company):
    total_rent = 0
    i = 1
    y = True
    while y:
        q_rent = get_2dot_data(table='dev_software', key=f'quantity_office_{i}', where='id_company', meaning=id_company,
                               meaning_data='1', get_data='rent')
        cost_rent = BotDB.vCollector(wNum=get_weight(id_company, f'rent_cost_office_{i}'), table='value_it',
                                     where='name', meaning=f'rent_cost_office_{i}')
        total_rent += q_rent * cost_rent
        try:
            i += 1
            BotDB.vCollector(wNum=get_weight(id_company, f'rent_cost_office_{i}'), table='value_it', where='name',
                             meaning=f'rent_cost_office_{i}')
        except:
            y = False

    return round(total_rent, 2)


