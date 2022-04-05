import abc
import time
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ChatActions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from aiogram.utils.mixins import T
from dispatcher import dp
from bot import BotDB
from dispatcher import bot 
import asyncio
from keyboards.default import keyboard_default
from keyboards.inline import keyboard_inline
from aiogram.types import CallbackQuery


class game_beginning(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()


class company_dev_software(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()


class exchange_rub_usd(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()


class exchange_usd_rub(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()


class exchange_usd_btc(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()


class exchange_btc_usd(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()


def referrer_linc(id_user, bot_name='company_inc_game_bot'):
    '''Функция для создания реферральной ссылки юзера'''
    return f'http://t.me/{bot_name}?start={id_user}'


def last_tap(button, call=False): 
    '''Декоратор для отслеживания последнего нажатия юзера на любую кнопку в боте'''
    def actual_dec(func):
        if not call:
            async def wrapper(message: types.Message):

                date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
                BotDB.updateT(key='last_tap', where='id_user', meaning=message.from_user.id, text=date)
                BotDB.add(table='click_button', key='amount_click', where='button', meaning=button, num=1)
                return await func(message)

            
        else:
            async def wrapper(call: CallbackQuery):

                date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
                BotDB.updateT(key='last_tap', where='id_user', meaning=call.from_user.id, text=date)
                BotDB.add(table='click_button', key='amount_click', where='button', meaning=button, num=1)
                return await func(call)

        return wrapper

    return actual_dec


# def last_tap_callback(button): 
#     '''Декоратор для отслеживания последнего нажатия юзера на любую кнопку в боте'''
#     def actual_dec_callback(func):

#         async def wrapper_callback(call: CallbackQuery):

#             date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
#             BotDB.updateT(key='last_tap', where='id_user', meaning=call.from_user.id, text=date)
#             BotDB.add(table='click_button', key='amount_click', where='button', meaning=button, num=1)
#             return await func(call)

#         return wrapper_callback

#     return actual_dec_callback   


'''Пример асинхроного декоратора, пока не удолять!'''
# def name_decorator(func):
#     async def wrapper(message: types.Message):
#         if message.from_user.id != 474701274:
#             arr = 44
#         else:
#             arr = 55
#         return await func(arr,message)
#     return wrapper




@dp.message_handler(Command("start"))
@last_tap('start')
async def start_menu(message: Message):
    id_user = message.from_user.id
    # проверяем пользователя на существование в БД
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)
        # проверяем пользователя на приглашение
        try:
            id_referrer = int(message.text.split()[1])
            if id_referrer == message.from_user.id:
                await message.answer('<i>Вы не можете быть рефералом себе</i>')
            else:
                BotDB.updateN(key='referal', where='id_user', meaning=id_user, num=id_referrer)
        except Exception as e:
            pass
        # проверяем пользователя на наличие last_name
        if message.from_user.last_name is None:
            name = message.from_user.first_name
        else:
            name = message.from_user.first_name + ' ' + message.from_user.last_name
        # проверяем пользователя на наличие username
        if message.from_user.username is None:
            username = 'Отсутствует'
        else:
            username = '@' + message.from_user.username
        # записываем все полученые данные о пользователе в БД
        BotDB.updateT(key='username', where='id_user', meaning=id_user, text=username)  # запись username
        BotDB.updateT(key='name', where='id_user', meaning=id_user, text=name.strip())  # запись имени
        await message.answer('<i>Введите ваш псевдоним(никнейм)</i>', reply_markup=ReplyKeyboardRemove())
        await game_beginning.Q1.set()
    else:
        await message.answer('Главное меню',reply_markup=keyboard_default.main_page)


@dp.message_handler(state=game_beginning.Q1)
async def q1(message: Message):
    if len(message.text) > 15:
        await message.answer('<b>Допустимое кол-во символов 15❗️</b>')
        await message.answer('<i>Попробуйте снова</i>')
    else:
        # запись nickname(псевдонима)
        BotDB.updateT(key='nickname', where='id_user', meaning=message.from_user.id, text=message.text)
        await message.answer('<i>Потрясающе! Давайте выберем сферу деятельности вашей компании</i>', reply_markup=keyboard_default.fields)
        await game_beginning.Q2.set()
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(1)


@dp.message_handler(state=game_beginning.Q2)
async def q2(message: Message):
    if message.text == "Производство таваров🍦":
        await message.answer('<i>Выбери тип предприятия</i>', reply_markup=keyboard_default.types_product)
        await game_beginning.Q3.set()
    elif message.text == "Оказание услуг💇🏻‍♂️️️":
        await message.answer('<i>Выбери тип предприятия</i>', reply_markup=keyboard_default.types_services)
        await game_beginning.Q3.set()
    elif message.text == "Нефтяная промышленность🛢":
        await message.answer('<i>Выбери тип предприятия</i>', reply_markup=keyboard_default.types_blackgold)
        await game_beginning.Q3.set()
    elif message.text == "IT🕹":
        await message.answer('<i>Выбери тип предприятия</i>', reply_markup=keyboard_default.types_it)
        await game_beginning.Q3.set()
    else:
        await message.answer('<i>Давайте выберем сферу деятельности вашей компании</i>')


@dp.message_handler(state=game_beginning.Q3)
async def q3(message: Message):
    if message.text == "Назад⤴️":
        await message.answer('<i>Давайте выберем сферу деятельности вашей компании</i>', reply_markup=keyboard_default.fields)
        await game_beginning.Q2.set()
    else:
        # проверяем пользователя на обход системы
        if message.text in list(map(lambda x: x.strip(),BotDB.get(key='text_box1',where='name',meaning='types_field',table='value_main').split(','))):
            # записываем тип деятельности в БД
            BotDB.updateT(key='type_of_activity', where='id_user', meaning=message.from_user.id, text=message.text)
            await message.answer('<i>Дайте название вашей компании</i>', reply_markup=ReplyKeyboardRemove())
            await game_beginning.Q4.set()
        else:
            await message.answer('<i>Выберите тип предприятия</i>')


@dp.message_handler(state=game_beginning.Q4)
async def q4(message: Message, state: FSMContext):
    if len(message.text) > 15:
        await message.answer('<b>Допустимое кол-во символов 15❗️</b>')
        await message.answer('<i>Попробуйте снова</i>')
    else:
        type_of_activity = BotDB.get(key='type_of_activity', where='id_user', meaning=message.from_user.id)
        # BotDB.updateT(table=type_of_activity, key='name_company', where='id_founder', meaning=message.from_user.id, text=message.text)
        date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
        BotDB.updateT(key='date_reg', where='id_user', meaning=message.from_user.id, text=date)  # регистрируем дату создания аккаунта юзера
        await message.answer('<i>А теперь ты можешь прочесть руководство, нажав сюда 👉🏻 /manual</i>',
                             reply_markup=ReplyKeyboardRemove())
        await message.answer('Приятной игры 😉', reply_markup=keyboard_default.main_page)
        await state.finish()


@dp.message_handler(Command("manual"))
@last_tap('manual')
async def game_manual(message: Message):
    await message.answer('Статья')


# @dp.message_handler(Command("del"))
# async def del_table(message: Message):
#     delete_table_user('hh')
#     print('Выполнил')


# @dp.message_handler(Command("crt"))
# async def crt_table(message: Message):
#     create_table_graf_rate()
#     print('Выполнил')


# @dp.message_handler(content_types=['photo'])
# async def crt_table(message: Message):
#     await message.answer(f"{message}")


# @dp.message_handler(Command('test'))
# async def crt_table(message: Message):
#     await message.answer(f'{message}')



def shell_money(quantity_money, currency='usd'):
    '''Обертка для '''
    lnum = '{0:,.2f}'.format(float(quantity_money))
    lnum = int(lnum.split('.')[1])
    if lnum == 0:
        return '<b>{0:,}</b>'.format(quantity_money)
    else:
        if currency == 'usd':
            return '<b>{0:,.2f}</b>'.format(float(quantity_money))
        elif currency == 'btc':
            return '<b>{0:,.5f}</b>'.format(float(quantity_money))


def currency_calculation(money, what_calculate='rub_in_usd', currency='rate_usd'):
    '''Конвертирует валюты'''
    rate = BotDB.get(table='value_main', key='float_box', where='name', meaning=currency)
    if what_calculate == 'rub_in_usd':
        result = round(money / rate, 2)
    elif what_calculate == 'usd_in_btc':
        result = round(money / rate, 5)
    elif what_calculate == 'usd_in_rub':
        result = int(money * rate)
    elif what_calculate == 'btc_in_usd':
        result = round(money * rate,2)
    else:
        print('Ошибка конвертации!')
    return result


@dp.message_handler(Text(equals="Счет💳️"))
@last_tap('account')
async def account_user(message: Message):
    pic = BotDB.get(table='value_main', key='text_box1', where='name', meaning='account_pic')
    rub = BotDB.get(key='rub', where='id_user', meaning=message.from_user.id)
    usd = BotDB.get(key='usd', where='id_user', meaning=message.from_user.id)
    btc = BotDB.get(key='btc', where='id_user', meaning=message.from_user.id)
    text = f'- RUB = {shell_money(rub)}руб.\n- USD = {shell_money(usd)}$\n- BTC = {shell_money(btc, "btc")}BTC'
    await bot.send_photo(message.from_user.id, pic, text)


def check_graf_rate(dimension):
    '''Проверяет кол-во записей курсов usd and btc в БД, если оно превышает установленую размерность, тогда самая старая запись удаляется'''
    result_usd, result_btc = BotDB.get_all('*','graf_rate_usd'), BotDB.get_all('*','graf_rate_usd')
    if len(result_usd) > dimension:
        BotDB.delete('id',result_usd[0][0],'graf_rate_usd')
    elif len(result_btc) > dimension:
        BotDB.delete('id',result_usd[0][0],'graf_rate_btc')
    else:
        pass



def exchange_balans(count_money, type_currency='rate_usd'):
    abs_money = abs(count_money)
    rate_currency = BotDB.get(table='value_main', key='float_box', where='name', meaning=type_currency)
    ratio = BotDB.get(table='value_main', key='int_box1', where='name', meaning=f'ratio_exchange')  # коеффициент обмена
    result = list(map(lambda x: x[0],BotDB.get_all(type_currency.split('_')[1]))) #получаем все имеющиеся деньги указоного типа от всех юзеров
    type_percent = 'perc_' + type_currency.split('_')[1] 
    type_graf_rate = 'graf_rate_' + type_currency.split('_')[1] 
    if count_money > 0:
        percent = round((abs_money/(sum(result)+abs_money))/ratio, 2) #теперь делим кол-во денег которое человек хочет получить на общее их кол-во имеющееся у всех юзеров и делим на коэффициент обмена
        currency = rate_currency + percent * rate_currency
        percent_to_text = f"{percent * 100}"
    else:
        percent = round((abs_money/sum(result))/ratio, 2)
        currency = rate_currency - percent * rate_currency
        percent_to_text = f"-{percent * 100}"
    BotDB.updateN(table='value_main', key='float_box', where='name', meaning=type_currency, num=round(currency, 2))
    date = time.strftime('%X') + time.strftime(' %m/%d/%Y')
    rate_now_text = type_currency + '_now'
    BotDB.cur.execute(f'INSERT INTO "{type_graf_rate}" (time_update, {type_currency}, {type_percent}, {rate_now_text}) VALUES (?,?,?,?)',(date, rate_currency, percent_to_text, round(currency,2)))
    BotDB.conn.commit()
    check_graf_rate(15)



@dp.message_handler(Text(equals="Банк🏦"))
@last_tap('bank')
async def bank(message: Message):
    pic = BotDB.get(table='value_main', key='text_box1', where='name', meaning='bank_pic')
    usd = BotDB.get(key='usd', where='id_user', meaning=message.from_user.id)
    btc = BotDB.get(key='btc', where='id_user', meaning=message.from_user.id)
    rub = BotDB.get(key='rub', where='id_user', meaning=message.from_user.id)
    rate_usd = BotDB.get(table='value_main', key='float_box', where='name', meaning='rate_usd')
    rate_btc = BotDB.get(table='value_main', key='float_box', where='name', meaning='rate_btc')
    time_ = time.strftime('%X').split()[0]
    sec = 60 - int(time_.split(':')[2])
    text = f'На вашем счету\n' \
           f'- RUB = {shell_money(rub)} руб.\n' \
           f'- USD = {shell_money(usd)} $\n' \
           f'- BTC = {shell_money(btc, "btc")} BTC\n\n' \
           f'Курс валют💱\n' \
           f'- 1$ = {shell_money(rate_usd)} руб.\n' \
           f'- 1BTC = {shell_money(rate_btc)} $\n\n' \
           f'До обновления \nкурса осталось: {sec} сек.'
    await bot.send_photo(message.from_user.id, pic, text, reply_markup=keyboard_inline.update_and_convert)


@dp.callback_query_handler(Text(equals='update'))
@last_tap('update',True)
async def up_and_convert(call: CallbackQuery):
    await call.answer(cache_time=1)
    usd = BotDB.get(key='usd', where='id_user', meaning=call.from_user.id)
    btc = BotDB.get(key='btc', where='id_user', meaning=call.from_user.id)
    rub = BotDB.get(key='rub', where='id_user', meaning=call.from_user.id)
    rate_usd = BotDB.get(table='value_main', key='float_box', where='name', meaning='rate_usd')
    rate_btc = BotDB.get(table='value_main', key='float_box', where='name', meaning='rate_btc')
    time_ = time.strftime('%X').split()[0]
    sec = 60 - int(time_.split(':')[2])
    text = f'На вашем счету\n' \
           f'- RUB = {shell_money(rub)} руб.\n' \
           f'- USD = {shell_money(usd)} $\n' \
           f'- BTC = {shell_money(btc, "btc")} BTC\n\n' \
           f'Курс валют💱\n' \
           f'- 1$ = {shell_money(rate_usd)} руб.\n' \
           f'- 1BTC = {shell_money(rate_btc)} $\n\n' \
           f'До обновления \nкурса осталось: {sec} сек.'
    try:
        await bot.edit_message_caption(message_id=call.message.message_id, chat_id=call.from_user.id, caption=text,
                                       reply_markup=keyboard_inline.update_and_convert)
    except Exception as e:
        pass


@dp.callback_query_handler(Text(equals='ru'))
@last_tap('rub_usd',call=True)
async def rub_usd(call: CallbackQuery):
    await call.answer(cache_time=1)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, '<i>Введите количество рублей, которое хотите обменять</i>',
                           reply_markup=keyboard_default.exchange)
    await exchange_rub_usd.Q1.set()
    BotDB.update_user_state(call.from_user.id, True)


@dp.message_handler(state=exchange_rub_usd.Q1)
async def q1(message: Message, state: FSMContext):
    rub = BotDB.get(key='rub', where='id_user', meaning=message.from_user.id)
    percent_bank = BotDB.get(table='value_main', key='float_box', where='name', meaning='percent_bank')
    try:
        num = round(float(message.text), 2)
        if num <= rub:
            
            usd = currency_calculation(num)
            exchange_balans(round(usd,2))
            usd_with_fee = usd - usd * percent_bank
            BotDB.add(key='usd', where='id_user', meaning=message.from_user.id, num=round(usd_with_fee, 2))
            BotDB.add(key='rub', where='id_user', meaning=message.from_user.id, num=-num)
            await message.answer(f'Сделка удалась!\n\n'
                                 f'- {int(percent_bank * 100)}%({shell_money(usd * percent_bank)}$) - получил банк за '
                                 f'транзакцию\n\n '
                                 f'Итого: {shell_money(usd_with_fee)}$', reply_markup=keyboard_default.main_page)
            await state.finish()
            BotDB.update_user_state(message.from_user.id)
        else:
            await message.answer('<i>У вас нет таких денег, попробуйте заново</i>',
                                 reply_markup=keyboard_default.exchange)
    except Exception as e:
        if message.text == 'Обменять всю имеющююся валюту⏩':
            if rub != 0:
                usd = currency_calculation(rub)
                exchange_balans(round(usd, 2))
                usd_with_fee = usd - usd * percent_bank
                BotDB.add(key='usd', where='id_user', meaning=message.from_user.id, num=round(usd_with_fee, 2))
                BotDB.updateN(key='rub', where='id_user', meaning=message.from_user.id, num=0)
                await message.answer(f'Сделка удалась!\n\n'
                                     f'- {int(percent_bank * 100)}%({shell_money(usd * percent_bank)}$) - получил '
                                     f'банк за транзакцию\n\n '
                                     f'Итого: {shell_money(usd_with_fee)}$', reply_markup=keyboard_default.main_page)
                
                await state.finish()
                BotDB.update_user_state(message.from_user.id)
            else:
                await message.answer('<i>У вас нет денег, заходите попозже</i>',
                                     reply_markup=keyboard_default.main_page)
                await state.finish()
                BotDB.update_user_state(message.from_user.id)
        elif message.text == "Отмена❌️":
            await message.answer('Главное меню', reply_markup=keyboard_default.main_page)
            await state.finish()
            BotDB.update_user_state(message.from_user.id)
        else:
            await message.answer('<i>Я вас не понимаю, попробуйте заново</i>',
                                 reply_markup=keyboard_default.exchange)


@dp.callback_query_handler(Text(equals='ur'))
@last_tap('usd_rub',call=True)
async def usd_rub(call: CallbackQuery):
    await call.answer(cache_time=1)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, '<i>Введите количество долларов, которое хотите обменять</i>',
                           reply_markup=keyboard_default.exchange)
    await exchange_usd_rub.Q1.set()
    BotDB.update_user_state(call.from_user.id,True)


@dp.message_handler(state=exchange_usd_rub.Q1)
async def q1(message: Message, state: FSMContext):
    usd = BotDB.get(key='usd', where='id_user', meaning=message.from_user.id)
    percent_bank = BotDB.get(table='value_main', key='float_box', where='name', meaning='percent_bank')
    try:
        num = round(float(message.text), 2)
        if num <= usd:
            
            
            rub = currency_calculation(num, what_calculate='usd_in_rub')
            exchange_balans(-num)  # usd-
            rub_with_fee = rub - rub * percent_bank
            BotDB.add(key='rub', where='id_user', meaning=message.from_user.id, num=round(rub_with_fee, 2))
            BotDB.add(key='usd', where='id_user', meaning=message.from_user.id, num=-num)
            await message.answer(f'Сделка удалась!\n\n'
                                 f'- {int(percent_bank * 100)}%({shell_money(rub * percent_bank)}руб.) - получил банк за '
                                 f'транзакцию\n\n '
                                 f'Итого: {shell_money(rub_with_fee)}руб.', reply_markup=keyboard_default.main_page)
            
            await state.finish()
            BotDB.update_user_state(message.from_user.id)
        else:
            await message.answer('<i>У вас нет таких денег, попробуйте заново</i>',
                                 reply_markup=keyboard_default.exchange)
    except Exception as e:
        if message.text == 'Обменять всю имеющююся валюту⏩':
            if usd != 0:
                
                rub = currency_calculation(usd, what_calculate='usd_in_rub')
                exchange_balans(-usd)  # usd-
                rub_with_fee = rub - rub * percent_bank
                BotDB.add(key='rub', where='id_user', meaning=message.from_user.id, num=round(rub_with_fee, 2))
                BotDB.updateN(key='usd', where='id_user', meaning=message.from_user.id, num=0)
                await message.answer(f'Сделка удалась!\n\n'
                                     f'- {int(percent_bank * 100)}%({shell_money(rub * percent_bank)}руб.) - получил '
                                     f'банк за транзакцию\n\n '
                                     f'Итого: {shell_money(rub_with_fee)}руб.', reply_markup=keyboard_default.main_page)
                
                await state.finish()
                BotDB.update_user_state(message.from_user.id)
            else:
                await message.answer('<i>У вас нет денег, заходите попозже</i>',
                                     reply_markup=keyboard_default.main_page)
                await state.finish()
                BotDB.update_user_state(message.from_user.id)
        elif message.text == "Отмена❌️":
            await message.answer('Главное меню', reply_markup=keyboard_default.main_page)
            await state.finish()
            BotDB.update_user_state(message.from_user.id)
        else:
            await message.answer('<i>Я вас не понимаю, попробуйте заново</i>',
                                 reply_markup=keyboard_default.exchange)


@dp.callback_query_handler(Text(equals='ub'))
@last_tap('usd_btc',call=True)
async def usd_btc(call: CallbackQuery):
    usd = BotDB.get(key='usd', where='id_user', meaning=call.from_user.id)
    rate_btc = BotDB.get(table='value_main', key='float_box', where='name', meaning='rate_btc')
    if usd > rate_btc / 10:
        await call.answer(cache_time=1)
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
        await bot.send_message(call.from_user.id, '<i>Введите количество доларов, которое хотите обменять</i>',
                               reply_markup=keyboard_default.exchange)
        await exchange_usd_btc.Q1.set()
        BotDB.update_user_state(call.from_user.id,True)
    else:
        await bot.send_message(call.from_user.id, '<i>Количество долларов на вашем счету не '
                                                  'позволяет купить вам 1/10 часть биткоина, '
                                                  ' что является максимальным минимумом для транзакции</i>')


@dp.message_handler(state=exchange_usd_btc.Q1)
async def q1(message: Message, state: FSMContext):
    percent_bank = BotDB.get(table='value_main', key='float_box', where='name', meaning='percent_bank')
    usd = BotDB.get(key='usd', where='id_user', meaning=message.from_user.id)
    rate_btc = BotDB.get(table='value_main', key='float_box', where='name', meaning='rate_btc')
    try:
        num = round(float(message.text), 2)
        if num > rate_btc / 10:
            if num <= usd:
                btc = currency_calculation(num, what_calculate='usd_in_btc', currency='rate_btc')
                exchange_balans(-num)  # usd-
                exchange_balans(btc ,'rate_btc')  # btc+
                btc_with_fee = btc - btc * percent_bank
                BotDB.add(key='btc', where='id_user', meaning=message.from_user.id, num=round(btc_with_fee, 5))
                BotDB.add(key='usd', where='id_user', meaning=message.from_user.id, num=-num)
                await message.answer(f'Сделка удалась!\n\n'
                                     f'- {int(percent_bank * 100)}%({shell_money(btc * percent_bank, "btc")}BTC) - '
                                     f'получил банк за '
                                     f'транзакцию\n\n '
                                     f'Итого: {shell_money(btc_with_fee, "btc")}BTC', reply_markup=keyboard_default.main_page)
                
                await state.finish()
                BotDB.update_user_state(message.from_user.id)
            else:
                await message.answer('<i>У вас нет таких денег, попробуйте заново</i>',
                                     reply_markup=keyboard_default.exchange)
        else:
            await message.answer('<i>Количество долларов, которое вы ввели, не позволяет купить '
                                 'вам 1/10 часть биткоина,'
                                 ' что является максимальным минимумом для транзакции</i>')
            await message.answer('<i>Попробуйте заново</i>')
    except Exception as e:
        if message.text == 'Обменять всю имеющююся валюту⏩':
            if usd > rate_btc / 10:
                btc = currency_calculation(usd, what_calculate='usd_in_btc', currency='rate_btc')
                exchange_balans(-usd)  # usd-
                exchange_balans(btc ,'rate_btc')  # btc+
                btc_with_fee = btc - btc * percent_bank
                BotDB.add(key='btc', where='id_user', meaning=message.from_user.id, num=round(btc_with_fee, 5))
                BotDB.updateN(key='usd', where='id_user', meaning=message.from_user.id, num=0)
                await message.answer(f'Сделка удалась!\n\n'
                                     f'- {int(percent_bank * 100)}%({shell_money(btc * percent_bank, "btc")}'
                                     f'BTC) - получил '
                                     f'банк за '
                                     f'транзакцию\n\n '
                                     f'Итого: {shell_money(btc_with_fee, "btc")}BTC', reply_markup=keyboard_default.main_page)
                
                await state.finish()
                BotDB.update_user_state(message.from_user.id)
            else:
                await message.answer('<i>Количество долларов, на вашем счету, не позволяет купить '
                                    'вам 1/10 часть биткоина,'
                                    ' что является максимальным минимумом для транзакции</i>')
                await state.finish()
                BotDB.update_user_state(message.from_user.id)
        elif message.text == "Отмена❌️":
            await message.answer('Главное меню', reply_markup=keyboard_default.main_page)
            await state.finish()
            BotDB.update_user_state(message.from_user.id)
        else:
            await message.answer('<i>Я вас не понимаю, попробуйте заново</i>',
                                 reply_markup=keyboard_default.exchange)


@dp.callback_query_handler(Text(equals='bu'))
@last_tap('btc_usd',call=True)
async def btc_usd(call: CallbackQuery):
    await call.answer(cache_time=1)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, '<i>Введите количество биткоинов, которое хотите обменять</i>',
                           reply_markup=keyboard_default.exchange)
    await exchange_btc_usd.Q1.set()
    BotDB.update_user_state(call.from_user.id,True)


@dp.message_handler(state=exchange_btc_usd.Q1)
async def q1(message: Message, state: FSMContext):
    percent_bank = BotDB.get(table='value_main', key='float_box', where='name', meaning='percent_bank')
    btc = BotDB.get(key='btc', where='id_user', meaning=message.from_user.id)
    try:
        num = round(float(message.text), 5)
        if num <= btc:
            usd = currency_calculation(num, what_calculate='btc_in_usd', currency='rate_btc')
            exchange_balans(usd)  # usd+
            exchange_balans(-num ,'rate_btc')  # btc-
            usd_with_fee = usd - usd * percent_bank
            BotDB.add(key='usd', where='id_user', meaning=message.from_user.id, num=round(usd_with_fee, 2))
            BotDB.add(key='btc', where='id_user', meaning=message.from_user.id, num=-num)
            await message.answer(f'Сделка удалась!\n\n'
                                 f'- {int(percent_bank * 100)}%({shell_money(usd * percent_bank)}$) - получил банк за '
                                 f'транзакцию\n\n '
                                 f'Итого: {shell_money(usd_with_fee)}$', reply_markup=keyboard_default.main_page)
            
            await state.finish()
            BotDB.update_user_state(message.from_user.id)
        else:
            await message.answer('<i>У вас нет таких денег, попробуйте заново</i>',
                                 reply_markup=keyboard_default.exchange)
    except Exception as e:
        if message.text == 'Обменять всю имеющююся валюту⏩':
            if btc > 0:
                usd = currency_calculation(btc, what_calculate='btc_in_usd', currency='rate_btc')
                exchange_balans(usd)  # usd+
                exchange_balans(-btc ,'rate_btc')  # btc-
                usd_with_fee = usd - usd * percent_bank
                BotDB.add(key='usd', where='id_user', meaning=message.from_user.id, num=round(usd_with_fee, 2))
                BotDB.updateN(key='btc', where='id_user', meaning=message.from_user.id, num=0)
                await message.answer(f'Сделка удалась!\n\n'
                                     f'- {int(percent_bank * 100)}%({shell_money(usd * percent_bank)}$) - получил '
                                     f'банк за транзакцию\n\n '
                                     f'Итого: {shell_money(usd_with_fee)}$', reply_markup=keyboard_default.main_page)
                
                await state.finish()
                BotDB.update_user_state(message.from_user.id)
            else:
                await message.answer('<i>У вас нет криптовалюты, заходите попозже</i>',
                                     reply_markup=keyboard_default.main_page)
                await state.finish()
                BotDB.update_user_state(message.from_user.id)
        elif message.text == "Отмена❌️":
            await message.answer('Главное меню', reply_markup=keyboard_default.main_page)
            await state.finish()
            BotDB.update_user_state(message.from_user.id)
        else:
            await message.answer('<i>Я вас не понимаю, попробуйте заново</i>',
                                 reply_markup=keyboard_default.exchange)


@dp.message_handler(Text(equals="Рефералы🗿"))
@last_tap('referal')
async def referal_invite(message: Message):
    five = BotDB.get(table='value_main', key='int_box1', where='name', meaning='five')
    seven = BotDB.get(table='value_main', key='int_box1', where='name', meaning='seven')
    award_referrer = BotDB.get(table='value_main', key='int_box1', where='name',
                      meaning='award_referrer')  # награда того кто пригласил(реферрер)
    award_referral = BotDB.get(table='value_main', key='int_box1', where='name',
                   meaning='award_referral')  # награда реферала перешедшего по ссылке
    await message.answer(f'Реферал - это ваш друг или знакомый, который перешёл по '
                         f'вашей уникальной ссылке, в следствии чего, вы получаете <b>{five}-{seven}%*</b> с '
                         f'его дохода.\n\n'
                         f'Чтобы реферал приносил вам доход, ему необходимо пройти <b>верификацию*</b>, '
                         f'по завершению которой '
                         f'каждая из сторон получит единоразовое вознаграждение\n\n'
                         f'- Вы ➡️ <b>{shell_money(award_referrer)}</b>$\n'
                         f'- Реферал ➡️ <b>{shell_money(award_referral)}</b>$\n\n'
                         f'Вот ваша уникальная ссылка \n{referrer_linc(message.from_user.id)}\n'
                         f'Скопируйте её и отправте человеку, которого хотите пригласить в игру!\n\n'
                         f'* - узнать подробнее в /FAQ\n'
                         f'У вас рефералов: {BotDB.get_user_referals(message.from_user.id)[1]}')


@dp.message_handler(Text(equals='🎁'))
@last_tap('bonus')
async def bonus(message: Message):
    await message.answer('|---in process---|')
    


# def company_info(id_user):
#     text = ""
#     field_company_user = get(key='field', where='id_user', meaning=id_user)
#     type_company = get(table=field_company_user, key='type', where='id_founder', meaning=id_user)
#     name_company = get(table=field_company_user, key='name_company', where='id_founder', meaning=id_user)
#     income = get(table=field_company_user, key='income', where='id_founder', meaning=id_user)
#     if type_company == "Разработка ПО":
#         users = get(table=field_company_user, key='users', where='id_founder', meaning=id_user)
#         apps = get(table=field_company_user, key='apps', where='id_founder', meaning=id_user)
#         dataC = get(table=field_company_user, key='dataC', where='id_founder', meaning=id_user)
#         staff = get(table=field_company_user, key='count_junior', where='id_founder', meaning=id_user) + \
#                 get(table=field_company_user, key='count_middle', where='id_founder', meaning=id_user) + \
#                 get(table=field_company_user, key='count_senior', where='id_founder', meaning=id_user)

#         w = get(table=field_company_user, key='workplace', where='id_founder', meaning=id_user)
#         workplace = get(table='value_it', key='matter_text', where='name', meaning=w)

#         c = get(table=field_company_user, key='comp', where='id_founder', meaning=id_user)
#         comp = get(table='value_it', key='matter_text', where='name', meaning=c)

#         text = f'<i>Тип компании:</i> {type_company}\n' \
#                f'<i>Название:</i> {name_company}\n\n' \
#                f'<i>Помещение:</i> {workplace}\n' \
#                f'<i>Оборудование:</i> {comp}\n\n' \
#                f'<i>Доход:</i> {shell_money(income)} руб./мин.\n\n' \
#                f'Кол-во➡️\n' \
#                f'├<i>пользователей:</i> {shell_money(users)}\n' \
#                f'├<i>выпущенного ПО:</i> {shell_money(apps)}\n' \
#                f'├<i>data-centre:</i> {shell_money(dataC)}\n' \
#                f'└<i>сотрудников:</i> {shell_money(staff)}\n'
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     return text


# def company_keyboard(id_user):
#     field_company_user = get(key='field', where='id_user', meaning=id_user)
#     type_company = get(table=field_company_user, key='type', where='id_founder', meaning=id_user)
#     keyboard = 0
#     if type_company == "Разработка ПО":
#         keyboard = company_it_main_menu
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     elif type_company == '':
#         pass
#     return keyboard


# @dp.message_handler(Text(equals="Компания®️"))
# async def company(message: Message):
#     last_tap(message.from_user.id, 'company')
#     await message.answer(company_info(message.from_user.id), reply_markup=company_keyboard(message.from_user.id))
#     await company_dev_software.Q1.set()


# @dp.message_handler(state=company_dev_software.Q1)
# async def company_q1(message: Message, state: FSMContext):
#     text = message.text
#     field_company_user = get(key='field', where='id_user', meaning=message.from_user.id)
#     type_company = get(table=field_company_user, key='type', where='id_founder', meaning=message.from_user.id)
#     if text == 'Назад⤴️':
#         await message.answer('Главное меню', reply_markup=main_page)
#         await state.finish()
#     elif text == "Инфо о компании":
#         await message.answer(company_info(message.from_user.id), reply_markup=company_keyboard(message.from_user.id))
#     # IT
#     if type_company == 'Разработка ПО':
#         if text == "Маркетинговое исследование":
#             pass
#         elif text == "Нанять программиста(-ов)":
#             countJunior = get(table='it_company', key='count_junior', where='id_founder', meaning=message.from_user.id)
#             requirements = get(table='value_it', key='matter_text', where='name', meaning='pJunior')
#             rText = get(table='value_it', key='matter_text', where='name', meaning=requirements)
#             pIncome = get(table='value_it', key='matter_int1', where='name', meaning='pJunior') * \
#                       get(table='it_company', key='PofP', where='id_founder', meaning=message.from_user.id) / 100
#             expenditure = get(table='value_it', key='matter_int2', where='name', meaning='pJunior')
#             await message.answer(f'<b>Junior</b> програмист\n\n'
#                                  f'<i>Прибыль</i>: {shell_money(pIncome)} руб./мин\n'
#                                  f'<i>Зарплата</i>: {shell_money(expenditure)} руб./час\n'
#                                  f'<i>Требования</i>: {rText}\n\n'
#                                  f'У тебя работают: {shell_money(countJunior)} чел.', reply_markup=programmists_j)
#         elif text == "Открыть data-centre":
#             pass
#         elif text == "Улучшить оборудование":
#             pass
#         elif text == "Создать новое ПО":
#             pass
#     if type_company == 'Создание игр':
#         if text == '':
#             pass
#         elif text == '':
#             pass
#     # Производство товаров
#     if type_company == 'Фермерство':
#         if text == '':
#             pass
#         elif text == '':
#             pass
#     if type_company == 'Одежда и обувь':
#         if text == '':
#             pass
#         elif text == '':
#             pass
#     if type_company == 'Производство автомобилей':
#         if text == '':
#             pass
#         elif text == '':
#             pass
#     if type_company == 'Производство телефонов':
#         if text == '':
#             pass
#         elif text == '':
#             pass
#     if type_company == 'Продукты питания':
#         if text == '':
#             pass
#         elif text == '':
#             pass
#     # Оказание услуг
#     if type_company == 'Ресторан':
#         if text == '':
#             pass
#         elif text == '':
#             pass
#     if type_company == 'Салон красоты':
#         if text == '':
#             pass
#         elif text == '':
#             pass
#     if type_company == 'С.Т.О':
#         if text == '':
#             pass
#         elif text == '':
#             pass
#     if type_company == 'Адвокатское агенство':
#         if text == '':
#             pass
#         elif text == '':
#             pass
#     if type_company == 'Частная клиника':
#         if text == '':
#             pass
#         elif text == '':
#             pass
#     # Нефтяная промышленость
#     if type_company == 'Производство топлива':
#         if text == '':
#             pass
#         elif text == '':
#             pass
#     if type_company == 'Добыча нефти':
#         if text == '':
#             pass
#         elif text == '':
#             pass
#     else:
#         pass


# @dp.callback_query_handler(state=company_dev_software.Q1)
# async def prog(call: CallbackQuery):
#     w = get(table='it_company', key='workplace', where='id_founder', meaning=call.from_user.id)
#     workplace = get(table='value_it', key='matter_int2', where='name', meaning=w)
#     if call.data == 'jun':
#         await call.answer(cache_time=0.1)
#         countJunior = get(table='it_company', key='count_junior', where='id_founder', meaning=call.from_user.id)
#         requirements = get(table='value_it', key='matter_text', where='name', meaning='pJunior')
#         rText = get(table='value_it', key='matter_text', where='name', meaning=requirements)
#         pIncome = get(table='value_it', key='matter_int1', where='name', meaning='pJunior') * \
#                   get(table='it_company', key='PofP', where='id_founder', meaning=call.from_user.id) / 100
#         expenditure = get(table='value_it', key='matter_int2', where='name', meaning='pJunior')
#         text = f'<b>Junior</b> програмист\n\n' \
#                f'<i>Прибыль</i>: {shell_money(pIncome)} руб./мин\n' \
#                f'<i>Зарплата</i>: {shell_money(expenditure)} руб./час\n' \
#                f'<i>Требования</i>: {rText}\n\n' \
#                f'У тебя работают: {shell_money(countJunior)} чел.'
#         try:
#             await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=text,
#                                         reply_markup=programmists_j)
#         except Exception as e:
#             pass
#     elif call.data == 'mid':
#         await call.answer(cache_time=0.1)
#         countMiddle = get(table='it_company', key='count_middle', where='id_founder', meaning=call.from_user.id)
#         requirements = get(table='value_it', key='matter_text', where='name', meaning='pMiddle')
#         rS = requirements.split(',')
#         rText = get(table='value_it', key='matter_text', where='name', meaning=rS[0]) + ', ' + get(table='value_it',
#                                                                                                   key='matter_text',
#                                                                                                   where='name',
#                                                                                                   meaning=rS[1])
#         pIncome = get(table='value_it', key='matter_int1', where='name', meaning='pMiddle') * \
#                   get(table='it_company', key='PofP', where='id_founder', meaning=call.from_user.id) / 100
#         expenditure = get(table='value_it', key='matter_int2', where='name', meaning='pMiddle')
#         text = f'<b>Middle</b> програмист\n\n' \
#                f'<i>Прибыль</i>: {shell_money(pIncome)} руб./мин\n' \
#                f'<i>Зарплата</i>: {shell_money(expenditure)} руб./час\n' \
#                f'<i>Требования</i>: {rText}\n\n' \
#                f'У тебя работают: {shell_money(countMiddle)} чел.'
#         try:
#             await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=text,
#                                         reply_markup=programmists_m)
#         except Exception as e:
#             pass
#     elif call.data == 'sir':
#         await call.answer(cache_time=0.1)
#         countSenior = get(table='it_company', key='count_senior', where='id_founder', meaning=call.from_user.id)
#         requirements = get(table='value_it', key='matter_text', where='name', meaning='pSenior')
#         rS = requirements.split(',')
#         rText = get(table='value_it', key='matter_text', where='name', meaning=rS[0]) + ', ' + get(table='value_it',
#                                                                                                   key='matter_text',
#                                                                                                   where='name',
#                                                                                                   meaning=rS[1])
#         pIncome = get(table='value_it', key='matter_int1', where='name', meaning='pSenior') * \
#                   get(table='it_company', key='PofP', where='id_founder', meaning=call.from_user.id) / 100
#         expenditure = get(table='value_it', key='matter_int2', where='name', meaning='pSenior')
#         text = f'<b>Senior</b> програмист\n\n' \
#                f'<i>Прибыль</i>: {shell_money(pIncome)} руб./мин\n' \
#                f'<i>Зарплата</i>: {shell_money(expenditure)} руб./час\n' \
#                f'<i>Требования</i>: {rText}\n\n' \
#                f'У тебя работают: {shell_money(countSenior)} чел.'
#         try:
#             await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=text,
#                                         reply_markup=programmists_s)
#         except Exception as e:
#             pass
#     elif call.data == 'junior':
#         comp = get(table="it_company", key='comp', where='id_founder', meaning=call.from_user.id)
#         eqr = get(table='value_it', key='matter_text', where='name', meaning='pJunior')
#         if comp.split('_')[2] >= eqr.split('_')[2]:
#             staff = get(table="it_company", key='count_junior', where='id_founder', meaning=call.from_user.id) + \
#                     get(table="it_company", key='count_middle', where='id_founder', meaning=call.from_user.id) + \
#                     get(table="it_company", key='count_senior', where='id_founder', meaning=call.from_user.id)
#             rub = get(key='rub', where='id_user', meaning=call.from_user.id)
#             if staff + 1 <= workplace:
#                 time_ = time.strftime('%X').split()[0]
#                 time_work_min = 60 - int(time_.split(':')[1])
#                 time_work_sec = 60 - int(time_.split(':')[2])
#                 time_money = time_work_min * get(table='value_it', key='matter_int1', where='name', meaning='pJunior')
#                 if rub - time_money > 0:

#                     payment = rub - time_money
#                     updateN(key='rub', where='id_user', meaning=call.from_user.id, num=round(payment, 2))

#                     pIncome = get(table='value_it', key='matter_int1', where='name', meaning='pJunior') * \
#                               get(table='it_company', key='PofP', where='id_founder', meaning=call.from_user.id) / 100
#                     add(table='it_company', key='income', where='id_founder', meaning=call.from_user.id,
#                         num=round(pIncome, 2))

#                     add(table='it_company', key='count_junior', where='id_founder', meaning=call.from_user.id,
#                         num=1)
#                     text = f'Первая оплата была произведена за {shell_money(time_work_min)}мин. ' \
#                            f'{shell_money(time_work_sec)}сек. = {shell_money(time_money)}руб. работы программиста, ' \
#                            f'после она будет взиматься ' \
#                            f'ровно каждый час❗️'
#                     try:
#                         await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
#                                                     text=text,
#                                                     reply_markup=okJ)
#                     except Exception as e:
#                         pass
#                 else:
#                     await call.answer('На вашем счету недостаточно средств!', show_alert=True)
#             else:
#                 await call.answer(f'У вас нет мест {staff}/{workplace} заняты!', show_alert=True)
#         else:
#             await call.answer(f'У вас не соблюдены требования разроботчика!', show_alert=True)
#     elif call.data == 'middle':
#         comp = get(table="it_company", key='comp', where='id_founder', meaning=call.from_user.id)
#         wp = get(table="it_company", key='workplace', where='id_founder', meaning=call.from_user.id)
#         eqr = get(table='value_it', key='matter_text', where='name', meaning='pMiddle')
#         eqrW = eqr.split(',')[0]
#         eqrC = eqr.split(',')[1]
#         if comp.split('_')[2] >= eqrC.split('_')[2] and wp.split('_')[2] >= eqrW.split('_')[2]:
#             staff = get(table="it_company", key='count_junior', where='id_founder', meaning=call.from_user.id) + \
#                     get(table="it_company", key='count_middle', where='id_founder', meaning=call.from_user.id) + \
#                     get(table="it_company", key='count_senior', where='id_founder', meaning=call.from_user.id)
#             rub = get(key='rub', where='id_user', meaning=call.from_user.id)
#             if staff + 1 <= workplace:
#                 time_ = time.strftime('%X').split()[0]
#                 time_work_min = 60 - int(time_.split(':')[1])
#                 time_work_sec = 60 - int(time_.split(':')[2])
#                 time_money = time_work_min * get(table='value_it', key='matter_int1', where='name', meaning='pMiddle')
#                 if rub - time_money > 0:

#                     payment = rub - time_money
#                     updateN(key='rub', where='id_user', meaning=call.from_user.id, num=round(payment, 2))

#                     pIncome = get(table='value_it', key='matter_int1', where='name', meaning='pMiddle') * \
#                               get(table='it_company', key='PofP', where='id_founder', meaning=call.from_user.id) / 100
#                     add(table='it_company', key='income', where='id_founder', meaning=call.from_user.id,
#                         num=round(pIncome, 2))

#                     add(table='it_company', key='count_middle', where='id_founder', meaning=call.from_user.id,
#                         num=1)
#                     text = f'Первая оплата была произведена за {shell_money(time_work_min)}мин. ' \
#                            f'{shell_money(time_work_sec)}сек. = {shell_money(time_money)}руб. работы программиста, ' \
#                            f'после она будет взиматься ' \
#                            f'ровно каждый час❗️'
#                     try:
#                         await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
#                                                     text=text,
#                                                     reply_markup=okM)
#                     except Exception as e:
#                         pass
#                 else:
#                     await call.answer('На вашем счету недостаточно средств!', show_alert=True)
#             else:
#                 await call.answer(f'У вас нет мест {staff}/{workplace} заняты!', show_alert=True)
#         else:
#             await call.answer(f'У вас не соблюдены требования разроботчика!', show_alert=True)
#     elif call.data == 'senior':
#         comp = get(table="it_company", key='comp', where='id_founder', meaning=call.from_user.id)
#         wp = get(table="it_company", key='workplace', where='id_founder', meaning=call.from_user.id)
#         eqr = get(table='value_it', key='matter_text', where='name', meaning='pSenior')
#         eqrW = eqr.split(',')[0]
#         eqrC = eqr.split(',')[1]
#         if comp.split('_')[2] >= eqrC.split('_')[2] and wp.split('_')[2] >= eqrW.split('_')[2]:
#             staff = get(table="it_company", key='count_junior', where='id_founder', meaning=call.from_user.id) + \
#                     get(table="it_company", key='count_middle', where='id_founder', meaning=call.from_user.id) + \
#                     get(table="it_company", key='count_senior', where='id_founder', meaning=call.from_user.id)
#             rub = get(key='rub', where='id_user', meaning=call.from_user.id)
#             if staff + 1 <= workplace:
#                 time_ = time.strftime('%X').split()[0]
#                 time_work_min = 60 - int(time_.split(':')[1])
#                 time_work_sec = 60 - int(time_.split(':')[2])
#                 time_money = time_work_min * get(table='value_it', key='matter_int1', where='name', meaning='pSenior')
#                 if rub - time_money > 0:

#                     payment = rub - time_money
#                     updateN(key='rub', where='id_user', meaning=call.from_user.id, num=round(payment, 2))

#                     pIncome = get(table='value_it', key='matter_int1', where='name', meaning='pSenior') * \
#                               get(table='it_company', key='PofP', where='id_founder', meaning=call.from_user.id) / 100
#                     add(table='it_company', key='income', where='id_founder', meaning=call.from_user.id,
#                         num=round(pIncome, 2))

#                     add(table='it_company', key='count_senior', where='id_founder', meaning=call.from_user.id,
#                         num=1)
#                     text = f'Первая оплата была произведена за {shell_money(time_work_min)}мин. ' \
#                            f'{shell_money(time_work_sec)}сек. = {shell_money(time_money)}руб. работы программиста, ' \
#                            f'после она будет взиматься ' \
#                            f'ровно каждый час❗️'
#                     try:
#                         await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
#                                                     text=text,
#                                                     reply_markup=okS)
#                     except Exception as e:
#                         pass
#                 else:
#                     await call.answer('На вашем счету недостаточно средств!', show_alert=True)
#             else:
#                 await call.answer(f'У вас нет мест {staff}/{workplace} заняты!', show_alert=True)
#         else:
#             await call.answer(f'У вас не соблюдены требования разроботчика!', show_alert=True)
#     elif call.data == 'okay_j':
#         await call.answer(cache_time=0.1)
#         countJunior = get(table='it_company', key='count_junior', where='id_founder', meaning=call.from_user.id)
#         requirements = get(table='value_it', key='matter_text', where='name', meaning='pJunior')
#         rText = get(table='value_it', key='matter_text', where='name', meaning=requirements)
#         pIncome = get(table='value_it', key='matter_int1', where='name', meaning='pJunior') * \
#                   get(table='it_company', key='PofP', where='id_founder', meaning=call.from_user.id) / 100
#         expenditure = get(table='value_it', key='matter_int2', where='name', meaning='pJunior')
#         text = f'<b>Junior</b> програмист\n\n' \
#                f'<i>Прибыль</i>: {shell_money(pIncome)} руб./мин\n' \
#                f'<i>Зарплата</i>: {shell_money(expenditure)} руб./час\n' \
#                f'<i>Требования</i>: {rText}\n\n' \
#                f'У тебя работают: {shell_money(countJunior)} чел.'
#         try:
#             await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=text,
#                                         reply_markup=programmists_j)
#         except Exception as e:
#             pass
#     elif call.data == 'okay_m':
#         await call.answer(cache_time=0.1)
#         countJunior = get(table='it_company', key='count_middle', where='id_founder', meaning=call.from_user.id)
#         eqr = get(table='value_it', key='matter_text', where='name', meaning='pMiddle')
#         eqrW = eqr.split(',')[0]
#         eqrC = eqr.split(',')[1]
#         rText = get(table='value_it', key='matter_text', where='name', meaning=eqrW) + ', ' + \
#                 get(table='value_it', key='matter_text', where='name', meaning=eqrC)
#         pIncome = get(table='value_it', key='matter_int1', where='name', meaning='pMiddle') * \
#                   get(table='it_company', key='PofP', where='id_founder', meaning=call.from_user.id) / 100
#         expenditure = get(table='value_it', key='matter_int2', where='name', meaning='pMiddle')
#         text = f'<b>Middle</b> програмист\n\n' \
#                f'<i>Прибыль</i>: {shell_money(pIncome)} руб./мин\n' \
#                f'<i>Зарплата</i>: {shell_money(expenditure)} руб./час\n' \
#                f'<i>Требования</i>: {rText}\n\n' \
#                f'У тебя работают: {shell_money(countJunior)} чел.'
#         try:
#             await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=text,
#                                         reply_markup=programmists_m)
#         except Exception as e:
#             pass
#     elif call.data == 'okay_s':
#         await call.answer(cache_time=0.1)
#         countJunior = get(table='it_company', key='count_senior', where='id_founder', meaning=call.from_user.id)
#         eqr = get(table='value_it', key='matter_text', where='name', meaning='pSenior')
#         eqrW = eqr.split(',')[0]
#         eqrC = eqr.split(',')[1]
#         rText = get(table='value_it', key='matter_text', where='name', meaning=eqrW) + ', ' + \
#                 get(table='value_it', key='matter_text', where='name', meaning=eqrC)
#         pIncome = get(table='value_it', key='matter_int1', where='name', meaning='pSenior') * \
#                   get(table='it_company', key='PofP', where='id_founder', meaning=call.from_user.id) / 100
#         expenditure = get(table='value_it', key='matter_int2', where='name', meaning='pSenior')
#         text = f'<b>Senior</b> програмист\n\n' \
#                f'<i>Прибыль</i>: {shell_money(pIncome)} руб./мин\n' \
#                f'<i>Зарплата</i>: {shell_money(expenditure)} руб./час\n' \
#                f'<i>Требования</i>: {rText}\n\n' \
#                f'У тебя работают: {shell_money(countJunior)} чел.'
#         try:
#             await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=text,
#                                         reply_markup=programmists_s)
#         except Exception as e:
#             pass
#     elif call.data == 'dismiss_junior':
#         cP = get(table="it_company", key='count_junior', where='id_founder', meaning=call.from_user.id)
#         if cP - 1 >= 0:
#             await call.answer(cache_time=0.1)
#             add(table='it_company', key='count_junior', where='id_founder', meaning=call.from_user.id, num=-1)

#             countP = get(table='it_company', key='count_junior', where='id_founder', meaning=call.from_user.id)
#             requirements = get(table='value_it', key='matter_text', where='name', meaning='pJunior')
#             rText = get(table='value_it', key='matter_text', where='name', meaning=requirements)
#             pIncome = get(table='value_it', key='matter_int1', where='name', meaning='pJunior') * \
#                       get(table='it_company', key='PofP', where='id_founder', meaning=call.from_user.id) / 100
#             add(table='it_company', key='income', where='id_founder', meaning=call.from_user.id,
#                 num=-1 * round(pIncome, 2))
#             expenditure = get(table='value_it', key='matter_int2', where='name', meaning='pJunior')
#             text = f'<b>Junior</b> програмист\n\n' \
#                    f'<i>Прибыль</i>: {shell_money(pIncome)} руб./мин\n' \
#                    f'<i>Зарплата</i>: {shell_money(expenditure)} руб./час\n' \
#                    f'<i>Требования</i>: {rText}\n\n' \
#                    f'У тебя работают: {shell_money(countP)} чел.'
#             try:
#                 await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
#                                             text=text,
#                                             reply_markup=programmists_j)
#             except Exception as e:
#                 pass
#         else:
#             await call.answer(f'Вам нéкого увольнять 😅', show_alert=True)
#     elif call.data == 'dismiss_middle':
#         cP = get(table="it_company", key='count_middle', where='id_founder', meaning=call.from_user.id)
#         if cP - 1 >= 0:
#             await call.answer(cache_time=0.1)
#             add(table='it_company', key='count_middle', where='id_founder', meaning=call.from_user.id, num=-1)

#             countP = get(table='it_company', key='count_middle', where='id_founder', meaning=call.from_user.id)
#             eqr = get(table='value_it', key='matter_text', where='name', meaning='pMiddle')
#             eqrW = eqr.split(',')[0]
#             eqrC = eqr.split(',')[1]
#             rText = get(table='value_it', key='matter_text', where='name', meaning=eqrW) + ', ' + \
#                 get(table='value_it', key='matter_text', where='name', meaning=eqrC)
#             pIncome = get(table='value_it', key='matter_int1', where='name', meaning='pMiddle') * \
#                       get(table='it_company', key='PofP', where='id_founder', meaning=call.from_user.id) / 100
#             add(table='it_company', key='income', where='id_founder', meaning=call.from_user.id,
#                 num=-1 * round(pIncome, 2))
#             expenditure = get(table='value_it', key='matter_int2', where='name', meaning='pMiddle')
#             text = f'<b>Middle</b> програмист\n\n' \
#                    f'<i>Прибыль</i>: {shell_money(pIncome)} руб./мин\n' \
#                    f'<i>Зарплата</i>: {shell_money(expenditure)} руб./час\n' \
#                    f'<i>Требования</i>: {rText}\n\n' \
#                    f'У тебя работают: {shell_money(countP)} чел.'
#             try:
#                 await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
#                                             text=text,
#                                             reply_markup=programmists_m)
#             except Exception as e:
#                 pass
#         else:
#             await call.answer(f'Вам нéкого увольнять 😅', show_alert=True)
#     elif call.data == 'dismiss_senior':
#         cP = get(table="it_company", key='count_senior', where='id_founder', meaning=call.from_user.id)
#         if cP - 1 >= 0:
#             await call.answer(cache_time=0.1)
#             add(table='it_company', key='count_senior', where='id_founder', meaning=call.from_user.id, num=-1)

#             countP = get(table='it_company', key='count_senior', where='id_founder', meaning=call.from_user.id)
#             eqr = get(table='value_it', key='matter_text', where='name', meaning='pSenior')
#             eqrW = eqr.split(',')[0]
#             eqrC = eqr.split(',')[1]
#             rText = get(table='value_it', key='matter_text', where='name', meaning=eqrW) + ', ' + \
#                 get(table='value_it', key='matter_text', where='name', meaning=eqrC)
#             pIncome = get(table='value_it', key='matter_int1', where='name', meaning='pSenior') * \
#                       get(table='it_company', key='PofP', where='id_founder', meaning=call.from_user.id) / 100
#             add(table='it_company', key='income', where='id_founder', meaning=call.from_user.id,
#                 num=-1 * round(pIncome, 2))
#             expenditure = get(table='value_it', key='matter_int2', where='name', meaning='pSenior')
#             text = f'<b>Senior</b> програмист\n\n' \
#                    f'<i>Прибыль</i>: {shell_money(pIncome)} руб./мин\n' \
#                    f'<i>Зарплата</i>: {shell_money(expenditure)} руб./час\n' \
#                    f'<i>Требования</i>: {rText}\n\n' \
#                    f'У тебя работают: {shell_money(countP)} чел.'
#             try:
#                 await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
#                                             text=text,
#                                             reply_markup=programmists_s)
#             except Exception as e:
#                 pass
#         else:
#             await call.answer(f'Вам нéкого увольнять 😅', show_alert=True)
#     else:
#         print(call.data)


@dp.message_handler(content_types=['text'])
async def any_text(message: Message):
    await message.answer('Главное меню', reply_markup=keyboard_default.main_page)