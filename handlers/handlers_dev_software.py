import time
import datetime
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ChatActions
from aiogram.dispatcher import FSMContext
from aiogram import types
from bot import BotDB
from dispatcher import bot, dp
from keyboards.default import keyboard_default
from keyboards.inline import keyboard_inline
from aiogram.types import CallbackQuery
from aiogram.types.input_media import InputMedia, InputMediaPhoto
from all_function import *
from all_states import *



@dp.message_handler(Text(equals=get_button('*1')), state=company_dev_software.Q1)
@ban(state=True)
@last_tap('back', state=True)
async def company_q1(message: Message, state: FSMContext):
    await message.answer(get_text('company_back', format=False), reply_markup=keyboard_default.main_page())
    await state.finish()

# #########################################

@dp.message_handler(Text(equals=get_button('8.1')), state=company_dev_software.Q1)
@ban(state=True)
@last_tap('-', state=True)
async def create_app(message: Message, state: FSMContext):
    try:
        BotDB.get(key='id_company', where='id_company', meaning=message.from_user.id, table='dev_software_apps')
        await message.answer(get_text('menu_create_apps', format=True, d=app_menu_data(message.from_user.id)), reply_markup=keyboard_inline.menu_apps())
    except Exception as e:
        await message.answer(get_text('create_first_app', format=False), reply_markup=keyboard_inline.create_first_app())


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'create_app' and call.data.split(':')[0] == 'app', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def first_app1(call: CallbackQuery, state: FSMContext):
    date = BotDB.get(key='cd_time_app', where='id_company', meaning=call.from_user.id, table='dev_software')
    cd_time = datetime.datetime.strptime(date, '%Y-%m-%d %X')
    if datetime.datetime.today() > cd_time:
        if BotDB.count_dev(call.from_user.id) > BotDB.vCollector(where='name', meaning='quantity_dev_for_app', table='value_it'):
            await bot.delete_message(chat_id=call.from_user.id,message_id=call.message.message_id)
            await bot.send_message(text=get_text('first_app1'),chat_id=call.from_user.id, reply_markup=keyboard_default.cancel())
            await company_dev_software.Q9.set()
        else:
            await call.answer(get_text('first_app_cancel'), show_alert=True)
    else:
        remains_cd = cd_time - datetime.datetime.today()
        d = {
            'remains_cd': str(remains_cd).split('.')[0]
            }
        await call.answer(get_text('create_app_cd', format=True, d=d), show_alert=True)


@dp.message_handler(state=company_dev_software.Q9)
@ban(state=True)
@last_tap('-', state=True)
async def first_app2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('first_app2.5', format=False), reply_markup=keyboard_default.company_dev_software())
        await company_dev_software.Q1.set()
    elif 2 > len(message.text) or len(message.text) > BotDB.vCollector(table='value_it', where='name', meaning='max_symbols_name_app'):
        await message.answer(get_text('first_app2.1', format=False))
    elif check_on_simbols(message.text) > 0:
        await message.answer(get_text('first_app2.2', format=False))
    elif check_name_app(message.text):
        await message.answer(get_text('first_app2.3', format=False))
    else:
        date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
        BotDB.add_new_app(id_company=message.from_user.id, name_app=message.text, one_pay=one_pay(message.from_user.id), income=average_income_dev(message.from_user.id), date_reg=date, quantity_min_build=time_for_build(message.from_user.id))
        cd = BotDB.vCollector(where='name', meaning=f'cooldown_app', table='value_it')
        cd_time = datetime.datetime.strptime(date, '%X %m/%d/%Y') + datetime.timedelta(hours=cd)
        BotDB.updateT(key='cd_time_app', where='id_company', meaning=message.from_user.id, text=cd_time, table='dev_software')
        await message.answer(get_text('first_app2.4', format=False), reply_markup=keyboard_default.company_dev_software())
        await company_dev_software.Q1.set()


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'my_top_apps' and call.data.split(':')[0] == 'app', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def my_top_apps(call: CallbackQuery, state: FSMContext):
    d = {
        'list_top_apps': list_my_top_apps(call.from_user.id)
        }
    try:
        await bot.edit_message_text(text=get_text('my_top_apps', format=True, d=d), chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard_inline.app_back())
    except:
        pass


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'top_apps' and call.data.split(':')[0] == 'app', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def top_apps(call: CallbackQuery, state: FSMContext):
    d = {
        'list_top_apps': list_top_apps(call.from_user.id).strip('\n'),
        'end': your_app_top(call.from_user.id)
        }
    try:
        await bot.edit_message_text(text=get_text('top_apps', format=True, d=d), chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard_inline.app_back())
    except:
        pass


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'back' and call.data.split(':')[0] == 'app', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def back_to_menu_apps(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(get_text('menu_create_apps', format=True, d=app_menu_data(call.from_user.id)), chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard_inline.menu_apps())

# #########################################

@dp.message_handler(Text(equals=get_button('8.2')), state=company_dev_software.Q1)
@ban(state=True)
@last_tap('-', state=True)
async def menu_data_centre(message: Message, state: FSMContext):
    parse = parse_2dot_data(key=f'data_centre', where='id_company', meaning=message.from_user.id, table='dev_software')[1]
    home_one_pay, foreign_one_pay= BotDB.vCollector(table='value_it', where='name', meaning='percent_datacentre_home_onepay'), BotDB.vCollector(table='value_it', where='name', meaning='percent_datacentre_foreign_onepay') 
    home_infinity_pay, foreign_infinity_pay= BotDB.vCollector(table='value_it', where='name', meaning='percent_datacentre_home_infinitypay'), BotDB.vCollector(table='value_it', where='name', meaning='percent_datacentre_foreign_infinitypay') 
    improve_percent_one_pay = round((parse[1] * home_one_pay) + (parse[2] * foreign_one_pay), 2) * 100
    improve_percent_infinity_pay = round((parse[1] * home_infinity_pay) + (parse[2] * foreign_infinity_pay), 2) * 100
    d = {
        'home': parse[1],
        'foreign': parse[2],
        'improve_percent_one_pay': shell_money(improve_percent_one_pay),
        'improve_percent_infinity_pay': shell_money(improve_percent_infinity_pay)
        }
    await message.answer(get_text('menu_data_centre', format=True, d=d), reply_markup=keyboard_inline.menu_data_centre())


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'foreign' and call.data.split(':')[0] == 'data_centre', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def data_centre_foreign(call: CallbackQuery, state: FSMContext):
    percent_one_pay = BotDB.vCollector(table='value_it', where='name', meaning='percent_datacentre_foreign_onepay') * 100
    percent_infinity_pay = BotDB.vCollector(table='value_it', where='name', meaning='percent_datacentre_foreign_infinitypay') * 100
    d = {
        'cost_datacentre_foreign': shell_money(BotDB.vCollector(where='name', meaning=f'cost_datacentre_foreign', table='value_it')),
        'percent_one_pay': shell_money(percent_one_pay), 
        'percent_infinity_pay': shell_money(percent_infinity_pay)
        }
    await bot.edit_message_text(get_text('data_centre_foreign', format=True, d=d), chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard_inline.data_centre_open_back(place='foreign'))


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'home' and call.data.split(':')[0] == 'data_centre', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def data_centre_home(call: CallbackQuery, state: FSMContext):
    percent_one_pay = BotDB.vCollector(table='value_it', where='name', meaning='percent_datacentre_home_onepay') * 100
    percent_infinity_pay = BotDB.vCollector(table='value_it', where='name', meaning='percent_datacentre_home_infinitypay') * 100
    d = {
        'cost_datacentre_home': shell_money(BotDB.vCollector(where='name', meaning=f'cost_datacentre_home', table='value_it')),
        'percent_one_pay': shell_money(percent_one_pay), 
        'percent_infinity_pay': shell_money(percent_infinity_pay)
        }
    await bot.edit_message_text(get_text('data_centre_home', format=True, d=d), chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard_inline.data_centre_open_back(place='home'))


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'back' and call.data.split(':')[0] == 'data_centre', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def data_centre_back(call: CallbackQuery, state: FSMContext):
    parse = parse_2dot_data(key=f'data_centre', where='id_company', meaning=call.from_user.id, table='dev_software')[1]
    home_one_pay, foreign_one_pay= BotDB.vCollector(table='value_it', where='name', meaning='percent_datacentre_home_onepay'), BotDB.vCollector(table='value_it', where='name', meaning='percent_datacentre_foreign_onepay') 
    home_infinity_pay, foreign_infinity_pay= BotDB.vCollector(table='value_it', where='name', meaning='percent_datacentre_home_infinitypay'), BotDB.vCollector(table='value_it', where='name', meaning='percent_datacentre_foreign_infinitypay') 
    improve_percent_one_pay = round((parse[1] * home_one_pay) + (parse[2] * foreign_one_pay), 2) * 100
    improve_percent_infinity_pay = round((parse[1] * home_infinity_pay) + (parse[2] * foreign_infinity_pay), 2) * 100
    d = {
        'home': parse[1],
        'foreign': parse[2],
        'improve_percent_one_pay': shell_money(improve_percent_one_pay),
        'improve_percent_infinity_pay': shell_money(improve_percent_infinity_pay)
        }
    await bot.edit_message_text(get_text('menu_data_centre', format=True, d=d), chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard_inline.menu_data_centre())


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'open' and call.data.split(':')[0] == 'data_centre', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def open_data_centre1(call: CallbackQuery, state: FSMContext):
    place = call.data.split(':')[2]
    currency = 'rub' if call.data.split(':')[2] == 'home' else 'usd'
    cost_datacentre = BotDB.vCollector(where='name', meaning=f'cost_datacentre_{place}', table='value_it')
    if BotDB.get(key=currency, where='id_user', meaning=call.from_user.id) >= cost_datacentre:
        await bot.delete_message(chat_id=call.from_user.id,message_id=call.message.message_id)
        add_index = 1 if place == 'home' else 2
        BotDB.add(key=currency, where='id_user', meaning=call.from_user.id, num=-cost_datacentre)
        add_2dot_data(key=f'data_centre', where='id_company', meaning=call.from_user.id, table='dev_software', where_data=0, meaning_data='1', add_index=add_index, add=1)  
        await bot.send_message(text=get_text('open_data_centre1'),chat_id=call.from_user.id, reply_markup=keyboard_default.company_dev_software())
    else:
        await call.answer(get_text('open_data_centre_cancel', format=True, d={'currency':currency}), show_alert=True)

# #########################################

@dp.message_handler(Text(equals=get_button('8.3')), state=company_dev_software.Q1)
@ban(state=True)
@last_tap('-', state=True)
async def menu_marketing_lab(message: Message, state: FSMContext):
    await message.answer(get_text('menu_marketing_lab', format=False), reply_markup=keyboard_inline.menu_marketing_lab())


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'simple' and call.data.split(':')[0] == 'marketing_lab', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def marketing_lab_simple(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(get_text('marketing_lab_simple', format=False), chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard_inline.marketing_lab_open_back(type='simple'))


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'hard' and call.data.split(':')[0] == 'marketing_lab', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def marketing_lab_hard(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(get_text('marketing_lab_hard', format=False), chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard_inline.marketing_lab_open_back(type='hard'))


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'back' and call.data.split(':')[0] == 'marketing_lab', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def marketing_lab_back(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(get_text('menu_marketing_lab', format=False), chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard_inline.menu_marketing_lab())


# @dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'study' and call.data.split(':')[0] == 'marketing_lab', state=company_dev_software.Q1)
# @ban_call(state=True)
# @last_tap_call('-', state=True)
# async def study_marketing_lab(call: CallbackQuery, state: FSMContext):
#     type = call.data.split(':')[2]
#     if BotDB.get(key='rub', where='id_user', meaning=call.from_user.id) >= BotDB.vCollector(where='name', meaning=f'data_centre_{type}', table='value_it'):
#         await bot.delete_message(chat_id=call.from_user.id,message_id=call.message.message_id)
#         await bot.send_message(text=get_text('study_marketing_lab'),chat_id=call.from_user.id, reply_markup=keyboard_default.company_dev_software())
#     else:
#         await call.answer(get_text('study_marketing_lab_cancel', format=False), show_alert=True)

# #########################################

@dp.message_handler(Text(equals=get_button('8.4')), state=company_dev_software.Q1)
@ban(state=True)
@last_tap('-', state=True)
async def hire_dev(message: Message, state: FSMContext):
    l = [{
        'description': get_text(f'description_dev_1', format=False),
        'quantity': shell_money(BotDB.get(key=f'quantity_dev_1', where='id_company', meaning=message.from_user.id, table='dev_software')),
        'salary': shell_money(BotDB.vCollector(where='name', meaning=f'salary_dev_1', table='value_it')),
        'income': shell_money(BotDB.vCollector(where='name', meaning=f'income_dev_1', table='value_it')),
        'photo': get_photo(f'photo_dev_1')
    }]
    async with state.proxy() as data:
            data['l'] = l
    await message.answer_photo(photo=l[0]['photo'], caption=get_text('hire_dev_template', format=True, d=l[0]), reply_markup=keyboard_inline.hire_dev(index=0))


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'dev' and call.data.split(':')[0] == 'left', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def hire_dev_left(call: CallbackQuery, state: FSMContext):
    l = []
    for i in range(1,3+1):
        l.append({
            'description': get_text(f'description_dev_{i}', format=False),
            'quantity': shell_money(BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=call.from_user.id, table='dev_software')),
            'salary': shell_money(BotDB.vCollector(where='name', meaning=f'salary_dev_{i}', table='value_it')),
            'income': shell_money(BotDB.vCollector(where='name', meaning=f'income_dev_{i}', table='value_it')),
            'photo': get_photo(f'photo_dev_{i}')
        })
    async with state.proxy() as data:
        data['l'] = l
    index = len(l)-1 if int(call.data.split(':')[2]) - 1 < 0 else int(call.data.split(':')[2]) - 1
    try:
        await bot.edit_message_media(media=InputMediaPhoto(l[index]['photo'], caption=get_text(f'hire_dev_template', format=True, d=l[index])),chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard_inline.hire_dev(index))
    except Exception as e:
        pass


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'dev' and call.data.split(':')[0] == 'right', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def hire_dev_right(call: CallbackQuery, state: FSMContext):
    l = []
    for i in range(1,3+1):
        l.append({
            'description': get_text(f'description_dev_{i}', format=False),
            'quantity': shell_money(BotDB.get(key=f'quantity_dev_{i}', where='id_company', meaning=call.from_user.id, table='dev_software')),
            'salary': shell_money(BotDB.vCollector(where='name', meaning=f'salary_dev_{i}', table='value_it')),
            'income': shell_money(BotDB.vCollector(where='name', meaning=f'income_dev_{i}', table='value_it')),
            'photo': get_photo(f'photo_dev_{i}')
        })
    async with state.proxy() as data:
        data['l'] = l
    index = 0 if int(call.data.split(':')[2]) + 1 > len(l)-1 else int(call.data.split(':')[2]) + 1
    try:
        await bot.edit_message_media(media=InputMediaPhoto(l[index]['photo'], caption=get_text('hire_dev_template', format=True, d=l[index])),chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard_inline.hire_dev(index))
    except Exception as e:
        pass


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'dev' and call.data.split(':')[0] == 'hire', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def hire_dev1(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    dic = data.get('l')
    index = int(call.data.split(':')[2]) + 1
    async with state.proxy() as data:
        data['index'] = index
    if BotDB.get(key='rub', where='id_user', meaning=call.from_user.id) >= float(cleannum(dic[index-1]['salary'])):
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
        d = {
            'available': shell_money(available(call.from_user.id, float(cleannum(dic[index-1]['salary']))))
            }
        await bot.send_message(call.from_user.id, get_text('hire_dev1.1', format=True, d=d), reply_markup=keyboard_default.cancel())
        await company_dev_software.Q2.set()
    else:
        await call.answer(get_text('hire_dev1.2'), show_alert=True)


@dp.message_handler(state=company_dev_software.Q2)
@ban(state=True)
@last_tap('-', state=True)
async def hire_dev2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('hire_dev2.1', format=False), reply_markup=keyboard_default.company_dev_software())
        await company_dev_software.Q1.set()    
    elif cleannum(message.text).isdigit():
        cleannums = cleannum(message.text)
        data = await state.get_data()
        dic = data.get('l')
        index = data.get('index')
        if quantity_dev_company(message.from_user.id) + int(cleannums) <= quantity_place_company(message.from_user.id):
            if BotDB.get(key='rub', where='id_user', meaning=message.from_user.id) >= float(cleannum(dic[index-1]['salary'])) * int(cleannums):
                pay = calculate_pay_dev(quantity=int(cleannums), salary_hour=float(cleannum(dic[index-1]['salary'])))
                BotDB.add(key='rub', where='id_user', meaning=message.from_user.id, num=-pay[0])
                BotDB.add(key=f'quantity_dev_{index}', where='id_company', meaning=message.from_user.id, table='dev_software', num=int(cleannums))
                d = {
                    'pay':shell_money(pay[0]),
                    'min_job': shell_money(pay[1])
                    }
                await message.answer(get_text('hire_dev2.3', format=True, d=d), reply_markup=keyboard_default.company_dev_software())
                await company_dev_software.Q1.set()
            else:
                await message.answer(get_text('hire_dev2.4', format=False))
        else:
            await message.answer(get_text('hire_dev2.5', format=False))
    else:
        await message.answer(get_text('hire_dev2.2', format=False))


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'dev' and call.data.split(':')[0] == 'dismiss', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def dismiss_dev1(call: CallbackQuery, state: FSMContext):
    index =int(call.data.split(':')[2]) + 1
    async with state.proxy() as data:
        data['index'] = index
    if BotDB.get(key=f'quantity_dev_{index}', where='id_company', meaning=call.from_user.id, table='dev_software') > 0:
        app_build_answ = app_build(call.from_user.id)
        if not app_build_answ[0]:
            await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
            await bot.send_message(call.from_user.id, get_text('dismiss_dev1.1', format=False), reply_markup=keyboard_default.cancel())
            await company_dev_software.Q6.set()
        else:
            await call.answer(get_text('dismiss_dev1.2', format=True, d={'name_app': app_build_answ[1]}), show_alert=True)
    else:
        await call.answer(get_text('dismiss_dev1.3'), show_alert=True)


@dp.message_handler(state=company_dev_software.Q6)
@ban(state=True)
@last_tap('-', state=True)
async def dismiss_dev2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('dismiss_dev2.1', format=False), reply_markup=keyboard_default.company_dev_software())
        await company_dev_software.Q1.set()    
    elif cleannum(message.text).isdigit():
        cleannums = cleannum(message.text)
        data = await state.get_data()
        index = data.get('index')
        dic = data.get('l')
        if int(cleannum(dic[index-1]['quantity'])) - int(cleannums) >= 0:
            BotDB.add(key=f'quantity_dev_{index}', where='id_company', meaning=message.from_user.id, table='dev_software', num=-int(cleannums))
            await message.answer(get_text('dismiss_dev2.3', format=False), reply_markup=keyboard_default.company_dev_software())
            await company_dev_software.Q1.set()
        else:
            await message.answer(get_text('dismiss_dev2.4', format=False))
    else:
        await message.answer(get_text('dismiss_dev2.2', format=False))

# #########################################

@dp.message_handler(Text(equals=get_button('8.6')), state=company_dev_software.Q1)
@ban(state=True)
@last_tap('-', state=True)
async def office_dev(message: Message, state: FSMContext):
        l = [{
            'description': get_text(f'description_office_1', format=False),
            'quantity_buy': shell_money(parse_2dot_data(key=f'quantity_office_1', where='id_company', meaning=message.from_user.id, table='dev_software')[1][1]),
            'quantity_rent': shell_money(parse_2dot_data(key=f'quantity_office_1', where='id_company', meaning=message.from_user.id, table='dev_software')[1][2]),
            'cost': shell_money(BotDB.vCollector(where='name', meaning=f'cost_office_1', table='value_it')),
            'rent_cost': shell_money(BotDB.vCollector(where='name', meaning=f'rent_cost_office_1', table='value_it')),
            'size': shell_money(BotDB.vCollector(where='name', meaning=f'size_office_1', table='value_it')),
            'photo': get_photo(f'photo_office_1')
        }]
        async with state.proxy() as data:
            data['l'] = l
        await message.answer_photo(photo=l[0]['photo'], caption=get_text('office_template', format=True, d=l[0]), reply_markup=keyboard_inline.office_dev(index=0))


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'office' and call.data.split(':')[0] == 'left', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def office_dev_left(call: CallbackQuery, state: FSMContext):
    l = []
    for i in range(1,5+1):
        l.append({
            'description': get_text(f'description_office_{i}', format=False),
            'quantity_buy': shell_money(parse_2dot_data(key=f'quantity_office_{i}', where='id_company', meaning=call.from_user.id, table='dev_software')[1][1]),
            'quantity_rent': shell_money(parse_2dot_data(key=f'quantity_office_{i}', where='id_company', meaning=call.from_user.id, table='dev_software')[1][2]),
            'cost': shell_money(BotDB.vCollector(where='name', meaning=f'cost_office_{i}', table='value_it')),
            'rent_cost': shell_money(BotDB.vCollector(where='name', meaning=f'rent_cost_office_{i}', table='value_it')),
            'size': shell_money(BotDB.vCollector(where='name', meaning=f'size_office_{i}', table='value_it')),
            'photo': get_photo(f'photo_office_{i}')
        })
    async with state.proxy() as data:
        data['l'] = l
    index = len(l)-1 if int(call.data.split(':')[2]) - 1 < 0 else int(call.data.split(':')[2]) - 1
    try:
        await bot.edit_message_media(media=InputMediaPhoto(l[index]['photo'], caption=get_text(f'office_template', format=True, d=l[index])),chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard_inline.office_dev(index))
    except Exception as e:
        pass


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'office' and call.data.split(':')[0] == 'right', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def office_dev_right(call: CallbackQuery, state: FSMContext):
    l = []
    for i in range(1,5+1):
        l.append({
            'description': get_text(f'description_office_{i}', format=False),
            'quantity_buy': shell_money(parse_2dot_data(key=f'quantity_office_{i}', where='id_company', meaning=call.from_user.id, table='dev_software')[1][1]),
            'quantity_rent': shell_money(parse_2dot_data(key=f'quantity_office_{i}', where='id_company', meaning=call.from_user.id, table='dev_software')[1][2]),
            'cost': shell_money(BotDB.vCollector(where='name', meaning=f'cost_office_{i}', table='value_it')),
            'rent_cost': shell_money(BotDB.vCollector(where='name', meaning=f'rent_cost_office_{i}', table='value_it')),
            'size': shell_money(BotDB.vCollector(where='name', meaning=f'size_office_{i}', table='value_it')),
            'photo': get_photo(f'photo_office_{i}')
        })
    async with state.proxy() as data:
        data['l'] = l
    index = 0 if int(call.data.split(':')[2]) + 1 > len(l)-1 else int(call.data.split(':')[2]) + 1
    try:
        await bot.edit_message_media(media=InputMediaPhoto(l[index]['photo'], caption=get_text('office_template', format=True, d=l[index])),chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard_inline.office_dev(index))
    except Exception as e:
        pass


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'office' and call.data.split(':')[0] == 'buy', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def buy_office1(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    dic = data.get('l')
    index =int(call.data.split(':')[2]) + 1
    async with state.proxy() as data:
        data['index'] = index
    if BotDB.get(key='rub', where='id_user', meaning=call.from_user.id) >= float(cleannum(dic[index-1]['cost'])):
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
        d = {
            'available': shell_money(available(call.from_user.id, float(cleannum(dic[index-1]['cost']))))
            }
        await bot.send_message(call.from_user.id, get_text('buy_office1.1', format=True, d=d), reply_markup=keyboard_default.cancel())
        await company_dev_software.Q3.set()
    else:
        await call.answer(get_text('buy_office1.2'), show_alert=True)


@dp.message_handler(state=company_dev_software.Q3)
@ban(state=True)
@last_tap('-', state=True)
async def buy_office2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('buy_office2.1', format=False), reply_markup=keyboard_default.company_dev_software())
        await company_dev_software.Q1.set()    
    elif cleannum(message.text).isdigit():
        cleannums = cleannum(message.text)
        data = await state.get_data()
        index = data.get('index')
        dic = data.get('l')
        if BotDB.get(key='rub', where='id_user', meaning=message.from_user.id) >= float(cleannum(dic[index-1]['cost'])) * int(cleannums):
            pay = float(cleannum(dic[index-1]['cost'])) * int(cleannums)
            BotDB.add(key='rub', where='id_user', meaning=message.from_user.id, num=-pay)
            add_2dot_data(key=f'quantity_office_{index}', where='id_company', meaning=message.from_user.id, table='dev_software', where_data=0, meaning_data='1', add_index=1, add=int(cleannums))
            await message.answer(get_text('buy_office2.3', format=False), reply_markup=keyboard_default.company_dev_software())
            await company_dev_software.Q1.set()
        else:
            await message.answer(get_text('buy_office2.4', format=False))
    else:
        await message.answer(get_text('buy_office2.2', format=False))

    
@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'office' and call.data.split(':')[0] == 'rent', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def rent_office1(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    dic = data.get('l')
    index =int(call.data.split(':')[2]) + 1
    async with state.proxy() as data:
        data['index'] = index
    if BotDB.get(key='rub', where='id_user', meaning=call.from_user.id) >= float(cleannum(dic[index-1]['rent_cost'])):
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
        d = {
            'available': shell_money(available(call.from_user.id, float(cleannum(dic[index-1]['rent_cost']))))
            }
        await bot.send_message(call.from_user.id, get_text('rent_office1.1', format=True, d=d), reply_markup=keyboard_default.cancel())
        await company_dev_software.Q4.set()
    else:
        await call.answer(get_text('rent_office1.2'), show_alert=True)


@dp.message_handler(state=company_dev_software.Q4)
@ban(state=True)
@last_tap('-', state=True)
async def rent_office2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('rent_office2.1', format=False), reply_markup=keyboard_default.company_dev_software())
        await company_dev_software.Q1.set()    
    elif cleannum(message.text).isdigit():
        cleannums = cleannum(message.text)
        data = await state.get_data()
        dic = data.get('l')
        index = data.get('index')
        if BotDB.get(key='rub', where='id_user', meaning=message.from_user.id) >= float(cleannum(dic[index-1]['rent_cost'])) * int(cleannums):
            pay = calculate_pay_rent(quantity=int(cleannums), cost_rent_day=float(cleannum(dic[index-1]['rent_cost'])))
            BotDB.add(key='rub', where='id_user', meaning=message.from_user.id, num=-pay[0])
            add_2dot_data(key=f'quantity_office_{index}', where='id_company', meaning=message.from_user.id, table='dev_software', where_data=0, meaning_data='1', add_index=2, add=int(cleannums))
            d = {
                'pay':shell_money(pay[0]),
                'hour': shell_money(pay[1]),
                'min': shell_money(pay[2])
                }
            await message.answer(get_text('rent_office2.3', format=True, d=d), reply_markup=keyboard_default.company_dev_software())
            await company_dev_software.Q1.set()
        else:
            await message.answer(get_text('rent_office2.4', format=False))
    else:
        await message.answer(get_text('rent_office2.2', format=False))


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'office' and call.data.split(':')[0] == 'sell', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def sell_office1(call: CallbackQuery, state: FSMContext):
    index =int(call.data.split(':')[2]) + 1
    async with state.proxy() as data:
        data['index'] = index
    if parse_2dot_data(key=f'quantity_office_{index}', where='id_company', meaning=call.from_user.id, table='dev_software')[1][1] > 0:
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
        await bot.send_message(call.from_user.id, get_text('sell_office1.1', format=False), reply_markup=keyboard_default.cancel())
        await company_dev_software.Q5.set()
    else:
        await call.answer(get_text('sell_office1.2'), show_alert=True)


@dp.message_handler(state=company_dev_software.Q5)
@ban(state=True)
@last_tap('-', state=True)
async def sell_office2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('sell_office2.1', format=False), reply_markup=keyboard_default.company_dev_software())
        await company_dev_software.Q1.set()    
    elif cleannum(message.text).isdigit():
        cleannums = cleannum(message.text)
        data = await state.get_data()
        index = data.get('index')
        dic = data.get('l')
        if int(cleannum(dic[index-1]['quantity_buy'])) - int(cleannums) >= 0:
            percent_back = BotDB.vCollector(where='name', meaning='percent_back_money_office', table='value_it')
            pay = round(float(cleannum(dic[index-1]['cost'])) * int(cleannums) * percent_back, 2)
            BotDB.add(key='rub', where='id_user', meaning=message.from_user.id, num=pay)
            add_2dot_data(key=f'quantity_office_{index}', where='id_company', meaning=message.from_user.id, table='dev_software', where_data=0, meaning_data='1', add_index=1, add=-int(cleannums))
            await message.answer(get_text('sell_office2.3', format=False), reply_markup=keyboard_default.company_dev_software())
            await company_dev_software.Q1.set()
        else:
            await message.answer(get_text('sell_office2.4', format=False))
    else:
        await message.answer(get_text('sell_office2.2', format=False))


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'office' and call.data.split(':')[0] == 'stoprent', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def stoprent_office1(call: CallbackQuery, state: FSMContext):
    index =int(call.data.split(':')[2]) + 1
    async with state.proxy() as data:
        data['index'] = index
    if parse_2dot_data(key=f'quantity_office_{index}', where='id_company', meaning=call.from_user.id, table='dev_software')[1][2] > 0:
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
        await bot.send_message(call.from_user.id, get_text('stoprent_office1.1', format=False), reply_markup=keyboard_default.cancel())
        await company_dev_software.Q10.set()
    else:
        await call.answer(get_text('stoprent_office1.2'), show_alert=True)


@dp.message_handler(state=company_dev_software.Q10)
@ban(state=True)
@last_tap('-', state=True)
async def stoprent_office2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('stoprent_office2.1', format=False), reply_markup=keyboard_default.company_dev_software())
        await company_dev_software.Q1.set()    
    elif cleannum(message.text).isdigit():
        cleannums = cleannum(message.text)
        data = await state.get_data()
        index = data.get('index')
        dic = data.get('l')
        if int(cleannum(dic[index-1]['quantity_rent'])) - int(cleannums) >= 0:
            percent_back = BotDB.vCollector(where='name', meaning='percent_back_money_office_rent', table='value_it')
            pay = round(float(cleannum(dic[index-1]['rent_cost'])) * int(cleannums) * percent_back, 2)
            BotDB.add(key='rub', where='id_user', meaning=message.from_user.id, num=pay)
            add_2dot_data(key=f'quantity_office_{index}', where='id_company', meaning=message.from_user.id, table='dev_software', where_data=0, meaning_data='1', add_index=2, add=-int(cleannums))
            await message.answer(get_text('stoprent_office2.3', format=False), reply_markup=keyboard_default.company_dev_software())
            await company_dev_software.Q1.set()
        else:
            await message.answer(get_text('stoprent_office2.4', format=False))
    else:
        await message.answer(get_text('stoprent_office2.2', format=False))

# #########################################

@dp.message_handler(Text(equals=get_button('8.5')), state=company_dev_software.Q1)
@ban(state=True)
@last_tap('-', state=True)
async def device_menu(message: Message, state: FSMContext):
    d = {
        'quantity_devices': quantity_devices(message.from_user.id),
        'percents': count_percent_device(message.from_user.id)
        }
    await message.answer(get_text('device', format=True, d=d), reply_markup=keyboard_inline.device())


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'back' and call.data.split(':')[0] == 'device', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def back_to_device(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=0.5)
    d = {
        'quantity_devices': quantity_devices(call.from_user.id),
        'percents': count_percent_device(call.from_user.id)
        }
    await bot.edit_message_text(get_text('device', format=True, d=d),call.from_user.id, call.message.message_id, reply_markup=keyboard_inline.device())


@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'device_item', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def device_item(call: CallbackQuery, state: FSMContext):
    device_item = call.data.split(':')[1]
    l = [{
            'description': get_text(f'description_{device_item}_1', format=False),
            'quantity': shell_money(get_2dot_data(key=f'quantity_{device_item}', where='id_company', meaning=call.from_user.id, table='dev_software', where_data='lvl', meaning_data='1', get_data='quantity')),
            'cost': shell_money(BotDB.vCollector(where='name', meaning=f'cost_{device_item}_1', table='value_it')),
            'percent': shell_money(BotDB.vCollector(where='name', meaning=f'percent_{device_item}_1', table='value_it'))
        }]
    async with state.proxy() as data:
        data['l'] = l
        data['device'] = device_item
    await bot.edit_message_text(get_text('device_template', format=True, d=l[0]), call.from_user.id, call.message.message_id, reply_markup=keyboard_inline.device_menu(device=device_item, index=0))

   
@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'device' and call.data.split(':')[0] == 'left', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def device_left(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    device_item = data.get('device')
    l = []
    i = 1
    y = True
    while y:
        l.append({
            'description': get_text(f'description_{device_item}_{i}', format=False),
            'quantity': shell_money(get_2dot_data(key=f'quantity_{device_item}', where='id_company', meaning=call.from_user.id, table='dev_software', where_data='lvl', meaning_data=i, get_data='quantity')),
            'cost': shell_money(BotDB.vCollector(where='name', meaning=f'cost_{device_item}_{i}', table='value_it')),
            'percent': shell_money(BotDB.vCollector(where='name', meaning=f'percent_{device_item}_{i}', table='value_it'))
        })
        try:
            i+=1
            BotDB.vCollector(where='name', meaning=f'cost_{device_item}_{i}', table='value_it')
        except:
            y = False
    async with state.proxy() as data:
        data['l'] = l
    index = len(l)-1 if int(call.data.split(':')[2]) - 1 < 0 else int(call.data.split(':')[2]) - 1
    try:
        await bot.edit_message_text(text=get_text(f'device_template', format=True, d=l[index]),chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard_inline.device_menu(device=device_item, index=index))
    except Exception as e:
        pass


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'device' and call.data.split(':')[0] == 'right', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def device_right(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    device_item = data.get('device')
    l = []
    i = 1
    y = True
    while y:
        l.append({
            'description': get_text(f'description_{device_item}_{i}', format=False),
            'quantity': shell_money(get_2dot_data(key=f'quantity_{device_item}', where='id_company', meaning=call.from_user.id, table='dev_software', where_data='lvl', meaning_data=i, get_data='quantity')),
            'cost': shell_money(BotDB.vCollector(where='name', meaning=f'cost_{device_item}_{i}', table='value_it')),
            'percent': shell_money(BotDB.vCollector(where='name', meaning=f'percent_{device_item}_{i}', table='value_it'))
        })
        i+=1
        try:
            BotDB.vCollector(where='name', meaning=f'cost_{device_item}_{i}', table='value_it')
        except:
            y = False
    async with state.proxy() as data:
        data['l'] = l
    index = 0 if int(call.data.split(':')[2]) + 1 > len(l)-1 else int(call.data.split(':')[2]) + 1
    try:
        await bot.edit_message_text(text=get_text(f'device_template', format=True, d=l[index]),chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard_inline.device_menu(device=device_item, index=index))
    except Exception as e:
        pass


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'device' and call.data.split(':')[0] == 'buy', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def buy_device1(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    dic = data.get('l')
    index =int(call.data.split(':')[3]) + 1
    async with state.proxy() as data:
        data['index'] = index
        data['device'] = call.data.split(':')[2]
    if BotDB.get(key='rub', where='id_user', meaning=call.from_user.id) >= float(cleannum(dic[index-1]['cost'])):
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
        d = {
            'available': shell_money(available(call.from_user.id, float(cleannum(dic[index-1]['cost']))))
            }
        await bot.send_message(call.from_user.id, get_text('buy_device1.1', format=True, d=d), reply_markup=keyboard_default.cancel())
        await company_dev_software.Q7.set()
    else:
        await call.answer(get_text('buy_device1.2'), show_alert=True)


@dp.message_handler(state=company_dev_software.Q7)
@ban(state=True)
@last_tap('-', state=True)
async def buy_device2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('buy_device2.1', format=False), reply_markup=keyboard_default.company_dev_software())
        await company_dev_software.Q1.set()    
    elif cleannum(message.text).isdigit():
        cleannums = cleannum(message.text)
        if quantity_dev_company(message.from_user.id) - int(cleannums) >= 0:
            data = await state.get_data()
            index = data.get('index')
            dic = data.get('l')
            if BotDB.get(key='rub', where='id_user', meaning=message.from_user.id) >= float(cleannum(dic[index-1]['cost'])) * int(cleannums):
                device = data.get('device')
                pay = round(float(cleannum(dic[index-1]['cost'])) * int(cleannums), 2)
                BotDB.add(key='rub', where='id_user', meaning=message.from_user.id, num=-pay)
                add_2dot_data(key=f'quantity_{device}', where='id_company', meaning=message.from_user.id, table='dev_software', add=int(cleannums), where_data='lvl', meaning_data=str(index), add_data='quantity')  
                await message.answer(get_text('buy_device2.3', format=False), reply_markup=keyboard_default.company_dev_software())
                await company_dev_software.Q1.set()
            else:
                await message.answer(get_text('buy_device2.4', format=False))
        else:
            await message.answer(get_text('buy_device2.5', format=False))
    else:
        await message.answer(get_text('buy_device2.2', format=False))


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'device' and call.data.split(':')[0] == 'sell', state=company_dev_software.Q1)
@ban_call(state=True)
@last_tap_call('-', state=True)
async def sell_device1(call: CallbackQuery, state: FSMContext):
    index =int(call.data.split(':')[3]) + 1
    device = call.data.split(':')[2]
    async with state.proxy() as data:
        data['index'] = index
        data['device'] = device
    if get_2dot_data(key=f'quantity_{device}', where='id_company', meaning=call.from_user.id, table='dev_software', where_data='lvl', meaning_data=str(index), get_data='quantity') > 0:
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
        await bot.send_message(call.from_user.id, get_text('sell_device1.1', format=False), reply_markup=keyboard_default.cancel())
        await company_dev_software.Q8.set()
    else:
        await call.answer(get_text('sell_device1.2'), show_alert=True)


@dp.message_handler(state=company_dev_software.Q8)
@ban(state=True)
@last_tap('-', state=True)
async def sell_device2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('sell_device2.1', format=False), reply_markup=keyboard_default.company_dev_software())
        await company_dev_software.Q1.set()    
    elif cleannum(message.text).isdigit():
        cleannums = cleannum(message.text)
        data = await state.get_data()
        index = data.get('index')
        device = data.get('device')
        dic = data.get('l')
        if get_2dot_data(key=f'quantity_{device}', where='id_company', meaning=message.from_user.id, table='dev_software', where_data='lvl', meaning_data=str(index), get_data='quantity') >= int(cleannums):
            percent_back = BotDB.vCollector(where='name', meaning='percent_back_money_device', table='value_it')
            pay = round(float(cleannum(dic[index-1]['cost'])) * int(cleannums) * percent_back, 2)
            BotDB.add(key='rub', where='id_user', meaning=message.from_user.id, num=pay)
            add_2dot_data(key=f'quantity_{device}', where='id_company', meaning=message.from_user.id, table='dev_software', add=-int(cleannums), where_data='lvl', meaning_data=str(index), add_data='quantity')  
            await message.answer(get_text('sell_device2.3', format=False), reply_markup=keyboard_default.company_dev_software())
            await company_dev_software.Q1.set()
        else:
            await message.answer(get_text('sell_device2.4', format=False))
    else:
        await message.answer(get_text('sell_device2.2', format=False))

# #########################################

@dp.message_handler(content_types=['text'])
@ban()
@error_reg
@last_tap(button='anytext')
async def anytext(message: Message):
    await message.answer(get_text(unique_name='anytext', format=False), reply_markup=keyboard_default.main_page())


