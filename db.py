
import sqlite3


# path_db_for_mac = '/Users/jcu/Documents/GitHub/Company-INC/server.db'
# path_db = 'C:\\Users\\Admin\Desktop\\MyProjects\\Company INC\\server.db'
path_db = 'my_bot/Company-INC/server.db'


# def clean_string(input):
#     return re.sub(r"[^\w{}:.,_ =']", "", input)

# def event_sourced(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         # Execute the function and get the result
#         result = fn(*args, **kwargs)
        
#         # Get the current time
#         now = datetime.datetime.now()
        
#         # Get the event data
#         event_data = {
#             'ts': now.isoformat(),
#             'f': fn.__name__,
#             # 'args': args,
#             'k': kwargs,
#             'r': result 
#         }
#         text = clean_string(f'{event_data}')
#         with open('event_log.txt', 'a') as event_log:
#             event_log.write(text)
#             event_log.write('\n')
#         # Append the event to the event log
#         # with open('even_log.json', 'w') as json_file:
#         #     json.dump(event_data, json_file, indent=4, ensure_ascii=True)
        
#         return fn(*args, **kwargs)
#     return wrapper

class BotDB:

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
    
    def create_connection(self):
        new_conn = sqlite3.connect(self.db_file)
        new_cur = new_conn.cursor()
        return new_conn, new_cur

    def user_exists(self, id_user):
        """Проверяем, есть ли юзер в базе"""
        result = self.cur.execute("SELECT `id_user` FROM `users` WHERE `id_user` = ?", (id_user,))
        return bool(len(result.fetchall()))
    
    def get_user_referals(self, id_user):
        '''Получаем кортеж состоящий из ([список], кол-во) рефералов юзера'''
        result = [i[0] for i in self.cur.execute("SELECT username FROM users WHERE referrer = (?)", (id_user))]
        return (result, len(result))

    def add_new_text(self, name):
        self.cur.execute("INSERT INTO `texts` (`name`) VALUES (?)", (name,))
        return self.conn.commit()
    
    def add_new_slot_weights(self, id_user):
        self.cur.execute("INSERT INTO `weights` (`id_user`) VALUES (?)", (id_user,))
        return self.conn.commit()
    
    def add_new_button(self, number):
        self.cur.execute("INSERT INTO `button_name` (`number`) VALUES (?)", (number,))
        return self.conn.commit()

    def add_user(self, id_user):
        """Добавляем юзера в базу"""
        self.cur.execute("INSERT INTO `users` (`id_user`) VALUES (?)", (id_user,))
        self.add_new_slot_weights(id_user)
        return self.conn.commit()
    
    def add_support_message(self, tag, id_user, message, info_message):
        self.cur.execute("INSERT INTO `message_in_support` (tag, id_user, message, info_message) VALUES (?, ?, ?, ?)", (tag, id_user, message, info_message))
        return self.conn.commit()
    
    def add_new_app(self, id_company, name_app, one_pay, income, date_reg, quantity_min_build):
        self.cur.execute("INSERT INTO `dev_software_apps` (id_company, name_app, one_pay, income, date_reg, quantity_min_build) VALUES (?, ?, ?, ?, ?, ?)", (id_company, name_app, one_pay, income, date_reg, quantity_min_build))
        return self.conn.commit()

    def add_company(self, id_user, table):
        """Добавляем компанию юзера в базу"""
        result = self.cur.execute("SELECT `name` FROM `users` WHERE `id_user` = ?", (id_user,))
        name = result.fetchone()[0]
        self.cur.execute(f"INSERT INTO {table} (id_company, name_founder) VALUES (?,?)", (id_user, name))
        return self.conn.commit()
    
    def add_stocks(self, id_slot, seller, id_stocks, quantity_stocks, percent_of_income, currency):
        self.cur.execute("INSERT INTO stocks (id_slot, seller, id_stocks, quantity_stocks, percent_of_income, currency) VALUES (?, ?, ?, ?, ?, ?)", (id_slot, seller, id_stocks, quantity_stocks, percent_of_income, currency))

        return self.conn.commit()
    
    # def get_tables_name(self):
    #     result = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    #     return result.fetchone()[0]
    # def add(self, key, where, meaning, table='users', num=0):
    #     '''Добавляем любое значение к числу в БД'''
    #     result = self.cur.execute(f"""SELECT {key} FROM {table} WHERE {where} = '{meaning}'""")
    #     self.cur.execute(f"""UPDATE {table} SET {key} = {num + result.fetchone()[0]} WHERE {where} = '{meaning}'""")
    #     return self.conn.commit()

    def add(self, key, where, meaning, table='users', num=0):
        '''Добавляем любое значение к числу в БД'''
        query = f"SELECT {key} FROM {table} WHERE {where} = ?"
        result = self.cur.execute(query, (meaning,))
        query = f"UPDATE {table} SET {key} = ? WHERE {where} = ?"
        self.cur.execute(query, (num + result.fetchone()[0], meaning))
        return self.conn.commit()

    
    # @event_sourced
    # def get(self, key, where, meaning, table='users'):
    #     '''Позволяет получить любое значение из БД'''
    #     result = self.cur.execute(f"""SELECT {key} FROM {table} WHERE {where} = '{meaning}'""")
    #     return result.fetchone()[0]
    def get(self, key, where, meaning, table='users'):
        '''Get any value from the database'''
        result = self.cur.execute(f"SELECT {key} FROM {table} WHERE {where} = ?", (meaning,))
        return result.fetchone()[0]

    
    def get_all(self, key, table='users'):
        result = self.cur.execute(f"""SELECT {key} FROM {table}""")
        result = list(map(lambda x: x[0], result.fetchall()))
        return result  
    
    def get_alls(self, keys, table='users'):
        result = self.cur.execute(f"""SELECT {keys} FROM {table}""")
        return result.fetchall()  

    def get_alls_with_order(self, keys, order, table='users'):
        result = self.cur.execute(f"""SELECT {keys} FROM {table} ORDER BY {order} DESC""")
        return result.fetchall()  

    def delete(self, where, meaning, table='users'):
        self.cur.execute(f'DELETE FROM {table} WHERE {where} = ?', (meaning,))
        return self.conn.commit()

    def updateT(self, key, where, meaning, table='users', text=''):
        self.cur.execute(f'UPDATE {table} SET {key} = "{text}" WHERE {where} = ?', (meaning,))
        return self.conn.commit()
   
    def updateN(self, key, where, meaning, table='users', num=0):
        '''Позволяет обновить любое число в БД'''
        self.cur.execute(f'UPDATE {table} SET {key} = {num} WHERE {where} = ?', (meaning,))
        return self.conn.commit()

    def vCollector(self, table, where, meaning, wNum=(1, 0), perc=False, mn=False) -> float:
        ratio_query = f"SELECT ratio FROM {table} WHERE {where} = ?"
        main_num_query = f"SELECT main_num FROM {table} WHERE {where} = ?"
        plus_num_query = f"SELECT plus_num FROM {table} WHERE {where} = ?"

        ratio = self.cur.execute(ratio_query, (meaning,)).fetchone()[0]
        main_num = self.cur.execute(main_num_query, (meaning,)).fetchone()[0]
        plus_num = self.cur.execute(plus_num_query, (meaning,)).fetchone()[0]
        
        unique_ratio, unique_plus = wNum
        i = 100 if perc else 1
        return ((unique_ratio - 1) + ratio) * main_num + ((plus_num + unique_plus) / i)

    def close(self, conn):
        """Закрываем соединение с БД"""
        conn.close()


