from asyncio import sleep
from decimal import getcontext
import math
import time
from pprint import pprint

from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, ContentType

from all_function import *
from all_states import *
from classes import DevSoftware, User
from dispatcher import BotDB, bot, dp
from keyboards.default import keyboard_default
from keyboards.inline import keyboard_inline
from aiogram.types import BotCommand


# #########################################

@dp.message_handler(Command("start"), state='*')
@tech_break(state=True)
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
    elif check_nickname(message.from_user.id, message.text):
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
@tech_break()
@ban()
@error_reg()
@last_tap('manual')
async def game_manual(message: Message):
    await message.answer(get_text('game_manual', format=False))


@dp.message_handler(Command("reg"))
@tech_break()
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
@tech_break()
@ban()
@error_reg()
@last_tap('items')
async def items_menu(message: Message):
    await message.answer(get_text('items_menu', format=False), reply_markup=keyboard_inline.get_items())


@dp.message_handler(Text(equals=get_button('1')))
@tech_break()
@ban()
@error_reg()
@last_tap('account')
async def account_user(message: Message):
    user = User(message.from_user.id)
    # pic = get_photo('account')
    d = {
        'nickname': user.nickname,
        'name_company': user.company_name,
        'rub':shell_num(user.rub),
        'usd':shell_num(user.usd),
        'btc':shell_num(user.btc, q_signs_after_comma=5)
    }
    await message.answer(get_text('account_user1', d=d))



@dp.message_handler(Text(equals=get_button('2')))
@tech_break()
@ban()
@error_reg()
@last_tap('bank')
async def bank(message: Message):
    user = User(message.from_user.id)
    pic = get_photo('bank')
    rub, usd, btc = user.rub, user.usd, user.btc
    time_ = time.strftime('%X').split()[0]
    sec = 60 - int(time_.split(':')[2])
    rate_usd, rate_btc = [BotDB.vCollector(table='value_main', where='name', meaning=i) for i in ['rate_usd', 'rate_btc']]
    tag_usd, tag_btc = [BotDB.get(key='text_box2', where='name', meaning=f'{i}_unique_id', table='value_main') for i in ['rate_usd', 'rate_btc']]
    percent_usd = BotDB.get(key='perc_usd', where='id', meaning=tag_usd, table='graf_rate_usd')
    percent_btc = BotDB.get(key='perc_btc', where='id', meaning=tag_btc, table='graf_rate_btc')
    znak_u = '+' if percent_usd > 0 else ''
    znak_b = '+' if percent_btc > 0 else ''
    str_with_sign_usd = f'{emodziside(percent_usd)}({znak_u}{shell_num(percent_usd)}%)'
    str_with_sign_btc = f'{emodziside(percent_btc)}({znak_b}{shell_num(percent_btc)}%)'
    d = {
        'sec':sec,
        'rub':shell_num(rub),
        'usd':shell_num(usd),
        'btc':shell_num(btc, q_signs_after_comma=5),
        'rate_usd':shell_num(rate_usd),
        'rate_btc':shell_num(rate_btc),
        'percent_usd': str_with_sign_usd,
        'percent_btc': str_with_sign_btc
        }
    text = get_text('bank1', d)
    await message.answer_photo(pic, text, reply_markup=keyboard_inline.update_and_convert())


@dp.callback_query_handler(Text(equals='update'), state='*')
@tech_break_call()
@ban_call()
@error_reg_call()
@last_tap_call('update')
async def bank2(call: CallbackQuery):
    await call.answer(cache_time=0.7)
    user = User(call.from_user.id)
    rub, usd, btc = user.rub, user.usd, user.btc
    time_ = time.strftime('%X').split()[0]
    sec = 60 - int(time_.split(':')[2])
    rate_usd, rate_btc = [BotDB.vCollector(table='value_main', where='name', meaning=i) for i in ['rate_usd', 'rate_btc']]
    tag_usd, tag_btc = [BotDB.get(key='text_box2', where='name', meaning=f'{i}_unique_id', table='value_main') for i in ['rate_usd', 'rate_btc']]
    percent_usd = BotDB.get(key='perc_usd', where='id', meaning=tag_usd, table='graf_rate_usd')
    percent_btc = BotDB.get(key='perc_btc', where='id', meaning=tag_btc, table='graf_rate_btc')
    znak_u = '+' if percent_usd > 0 else ''
    znak_b = '+' if percent_btc > 0 else ''
    str_with_sign_usd = f'{emodziside(percent_usd)}({znak_u}{shell_num(percent_usd)}%)'
    str_with_sign_btc = f'{emodziside(percent_btc)}({znak_b}{shell_num(percent_btc)}%)'
    d = {
        'sec':sec,
        'rub':shell_num(rub),
        'usd':shell_num(usd),
        'btc':shell_num(btc, q_signs_after_comma=5),
        'rate_usd':shell_num(rate_usd),
        'rate_btc':shell_num(rate_btc),
        'percent_usd': str_with_sign_usd,
        'percent_btc': str_with_sign_btc
        }
    text = get_text('bank1', d)
    try:
        await bot.edit_message_caption(message_id=call.message.message_id, chat_id=user.id, caption=text,
                                       reply_markup=keyboard_inline.update_and_convert())
    except Exception as e:
        pass


@dp.callback_query_handler(Text(equals=['rub_usd', 'usd_rub', 'usd_btc', 'btc_usd']))
@tech_break(state=True)
@ban_call(state=True)
@error_reg_call(state=True)
@last_tap_call('-', state=True)
async def exchange_currency1(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, get_text(f'{call.data}_exchange_currency1', format=False), reply_markup=keyboard_default.exchange())
    async with state.proxy() as data:
        data['currency'] = call.data
    await exchange_currency.Q1.set()


@dp.message_handler(state=exchange_currency.Q1)
@last_tap('-', state=True)
async def exchange_currency2(message: Message, state: FSMContext):
    user = User(message.from_user.id)
    data = await state.get_data()
    left, right = data.get('currency').split('_')
    signs_after_comma1 = 5 if left == 'btc' else 2
    signs_after_comma2 = 5 if right == 'btc' else 2
    left_sign, right_sign = [1, -1]
    percent_bank = BotDB.vCollector(table='value_main', where='name', meaning='percent_bank', wNum=user.weight.get_weight('percent_bank'), perc=True)
    if cleannum(message.text).isdigit() or isfloat(cleannum(message.text)):
        num = round(float(cleannum(message.text)), signs_after_comma1)
        if num < 0:
            await message.answer(get_text('exchange_currency2.condition1', format=False),reply_markup=keyboard_default.exchange())
            return
        if num == 0:
            await message.answer(get_text('exchange_currency2.condition2', format=False),reply_markup=keyboard_default.exchange())
            return
        if num > BotDB.get(key=left, where='id_user', meaning=user.id):
            await message.answer(get_text('exchange_currency2.condition3', format=False),reply_markup=keyboard_default.exchange())
            return
        if num < 1 and right == 'btc':
            await message.answer(get_text('exchange_currency2.condition4', format=False),reply_markup=keyboard_default.exchange())
            return
        if right == 'rub' or left == 'rub':
            currency, rate = currency_calculation(num, f'{left}_in_{right}')
            sign = 1 if right == 'rub' else -1
            exchange_balans(id_user=user.id, count_money=currency * sign)
        else:
            currency, rate = currency_calculation(num, f'{left}_in_{right}', currency='rate_btc')
            exchange_balans(id_user=user.id, count_money=currency * left_sign, type_currency=f'rate_{left}')
            exchange_balans(id_user=user.id, count_money=currency * right_sign,  type_currency=f'rate_{right}')
        currency_with_fee = round(currency * (1 - percent_bank), signs_after_comma2)
        BotDB.add(key=left, where='id_user', meaning=user.id, num=-num)
        BotDB.add(key=right, where='id_user', meaning=user.id, num=currency_with_fee)
        d = {
            'rate_exchange': shell_num(rate),
            'percent_bank':shell_num(percent_bank * 100),
            'get_bank':shell_num(currency * percent_bank, q_signs_after_comma=signs_after_comma2),
            'get_user':shell_num(currency_with_fee, q_signs_after_comma=signs_after_comma2)
            }
        await message.answer(get_text(f'exchange_currency2.3{left}_{right}', d), reply_markup=keyboard_default.main_page())
        await state.finish()    
    elif message.text == get_button('2.1'):
        num = BotDB.get(key=left, where='id_user', meaning=user.id)
        if num == 0:
            await message.answer(get_text('exchange_currency2.condition2', format=False),reply_markup=keyboard_default.main_page())
            await state.finish()
            return
        if right == 'rub' or left == 'rub':
            currency, rate = currency_calculation(num, f'{left}_in_{right}')
            sign = 1 if right == 'rub' else -1
            exchange_balans(id_user=user.id, count_money=currency * sign)
        else:
            currency, rate = currency_calculation(num, f'{left}_in_{right}', currency='rate_btc')
            exchange_balans(id_user=user.id, count_money=currency * left_sign, type_currency=f'rate_{left}')
            exchange_balans(id_user=user.id, count_money=currency * right_sign,  type_currency=f'rate_{right}')
        currency_with_fee = round(currency * (1 - percent_bank), signs_after_comma2)
        BotDB.updateN(key=left, where='id_user', meaning=user.id, num=0)
        BotDB.add(key=right, where='id_user', meaning=user.id, num=currency_with_fee)
        d = {
            'rate_exchange': shell_num(rate),
            'percent_bank':shell_num(percent_bank * 100),
            'get_bank':shell_num(currency * percent_bank, q_signs_after_comma=signs_after_comma2),
            'get_user':shell_num(currency_with_fee, q_signs_after_comma=signs_after_comma2)
            }
        await message.answer(get_text(f'exchange_currency2.3{left}_{right}', d), reply_markup=keyboard_default.main_page())
        await state.finish()
                
    elif message.text == get_button('2.2'):
        await message.answer(get_text('exchange_currency2.1', format=False), reply_markup=keyboard_default.main_page())
        await state.finish()
        
    else:
        await message.answer(get_text('exchange_currency2.2', format=False),reply_markup=keyboard_default.exchange())

########################################

@dp.message_handler(Text(equals=get_button('3')))
@tech_break()
@ban()
@error_reg()
@last_tap('-')
async def menu_stocks(message: Message):
    await message.answer(get_text('menu_stocks', format=False), reply_markup=keyboard_default.menu_stocks())

########################################

@dp.message_handler(Text(equals=get_button('3.2')))
@tech_break()
@ban()
@error_reg()
@last_tap('-')
async def my_stocks(message: Message):
    user = User(message.from_user.id)
    if stocks_exist(user.id):
        d = {
            'total_stocks': shell_num(all:= get_total_quantity_stocks(user.id)),
            'quantity_stocks_currently': shell_num(curr:= get_quantity_stocks_currently(user.id)),
            'price_one_stock': shell_num(get_price_one_stock(user.id)),
            'bought_stocks': shell_num(all - curr),
            'total_income_from_stocks': shell_num(user.total_income_from_stocks),
            'curr': get_curr_stock(user.id)
            }
        name_text = 'my_stocks'
        keyboard = keyboard_inline.split_stocks() if enable_split(user.id) else None
        if poll_status_extend_stocks(user.id):
            info = parse_2dot_data(table='users', key='info_for_extend_stocks', where='id_user', meaning=user.id)[-1]
            responses = parse_2dot_data(table='users', key='poll_responses', where='id_user', meaning=user.id)[1:]
            d['q_sendmess_user'] = info[2]
            d['q_responses'] = len(responses)
            name_text = 'my_stocks_poll_extend_stocks'
        return await message.answer(get_text(name_text, format=True, d=d), reply_markup=keyboard)
    await message.answer(get_text('create_stocks', format=False), reply_markup=keyboard_inline.create_stocks())

@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'extend_quantity_stocks' and call.data.split(':')[0] == 'stocks')
@tech_break_call()
@ban_call()
@error_reg_call()
@last_tap_call('-')
async def extend_quantity_stocks1(call: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, get_text('extend_quantity_stocks1.1', format=False), reply_markup=keyboard_default.cancel())
    await extend_quantity_stocks.Q1.set()

@dp.message_handler(state=extend_quantity_stocks.Q1)
@last_tap('-', state=True)
async def extend_quantity_stocks2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks', format=False), reply_markup=keyboard_default.menu_stocks())
        await my_stocks(message=message)
        await state.finish()
    elif cleannum(message.text).isdigit() or isfloat(cleannum(message.text)):
        if isfloat(cleannum(message.text)):
            return await message.answer(get_text('extend_quantity_stocks2.condition1', format=False))

        user = User(message.from_user.id)
        num = int(cleannum(message.text))

        if (BotDB.vCollector(table='value_main', where='name', meaning='count_stocks_min') > num) | (num > BotDB.vCollector(table='value_main', where='name', meaning='count_stocks_max')):
            return await message.answer(get_text('extend_quantity_stocks2.condition2', format=False)) 

        total_quantity_stocks = get_total_quantity_stocks(user.id)
        percent_q_stocks_up = (total_quantity_stocks + num) * 100 / total_quantity_stocks - 100
        perc_cost_stocks = 0.8 if percent_q_stocks_up >= 80 else percent_q_stocks_up/100
        cost_stocks = get_price_one_stock(user.id) * (1 - perc_cost_stocks)
        confirmation_comunity = 'yes' if percent_q_stocks_up > 25 else 'no'
        curr = get_curr_stock(user.id)
        d = {
            'percent_q_stocks_up': shell_num(percent_q_stocks_up),
            'cost_stocks': shell_num(cost_stocks),
            'confirmation_comunity': confirmation_comunity,
            'curr': curr
        }
        async with state.proxy() as data:
            data['quantity_stocks'] = num
            data['confirmation_comunity'] = percent_q_stocks_up > 25
            data['cost_stocks'] = cost_stocks
        await message.answer(get_text('extend_quantity_stocks2.1', format=True, d=d), reply_markup=keyboard_inline.confirm_extension())
    else:
        return await message.answer(get_text('extend_quantity_stocks2.2', format=False)) 

@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'confirm_extension' and call.data.split(':')[0] == 'stocks', state=extend_quantity_stocks.Q1)
@last_tap_call('-', state=True)
async def extend_quantity_stocks3(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=0.2)
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    data = await state.get_data()
    num = data.get('quantity_stocks')
    cost_stocks = data.get('cost_stocks')
    user = User(call.from_user.id)
    BotDB.updateN(key='quantity_split', where='id_user', meaning=user.id, num=0)
    if not data.get('confirmation_comunity'):
        percent_of_income = BotDB.get(table='stocks', key='percent_of_income', where='id_stocks AND seller', meaning=call.from_user.id)
        percent_total = get_total_quantity_stocks(user.id) * percent_of_income
        BotDB.add(table='stocks', key='quantity_stocks', where='id_stocks AND seller', meaning=user.id, num=num)
        new_percent_of_income = percent_total/get_total_quantity_stocks(user.id)
        BotDB.updateN(table='stocks', key='percent_of_income', where='id_stocks AND seller', meaning=user.id, num=new_percent_of_income)
        update_relative_perc_users(user.id)
        d = [get_date_now(h=False, m=False, s=False), round(cost_stocks, 2)]
        create_2dot_data(table='stocks', key='price_one_stock', where='id_stocks AND seller', meaning=user.id, d=d)
        d = [0, 0, 0, 0, 0]
        create_2dot_data(key='info_for_extend_stocks', where='id_user', meaning=user.id, d=d)
        await bot.send_message(call.from_user.id, get_text('extend_quantity_stocks3.1', format=False), reply_markup=keyboard_default.menu_stocks())
        return await state.finish()

    users: list = get_all_stocksholder(call.from_user.id)
    quantity_exception = len(users) * 3
    q_all_user = len(users)
    exception_ = 0
    set_exception = set()
    while users and exception_ <= quantity_exception:
        try:
            t = get_text('extend_quantity_stocks3.2', format=False)
            mess = await bot.send_message(chat_id=users[-1], text=t, reply_markup=keyboard_inline.poll_extend_stocks(user.id))
            await bot.pin_chat_message(chat_id=users[-1], message_id=mess.message_id)
            users.pop()
            await sleep(0.3)
        except Exception:
            _ = users.pop()
            users.insert(0, _)
            set_exception.add(_)
            exception_ += 1
    if set_exception:
        for i in set_exception:
            q_stocks_all = get_total_quantity_stocks(int(user.id))
            q_stocks_ihave = get_2dot_data(table='users', key='briefcase', where='id_user', meaning=i, meaning_data=user.id, where_data='id_stocks', get_data='quantity_stocks')
            q_stocks_ihave = 0 if q_stocks_ihave is None else q_stocks_ihave
            weight_response = q_stocks_ihave * 100 / q_stocks_all / 2
            d = [i, weight_response]
            create_2dot_data(table='users', key='poll_responses', where='id_user', meaning=user.id, d=d)
    q_sendmess_user = q_all_user - len(users)
    d = [num, round(cost_stocks, 2), q_sendmess_user, q_all_user, 1]
    create_2dot_data(table='users', key='info_for_extend_stocks', where='id_user', meaning=user.id, d=d)
    d = {'q_sendmess_user': shell_num(q_sendmess_user),
        'q_all_user': shell_num(q_all_user)}
    await bot.send_message(call.from_user.id, get_text('extend_quantity_stocks3.3', format=True, d=d), reply_markup=keyboard_default.menu_stocks())
    await state.finish()

@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'poll' and call.data.split(':')[0] == 'stocks', state='*')
@tech_break_call()
@ban_call()
@error_reg_call()
@last_tap_call('-')
async def poll_extend_stocks(call: CallbackQuery):
    await call.answer(cache_time=0.2)
    response, id_stocks = call.data.split(':')[2:]
    user_ = User(call.from_user.id)
    q_stocks_all = get_total_quantity_stocks(int(id_stocks))
    q_stocks_ihave = get_2dot_data(table='users', key='briefcase', where='id_user', meaning=user_.id, meaning_data=id_stocks, where_data='id_stocks', get_data='quantity_stocks')
    q_stocks_ihave = 0 if q_stocks_ihave is None else q_stocks_ihave
    weight_response = q_stocks_ihave * 100 / q_stocks_all
    weight_response = weight_response if response == 'yes' else -weight_response
    d = [call.from_user.id, weight_response]
    create_2dot_data(table='users', key='poll_responses', where='id_user', meaning=id_stocks, d=d)
    responses = parse_2dot_data(table='users', key='poll_responses', where='id_user', meaning=id_stocks)[1:]
    info_for_extend_stocks = parse_2dot_data(table='users', key='info_for_extend_stocks', where='id_user', meaning=id_stocks)[-1]
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=user_.id, text=get_text('poll_extend_stocks.1', format=False), reply_markup=None)
    await bot.unpin_chat_message(message_id=call.message.message_id, chat_id=user_.id)
    if len(responses) == info_for_extend_stocks[2]:
        # za = len([i[1] for i in responses if i[1] == 'yes'])
        # protiv = len(responses) - za
        all_weight_response = sum(i[1] for i in responses) 

        if all_weight_response < 0:
            update_2dot_data(table='users', key='info_for_extend_stocks', where='id_user', meaning=id_stocks, update_data='poll_status', where_data='poll_status', meaning_data='1', num='0')
            BotDB.updateT(key='poll_responses', where='id_user', meaning=id_stocks, text='id_user:weight_response')
            BotDB.updateN(key='quantity_split', where='id_user', meaning=id_stocks, num=1)
            return await bot.send_message(chat_id=id_stocks, text=get_text('poll_extend_stocks.3', format=False))

        percent_of_income = BotDB.get(table='stocks', key='percent_of_income', where='id_stocks AND seller', meaning=id_stocks)
        percent_total = get_total_quantity_stocks(int(id_stocks)) * percent_of_income
        BotDB.add(table='stocks', key='quantity_stocks', where='id_stocks AND seller', meaning=id_stocks, num=info_for_extend_stocks[0])
        new_percent_of_income = percent_total/get_total_quantity_stocks(int(id_stocks))
        BotDB.updateN(table='stocks', key='percent_of_income', where='id_stocks', meaning=id_stocks, num=new_percent_of_income)
        update_relative_perc_users(id_stocks)
        d = [get_date_now(h=False, m=False, s=False), round(info_for_extend_stocks[1], 2)]
        create_2dot_data(table='stocks', key='price_one_stock', where='id_stocks AND seller', meaning=id_stocks, d=d)
        BotDB.updateT(key='poll_responses', where='id_user', meaning=id_stocks, text='id_user:weight_response')
        update_2dot_data(table='users', key='info_for_extend_stocks', where='id_user', meaning=id_stocks, update_data='poll_status', where_data='poll_status', meaning_data='1', num='0')
        await bot.send_message(id_stocks, get_text('poll_extend_stocks.2', format=False), reply_markup=keyboard_default.menu_stocks())
            
        

@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'create_stocks' and call.data.split(':')[0] == 'stocks')
@tech_break_call()
@ban_call()
@error_reg_call()
@last_tap_call('-')
async def create_stocks1(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id, get_text('create_stocks1.1', format=False), reply_markup=keyboard_default.cancel())
    await stocks.Q1.set()

@dp.message_handler(state=stocks.Q1)
@last_tap('-', state=True)
async def create_stocks2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif cleannum(message.text).isdigit():
        num = int(cleannum(message.text))
        if (BotDB.vCollector(table='value_main', where='name', meaning='percent_stocks_min') > num) | (num > BotDB.vCollector(table='value_main', where='name', meaning='percent_stocks_max')):
            return await message.answer(get_text('create_stocks2.condition', format=False))

        async with state.proxy() as data:
                data['percent_of_income'] = num/100
        await message.answer(get_text('create_stocks9.1', format=False), reply_markup=keyboard_default.choice_curr())
        await stocks.Q9.set()
    else:
        await message.answer(get_text('create_stocks2.3', format=False))

@dp.message_handler(state=stocks.Q9)
@last_tap('-', state=True)
async def create_stocks9(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif message.text in [get_button('3.1.1'), get_button('3.1.2')]:
        curr = 'rub' if message.text == get_button('3.1.1') else 'usd'
        async with state.proxy() as data:
                data['currency'] = curr
        await message.answer(get_text('create_stocks2.1', format=False), reply_markup=ReplyKeyboardRemove())
        await stocks.Q2.set()
    else:
        await message.answer(get_text('create_stocks9.3', format=False))


@dp.message_handler(state=stocks.Q2)
@last_tap('-', state=True)
async def create_stocks3(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif cleannum(message.text).isdigit():
        num = int(cleannum(message.text))
        if (BotDB.vCollector(table='value_main', where='name', meaning='count_stocks_min') > num) | (num > BotDB.vCollector(table='value_main', where='name', meaning='count_stocks_max')):
            return await message.answer(get_text('create_stocks3.condition', format=False))     
        async with state.proxy() as data:
                data['quantity_stocks'] = num
        await message.answer(get_text('create_stocks3.1', format=False))
        await stocks.Q3.set()
    else:
        await message.answer(get_text('create_stocks3.3', format=False))

@dp.message_handler(state=stocks.Q3)
@last_tap('-', state=True)
async def create_stocks4(message: Message, state: FSMContext):
    user = User(message.from_user.id)
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif cleannum(message.text).isdigit() or isfloat(cleannum(message.text)):
        num = round(float(cleannum(message.text)), 2)
        if num < BotDB.vCollector(where='name', meaning='min_price_stocks', table='value_main'):
            return await message.answer(get_text('create_stocks4.condition', format=False))
        
        data = await state.get_data()
        currency = data.get('currency')
        percent_of_income = data.get('percent_of_income')
        quantity_stocks = data.get('quantity_stocks')
        percent_for_one_stock = Decimal(str(percent_of_income)) / Decimal(str(quantity_stocks))
        tag = taG()
        BotDB.add_stocks(id_slot=tag, id_stocks=user.id, percent_of_income=float(percent_for_one_stock), quantity_stocks=quantity_stocks, seller=user.id, currency=currency)
        d = [get_date_now(h=False, m=False, s=False), num]
        create_2dot_data(table='stocks', key='price_one_stock', where='id_slot', meaning=tag, d = d)
        await message.answer(get_text('create_stocks4.1', format=False), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    else:
        await message.answer(get_text('create_stocks4.3', format=False))
    
# ########################################

@dp.message_handler(Text(equals=get_button('3.1')))
@tech_break()
@ban()
@error_reg()
@last_tap('-')
async def stock_market(message: Message):
    data = BotDB.get_all('quantity_stocks', table='stocks')
    if sum(data) == 0 or data == []:
        return await message.answer(get_text('do_not_exist_offers'))
    count_page = len([i for i in data if i != 0]) / BotDB.vCollector(where='name', meaning='count_string_in_one_page_stocks', table='value_main')
    d = {
        'list_stocks': list_stocks(),
        'page': 1,
        'count_page': math.ceil(count_page)
        }
    keyboard = keyboard_inline.buy_stocks() if math.ceil(count_page) == 1 else keyboard_inline.forward_page_stocks(1)
    await message.answer(get_text('stock_market', format=True, d=d), reply_markup=keyboard, disable_web_page_preview=True)

@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'forward' and call.data.split(':')[0] == 'stocks')
@tech_break_call()
@ban_call()
@error_reg_call()
@last_tap_call('-')
async def forward_page_stocks(call: CallbackQuery):
    page = int(call.data.split(':')[2]) + 1
    data = BotDB.get_all('quantity_stocks', table='stocks')
    count_page = len([i for i in data if i != 0]) / BotDB.vCollector(where='name', meaning='count_string_in_one_page_stocks', table='value_main')
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
@tech_break_call()
@ban_call()
@error_reg_call()
@last_tap_call('-')
async def back_page_stocks(call: CallbackQuery):
    page = int(call.data.split(':')[2]) - 1
    data = BotDB.get_all('quantity_stocks', table='stocks')
    count_page = len([i for i in data if i != 0]) / BotDB.vCollector(where='name', meaning='count_string_in_one_page_stocks', table='value_main')
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
@tech_break_call()
@ban_call()
@error_reg_call()
@last_tap_call('-')
async def buy_stocks1(call: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id, get_text('buy_stocks1.1', format=False), reply_markup=keyboard_default.cancel())
    await stocks.Q4.set()

@dp.message_handler(state=stocks.Q4)
@last_tap('-', state=True)
async def buy_stocks2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif message.text:
        try:
            id_slot = BotDB.get(key='id_slot', where='id_slot', meaning=message.text, table='stocks')
            seller = BotDB.get(key='seller', where='id_slot', meaning=message.text, table='stocks')
        except:
            return await message.answer(get_text('buy_stocks2.2', format=False))
            
        if seller == message.from_user.id:
            return await message.answer(get_text('buy_stocks2.condition', format=False))
            
        async with state.proxy() as data:
            data['seller'] = seller
            data['id_slot'] = id_slot
            data['price_one_stock'] = parse_2dot_data(key='price_one_stock', where='id_slot', meaning=id_slot, table='stocks')[-1][-1]
            data['id_stocks'] = BotDB.get(key='id_stocks', where='id_slot', meaning=id_slot, table='stocks')
            data['currency'] = BotDB.get(key='currency', where='id_slot', meaning=id_slot, table='stocks')
        await message.answer(get_text('buy_stocks2.1', format=False))
        await stocks.Q5.set()

@dp.message_handler(state=stocks.Q5)
@last_tap('-', state=True)
async def buy_stocks3(message: Message, state: FSMContext):
    user = User(message.from_user.id)
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif cleannum(message.text).isdigit():
        num = int(cleannum(message.text))
        data = await state.get_data()
        id_slot: str = data.get('id_slot')
        seller = data.get('seller')
        curr = data.get('currency')
        price_one_stock = data.get('price_one_stock')
        id_stocks = data.get('id_stocks')

        curr_money = user.rub if curr == 'rub' else user.usd

        if num * price_one_stock > curr_money:
            return await message.answer(get_text('buy_stocks3.condition1', format=False))

        if BotDB.get(key='quantity_stocks', where='id_slot', meaning=id_slot, table='stocks') - num < 0:
            return await message.answer(get_text('buy_stocks3.condition2', format=False))

        pay = round(num * price_one_stock, 2)
        BotDB.add(key=curr, where='id_user', meaning=user.id, num=-pay)

        BotDB.add(key='quantity_stocks', where='id_slot', meaning=id_slot, table='stocks', num=-num)
        user2 = User(id_stocks)

        id_slot_stocks_old = True in list(map(lambda x: id_slot in x, parse_2dot_data(table='users', key='briefcase', where='id_user', meaning=user.id)))


        if id_slot_stocks_old:
            add_2dot_data(table='users', key='briefcase', where='id_user', meaning=user.id, where_data='id_stocks', meaning_data=str(id_stocks), add_data='quantity_stocks', add=num)
            qs = get_2dot_data(table='users', key='briefcase', where='id_user', meaning=user.id, where_data='id_slot', meaning_data=id_slot, get_data='quantity_stocks')
            relative_perc = qs * BotDB.get(table='stocks', key='percent_of_income', where='id_slot', meaning=id_slot)
            update_2dot_data(table='users', key='briefcase', where='id_user', meaning=user.id, where_data='id_slot', meaning_data=id_slot, update_data='relative_perc', num=relative_perc)
        else:
            relative_perc = num * BotDB.get(table='stocks', key='percent_of_income', where='id_slot', meaning=id_slot)
            d = [id_slot, str(id_stocks), str(user2.company_name), str(num), str(price_one_stock), curr, relative_perc]

            create_2dot_data(table='users', key='briefcase', where='id_user', meaning=user.id, d = d)

        if seller == user2.id:
            BotDB.add(key='total_income_from_stocks', where='id_user', meaning=user2.id, num=pay)

        update_rating_stocks(id_slot)

        await message.answer(get_text('buy_stocks3.1', format=False), reply_markup=keyboard_default.menu_stocks())
        await state.finish()

    else:
        await message.answer(get_text('buy_stocks3.4', format=False))

########################################

@dp.message_handler(Text(equals=get_button('3.3')))
@tech_break()
@ban()
@error_reg()
@last_tap('-')
async def menu_briefcase(message: Message):
    if i_have_stocks(message.from_user.id): 
        d = {'stocks': get_your_stocks(message.from_user.id)}
        return await message.answer(get_text('menu_briefcase', format=True, d=d), reply_markup=keyboard_inline.menu_briefcase())
    await message.answer(get_text('menu_briefcase_empty', format=False))

@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'sell_stocks' and call.data.split(':')[0] == 'briefcase')
@tech_break_call()
@ban_call()
@error_reg_call()
@last_tap_call('-')
async def briefcase_sell_stocks1(call: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id, get_text('briefcase_sell_stocks1.1', format=False), reply_markup=keyboard_default.cancel())
    await stocks.Q6.set()

@dp.message_handler(state=stocks.Q6)
@last_tap('-', state=True)
async def briefcase_sell_stocks2(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif message.text:
        id_slot = get_2dot_data(table='users', key='briefcase', where='id_user', meaning=message.from_user.id, meaning_data=message.text, where_data='id_slot', get_data='id_slot')
        id_stocks = get_2dot_data(table='users', key='briefcase', where='id_user', meaning=message.from_user.id, meaning_data=message.text, get_data='id_stocks', where_data='id_slot')
        if id_slot is None:
            return await message.answer(get_text('briefcase_sell_stocks2.5', format=False))
        async with state.proxy() as data:
            data['id_slot'] = id_slot
            data['id_stocks'] = id_stocks
        await message.answer(get_text('briefcase_sell_stocks2.1', format=False))
        await stocks.Q7.set()

@dp.message_handler(state=stocks.Q7)
@last_tap('-', state=True)
async def briefcase_sell_stocks3(message: Message, state: FSMContext):
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif cleannum(message.text).isdigit() or isfloat(cleannum(message.text)):
        num = round(float(cleannum(message.text)), 2)
        if num == 0:
            return await message.answer(get_text('briefcase_sell_stocks3.condition1', format=False))
        if num < 0:
            return await message.answer(get_text('briefcase_sell_stocks3.condition2', format=False))
            
        async with state.proxy() as data:
            data['price_one_stock'] = num
        await message.answer(get_text('briefcase_sell_stocks3.1', format=False))
        await stocks.Q8.set()
    else:
        await message.answer(get_text('briefcase_sell_stocks3.4', format=False))

@dp.message_handler(state=stocks.Q8)
@last_tap('-', state=True)
async def briefcase_sell_stocks4(message: Message, state: FSMContext):
    user = User(message.from_user.id)
    if message.text == get_button('*2'):
        await message.answer(get_text('menu_stocks'), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    elif cleannum(message.text).isdigit():
        num = int(cleannum(message.text))
        data = await state.get_data()
        id_slot = data.get('id_slot')
        id_stocks = data.get('id_stocks')
        price_one_stock = data.get('price_one_stock')
        quantity_stocks = get_2dot_data(table='users', key='briefcase', where='id_user', meaning=user.id, where_data='id_slot', meaning_data=id_slot, get_data='quantity_stocks')
        tag = taG()
        curr = get_curr_stock(id_stocks)

        if int(quantity_stocks) - num < 0:
            return await message.answer(get_text('briefcase_sell_stocks4.condition1', format=False))
        if int(quantity_stocks) - num == 0:
            delete_2dot_data(table='users', key='briefcase', where='id_user', meaning=user.id, unique_value_data=id_slot)
        else:
            add_2dot_data(table='users', key='briefcase', where='id_user', meaning=user.id, where_data='id_slot', meaning_data=id_slot, add_data='quantity_stocks', add=-num)
    
        percent_of_income = BotDB.get(key='percent_of_income', where='id_stocks', meaning=id_stocks, table='stocks')     
        BotDB.add_stocks(id_slot=tag, id_stocks=id_stocks, percent_of_income=percent_of_income, quantity_stocks=num, currency=curr, seller=user.id)
        d = [get_date_now(h=False, m=False, s=False), price_one_stock]
        create_2dot_data(table='stocks', key='price_one_stock', where='id_slot', meaning=tag, d = d)
        await message.answer(get_text('briefcase_sell_stocks4.1', format=False), reply_markup=keyboard_default.menu_stocks())
        await state.finish()
    else:
        await message.answer(get_text('briefcase_sell_stocks4.4', format=False))


########################################

@dp.message_handler(Text(equals=get_button('5')))
@tech_break()
@ban()
@error_reg()
@last_tap('trends')
async def trends_menu(message: Message):
    await message.answer(get_text('trends_menu', format=False), reply_markup=keyboard_inline.trends_menu_())


@dp.callback_query_handler(lambda call: call.data.split(':')[1] == 'voting' and call.data.split(':')[0] == 'trends')
@last_tap_call('-')
async def voting_menu(call: CallbackQuery):
    await bot.edit_message_text(get_text('voting_menu', format=False), chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=keyboard_inline.all_voting_company(call.from_user.id))

# ###############################################

@dp.message_handler(Text(equals=get_button('6')))
@tech_break()
@ban()
@error_reg()
@last_tap('referal')
async def referal_invite(message: Message):
    user = User(message.from_user.id)
    oneseven = BotDB.vCollector(table='value_main', where='name', meaning='oneseven', wNum=user.weight.get_weight('oneseven'))
    award_referrer = BotDB.vCollector(table='value_main', where='name', meaning='award_referrer', wNum=user.weight.get_weight('award_referrer'))  # награда того кто пригласил(реферрер)
    award_referral = BotDB.vCollector(table='value_main', where='name', meaning='award_referral', wNum=user.weight.get_weight('award_referral'))  # награда реферала перешедшего по ссылке
    d = {
        'oneseven': shell_num(oneseven),
        'award_referrer': shell_num(award_referrer),
        'award_referral': shell_num(award_referral),
        'referrer_linc': referrer_linc(user.id),
        'get_user_referals': BotDB.get_user_referals(user.id)[1]
        }
    await message.answer(get_text('referal_invite1', format=True, d=d))
 

@dp.message_handler(Text(equals=get_button('7')))
@tech_break()
@ban()
@error_reg()
@last_tap('bonus')
async def bonus(message: Message):
    user = User(message.from_user.id)
    if user.bonus == 0:
        return await message.answer(get_text('bonus.condition', format=False))

    quantity_min = 60
    income = income_dev_software(user.id)
    perecnt_bonus = BotDB.vCollector(table='value_main', where='name', meaning='percent_bonus', wNum=user.weight.get_weight('percent_bonus'))
    bonus = round((quantity_min * income) * perecnt_bonus, 2)
    BotDB.add(key='rub', where='id_user', meaning=user.id, num=bonus)
    BotDB.updateN(key='bonus', where='id_user', meaning=user.id, num=0)
    await message.answer(get_text('bonus', format=True, d={'bonus': shell_num(bonus)}))  



def company_keyboard(id_user):
    type_of_activity = BotDB.get(key='type_of_activity', where='id_user', meaning=id_user)
    keyboard = keyboard_default.company_dev_software()
    if type_of_activity == 'dev_software':
        user = DevSoftware(id_user)
        income = income_calc(user.user.id)
        d = {
            'name_company': user.user.company_name,
            'base_income': shell_num(income[0]),
            'stock_income': shell_num(income[2]),
            'stock_holder_income': shell_num(income[1]),
            'expense': shell_num(salary_dev(id_user)),
            'count_place': shell_num(user.quantity_all_places),
            'count_dev': shell_num(user.quantity_all_devs),
            'count_device': shell_num(user.quantity_devices) 
            }
        text_menu = get_text('company_dev_software', format=True, d=d)
        keyboard = keyboard_default.company_dev_software()
    return keyboard, text_menu


@dp.message_handler(Text(equals=get_button('8')))
@tech_break()
@ban()
@error_reg()
@last_tap('company')
async def company(message: Message):
    keyboard, text = company_keyboard(message.from_user.id)
    await message.answer(get_text('company', format=True, d={'text': text}), reply_markup=keyboard)
    await company_dev_software.Q1.set() 

@dp.message_handler(Text(equals=get_button('9')))
@tech_break()
@ban()
@error_reg()
@last_tap('forbs')
async def forbs(message: Message):
    try:
        await message.answer(get_text('forbs', format=True, d={'t': list_forbes()}), reply_markup=keyboard_default.forbs())
    except:
        await message.answer(get_text('not_list_forbes_yet'), reply_markup=keyboard_default.forbs())

@dp.message_handler(Text(equals=get_button('10')))
@tech_break()
@ban()
@error_reg()
@last_tap('setting')
async def setting(message: Message):
    user = User(message.from_user.id)
    await message.answer(get_text('setting', format=False), reply_markup=keyboard_default.user_setting(quantity_changes_name=user.amount_of_changes_nickname, number_of_requests=user.number_of_requests))

# ######

@dp.message_handler(Command('inventory'))
@tech_break()
@ban()
@error_reg()
@last_tap('-')
async def inventory_viev(message: Message):
    id_user = message.from_user.id
    await message.answer(get_text('inventory_viev', format=False), reply_markup=keyboard_inline.create_inventory_items_keyboard(id_user))

@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'item_inventory_name')
@last_tap_call('-')
async def discription_inventory_item(call: CallbackQuery):
    item_name = call.data.split(':')[1]
    status = call.data.split(':')[-1]
    params = get_item_param_viev(item_name=item_name)
    description = get_text(f'{item_name}_description', d=params)
    text_template_page = get_text('template_item_inventory_page', d={'description': description})
    keyboard = keyboard_inline.item_inventory_menu(item_name=item_name, activated=status)
    await bot.edit_message_text(text=text_template_page, chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'item_inventory' and call.data.split(':')[1] == 'back')
@last_tap_call('-')
async def item_inventory_back(call: CallbackQuery):
    id_user = call.from_user.id
    items_keyboard = keyboard_inline.create_inventory_items_keyboard(id_user=id_user)
    await bot.edit_message_text(text=get_text('inventory_viev', format=False), chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=items_keyboard)

@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'item_inventory_adg')
@last_tap_call('-')
async def item_is_adg(call: CallbackQuery):
    id_user = call.from_user.id
    call_data = call.data.split(':')
    if call_data[1]== 'deactivated':
        deactivate_item(id_user=id_user, item_name=call_data[2])
        status = 0
    
    elif call_data[1] == 'activated':
        if have_activated_item(id_user):
            return await call.answer(get_text('have_activated_item.condition', format=False), show_alert=True)
        status = 1
        activate_item(id_user=id_user, item_name=call_data[2])
    elif call_data[1] == 'gift':
        activate_item(id_user=id_user, item_name=call_data[2])
        return await item_inventory_back(call=call)
    keyboard = keyboard_inline.item_inventory_menu(item_name=call_data[2], activated=status)
    await bot.edit_message_reply_markup(chat_id=id_user, message_id=call.message.message_id, reply_markup=keyboard)

# @dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'item_inventory_gift')
# @last_tap_call('-')
# async def item_is_gift(call: CallbackQuery):
#     pass



# ######

@dp.message_handler(Text(equals=get_button('10.1')))
@tech_break()
@ban()
@error_reg()
@last_tap('-')
async def shop_items(message: Message):
    user = User(message.from_user.id)
    items_keyboard = keyboard_inline.create_items_keyboard()
    await message.answer(get_text('shop_items', format=False), reply_markup=items_keyboard) 

@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'item_shop_name')
@last_tap_call('-')
async def discription_item(call: CallbackQuery):
    item_name = call.data.split(':')[1]
    params = get_item_param_viev(item_name=item_name)
    description = get_text(f'{item_name}_description', d=params)
    text_template_page = get_text('template_item_shop_page', d={'description': description})
    await bot.edit_message_text(text=text_template_page, chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=keyboard_inline.item_shop_menu(item_name=item_name))


@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'item_shop' and call.data.split(':')[1] == 'back')
@last_tap_call('-')
async def item_back(call: CallbackQuery):
    items_keyboard = keyboard_inline.create_items_keyboard()
    await bot.edit_message_text(text=get_text('shop_items', format=False), chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=items_keyboard)

@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'item_shop' and call.data.split(':')[1] == 'buy')
@last_tap_call('-')
async def item_buy(call: CallbackQuery):
    user = User(call.from_user.id)
    item_name = call.data.split(':')[-1]
    quantity_items = BotDB.get(table='items', key='quantity', where='name', meaning=item_name)
    cost_currency, cost_num = parse_2dot_data(key='cost', where='name', meaning=item_name, table='items')[1:][0]
    user_account = BotDB.get(key=cost_currency, where='id_user', meaning=user.id)
    user_items = parse_2dot_data(key='items', where='id_user', meaning=user.id, table='users')[1:]
    if user_has_item := [True for i in user_items if item_name in i]:
        await call.answer(text=get_text('item_buy.condition.1'), show_alert=True)
        return
    if quantity_items <= 0:
        await call.answer(text=get_text('item_buy.condition.3'), show_alert=True)
        return
    if user_account - cost_num < 0:
        await call.answer(text=get_text('item_buy.condition.2'), show_alert=True)
        return
    
    num = user_account - cost_num
    q_items = quantity_items - 1
    BotDB.updateN(table='items', key='quantity', where='name', meaning=item_name, num=q_items)
    BotDB.updateN(key=cost_currency, where='id_user', meaning=user.id, num=num)
    create_2dot_data(table='users', key='items', where='id_user', meaning=user.id, d=[item_name, 0])

    await bot.edit_message_text(text=get_text('item_bought', format=False), chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
    items_keyboard = keyboard_inline.create_items_keyboard()
    await bot.send_message(chat_id=call.from_user.id, text=get_text('shop_items', format=False), reply_markup=items_keyboard)  

@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'item' and call.data.split(':')[1] == 'back')
@last_tap_call('-')
async def item_back(call: CallbackQuery):
    items_keyboard = keyboard_inline.create_items_keyboard()
    await bot.edit_message_text(text=get_text('shop_items', format=False), chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=items_keyboard)

@dp.message_handler(Text(contains=get_button('10.2').split(' ')[0]))
@tech_break()
@ban()
@error_reg()
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
    user = User(message.from_user.id)
    if message.text == get_button('*2'):
        await message.answer(get_text('setting', format=False), reply_markup=keyboard_default.user_setting(user.amount_of_changes_nickname, number_of_requests=user.number_of_requests))
        await state.finish()
    elif 2 > len(message.text) or len(message.text) > BotDB.vCollector(table='value_main', where='name', meaning='max_symbols_name'):
        length_word = len(message.text)
        await message.answer(get_text('q1_1', d={'word': message.text, 'length_word': length_word}))
    elif check_on_simbols(message.text) > 0:
        await message.answer(get_text('q1_2', format=False))
    elif check_nickname(user.id, message.text):
        await message.answer(get_text('q1_3', format=False))
    else:
        async with state.proxy() as data:
            data['answer'] = message.text
        await message.answer(get_text('change_nickname2', format=False))
        await Change_Nickname.Q2.set()
    
@dp.message_handler(state=Change_Nickname.Q2)
@last_tap(button='-', state=True)
async def change_nickname3(message: Message, state: FSMContext):
    user = User(message.from_user.id)
    data = await state.get_data()
    answer = data.get('answer')
    if message.text == get_button('*2'):
        await message.answer(get_text('setting', format=False), reply_markup=keyboard_default.user_setting(user.amount_of_changes_nickname, number_of_requests=user.number_of_requests))
        await state.finish()
    elif answer == message.text:
        # запись nickname(псевдонима)
        BotDB.add(key='amount_of_changes_nickname', where='id_user', meaning=message.from_user.id, num=-1)
        await message.answer(get_text('change_nickname3.1', format=False), reply_markup=keyboard_default.user_setting(user.amount_of_changes_nickname, number_of_requests=user.number_of_requests))
        BotDB.updateT(key='nickname', where='id_user', meaning=message.from_user.id, text=answer)
        await state.finish()
    else:
        await message.answer(get_text('change_nickname3.2', format=False))

# ######

@dp.message_handler(Text(contains=get_button('10.3').split(' ')[0]))
@tech_break()
@ban()
@error_reg()
@last_tap('contact_support')
async def contact_support(message: Message):
    if BotDB.get(key='number_of_requests', where='id_user', meaning=message.from_user.id) == 0:
        return await message.answer(get_text('not_enough_requests', format=False))
    await message.answer(get_text('contact_support', format=False), reply_markup=keyboard_default.cancel())
    await Contact_Support.Q1.set()

@dp.message_handler(state=Contact_Support.Q1)
@last_tap('-', state=True)
async def contact_support1(message: Message, state: FSMContext):
    user = User(message.from_user.id)
    if message.text == get_button('*2'):
        await message.answer(get_text('setting', format=False), reply_markup=keyboard_default.user_setting(user.amount_of_changes_nickname, number_of_requests=user.number_of_requests))
    else:
        teg = taG()
        date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
        d={
            'user': message.from_user.get_mention(name=user.nickname),
            'date': date,
            'text': message.text,
            'tag': teg
        }
        BotDB.add_support_message(tag=teg, id_user=user.id, info_message=get_text('message_in_chat_support', format=True, d=d), message=message.text)
        await bot.send_message(BotDB.vCollector(table='value_main', where='name', meaning='id_chat_support'), get_text('message_in_chat_support', format=True, d=d), reply_markup=keyboard_inline.i_am_take(teg))

        BotDB.add(key='number_of_requests', where='id_user', meaning=user.id, num=-1)
        await message.answer(get_text('contact_support1.2', format=False), reply_markup=keyboard_default.user_setting(user.amount_of_changes_nickname, number_of_requests=user.number_of_requests))

    await state.finish()

@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'i_am_take')
@last_tap_call('-')
async def answer_button(call: CallbackQuery):
    id_user = call.from_user.id
    teg = call.data.split(':')[1]
    id_chat_support = BotDB.vCollector(table='value_main', where='name', meaning='id_chat_support')
    info_message = BotDB.get(key='info_message', where='tag', meaning=teg, table='message_in_support')
    
    await bot.delete_message(message_id=call.message.message_id, chat_id=id_chat_support)
    await bot.send_message(id_user, info_message, reply_markup=keyboard_inline.give_an_answer(teg))


@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'give_an_answer')
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
    user = User(message.from_user.id)
    data = await state.get_data()
    teg = data.get('tag')
    id_chat_support = BotDB.vCollector(table='value_main', where='name', meaning='id_chat_support')
    if message.text == get_button('*3'):
        # возвращаем удоленное сообщение рание в чат теч. поддержки
        info_message = BotDB.get(key='info_message', where='tag', meaning=teg, table='message_in_support')
        await bot.send_message(id_chat_support, info_message, reply_markup=keyboard_inline.i_am_take(teg))
        # отправляем сообщение ответчику
        await message.answer(get_text('answer_button1.1',format=False), reply_markup=keyboard_default.main_page())
    else:
        user_message = BotDB.get(key='message', where='tag', meaning=teg, table='message_in_support')
        d = {
            'user_text': user_message,
            'admin_answer': message.text
        }
        # отправляем ответ юзеру
        _ = BotDB.get(key='id_user', where='tag', meaning=teg, table='message_in_support') # id юзера, который обратился в тех поддержку
        await bot.send_message(_, get_text('answer_button1.2', format=True, d=d))
        # отправляем админу сообщение о том, что его ответ доставлен юзеру
        await message.answer(get_text('answer_button1.3', format=False), reply_markup=keyboard_default.main_page())
        date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
        d = {
            'message': BotDB.get(key='info_message', where='tag', meaning=teg, table='message_in_support'),
            'respondent': message.from_user.get_mention(),
            'answer': message.text,
            'date': date
            }
        # отправляем в чат тех. поддержки всю информацию о вопросе и ответе, юзере и админе
        await bot.send_message(id_chat_support, get_text('answer_button1.4',format=True, d=d))

    await state.finish()

# ######

@dp.message_handler(Command('upcommand'))
async def tetst(message: Message):
    print('command update done!')
    commands = (
    ('start', 'начало работы с ботом'),
    ('help', 'поможет тебе'),
    ('inventory', 'твой инвентарь предметов'),
    ('faq', 'руководство по игре'))
    l = [BotCommand(command=i[0], description=i[1]) for i in commands]
    await bot.set_my_commands(l)

@dp.message_handler(Command('get_file'))
async def get_file(message: Message):
    if message.get_args() == '7777':
        await message.answer(get_text('files', format=False), reply_markup=keyboard_inline.get_files_k()) 
    # get_xlsx_table(BotDB.conn, 'users')
    # await message.answer_document(document=open('users.xlsx', 'rb'))

@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'name_table')
async def answer_button(call: CallbackQuery, state: FSMContext):
    name_table = call.data.split(':')[1]
    get_xlsx_table(BotDB.conn, f'{name_table}')
    await bot.send_document(call.from_user.id, document=open(f'{name_table}.xlsx', 'rb'))

@dp.message_handler(content_types=ContentType.DOCUMENT)
async def handle_docs(message: Message):
    file_name = message.document.file_name
    if is_xlsx_extend(file_name) and message.from_user.id == 474701274:
        BotDB.close(BotDB.conn)
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        await bot.download_file(file.file_path, f'{file_name}')
        conn, cur = BotDB.create_connection()
        write_excel_to_db(excel_file=file_name, conn=conn)
        BotDB.conn, BotDB.cur = conn, cur
        return await message.answer(get_text('handle_docs.done', format=False))
    await message.answer(get_text('handle_docs.error', format=False))


@dp.message_handler(Text(equals=get_button('*1')))
@tech_break()
@ban()
@error_reg()
@last_tap('back')
async def back(message: Message):
    await message.answer(get_text('back', format=False), reply_markup=keyboard_default.main_page())

# @dp.message_handler(content_types=['photo'], state='*')
# async def get_PHOTO_id(message: Message):
#     await message.answer(message.photo[-1].file_id)

# @dp.message_handler(Text('poll'))
# async def send_poll(message: Message):
#     await message.answer_poll('How', ['good', 'bad'], is_anonymous=False)

# @dp.poll_answer_handler()
# async def anytext(poll_answer: types.PollAnswer):
#     pprint((poll_answer.poll_id))












