


from dispatcher import BotDB
from all_function import parse_2dot_data, get_2dot_data, Weight


class User:

    def __init__(self, id_user):
        # self.BotDB = BotDB('/Users/jcu/Desktop/MyProjects/Company INC/server.db')
        self.BotDB = BotDB

        self.id: int = id_user
        self.weight = Weight(self.id)
        self.username: str = self.BotDB.get(key='username', where='id_user', meaning=self.id)
        self.name: str = self.BotDB.get(key='name', where='id_user', meaning=self.id)

    @property
    def verify(self):
        return self.BotDB.get(key='verify', where='id_user', meaning=self.id)

    @property
    def active(self):
        return self.BotDB.get(key='active', where='id_user', meaning=self.id)

    @property
    def amount_of_changes_nickname(self):
        return self.BotDB.get(key='amount_of_changes_nickname', where='id_user', meaning=self.id)
    
    @property
    def number_of_requests(self):
        return self.BotDB.get(key='number_of_requests', where='id_user', meaning=self.id)

    @property
    def count_tap(self):
        return self.BotDB.get(key='count_tap', where='id_user', meaning=self.id)

    @property
    def referrer(self):
        return self.BotDB.get(key='referrer', where='id_user', meaning=self.id)

    @property
    def date_reg(self):
        return self.BotDB.get(key='date_reg', where='id_user', meaning=self.id)

    @property
    def last_tap(self):
        return self.BotDB.get(key='last_tap', where='id_user', meaning=self.id)

    @property
    def bonus(self):
        return self.BotDB.get(key='bonus', where='id_user', meaning=self.id)

    @property
    def nickname(self):
        return self.BotDB.get(key='nickname', where='id_user', meaning=self.id)

    @property
    def type_of_activity(self):
        return self.BotDB.get(key='type_of_activity', where='id_user', meaning=self.id)

    @property
    def rub(self):
        return round(self.BotDB.get(key='rub', where='id_user', meaning=self.id), 2)

    @property
    def usd(self):
        return round(self.BotDB.get(key='usd', where='id_user', meaning=self.id), 2)

    @property
    def btc(self):
        return round(self.BotDB.get(key='btc', where='id_user', meaning=self.id), 5)

    @property
    def company_name(self):
        return self.BotDB.get(key='name_company', where='id_company', meaning=self.id, table=self.type_of_activity)

    @property
    def total_income_from_stocks(self):
        return self.BotDB.get(key='total_income_from_stocks', where='id_user', meaning=self.id)


class DevSoftware:

    def __init__(self, id_company) -> None:
        self.user: User = User(id_company)

    def get_quantity_dev(self, dev: int):
        if dev in {1, 2, 3}:
            return self.user.BotDB.get(key=f'quantity_dev_{dev}', where='id_company', meaning=self.user.id,
                                       table='dev_software')

    def get_quantity_device(self, device: int, lvl: int):
        try:
            return get_2dot_data(key=f'quantity_device_{device}', where='id_company', meaning=self.user.id,
                                 table='dev_software', where_data='lvl', meaning_data=str(lvl), get_data='quantity')
        except Exception as e:
            return None

    def get_quantity_buy_office(self, office: int):
        return get_2dot_data(key=f'quantity_office_{office}', where='id_company', meaning=self.user.id,
                             table='dev_software', meaning_data='1', get_data='buy')

    def get_quantity_rent_office(self, office: int):
        return get_2dot_data(key=f'quantity_office_{office}', where='id_company', meaning=self.user.id,
                             table='dev_software', meaning_data='1', get_data='rent')

    @property
    def quantity_devices(self):
        i = 1
        ind = 1
        q_devices = 0
        y = True
        while y:
            data = parse_2dot_data(key=f'quantity_device_{ind}', where='id_company', meaning=self.user.id,
                                   table='dev_software')
            ind_q = data[0].index('quantity')
            for i in data[1:]:
                q_devices += i[ind_q]
            try:
                ind += 1
                self.user.BotDB.get(table='dev_software', key=f'quantity_device_{ind}', where='id_company',
                                    meaning=self.user.id)
            except:
                y = False
        return q_devices

    @property
    def data_centre_foreign(self):
        return get_2dot_data(key='data_centre', where='id_company', meaning=self.user.id, table='dev_software', meaning_data='1', get_data='foreign')

    @property
    def data_centre_home(self):
        return get_2dot_data(key='data_centre', where='id_company', meaning=self.user.id, table='dev_software', meaning_data='1', get_data='home')

    @property
    def cd_time_app(self):
        return self.user.BotDB.get(key='cd_time_app', where='id_company', meaning=self.user.id, table='dev_software')

    @property
    def quantity_all_devs(self):
        return sum(self.get_quantity_dev(i) for i in range(1, 3 + 1))

    @property
    def quantity_all_places(self):
        i = 1
        y = True
        own_base_places = BotDB.vCollector(table='value_it', where='name', meaning='own_base_office', wNum=self.user.weight.get_weight('own_base_office'))

        places = own_base_places
        while y:
            p = parse_2dot_data(key=f'quantity_office_{i}', where='id_company', meaning=self.user.id,
                                table='dev_software')
            places += (p[1][1] + p[1][2]) * self.user.BotDB.vCollector(where='name', meaning=f'size_office_{i}',
                                                                       table='value_it',
                                                                       wNum=self.user.weight.get_weight(
                                                                           f'size_office_{i}'))
            try:
                i += 1
                self.user.BotDB.vCollector(where='name', meaning=f'cost_office_{i}', table='value_it',
                                           wNum=self.user.weight.get_weight(f'cost_office_{i}'))
            except:
                y = False
        return places



