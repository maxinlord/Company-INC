import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

    def user_exists(self, id_user):
        """Проверяем, есть ли юзер в базе"""
        result = self.cur.execute("SELECT `id_user` FROM `users` WHERE `id_user` = ?", (id_user,))
        return bool(len(result.fetchall()))
    
    def get_user_referals(self,id_user):
        '''Получаем кортеж состоящий из ([список], кол-во) рефералов юзера'''
        result = [i[0] for i in self.cur.execute(f'SELECT username FROM users WHERE referrer = "{id_user}"')]
        return (result,len(result))

    def add_new_text(self, name):
        self.cur.execute("INSERT INTO `texts` (`name`) VALUES (?)", (name,))
        return self.conn.commit()
    
    def add_new_button(self, number):
        self.cur.execute("INSERT INTO `button_name` (`number`) VALUES (?)", (number,))
        return self.conn.commit()

    def add_user(self, id_user):
        """Добавляем юзера в базу"""
        self.cur.execute("INSERT INTO `users` (`id_user`) VALUES (?)", (id_user,))
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
    
    def add_stocks(self, id_slot, seller, id_stocks, quantity_stocks, price_one_stock, percent_of_income):
        self.cur.execute(f"INSERT INTO stocks (id_slot, seller, id_stocks, quantity_stocks, price_one_stock, percent_of_income) VALUES (?, ?, ?, ?, ?, ?)", (id_slot, seller, id_stocks, quantity_stocks, price_one_stock, percent_of_income))
        return self.conn.commit()

    def add(self, key, where, meaning, table='users', num=0):
        '''Добавляем любое значение к числу в БД'''
        result = self.cur.execute(f"""SELECT {key} FROM {table} WHERE {where} = '{meaning}'""")
        self.cur.execute(f"""UPDATE {table} SET {key} = {num + result.fetchone()[0]} WHERE {where} = '{meaning}'""")
        return self.conn.commit()

    def get(self, key, where, meaning, table='users'):
        '''Позволяет получить любое значение из БД'''
        result = self.cur.execute(f"""SELECT {key} FROM {table} WHERE {where} = '{meaning}'""")
        return result.fetchone()[0]
    
    def get_all(self, key, table='users'):
        '''Позволяет получить любые значение из БД'''
        result = self.cur.execute(f"""SELECT {key} FROM {table}""")
        result = list(map(lambda x: x[0], result.fetchall()))
        return result  
    
    def get_alls(self, keys, table='users'):
        '''Позволяет получить любые значение из БД'''
        result = self.cur.execute(f"""SELECT {keys} FROM {table}""")
        return result.fetchall()  

    def get_alls_with_order(self, keys, order, table='users'):
        '''Позволяет получить любые значение из БД'''
        result = self.cur.execute(f"""SELECT {keys} FROM {table} ORDER BY {order} DESC""")
        return result.fetchall()  

    def delete(self, where, meaning, table='users'):
        '''Позволяет удалить любые значение из БД'''
        self.cur.execute(f'DELETE FROM {table} WHERE {where} = "{meaning}"')
        return self.conn.commit()

    def updateT(self, key, where, meaning, table='users', text=''):
        '''Позволяет обновить любой текст в БД'''
        self.cur.execute(f"""UPDATE {table} SET {key} = '{text}' WHERE {where} = '{meaning}'""")
        return self.conn.commit()
   
    def updateN(self, key, where, meaning, table='users', num=0):
        '''Позволяет обновить любое число в БД'''
        self.cur.execute(f"""UPDATE {table} SET {key} = {num} WHERE {where} = '{meaning}'""")
        return self.conn.commit()

    def count_dev(self, id_user):
        quantity = 0
        for i in range(1,3+1):
            quantity += self.cur.execute(f"""SELECT quantity_dev_{i} FROM dev_software WHERE id_company = '{id_user}'""").fetchone()[0]
        return quantity

    def vCollector(self, table, where, meaning, mn=False) -> tuple:
        ratio = self.cur.execute(f"""SELECT ratio FROM {table} WHERE {where} = '{meaning}'""").fetchone()[0]
        main_num = self.cur.execute(f"""SELECT main_num FROM {table} WHERE {where} = '{meaning}'""").fetchone()[0]
        plus_num = self.cur.execute(f"""SELECT plus_num FROM {table} WHERE {where} = '{meaning}'""").fetchone()[0]
        num = ratio * main_num + plus_num
        margin = ratio - 1 * 100
        if mn:
            return (num, margin)
        return num


    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()


