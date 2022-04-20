from pprint import pprint
import time
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import types
from classes import DevSoftware
from dispatcher import dp, bot
from bot import BotDB
from db import User
from keyboards.default import keyboard_default
from keyboards.inline import keyboard_inline
from aiogram.types import CallbackQuery
from all_function import *
from all_states import *
import math


# #########################################

@dp.message_handler(Command("start"), state='*')
@ban(state=True)
@last_tap(button='start', state=True)
async def start_menu(message: Message, state: FSMContext):
    id_user = message.from_user.id
    await state.finish()
    # проверяем пользователя на существование в БД
    if (not BotDB.user_exists(id_user)):
        BotDB.add_user(id_user)
        # проверяем пользователя на приглашение
        try:
            id_referrer = int(message.get_args())
            BotDB.get(key='id_user', where='id_user', meaning=id_referrer)
            if id_referrer == id_user:
                await message.answer(get_text('you_dont_be_refferer_himself', format=False))
            else:
                BotDB.updateN(key='referrer', where='id_user', meaning=id_user, num=id_referrer)
        except Exception as e:
            pass
        
        # проверяем пользователя на наличие username
        username = message.from_user.mention

        # if message.from_user.username is not None:
        #     username = f'@{message.from_user.username}' 
        # else:
        #     username = 'Нет'

        # записываем все полученые данные о пользователе в БД
        BotDB.updateT(key='username', where='id_user', meaning=id_user, text=username)  # запись username
        BotDB.updateT(key='name', where='id_user', meaning=id_user, text=message.from_user.full_name.strip())  # запись имени

        # спрашиваем про никнейм
        await message.answer(get_text('start_menu1', format=False), reply_markup=ReplyKeyboardRemove())
        await game_beginning.Q1.set()
    elif check_emptys(id_user):
        clean_error_reg_company(message.from_user.id)
        await message.answer(get_text('exist_user1', format=False), reply_markup=ReplyKeyboardRemove()) 
    else:
        await message.answer(get_text('start_menu2', format=False),reply_markup=keyboard_default.main_page())


@dp.message_handler(state=game_beginning.Q1)
@last_tap(button='-')
async def q1(message: Message):
    if 2 > len(message.text) or len(message.text) > BotDB.vCollector(table='value_main', where='name', meaning='max_symbols_name'):
        await message.answer(get_text('q1_1', format=False))
    elif check_on_simbols(message.text) > 0:
        await message.answer(get_text('q1_2', format=False))
    elif check_nickname(message.text):
        await message.answer(get_text('q1_3', format=False))
    else:
        # запись nickname(псевдонима)
        BotDB.updateT(key='nickname', where='id_user', meaning=message.from_user.id, text=message.text)
        # спрашиваем сферу
        await message.answer(get_text('q1_4', format=False), reply_markup=keyboard_default.fields())
        await game_beginning.Q2.set()



@dp.message_handler(state=game_beginning.Q2)
@last_tap(button='-')
async def q2(message: Message):
    text1 = get_text('q2_1', format=False)
    if message.text == get_button('f1'):
        await message.answer(text1, reply_markup=keyboard_default.types_it())
        await game_beginning.Q3.set()
    elif message.text == get_button('f2'):
        await message.answer(text1, reply_markup=keyboard_default.types_services())
        await game_beginning.Q3.set()
    elif message.text == get_button('f3'):
        await message.answer(text1, reply_markup=keyboard_default.types_product())
        await game_beginning.Q3.set()
    elif message.text == get_button('f4'):
        await message.answer(text1, reply_markup=keyboard_default.types_blackgold())
        await game_beginning.Q3.set()
    else:
        await message.answer(get_text('q2_2', format=False))


@dp.message_handler(state=game_beginning.Q3)
@last_tap(button='-')
async def q3(message: Message):
    if message.text == get_button('*1'):
        await message.answer(get_text('q2_2', format=False), reply_markup=keyboard_default.fields())
        await game_beginning.Q2.set()
    else:
        # проверяем пользователя на обход системы
        # l = list(map(lambda x: x.strip(),BotDB.get(key='text_box1',where='name',meaning='types_field',table='value_main').split(',')))
        try:
            BotDB.get(key='number', where='name', meaning=message.text, table='button_name')
            answ = True
        except:
            answ = False
        if answ:
            # записываем тип деятельности в БД
            BotDB.updateT(key='type_of_activity', where='id_user', meaning=message.from_user.id, text=BotDB.get(key='en', where='name', meaning=message.text, table='button_name'))
            BotDB.add_company(message.from_user.id, BotDB.get(key='en', where='name', meaning=message.text, table='button_name'))
            # спрашиваем имя компании
            await message.answer(get_text('q3_1', format=False), reply_markup=ReplyKeyboardRemove())
            await game_beginning.Q4.set()
        else:
            await message.answer(get_text('q2_1', format=False))


@dp.message_handler(state=game_beginning.Q4)
@last_tap(button='-', state=True)
async def q4(message: Message, state: FSMContext):
    user = User(message.from_user.id)
    if 3 > len(message.text) or len(message.text) > BotDB.vCollector(table='value_main', where='name', meaning='max_symbols_name_company'):
        await message.answer(get_text('q4_1', format=False))
    elif check_on_simbols(message.text) > 0:
        await message.answer(get_text('q4_2', format=False))
    elif check_name_company(message.text):
        await message.answer(get_text('q4_3', format=False))
    else:
        BotDB.updateT(table=user.type_of_activity, key='name_company', where='id_company', meaning=user.id, text=message.text)
        date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
        BotDB.updateT(key='date_reg', where='id_user', meaning=user.id, text=date)  # регистрируем дату создания аккаунта юзера
        # можно изменить удаление кнопок на edit_reply_markup вроде как 
        await message.answer(get_text('q4_4', format=False),reply_markup=ReplyKeyboardRemove())
        # главное меню
        await message.answer(get_text('q4_5', format=False), reply_markup=keyboard_default.main_page())
        await state.finish()


@dp.message_handler(Command("manual"))
@ban()
@error_reg
@last_tap('manual')
async def game_manual(message: Message):
    await message.answer(get_text('game_manual', format=False))

@dp.message_handler(Command("test"))
async def game_manual(message: Message):
    await message.answer(get_text('test_viev', format=False), reply_markup=keyboard_inline.test_viev())


@dp.message_handler(Command("reg"))
@ban()
@last_tap('reg')
async def error_regg(message: Message):
    if check_emptys(message.from_user.id):
        # проверяем пользователя на существование в БД
        if(not BotDB.user_exists(message.from_user.id)):
            BotDB.add_user(message.from_user.id)
            # проверяем пользователя на наличие username
            username = message.from_user.mention

            # if message.from_user.username is not None:
            #     username = f'@{message.from_user.username}' 
            # else:
            #     username = 'Нет'

            # записываем все полученые данные о пользователе в БД
            BotDB.updateT(key='username', where='id_user', meaning=message.from_user.id, text=username)  # запись username
            BotDB.updateT(key='name', where='id_user', meaning=message.from_user.id, text=message.from_user.full_name.strip())  # запись имени

        # спрашиваем про никнейм
        await message.answer(get_text('error_reg', format=False))
        await game_beginning.Q1.set()
    else:
        await message.answer(get_text('error_regg', format=False))


@dp.message_handler(Command('items'))
@ban()
@error_reg
@last_tap('items')
async def items_menu(message: Message):
    await message.answer(get_text('items_menu', format=False), reply_markup=keyboard_inline.get_items())

@dp.message_handler(Text('test'))
async def crt_table(message: Message):
    await message.answer(message.from_user.mention)

@dp.message_handler(Text(equals=get_button('1')))
@ban()
@error_reg
@last_tap('account')
async def account_user(message: Message):
    id_user = message.from_user.id
    pic = get_photo('account')
    rub = BotDB.get(key='rub', where='id_user', meaning=id_user)
    usd = BotDB.get(key='usd', where='id_user', meaning=id_user)
    btc = BotDB.get(key='btc', where='id_user', meaning=id_user)
    text = get_text('account_user1', {'rub':shell_num(rub), 'usd':shell_num(usd), 'btc':shell_num(btc, "btc")})
    await message.answer_photo(pic, text)



@dp.message_handler(Text(equals=get_button('2')))
@ban()
@error_reg
@last_tap('bank')
async def bank(message: Message):
    id_user = message.from_user.id
    pic = get_photo('bank')
    usd = BotDB.get(key='usd', where='id_user', meaning=id_user)
    btc = BotDB.get(key='btc', where='id_user', meaning=id_user)
    rub = BotDB.get(key='rub', where='id_user', meaning=id_user)
    rate_usd = BotDB.vCollector(table='value_main', where='name', meaning='rate_usd')
    rate_btc = BotDB.vCollector(table='value_main', where='name', meaning='rate_btc')
    time_ = time.strftime('%X').split()[0]
    sec = 60 - int(time_.split(':')[2])
    percent_usd = BotDB.get(key='perc_usd', where='rate_usd_now', meaning=rate_usd, table='graf_rate_usd')
    percent_btc = BotDB.get(key='perc_btc', where='rate_btc_now', meaning=rate_btc, table='graf_rate_btc')
    str_with_sign_usd = f'{emodziside(percent_usd)}({shell_num(percent_usd)}%)'
    str_with_sign_btc = f'{emodziside(percent_btc)}({shell_num(percent_btc)}%)'
    d = {
        'sec':sec,
        'rub':shell_num(rub),
        'usd':shell_num(usd),
        'btc':shell_num(btc, "btc"),
        'rate_usd':shell_num(rate_usd),
        'rate_btc':shell_num(rate_btc),
        'percent_usd': str_with_sign_usd,
        'percent_btc': str_with_sign_btc
        }
    text = get_text('bank1', d)
    await message.answer_photo(pic, text, reply_markup=keyboard_inline.update_and_convert())


@dp.callback_query_handler(Text(equals='update'), state='*')
@ban_call()
@error_reg_call
@last_tap_call('update')
async def bank2(call: CallbackQuery):
    await call.answer(cache_time=0.7)
    id_user = call.from_user.id
    usd = BotDB.get(key='usd', where='id_user', meaning=id_user)
    btc = BotDB.get(key='btc', where='id_user', meaning=id_user)
    rub = BotDB.get(key='rub', where='id_user', meaning=id_user)
    rate_usd = BotDB.vCollector(table='value_main', where='name', meaning='rate_usd')
    rate_btc = BotDB.vCollector(table='value_main', where='name', meaning='rate_btc')
    time_ = time.strftime('%X').split()[0]
    sec = 60 - int(time_.split(':')[2])
    percent_usd = BotDB.get(key='perc_usd', where='rate_usd_now', meaning=rate_usd, table='graf_rate_usd')
    percent_btc = BotDB.get(key='perc_btc', where='rate_btc_now', meaning=rate_btc, table='graf_rate_btc')
    str_with_sign_usd = f'{emodziside(percent_usd)}({shell_num(percent_usd)}%)'
    str_with_sign_btc = f'{emodziside(percent_btc)}({shell_num(percent_btc)}%)'
    d = {
        'sec':sec,
        'rub':shell_num(rub),
        'usd':shell_num(usd),
        'btc':shell_num(btc, "btc"),
        'rate_usd':shell_num(rate_usd),
        'rate_btc':shell_num(rate_btc),
        'percent_usd': str_with_sign_usd,
        'percent_btc': str_with_sign_btc
        }
    text = get_text('bank1', d)
    try:
        await bot.edit_message_caption(message_id=call.message.message_id, chat_id=id_user, caption=text,
                                       reply_markup=keyboard_inline.update_and_convert())
    except Exception as e:
        pass


@dp.callback_query_handler(Text(equals='ru'))
@ban_call()
@error_reg_call
@last_tap_call('rub_usd')
async def rub_usd1(call: CallbackQuery):
    await call.answer(cache_time=1)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, get_text('rub_usd1', format=False), reply_markup=keyboard_default.exchange())
    await exchange_rub_usd.Q1.set()


@dp.message_handler(state=exchange_rub_usd.Q1)
@last_tap('-', state=True)
async def rub_usd2(message: Message, state: FSMContext):
    rub = BotDB.get(key='rub', where='id_user', meaning=message.from_user.id)
    percent_bank = BotDB.vCollector(table='value_main', where='name', meaning='percent_bank')
    try:
        num = round(float(message.text), 2)
        if num <= rub:
            
            usd = currency_calculation(num)
            exchange_balans(message.from_user.id,round(-usd,2))
            usd_with_fee = usd - usd * percent_bank
            BotDB.add(key='usd', where='id_user', meaning=message.from_user.id, num=round(usd_with_fee, 2))
            BotDB.add(key='rub', where='id_user', meaning=message.from_user.id, num=-num)
            d = {
                'percent_bank':int(percent_bank * 100),
                'get_bank':shell_num(usd * percent_bank),
                'get_user':shell_num(usd_with_fee)
                }
            await message.answer(get_text('rub_usd2', d), reply_markup=keyboard_default.main_page())
            await state.finish()
        else:
            await message.answer(get_text('rub_usd3', format=False),reply_markup=keyboard_default.exchange())
    except Exception as e:
        if message.text == get_button('2.1'):
            if rub != 0:
                usd = currency_calculation(rub)
                exchange_balans(message.from_user.id,round(-usd, 2))
                usd_with_fee = usd - usd * percent_bank
                BotDB.add(key='usd', where='id_user', meaning=message.from_user.id, num=round(usd_with_fee, 2))
                BotDB.updateN(key='rub', where='id_user', meaning=message.from_user.id, num=0)
                d = {
                    'percent_bank':int(percent_bank * 100),
                    'get_bank':shell_num(usd * percent_bank),
                    'get_user':shell_num(usd_with_fee)
                    }
                await message.answer(get_text('rub_usd2', d), reply_markup=keyboard_default.main_page())
                
                await state.finish()
                
            else:
                await message.answer(get_text('rub_usd3', format=False),reply_markup=keyboard_default.main_page())
                await state.finish()
                
        elif message.text == get_button('2.2'):
            await message.answer(get_text('rub_usd4', format=False), reply_markup=keyboard_default.main_page())
            await state.finish()
            
        else:
            await message.answer(get_text('rub_usd5', format=False),reply_markup=keyboard_default.exchange())


@dp.callback_query_handler(Text(equals='ur'))
@ban_call()
@error_reg_call
@last_tap_call('usd_rub')
async def usd_rub1(call: CallbackQuery):
    await call.answer(cache_time=1)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, get_text('usd_rub1', format=False),reply_markup=keyboard_default.exchange())
    await exchange_usd_rub.Q1.set()
    


@dp.message_handler(state=exchange_usd_rub.Q1)
@last_tap('-', state=True)
async def usd_rub2(message: Message, state: FSMContext):
    usd = BotDB.get(key='usd', where='id_user', meaning=message.from_user.id)
    percent_bank = BotDB.vCollector(table='value_main', where='name', meaning='percent_bank')
    try:
        num = round(float(message.text), 2)
        if num <= usd:
            
            
            rub = currency_calculation(num, what_calculate='usd_in_rub')
            exchange_balans(message.from_user.id,num)  # usd+
            rub_with_fee = rub - rub * percent_bank
            BotDB.add(key='rub', where='id_user', meaning=message.from_user.id, num=round(rub_with_fee, 2))
            BotDB.add(key='usd', where='id_user', meaning=message.from_user.id, num=-num)
            d = {
                'percent_bank':int(percent_bank * 100),
                'get_bank':shell_num(rub * percent_bank),
                'get_user':shell_num(rub_with_fee)
                }
            await message.answer(get_text('usd_rub2', d), reply_markup=keyboard_default.main_page())
            await state.finish()
            
        else:
            await message.answer(get_text('usd_rub3', format=False),reply_markup=keyboard_default.exchange())
    except Exception as e:
        if message.text == get_button('2.1'):
            if usd != 0:
                
                rub = currency_calculation(usd, what_calculate='usd_in_rub')
                exchange_balans(message.from_user.id,usd)  # usd+
                rub_with_fee = rub - rub * percent_bank
                BotDB.add(key='rub', where='id_user', meaning=message.from_user.id, num=round(rub_with_fee, 2))
                BotDB.updateN(key='usd', where='id_user', meaning=message.from_user.id, num=0)
                d = {
                    'percent_bank':int(percent_bank * 100),
                    'get_bank':shell_num(rub * percent_bank),
                    'get_user':shell_num(rub_with_fee)
                    }
                await message.answer(get_text('usd_rub2', d), reply_markup=keyboard_default.main_page())
                
                await state.finish()
                
            else:
                await message.answer(get_text('usd_rub3', format=False), reply_markup=keyboard_default.main_page())
                await state.finish()
                
        elif message.text == get_button('2.2'):
            await message.answer(get_text('usd_rub4', format=False), reply_markup=keyboard_default.main_page())
            await state.finish()
            
        else:
            await message.answer(get_text('usd_rub5', format=False), reply_markup=keyboard_default.exchange())


@dp.callback_query_handler(Text(equals='ub'))
@ban_call()
@error_reg_call
@last_tap_call('usd_btc')
async def usd_btc1(call: CallbackQuery):
    usd = BotDB.get(key='usd', where='id_user', meaning=call.from_user.id)
    rate_btc = BotDB.vCollector(table='value_main', where='name', meaning='rate_btc')
    if usd > rate_btc / 10:
        await call.answer(cache_time=1)
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
        await bot.send_message(call.from_user.id, get_text('usd_btc1', format=False),
                               reply_markup=keyboard_default.exchange())
        await exchange_usd_btc.Q1.set()
        
    else:
        await bot.send_message(call.from_user.id, get_text('usd_btc2', format=False))


@dp.message_handler(state=exchange_usd_btc.Q1)
@last_tap('-', state=True)
async def usd_btc2(message: Message, state: FSMContext):
    percent_bank = BotDB.vCollector(table='value_main', where='name', meaning='percent_bank')
    usd = BotDB.get(key='usd', where='id_user', meaning=message.from_user.id)
    rate_btc = BotDB.vCollector(table='value_main', where='name', meaning='rate_btc')
    try:
        num = round(float(message.text), 2)
        if num > rate_btc / 10:
            if num <= usd:
                btc = currency_calculation(num, what_calculate='usd_in_btc', currency='rate_btc')
                exchange_balans(message.from_user.id,num)  # usd+
                exchange_balans(message.from_user.id,-btc ,'rate_btc')  # btc-
                btc_with_fee = btc - btc * percent_bank
                BotDB.add(key='btc', where='id_user', meaning=message.from_user.id, num=round(btc_with_fee, 5))
                BotDB.add(key='usd', where='id_user', meaning=message.from_user.id, num=-num)
                d = {
                    'percent_bank':int(percent_bank * 100),
                    'get_bank':shell_num(btc * percent_bank, "btc"),
                    'get_user':shell_num(btc_with_fee, "btc")
                    }
                await message.answer(get_text('usd_btc3', d), reply_markup=keyboard_default.main_page()) 
                await state.finish()
                
            else:
                await message.answer(get_text('usd_btc4', format=False), reply_markup=keyboard_default.exchange())
        else:
            await message.answer(get_text('usd_btc5', format=False))
            await message.answer(get_text('usd_btc6', format=False))
    except Exception as e:
        if message.text == get_button('2.1'):
            if usd > rate_btc / 10:
                btc = currency_calculation(usd, what_calculate='usd_in_btc', currency='rate_btc')
                exchange_balans(message.from_user.id,usd)  # usd+
                exchange_balans(message.from_user.id,-btc ,'rate_btc')  # btc-
                btc_with_fee = btc - btc * percent_bank
                BotDB.add(key='btc', where='id_user', meaning=message.from_user.id, num=round(btc_with_fee, 5))
                BotDB.updateN(key='usd', where='id_user', meaning=message.from_user.id, num=0)
                d = {
                    'percent_bank':int(percent_bank * 100),
                    'get_bank':shell_num(btc * percent_bank, "btc"),
                    'get_user':shell_num(btc_with_fee, "btc")
                    }
                await message.answer(get_text('usd_btc3', d), reply_markup=keyboard_default.main_page()) 
                await state.finish()
                
            else:
                await message.answer(get_text('usd_btc7', format=False))
                await state.finish()
                
        elif message.text == get_button('2.2'):
            await message.answer(get_text('usd_btc8', format=False), reply_markup=keyboard_default.main_page())
            await state.finish()
            
        else:
            await message.answer(get_text('usd_btc9', format=False), reply_markup=keyboard_default.exchange())


@dp.callback_query_handler(Text(equals='bu'))
@ban_call()
@error_reg_call
@last_tap_call('btc_usd')
async def btc_usd1(call: CallbackQuery):
    await call.answer(cache_time=1)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, get_text('btc_usd1', format=False), reply_markup=keyboard_default.exchange())
    await exchange_btc_usd.Q1.set()
   


@dp.message_handler(state=exchange_btc_usd.Q1)
@last_tap('-', state=True)
async def btc_usd2(message: Message, state: FSMContext):
    percent_bank = BotDB.vCollector(table='value_main', where='name', meaning='percent_bank')
    btc = BotDB.get(key='btc', where='id_user', meaning=message.from_user.id)
    try:
        num = round(float(message.text), 5)
        if num <= btc:
            usd = currency_calculation(num, what_calculate='btc_in_usd', currency='rate_btc')
            exchange_balans(message.from_user.id,-usd)  # usd-
            exchange_balans(message.from_user.id,num ,'rate_btc')  # btc+
            usd_with_fee = usd - usd * percent_bank
            BotDB.add(key='usd', where='id_user', meaning=message.from_user.id, num=round(usd_with_fee, 2))
            BotDB.add(key='btc', where='id_user', meaning=message.from_user.id, num=-num)
            d = {
                'percent_bank':int(percent_bank * 100),
                'get_bank':shell_num(usd * percent_bank),
                'get_user':shell_num(usd_with_fee)
                }
            await message.answer(get_text('btc_usd2', d), reply_markup=keyboard_default.main_page()) 
            await state.finish()
            
        else:
            await message.answer(get_text('btc_usd3', format=False), reply_markup=keyboard_default.exchange())
    except Exception as e:
        if message.text == get_button('2.1'):
            if btc > 0:
                usd = currency_calculation(btc, what_calculate='btc_in_usd', currency='rate_btc')
                exchange_balans(message.from_user.id,-usd)  # usd-
                exchange_balans(message.from_user.id,btc ,'rate_btc')  # btc+
                usd_with_fee = usd - usd * percent_bank
                BotDB.add(key='usd', where='id_user', meaning=message.from_user.id, num=round(usd_with_fee, 2))
                BotDB.updateN(key='btc', where='id_user', meaning=message.from_user.id, num=0)
                d = {
                    'percent_bank':int(percent_bank * 100),
                    'get_bank':shell_num(usd * percent_bank),
                    'get_user':shell_num(usd_with_fee)
                    }
                await message.answer(get_text('btc_usd2', d), reply_markup=keyboard_default.main_page())   
                await state.finish()
                
            else:
                await message.answer(get_text('btc_usd4', format=False),
                                     reply_markup=keyboard_default.main_page())
                await state.finish()
                
        elif message.text == get_button('2.2'):
            await message.answer(get_text('btc_usd5', format=False), reply_markup=keyboard_default.main_page())
            await state.finish()
            
        else:
            await message.answer(get_text('btc_usd6', format=False), reply_markup=keyboard_default.exchange())

########################################

@dp.message_handler(Text(equals=get_button('3')))
@ban()
@error_reg
@last_tap('-')
async def menu_stocks(message: Message):
    await message.answer(get_text('menu_stocks', format=False), reply_markup=keyboard_default.menu_stocks())

########################################


@dp.message_handler(Text(equals=get_button('3.1')))
@ban()
@error_reg
@last_tap('-')
async def stock_market(message: Message):
    data = BotDB.get_alls('id_company, name_company, count_stocks_stay, price_one_stocks', table='stocks')
    count_page = len([i for i in data if i[2] != 0])/BotDB.vCollector(where='name', meaning='count_string_in_one_page_stocks', table='value_main')
    d = {
        'list_stocks': list_stocks(),
        'page': 1,
        'count_page': math.ceil(count_page)
        }
    keyboard = keyboard_inline.buy_stocks() if math.ceil(count_page) == 1 else keyboard_inline.forward_page_stocks(1)
    await message.answer(get_text('stock_market', format=True, d=d), reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'forward' and call.data.split(':')[0] == 'stocks')
@ban_call()
@error_reg_call
@last_tap_call('-')
async def forward_page_stocks(call: CallbackQuery):
    page = int(call.data.split(':')[2]) + 1
    data = BotDB.get_alls('id_company, name_company, count_stocks_stay, price_one_stocks', table='stocks')
    count_page = len([i for i in data if i[2] != 0])/BotDB.vCollector(where='name', meaning='count_string_in_one_page_stocks', table='value_main')
    if page == 1:
        keyboard = keyboard_inline.forward_page_stocks(page)
    elif page == math.ceil(count_page):
        keyboard = keyboard_inline.back_page_stocks(page)
    else:
        keyboard = keyboard_inline.back_forward_page_stocks(page)
    d = {
        'list_stocks': list_stocks(page),
        'page': page,
        'count_page': math.ceil(count_page)
        }
    await bot.edit_message_text(text=get_text('stock_market', format=True, d=d), chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'back' and call.data.split(':')[0] == 'stocks')
@ban_call()
@error_reg_call
@last_tap_call('-')
async def back_page_stocks(call: CallbackQuery):
    page = int(call.data.split(':')[2]) - 1
    data = BotDB.get_alls('id_company, name_company, count_stocks_stay, price_one_stocks', table='stocks')
    count_page = len([i for i in data if i[2] != 0])/BotDB.vCollector(where='name', meaning='count_string_in_one_page_stocks', table='value_main')
    if page == 1:
        keyboard = keyboard_inline.forward_page_stocks(page)
    elif page == math.ceil(count_page):
        keyboard = keyboard_inline.back_page_stocks(page)
    else:
        keyboard = keyboard_inline.back_forward_page_stocks(page)
    d = {
        'list_stocks': list_stocks(page),
        'page': page,
        'count_page': math.ceil(count_page)
        }
    await bot.edit_message_text(text=get_text('stock_market', format=True, d=d), chat_id=call.from_user.id,message_id=call.message.message_id, reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'buy' and call.data.split(':')[0] == 'stocks')
@ban_call()
@error_reg_call
@last_tap_call('-')
async def buy_stocks1(call: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=call.from_user.id,message_id=call.message.message_id)
    await bot.send_message(call.from_user.id, get_text('buy_stocks1.1', format=False), reply_markup=keyboard_default.cancel())
    await stocks.Q4.set()

@dp.message_handler(state=stocks.Q4)
@last_tap('-', state=True)
async def buy_stocks2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif message.text.isdigit():
        if message.from_user.id != int(message.text):
            try:
                price_one_stocks = BotDB.get(key='price_one_stocks', where='id_company', meaning=int(message.text), table='stocks')
                async with state.proxy() as data:
                    data['id_company'] = int(message.text)
                    data['price_one_stocks'] = price_one_stocks
                    await message.answer(get_text('buy_stocks2.1', format=False))
                await stocks.Q5.set()
            except:
                await message.answer(get_text('buy_stocks2.2', format=False))
        else:
            await message.answer(get_text('buy_stocks2.4', format=False))
    else:
        await message.answer(get_text('buy_stocks2.3', format=False))

@dp.message_handler(state=stocks.Q5)
@last_tap('-', state=True)
async def buy_stocks3(message: Message, state: FSMContext):
    user = User(message.from_user.id)
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif cleannum(message.text).isdigit():
        cleannums = cleannum(message.text)
        data = await state.get_data()
        id_company = data.get('id_company')
        price_one_stocks = data.get('price_one_stocks')
        if int(cleannums) * price_one_stocks < user.usd:
            if BotDB.get(key='count_stocks_stay', where='id_company', meaning=id_company, table='stocks') - int(cleannums) >= 0:

                pay = round(int(cleannums) * price_one_stocks, 2)
                BotDB.add(key='usd', where='id_user', meaning=user.id, num=-pay)

                BotDB.add(key='count_stocks_stay', where='id_company', meaning=id_company, table='stocks', num=-int(cleannums))

                if True in list(map(lambda x: True if int(id_company) in x else False, parse_2dot_data(table='users', key='briefcase', where='id_user', meaning=user.id))):
                    add_2dot_data(table='users', key='briefcase', where='id_user', meaning=user.id, where_data='id_company', meaning_data=str(id_company), add_data='quantity_stocks', add=int(cleannums))
                else:
                    name_company = BotDB.get(key='name_company', where='id_company', meaning=id_company, table='stocks')
                    d = [f'{id_company}', f'{name_company}', f'{cleannums}', f'{price_one_stocks}']
                    create_2dot_data(table='users', key='briefcase', where='id_user', meaning=user.id, headers=['id_company', 'name_company', 'quantity_stocks', 'price_buy'], d = d)
                
                update_rating_stocks(id_company)

                await message.answer(get_text('buy_stocks3.1', format=False), reply_markup=keyboard_default.menu_stocks())
                await state.finish()
            else:
                await message.answer(get_text('buy_stocks3.2', format=False))
        else:
            await message.answer(get_text('buy_stocks3.3', format=False))
    else:
        await message.answer(get_text('buy_stocks3.4', format=False))

########################################

@dp.message_handler(Text(equals=get_button('3.2')))
@ban()
@error_reg
@last_tap('-')
async def my_stocks(message: Message):
    try:
        d = {
            'count_stocks_stay': shell_num(BotDB.get(key='count_stocks_stay', where='id_company', meaning=message.from_user.id, table='stocks')),
            'price_one_stocks': shell_num(BotDB.get(key='price_one_stocks', where='id_company', meaning=message.from_user.id, table='stocks'))
            }
        await message.answer(get_text('my_stocks', format=True, d=d))
    except:
        await message.answer(get_text('create_first_stocks', format=False), reply_markup=keyboard_inline.create_first_stocks())

@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'create_first_stocks' and call.data.split(':')[0] == 'stocks')
@ban_call()
@error_reg_call
@last_tap_call('-')
async def create_first_stocks1(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id, get_text('create_first_stocks1.1', format=False), reply_markup=keyboard_default.cancel())
    await stocks.Q1.set()

@dp.message_handler(state=stocks.Q1)
@last_tap('-', state=True)
async def create_first_stocks2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif message.text.isdigit():
        if int(message.text) <= BotDB.vCollector(table='value_main', where='name', meaning='percent_stocks_max') and int(message.text) >= BotDB.vCollector(table='value_main', where='name', meaning='percent_stocks_min'):
            async with state.proxy() as data:
                data['piece_of_income'] = int(message.text)/100
            await message.answer(get_text('create_first_stocks2.1', format=False))
            await stocks.Q2.set()
        else:
            await message.answer(get_text('create_first_stocks2.2', format=False))
    else:
        await message.answer(get_text('create_first_stocks2.3', format=False))
    
@dp.message_handler(state=stocks.Q2)
@last_tap('-', state=True)
async def create_first_stocks3(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif message.text.isdigit():
        if int(message.text) <= BotDB.vCollector(table='value_main', where='name', meaning='count_stocks_max') and int(message.text) >= BotDB.vCollector(table='value_main', where='name', meaning='count_stocks_min'):
            async with state.proxy() as data:
                data['count_stocks'] = int(message.text)
            await message.answer(get_text('create_first_stocks3.1', format=False))
            await stocks.Q3.set()
        else:
            await message.answer(get_text('create_first_stocks3.2', format=False))
    else:
        await message.answer(get_text('create_first_stocks3.3', format=False))

@dp.message_handler(state=stocks.Q3)
@last_tap('-', state=True)
async def create_first_stocks4(message: Message, state: FSMContext):
    user = User(message.from_user.id)
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif message.text.isdigit() or isfloat(message.text):
        if round(float(message.text),2) > BotDB.vCollector(where='name', meaning=f'min_price_stocks', table='value_main'):
            data = await state.get_data()
            piece_of_income = data.get('piece_of_income')
            count_stocks = data.get('count_stocks')
            name_company = BotDB.get(key=f'name_company', where='id_company', meaning=user.id, table=user.type_of_activity)
            BotDB.add_stocks(id_company=user.id, name_company=name_company, piece_of_income=piece_of_income, count_stocks=count_stocks, count_stocks_stay=count_stocks, price_one_stocks=round(float(message.text), 2) if isfloat(message.text) else int(message.text), seller=user.id)
            await message.answer(get_text('create_first_stocks4.1', format=False), reply_markup=keyboard_default.menu_stocks())
            await state.finish()
        else:
            await message.answer(get_text('create_first_stocks4.2', format=False))
    else:
        await message.answer(get_text('create_first_stocks4.3', format=False))

########################################

@dp.message_handler(Text(equals=get_button('3.3')))
@ban()
@error_reg
@last_tap('-')
async def menu_briefcase(message: Message):
    d = {'stocks': get_your_stocks(message.from_user.id)}
    await message.answer(get_text('menu_briefcase', format=True, d=d), reply_markup=keyboard_inline.menu_briefcase())

@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'sell_stocks' and call.data.split(':')[0] == 'briefcase')
@ban_call()
@error_reg_call
@last_tap_call('-')
async def briefcase_sell_stocks1(call: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=call.from_user.id,message_id=call.message.message_id)
    await bot.send_message(call.from_user.id, get_text('briefcase_sell_stocks1.1', format=False), reply_markup=keyboard_default.cancel())
    await stocks.Q6.set()

@dp.message_handler(state=stocks.Q6)
@last_tap('-', state=True)
async def briefcase_sell_stocks2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif message.text.isdigit():
        if message.from_user.id != int(message.text):
            try:
                # name = BotDB.get(key='name_company', where='id_company', meaning=int(message.text), table='stocks')
                async with state.proxy() as data:
                    data['id_company'] = int(message.text)
                    await message.answer(get_text('briefcase_sell_stocks2.1', format=False))
                await stocks.Q7.set()
            except: 
                await message.answer(get_text('briefcase_sell_stocks2.5', format=False))
        else:
            await message.answer(get_text('briefcase_sell_stocks2.4', format=False))
    else:
        await message.answer(get_text('briefcase_sell_stocks2.3', format=False))

@dp.message_handler(state=stocks.Q7)
@last_tap('-', state=True)
async def briefcase_sell_stocks3(message: Message, state: FSMContext):
    user = User(message.from_user.id)
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif cleannum(message.text).isdigit():
        cleannums = cleannum(message.text)
        data = await state.get_data()
        id_company = data.get('id_company')
        price_one_stocks = BotDB.get(key='price_one_stocks', where='id_company', meaning=id_company, table='stocks')
        count_stocks_my = get_2dot_data(table='users', key='briefcase', where='id_user', meaning=user.id, where_data='id_company', meaning_data=str(id_company), get_data='quantity_stocks')
        count_stocks_company = BotDB.get(key='count_stocks', where='id_company', meaning=id_company, table='stocks')
        if int(count_stocks_my) - int(cleannums) >= 0:
            delete_2dot_data(table='users', key='briefcase', where='id_user', meaning=user.id, unique_value_data=str(id_company)) if int(count_stocks_my) - int(cleannums) == 0 else add_2dot_data(table='users', key='briefcase', where='id_user', meaning=user.id, where_data='id_company', meaning_data=str(id_company), add_data='quantity_stocks', add=-int(cleannums))
            piece_of_income = BotDB.get(key='piece_of_income', where='id_company', meaning=id_company, table='stocks')
            price_one_stocks = BotDB.get(key='price_one_stocks', where='id_company', meaning=id_company, table='stocks')      
            name_company = BotDB.get(key=f'name_company', where='id_company', meaning=message.from_user.id, table=user.type_of_activity)
            BotDB.add_stocks(id_company=user.id, name_company=name_company, piece_of_income=piece_of_income, count_stocks=count_stocks_company, count_stocks_stay=int(cleannums), price_one_stocks=price_one_stocks, seller=int(id_company))
            await message.answer(get_text('briefcase_sell_stocks3.1', format=False), reply_markup=keyboard_default.menu_stocks())
            await state.finish()
        else:
            await message.answer(get_text('briefcase_sell_stocks3.3', format=False))
    else:
        await message.answer(get_text('briefcase_sell_stocks3.4', format=False))


########################################

@dp.message_handler(Text(equals=get_button('5')))
@ban()
@error_reg
@last_tap('trends')
async def trends_menu(message: Message):
    await message.answer(get_text('trends_menu', format=False), reply_markup=keyboard_inline.trends_menu_())


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'voting' and call.data.split(':')[0] == 'trends')
@last_tap_call('-')
async def voting_menu(call: CallbackQuery):
    await bot.edit_message_text(get_text('voting_menu', format=False), chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=keyboard_inline.all_voting_company(call.from_user.id))

@dp.message_handler(Text(equals=get_button('6')))
@ban()
@error_reg
@last_tap('referal')
async def referal_invite(message: Message):
    oneseven = BotDB.vCollector(table='value_main', where='name', meaning='oneseven')
    award_referrer = BotDB.vCollector(table='value_main', where='name', meaning='award_referrer')  # награда того кто пригласил(реферрер)
    award_referral = BotDB.vCollector(table='value_main', where='name', meaning='award_referral')  # награда реферала перешедшего по ссылке
    d = {
            'oneseven':oneseven,
            'award_referrer':shell_num(award_referrer),
            'award_referral':shell_num(award_referral),
            'referrer_linc':referrer_linc(message.from_user.id),
            'get_user_referals':BotDB.get_user_referals(message.from_user.id)[1]
        }
    await message.answer(get_text('referal_invite1', d))

# @dp.message_handler(Text(equals='rrr'))
# @ban()
# @error_reg
# @last_tap('-')
# async def tetst(message: Message):
#     await message.answer(message.content_type)  

@dp.message_handler(Text(equals=get_button('7')))
@ban()
@error_reg
@last_tap('bonus')
async def bonus(message: Message):
    await message.answer(get_text('bonus1', format=False))  

def company_keyboard(id_user):
    type_of_activity = BotDB.get(key='type_of_activity', where='id_user', meaning=id_user)
    keyboard = keyboard_default.company_dev_software()
    if type_of_activity == 'dev_software':
        user = DevSoftware(id_user)
        d = {
            'name_company': user.user.company_name,
            'profit': 'profit',
            'income': 'income',
            'expense': 'expense',
            'count_place': user.quantity_all_places,
            'count_dev': user.quantity_all_devs,
            'count_device': user.quantity_devices 
            }
        text_menu = get_text('company_dev_software', format=True, d=d)
        keyboard = keyboard_default.company_dev_software()
    elif type_of_activity == '':
        pass
    elif type_of_activity == '':
        pass
    elif type_of_activity == '':
        pass
    elif type_of_activity == '':
        pass
    elif type_of_activity == '':
        pass
    elif type_of_activity == '':
        pass
    elif type_of_activity == '':
        pass
    elif type_of_activity == '':
        pass
    elif type_of_activity == '':
        pass
    return keyboard, text_menu


@dp.message_handler(Text(equals=get_button('8')))
@ban()
@error_reg
@last_tap('company')
async def company(message: Message):
    keyboard, text = company_keyboard(message.from_user.id)
    await message.answer(get_text('company', format=True, d={'text': text}),reply_markup=keyboard)
    await company_dev_software.Q1.set() 

@dp.message_handler(Text(equals=get_button('9')))
@ban()
@error_reg
@last_tap('forbs')
async def forbs(message: Message):
    await message.answer(get_text('forbs', format=False), reply_markup=keyboard_default.forbs())


@dp.message_handler(Text(equals=get_button('10')))
@ban()
@error_reg
@last_tap('setting')
async def setting(message: Message):
    await message.answer(get_text('setting', format=False), reply_markup=keyboard_default.user_setting())

# ######

@dp.message_handler(Text(equals=get_button('10.2')))
@ban()
@error_reg
@last_tap('change_nickname')
async def change_nickname(message: Message):
    amount_of_changes = BotDB.get(key='amount_of_changes_nickname', where='id_user', meaning=message.from_user.id)
    await message.answer(get_text('change_nickname', format=True, d={'amount_of_changes':amount_of_changes}), reply_markup=keyboard_inline.changes_nickname())

@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'change_nickname' and call.data.split(':')[0] == 'support')
@last_tap_call('inline_change_nickname')
async def change_nickname1(call: CallbackQuery):
    if BotDB.get(key='amount_of_changes_nickname', where='id_user', meaning=call.from_user.id) > 0:
        await bot.delete_message(message_id=call.message.message_id, chat_id=call.from_user.id)
        await bot.send_message(call.from_user.id, text=get_text('change_nickname1.1', format=False), reply_markup=keyboard_default.cancel())
        await Change_Nickname.Q1.set()
    else:
        await call.answer(text=get_text('change_nickname1.2'), show_alert=True)

@dp.message_handler(state=Change_Nickname.Q1)
@last_tap(button='-', state=True)
async def change_nickname2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('setting', format=False), reply_markup=keyboard_default.user_setting())
        await state.finish()
    elif 2 > len(message.text) and len(message.text) < BotDB.vCollector(table='value_main', where='name', meaning='max_symbols_name'):
        await message.answer(get_text('q1_1', format=False))
    elif check_on_simbols(message.text) > 0:
        await message.answer(get_text('q1_2', format=False))
    elif check_nickname(message.text):
        await message.answer(get_text('q1_3', format=False))
    else:
        async with state.proxy() as data:
            data['answer'] = message.text
        await message.answer(get_text('change_nickname2', format=False))
        await Change_Nickname.Q2.set()
    
@dp.message_handler(state=Change_Nickname.Q2)
@last_tap(button='-', state=True)
async def change_nickname3(message: Message, state: FSMContext):
    data = await state.get_data()
    answer = data.get('answer')
    if message.text == get_button('*2'):
        await message.answer(get_text('setting', format=False), reply_markup=keyboard_default.user_setting())
        await state.finish()
    elif answer == message.text:
        # запись nickname(псевдонима)
        await message.answer(get_text('change_nickname3.1', format=False), reply_markup=keyboard_default.user_setting())
        BotDB.add(key='amount_of_changes_nickname', where='id_user', meaning=message.from_user.id, num=-1)
        BotDB.updateT(key='nickname', where='id_user', meaning=message.from_user.id, text=message.text)
        await state.finish()
    else:
        await message.answer(get_text('change_nickname3.2', format=False))

# ######

@dp.message_handler(Text(equals=get_button('10.3')))
@ban()
@error_reg
@last_tap('contact_support')
async def contact_support(message: Message):
    await message.answer(get_text('contact_support', format=False), reply_markup=keyboard_default.cancel())
    await Contact_Support.Q1.set()

@dp.message_handler(state=Contact_Support.Q1)
@last_tap('-', state=True)
async def contact_support1(message: Message, state: FSMContext):
    id_user = message.from_user.id
    if message.text == get_button('*2'):
        await message.answer(get_text('setting', format=False), reply_markup=keyboard_default.user_setting())
        await state.finish()
    else:
        teg = taG()
        date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
        d={
            'user': f'<a href="tg://user?id={id_user}">{BotDB.get(key="nickname", where="id_user", meaning=id_user)}</a>',
            'date': date,
            'text': message.text,
            'tag': teg
        }
        BotDB.add_support_message(tag=teg, id_user=id_user, info_message=get_text('message_in_chat_support', format=True, d=d), message=message.text)
        await bot.send_message(BotDB.vCollector(table='value_main', where='name', meaning='id_chat_support'), get_text('message_in_chat_support', format=True, d=d), reply_markup=keyboard_inline.i_am_take(teg))
        
        await message.answer(get_text('contact_support1.2', format=False), reply_markup=keyboard_default.user_setting())
        await state.finish()

@dp.callback_query_handler(Text(contains='i_am_take'))
@last_tap_call('-')
async def answer_button(call: CallbackQuery):
    id_user = call.from_user.id
    teg = call.data.split(':')[1]
    await bot.delete_message(message_id=call.message.message_id, chat_id=BotDB.vCollector(table='value_main', where='name', meaning='id_chat_support'))
    await bot.send_message(id_user, BotDB.get(key='info_message', where='tag', meaning=teg, table='message_in_support'), reply_markup=keyboard_inline.give_an_answer(teg))


@dp.callback_query_handler(Text(contains='give_an_answer'))
@last_tap_call('-', state=True)
async def answer_button(call: CallbackQuery, state: FSMContext):
    id_user = call.from_user.id
    teg = call.data.split(':')[1]
    async with state.proxy() as data:
        data['tag'] = teg
    await bot.edit_message_text(text=call.message.text ,message_id=call.message.message_id, chat_id=call.from_user.id)
    await bot.send_message(id_user, get_text('answer_button', format=False), reply_markup=keyboard_default.cancel_answer())
    await Contact_Support.Q2.set()


@dp.message_handler(state=Contact_Support.Q2)
@last_tap('-', state=True)
async def answer_button1(message: Message, state: FSMContext):
    id_user = message.from_user.id
    data = await state.get_data()
    teg = data.get('tag')
    if message.text == get_button('*3'):
        # возвращаем удоленное сообщение рание в чат теч. поддержки
        await bot.send_message(BotDB.vCollector(table='value_main', where='name', meaning='id_chat_support'), BotDB.get(key='info_message', where='tag', meaning=teg, table='message_in_support'), reply_markup=keyboard_inline.i_am_take(teg))
        # отправляем сообщение ответчику
        await message.answer(get_text('answer_button1.1',format=False), reply_markup=keyboard_default.main_page())
        await state.finish()
    else:
        text = BotDB.get(key='message', where='tag', meaning=teg, table='message_in_support')
        d = {
            'text':text,
            'answer':message.text
        }
        # отправляем ответ юзеру
        await bot.send_message(BotDB.get(key='id_user', where='tag', meaning=teg, table='message_in_support'), get_text('answer_button1.2',format=True, d=d))
        # отправляем ответчику сообщение о том что его ответ доставлен юзеру
        await message.answer(get_text('answer_button1.3',format=False), reply_markup=keyboard_default.main_page())
        date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
        d = {
            'message': BotDB.get(key='info_message', where='tag', meaning=teg, table='message_in_support'),
            'respondent': f'<a href="tg://user?id={id_user}">{message.from_user.full_name}</a>',
            'answer': message.text,
            'date': date
        }
        # отправляем в чат тех. поддержки всю информацию о вопросе и ответе, юзере и ответчике
        await bot.send_message(BotDB.vCollector(table='value_main', where='name', meaning='id_chat_support'), get_text('answer_button1.4',format=True, d=d))
        await state.finish()

# ######

@dp.message_handler(Text(equals=get_button('*1')))
@ban()
@error_reg
@last_tap('back')
async def back(message: Message):
    await message.answer(get_text('back', format=False),reply_markup=keyboard_default.main_page())

@dp.message_handler(content_types=['photo'], state='*')
async def ph(message: Message):
    await message.answer(message.photo[-1].file_id)

# @dp.message_handler(Text('poll'))
# async def send_poll(message: Message):
#     await message.answer_poll('How', ['good', 'bad'], is_anonymous=False)

# @dp.poll_answer_handler()
# async def anytext(poll_answer: types.PollAnswer):
#     pprint((poll_answer.poll_id))










