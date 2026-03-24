from datetime import datetime, timedelta


class AirTicket:
    name_air_company = 'Roman_airlines'

    def __init__(self, name, surname, country):
        self._name = name
        self._surname = surname
        self._country = country
        self.time_up = datetime.now() + timedelta(days=1)
        self.time_down = self.time_up + timedelta(hours=4)

    @property
    def name(self):
        return self._name

    @property
    def surname(self):
        return self._surname

    @property
    def country(self):
        return self._country

    @name.setter
    def name(self, name):
        if len(name.split()) != 1:
            raise ValueError(f"Имя '{name}' должно состоять из 1 слова")
        if not name.strip().isalpha():
            raise ValueError(f"Имя '{name}' должно состоять только из букв")
        self._name = name.strip()

    @surname.setter
    def surname(self, surname):
        if len(surname.split()) != 1:
            raise ValueError(f"Фамилия '{surname}' должна состоять из 1 слова")
        if not surname.strip().isalpha():
            raise ValueError(f"Фамилия '{surname}' должна состоять только из букв")
        self._surname = surname.strip()

    @country.setter
    def country(self, country):
        if len(country.split()) != 1:
            raise ValueError(f"Страна '{country}' должна состоять из 1 слова")
        if not country.strip().isalpha():
            raise ValueError(f"Страна '{country}' должна состоять только из букв")
        self._country = country

    @classmethod
    def from_string(cls, string):
        if len(string.split()) != 3:
            raise ValueError('Йоу, введи корректные значения: Имя, Фамилия, Страна - через пробел')
        name, surname, country = string.strip().split()
        if not name.strip().isalpha():
            raise ValueError(f"Имя '{name}' должно состоять только из букв")
        if not surname.strip().isalpha():
            raise ValueError(f"Фамилия '{surname}' должна состоять только из букв")
        if not country.strip().isalpha():
            raise ValueError(f"Страна '{country}' должна состоять только из букв")
        return cls(name, surname, country)

    @staticmethod
    def hi():
        return f'Здравствуйте, мы рады приветствовать Вас в нашей авиакомпании {AirTicket.name_air_company}'


    def change_time_hours(self, hours):
        if not hours.isdigit():
            raise ValueError('Значение часов должно быть целым числом')
        hours = int(hours)
        self.time_up = self.time_up + timedelta(hours=hours)
        self.time_down = self.time_down + timedelta(hours=hours)

    @classmethod
    def change_name_company(cls, new_name_company):
        cls.name_air_company = new_name_company



ticket = AirTicket('Roman', 'Prokhorenko', 'USA')
print(ticket.hi())

print(ticket.name)
print(ticket.surname)
print(ticket.country)
print(ticket.time_up)
print(ticket.time_down)

ticket.name = 'Alexander'
print(ticket.name)
