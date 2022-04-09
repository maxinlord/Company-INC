import abc
from audioop import add
from base64 import decode
from copy import copy
from curses.ascii import isascii, isdigit
from pprint import pp, pprint
from pydoc import text
import string
from tkinter.messagebox import RETRY
from typing import List
from unicodedata import decimal
from db import BotDB
import time
import math
import random
import re
import emoji
import datetime
from all_function import *
import numpy as np

id_user = 474701274


# def isfloat(num):
#     if num.isdigit():
#         return False
#     else:
#         try:
#             float(num)
#             return True
#         except:
#             return False


# def parse_2dot_data(table, key, where, meaning) -> List[list]: 
#     get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
#     l = get_data.split(',')
#     l1 = []
#     l2 = []
#     for i in l:
#         for x in i.split(':'):
#             if x.isdigit() or isfloat(x):
#                 x = float(x) if isfloat(x) else int(x)
#             l1.append(x)
#         l2.append(l1)
#         l1 = []
#     return l2


# def add_2dot_data(table, key, where, meaning, add, where_data: str = 'id', add_data: str = 'id', meaning_data: str = '0'):
#     try:
#         parse = parse_2dot_data(key=key, where=where, meaning=meaning, table=table)
#         ind = parse[0].index(where_data)
#         ind_add = parse[0].index(add_data)
#     except Exception as e:
#         return print('Ошибка!\nФункция: add_2dot_data') 
#     s = ''
#     for i in parse[1:]:
#         if str(i[ind]) == meaning_data:
#             i[ind_add] = round(i[ind_add] + add, 2) if isfloat(i[ind_add]) else i[ind_add] + add
#         s += ',' + ':'.join(list(map(lambda x: str(x))))
#     BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=s.strip(','))

# print(add_2dot_data(key=f'quantity_comp', where='id_company', meaning=id_user, table='dev_software', add=12, where_data='lvl', meaning_data='1', add_data='lvl'))




# l = [{
#         'description': get_text(f'description_comp', format=False),
#         'quantity': shell_money(get_2dot_data(key=f'quantity_comp', where='id_company', meaning=id_user, table='dev_software', where_data='lvl', meaning_data='1', get_data='quantity')),
#         'cost': shell_money(BotDB.vCollector(where='name', meaning=f'cost_comp_1', table='value_it')),
#         'percent': shell_money(BotDB.vCollector(where='name', meaning=f'percent_comp_1', table='value_it'))
#     }]
# pprint(l)

# def delete_header_2dot_data(table, key, where, meaning, name_header):
#     try:
#         get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
#         l: list = get_data.split(',')
#         ind = l[0].split(':').index(name_header)
#     except Exception as e:
#         return print('Ошибка!\nФункция: delete_header_2dot_data') 
#     get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
#     l: list = get_data.split(',')
#     l_new = []
#     ind = l[0].split(':').index(name_header)
#     _: list = l[0].split(':')
#     _.pop(ind)
#     l_new.append(':'.join(_))
#     for i in l[1:]:
#         i = i.split(':')
#         i.pop(ind)
#         _ = ':'.join(i)
#         l_new.append(_)
#     BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=','.join(l_new))
    

# delete_header_2dot_data(table='dev_software', key='quantity_office_5', where='id_company', meaning=474701274, name_header='idd')


# def add_header_2dot_data(table, key, where, meaning, name_header):
#     get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
#     l = get_data.split(',')
#     l_new = []
#     l_new.append(l[0] + ':' + name_header)
#     for i in l[1:]:
#         l_new.append(i + ':0')
#     # BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=','.join(l_new))
#     return ','.join(l_new)

# print(add_header_2dot_data(table='dev_software', key='quantity_office_5', where='id_company', meaning=474701274, name_header='id_company'))




def count_percent_device(id_company):
    devices = ['screen', 'armchair', 'mouse', 'comp', 'keyboard', 'carpet']
    bring_data = []
    i = 1
    ind = 0

    y = True
    while y:
        device = devices[ind]
        q_device = parse_2dot_data(key=f'quantity_{device}', where='id_company', meaning=id_company, table='dev_software')
        # name_device = BotDB.get(key=f'name', where='name', meaning=f'percent_{device}_{i}', table='value_it')
        # p_device = BotDB.vCollector(where='name', meaning=f'percent_{device}_{i}', table='value_it')
        d = {
            'q_dev_1': BotDB.get(key=f'quantity_dev_1', where='id_company', meaning=id_company, table='dev_software'),
            'q_dev_2': BotDB.get(key=f'quantity_dev_2', where='id_company', meaning=id_company, table='dev_software'),
            'q_dev_3': BotDB.get(key=f'quantity_dev_3', where='id_company', meaning=id_company, table='dev_software'),
            'q_device': q_device
            }
        l = [d['q_dev_1'],d['q_dev_2'],d['q_dev_3']]
        for i in enumerate(q_device[1:], 1):
            p_device = BotDB.vCollector(where='name', meaning=f'percent_{device}_{i[0]}', table='value_it')
            name_device = BotDB.get(key=f'name', where='name', meaning=f'percent_{device}_{i[0]}', table='value_it')
            lvl = i[0]
            if i[1][1] == 0:
                continue
            l = [d['q_dev_1'], d['q_dev_2'], d['q_dev_3']]
            for x in enumerate(l, 1):
                if x[1] == 0:
                    continue
                elif i[1][1] <=x[1]:
                    d[f'q_dev_{x[0]}'] -= i[1][1]
                    bring_data.append([f'dev_{x[0]}', i[1][1], p_device, lvl])
                    break
                else:
                    bring_data.append([f'dev_{x[0]}', d[f'q_dev_{x[0]}'], p_device, lvl])
                    d[f'q_dev_{x[0]}'] = 0
                    i = ['заглушка', ['заглушка', i[1][1] - x[1]]]
        try:
            ind += 1
            device = devices[ind]
        except:
            y = False
    # pprint(bring_data)
    # lst = []
    # bring_data1 = bring_data.copy()
    # bring_data2 = bring_data.copy()
    # for x in sorted(bring_data1):
    #     print (f'Начало интереации беру обьект {x}')
    #     percent = x[2]
    #     print(f'Базовый процент равен {percent}')
    #     for i in sorted(bring_data2):
    #         print(f'Начинаю сравнивать обьекты, беру обьект для сравнения {i}')
    #         if x == i:
    #             print('Два обьекта равны, поэтому иду дальше')
    #             bring_data2.remove(i)
    #             continue
    #         elif x[0] == i[0] and x[3].split('_')[1] != i[3].split('_')[1]:
    #             if x[1] < i[1]:
    #                 percent += i[2] 
    #                 print(f'{x[1]} < {i[1]} поэтому я получаю разницу {i[1] - x[1]} и процент {percent}')
                    
    #                 i[1] = i[1] - x[1]
    #                 print(f'ПОЛУЧАЮ ИЗМЕНЕННЫЙ ОБЪЕКТ {i}')
    #             elif x[1] == i[1]:
    #                 percent += i[2]
    #                 print(f'{x[1]} == {i[1]} поэтому я просто получаю процент {percent}')
    #                 i[2] = percent
    #         else:
    #             print('Не одно утверждение не подошло, беру следующий обьект')
    #             continue
    #     if [x[0], x[1], round(percent, 2)] not in lst:
    #         print(f'Обеькта {[x[0], x[1], round(percent, 2)]} нет в списке, добовляю')
    #         lst.append([x[0], x[1], round(percent, 2)])
    #     else:
    #         print(f'Обькт {[x[0], x[1], round(percent, 2)]} есть в списке, пропускаю')
    #         pass

    # return '\n'.join([f'{i}' for i in sorted(lst)])
    return sorted(bring_data)

def percent_get(bring_data):
    pprint(bring_data)
    for j in ['dev_1', 'dev_2', 'dev_3']:
        l = []
        for i in bring_data:
            if i[0] == j:
                l.append([i[3] for x in range(1, i[1]+1)])
        pprint(l, width=100) 
        print('\n')
    

# percent_get(count_percent_device(474701274))

def count_percent_device2(id_company):
    devices = ['screen', 'armchair', 'mouse', 'comp', 'keyboard', 'carpet']
    bring_data = []
    i = 1
    ind = 0
    y = True
    devices_k = []
    while y:
        device = devices[ind]
        q_device = parse_2dot_data(key=f'quantity_{device}', where='id_company', meaning=id_company, table='dev_software')
        q_devs = [BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software') for i in range(1, 3+1)]
        # print(q_device)
        for i in q_device[1:]:
            s = []
            true_q_device = i[1]
            if i[0] > 1:
                s = [0]*q_device[q_device.index(i)-1][1] + s
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
    return pprint(devices_k, width=300)



def mat_plus(device_k, id_company):
    q_devs = [BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software') for i in range(1, 3+1)]
    dev_name = ['junior', 'middle', 'senior']
    percents = []
    for i in range(1, quantity_dev_company(id_company)+1):
        percent = 0
        for x in range(len(device_k)):
            if device_k[x][i] == 1:
                # print(device_k[x][0])
                percent += BotDB.vCollector(where='name', meaning=f'percent_{device_k[x][0]}', table='value_it') 
        percents.append(round(percent, 2))
    text = ''
    u = 0
    for i in enumerate(q_devs):
        slice = percents[u:i[1]+u]
        for j in list(set(percents[u:i[1]+u])):
            text += f'{dev_name[i[0]]}({slice.count(j)}) {j*100}%\n'
        u += i[1]
    return text

count_percent_device2(id_user)


# def n():
#     a = np.arange(200)
#     a.shape = 4, 50
#     # print(a)
#     for i in a:
#         print(i[0])

# n()

# @dp.callback_query_handler(user_id=admin_id, state=Mailing.Language)
# async def mailing_start(call: types.CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     text = data.get("text")
#     await state.reset_state()
#     await call.message.edit_reply_markup()

#     users = await User.query.where(User.language == call.data).gino.all()
#     for user in users:
#         try:
#             await bot.send_message(chat_id=user.user_id,
#                                    text=text)
#             await sleep(0.3)
#         except Exception:
#             pass
#     await call.message.answer(_("Рассылка выполнена."))

# def create_2dot_data(headers=[], d=[]):
#     get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
#     h = ':'.join(headers)
#     if get_data:
#         get_data if h == get_data.split(',')[0] else get_data + h
#     else:
#         get_data = get_data + h
#     s = ',' + ':'.join(d)
#     adding = get_data + s
#     return adding
#     # BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=adding.strip(','))

# print(create_2dot_data(['one', 'two', 'three', 'four'], ['5','6','7','8']))



# def add_2dot_data(add, where_data = 0, meaning_data = '0', add_index=0):
#     # get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
#     get_data = 'one:two,1:2.1,3:4'
#     l = get_data.split(',')
#     s = ''
#     for i in l:
#         i = i.split(':')
#         if i[where_data] == meaning_data:
#             i[add_index] = str(round(float(i[add_index]) + add, 2)) if isfloat(i[add_index]) else str(int(i[add_index]) + add)
#         s += ',' + ':'.join(i)
#     return s.strip(',')
#     # BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=s.strip(','))

# print(add_2dot_data(-2, where_data=0, meaning_data='1', add_index=1))      


# print(parse_2dot_data(key=f'quantity_office_1', where='id_company', meaning=474701274, table='dev_software'))

# def isfloat(num):
#     if num.isdigit():
#         return False
#     else:
#         try:
#             float(num)
#             return True
#         except:
#             return False

# print(isinstance('5.5', (int, float)))
# def calculate_pay(quantity, salary_hour):
#     min = int(time.strftime('%M'))
#     min_job = 60 - min
#     first_salary = round((min_job * salary_hour / 60) * quantity, 2) 
#     return first_salary

# print(calculate_pay(10, 1000))
# def quantity_dev_company_1(id_company):
#     i = 1
#     y = True
#     places = 0
#     while y:
#         places += BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=id_company, table='dev_software')
#         i+=1
#         try:
#             BotDB.vCollector(where='name', meaning=f'salary_dev_{i}', table='value_it')
#         except:
#             y = False
#     return places

# print(quantity_dev_company_1(474701274))

# def app_build(id_company):
#     for i in BotDB.get_alls(keys='done, id_company, name_app', table='dev_software_apps'):
#         if i[0] == 0 and i[1] == id_company:
#             return True, i[2]
#     return False

# print(app_build(474701274))


# def cleannum(numb):
#     numb = re.sub("[!\"#$%&'()*+,/\\\:;<=>?@[\]^`{|}~]", '', numb)
#     numb = re.sub('[^\x00-\x7F]', '', numb)
#     numb = re.sub('[а-яА-ЯёЁ]', '', numb)
#     numb = re.sub('[A-Za-z]', '', numb)
#     clean_num = re.findall("^[-+]?[0-9]*[.,]?[0-9]+(?:[eE][-+]?[0-9]+)?$", numb)
#     return clean_num[0]

# print(cleannum('<🧧>1,000</code>'))

# def calculate_pay_rent(quantity, cost_rent_day):
#     day = time.strftime('%d')
#     month = time.strftime('%m')
#     year = time.strftime('%Y')
#     day = int(time.strftime('%d')) + 1 if datetime.datetime.strptime(f'19:00:00 {month}/{day}/{year}', '%H:%M:%S %m/%d/%Y') < datetime.datetime.today() else time.strftime('%d')
#     t = datetime.datetime.strptime(f'19:00:00 {month}/{day}/{year}', '%H:%M:%S %m/%d/%Y') - datetime.datetime.today()
#     min_rent = t.seconds // 60
#     hours = min_rent // 60
#     mins = 0 if min_rent % 60 + 1 == 60 else min_rent % 60 + 1 
#     first_salary = round((min_rent * cost_rent_day / 1440) * quantity, 2) 
#     return first_salary, hours, mins

# print(calculate_pay_rent(2, 1000))

# day = int(time.strftime('%d')) + 1
# month = time.strftime('%m')
# year = time.strftime('%Y')
# s = (datetime.datetime.strptime(f'00:00:00 {month}/{day}/{year}', '%H:%M:%S %m/%d/%Y') - datetime.datetime.today())
# # s = s.seconds // 60
# print(s)


# def create_2dot_data(table, key, where, meaning, d=[]):
#     get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
#     s = ',' + ':'.join(d)
#     adding = get_data + s
#     BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=adding.strip(','))


# def parse_2dot_data(table, key, where, meaning):
#     get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
#     l = get_data.split(',')
#     l2 = []
#     for i in l:
#         l2.append([x for x in i.split(':')])
#     return l2

# def delete_2dot_data(table, key, where, meaning, unique_name_data):
#     get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
#     l = get_data.split(',')
#     for i in l:
#         i = i.split(':')
#         if unique_name_data not in i:
#             s = ',' + ':'.join(i)
#             BotDB.updateT(key=key, where=where, meaning=meaning, table=table, text=s.strip(','))



# print(delete_2dot_data(table='value_main', key='text_box1', where='name', meaning='test', unique_name_data='id'))


# print(create_2dot_data(table='value_main', key='text_box1', where='name', meaning='test', d=['name3', 'count3', 'id3']))
# print(parse_2dot_data(table='value_main', key='text_box1', where='name', meaning='test'))

            
        


# date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
# print(datetime.datetime.strptime(str(date), '%X %m/%d/%Y'))
# print(datetime.datetime.strptime(str(date), '%X %m/%d/%Y') + datetime.timedelta(hours=5)< datetime.datetime.today())
# # print(datetime.datetime.today() + datetime.timedelta(hours=5) < datetime.datetime.today())

# def parse_2dot_data(table, key, where, meaning):
#     get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
#     l = get_data.split(',')
#     l1 = []
#     l2 = []
#     for i in l:
#         for x in i.split(':'):
#             if x.isdigit() or isfloat(x):
#                 x = float(x) if isfloat(x) else int(x)
#             l1.append(x)
#         l2.append(l1)
#         l1 = []
#     return l2


# def update_rating_stocks(id_company):
#     rating = 0 
#     for i in BotDB.get_all(key='id_user'):
#         try:
#             parse = parse_2dot_data(table='users', key='briefcase', where='id_user', meaning=i)
#             for x in parse:
#                 if id_company in x:
#                     rating += 1
#         except Exception as e:
#             pass
#     BotDB.updateN(key='rating', where='id_company', meaning=id_company, table='stocks', num=rating)

# update_rating_stocks(474701272)

# def your_stocks(id_user):
#     t = ''
#     number_string = 1
#     parse = parse_2dot_data(table='users', key='briefcase', where='id_user', meaning=id_user)[1:]
#     for x in parse:
#         d = {
#             'number_string': number_string,
#             'id_company':x[0],
#             'name_company':x[1],
#             'quantity_stocks':x[2],
#             'price_buy': x[3]
#         }
#         t += get_text('template_string_my_app', format=True, d=d)
#         number_string += 1
#     return t
# def parse_2dot_data(table, key, where, meaning):
#     get_data = BotDB.get(key=key, where=where, meaning=meaning, table=table)
#     l = get_data.split(',')
#     l1 = []
#     l2 = []
#     for i in l:
#         for x in i.split(':'):
#             if x.isdigit() or isfloat(x):
#                 x = float(x) if isfloat(x) else int(x)
#             l1.append(x)
#         l2.append(l1)
#         l1 = []
#     return l2

# def get_2dot_data(table, key, where, meaning, where_data = 0, get_index = 0, meaning_data = '0'):
#     parse = parse_2dot_data(key=key, where=where, meaning=meaning, table=table)
#     for i in parse[1:]:
#         if i[where_data] == int(meaning_data):
#             return i[get_index]

# count_stocks = get_2dot_data(table='users', key='briefcase', where='id_user', meaning=474701274, where_data=0, meaning_data=str(474701272), get_index=2)
# print(count_stocks)
# print(list(map(lambda x: True if 1458391985 in x else False, parse_2dot_data(table='users', key='briefcase', where='id_user', meaning=474701274))))
# date_reg = BotDB.get(key='date_reg', where='id_user', meaning=474701274)
# date_string = date_reg.split(' ')[1]
# date_formatter = '%m/%d/%Y'
# ss = datetime.datetime.strptime(date_string, date_formatter)+datetime.timedelta(minutes=119)
# print((ss - datetime.datetime.today()).min)
# print(datetime.datetime.strptime(date_reg.split(' ')[0],'%H:%M:%S') > datetime.datetime.strptime(date_string, date_formatter)+datetime.timedelta(days=3))
# print(datetime.datetime.strptime('00:00:00 01/01/1900', '%H:%M:%S %m/%d/%Y'))
# verifi = datetime.datetime.today() > datetime.datetime.strptime(date_reg, '%H:%M:%S %m/%d/%Y') + datetime.timedelta(days=3)
# print(verifi)
# def clean_nickname(nickname):
#     try:
#         nickname1 = re.findall("[!\"#$%&'()*+,-./\\\:;<=>?@[\]^_`{|}~]", nickname)
#         nickname2 = re.findall('[^\x00-\x7Fа-яА-Я]', nickname)
#         return len(nickname1)+len(nickname2)
#     except:
#         pass

# def shell_money(quantity_money, currency='usd'):
#     '''Обертка для чисел финансовых'''
#     lnum = '{0:,.2f}'.format(float(quantity_money))
#     lnum = int(lnum.split('.')[1])
#     if lnum == 0:
#         return '<b>{0:,}</b>'.format(quantity_money)
#     else:
#         if currency == 'usd':
#             return '<b>{0:,.2f}</b>'.format(float(quantity_money))
#         elif currency == 'btc':
#             return '<b>{0:,.5f}</b>'.format(float(quantity_money))


# def clean_nickname(nickname):
#     nickname = re.sub("[!\"#$%&'()*+,-./\\\:;<=>?@[\]^_`{|}~]", '', nickname)
#     nickname = re.sub('[^\x00-\x7Fа-яА-Я]', '', nickname)
#     return print(nickname)


# def shell_money2(quantity_money, currency='usd'):
#     str_num = str(quantity_money)
#     quantity_money =int(quantity_money) if str_num.isnumeric() else float(quantity_money)
#     if str_num.isnumeric():
#         return '{:,}'.format(quantity_money)
#     else:
#         return '{:,.2f}'.format(quantity_money) if currency == 'usd' else '{:,.5f}'.format(quantity_money)

# def get_button(unique_number):
#     try:
#         BotDB.get(key='name', where='number', meaning=unique_number, table='button_name')
#     except:
#         BotDB.add_new_button(unique_number)
#     return BotDB.get(key='name', where='number', meaning=unique_number, table='button_name')


# print(text)
# ‍‍‍‍‍Какой прекрасный день!

# data = BotDB.get(table='value_main', key='text_box1', where='name', meaning='test')


# def get_minpercent(type_money,update=False) -> int:

#     users = BotDB.get_all('id_user')
#     type_average_percent = type_money + '_average_percent'
#     all_average_percent =  BotDB.get_all(type_average_percent)
#     sum_perc = 0

#     for i in all_average_percent:
#         idx = all_average_percent.index(i)
#         if i:
#             list_minpercent = [i for i in i.split(';') if i]
#             text_box = []
#             for i in list_minpercent:
#                 list_box = i.split(',')
#                 percent = float(list_box[1])
#                 min = int(list_box[0])
#                 if min == 0:
#                     text_box.append('')
#                 else:
#                     sum_perc += percent
#                     text_box.append(f'{min-1},{percent}')
#             if update:
#                 text_box = [i for i in text_box if i != '']
#                 text = ';'.join(text_box)
#                 BotDB.updateT(key=type_average_percent, where='id_user', meaning=users[idx], text=text)
#         else:
#             pass

#     return sum_perc


# def add_minperc(id_user, type_money, percent, min=15):
#     type_average_percent = type_money + '_average_percent'
#     text = f';{min},{percent}'
#     BotDB.updateT(key=type_average_percent, where='id_user', meaning=id_user, text=text)    



# def some(func):
#     def wrapper():
#         some_text = 'bla'
#         func(some_text)
#     return wrapper


# def main(some_text):
#     print(f'Some text and {some_text}')




# main()










# BotDB = BotDB('/Users/jcu/Desktop/MyProjects/Company INC/server.db')
# # l = list(map(lambda x: x[0],BotDB.get_all('usd')))

# s = 'Разработка ПО, dev_software, Создание игр, dev_game, Фермерство, farming, Одежда и обувь, clothing_and_shoes, Производство автомобилей, car_production, Производство телефонов, phone_production, Продукты питания, creating_food, Ресторан, restaurant, Салон красоты, beauty_salon, С.Т.О, tss, Адвокатское агенство, law_agency, Частная клиника, private_clinic, Производство топлива, fuel_production, Добыча нефти, oil_production'
# l = s.split(',')
# for i in l[1::2]:
#     BotDB.cur.execute(f"""CREATE TABLE IF NOT EXISTS {i}(
#                         id_company INT,
#                         name_founder TEXT,
#                         name_company TEXT);
#                     """)


# BotDB.conn.commit()




# 'Разработка ПО, dev_software, Создание игр, dev_game, Фермерство, farming, Одежда и обувь, clothing_and_shoes, Производство автомобилей, car_production, Производство телефонов, phone_production, Продукты питания, creating_food, Ресторан, restaurant, Салон красоты, beauty_salon, С.Т.О, tss, Адвокатское агенство, law_agency, Частная клиника, private_clinic, Производство топлива, fuel_production, Добыча нефти, oil_production'

# print(list(map(lambda x: x.strip(),BotDB.get(key='text_box1',where='name',meaning='types_field',table='value_main').split(','))))



# import random
#
#
# def rad(count_iter):
#     plus = 0
#     minus = 0
#     for i in range(1, count_iter+1):
#         a = random.choices(['+', '-'], weights=[0.55, 0.5])
#         if a[0] == '+':
#             plus += 1
#         else:
#             minus += 1
#     return print(plus, minus)
#
#
# rad(100)

# def updown(func):
#     def wrapper():
#         print('up')
#         func()
#         print('down')
#     return wrapper

# @updown
# def main():
#     print('main')


# main()