"""
Verydelivery
Модуль генерирует случайные адреса для тестирования ПО службы доставки
"""

import json
import re
import random


DATA_FILE = 'c:\\test\\ru-spb.json'
JSON_TEST_FAIL = '{"Country" : "Росс!и#я", "City" : "Москва", ' \
            '"Streets" : ["пр. Тверской", "пр. Сахарова", "ул. +Варварка",' \
            '"Моховая ул.", "бул. 1-й !Пятилетки", "ул. Лёни Голикова"]}'
JSON_TEST_OK = '{"Country" : "Россия", "City" : "Москва", ' \
            '"Streets" : ["пр. Тверской0", "пр. Сахарова0", "ул. Варварка0",' \
            '"Моховая ул.", "бул. 1-й Пятилетки", "ул. Лёни Голикова"]}'


def checkinput(data: str):
    """
    Процедура проверки входных данных на допустимые символы в адресе
    :param data: проверяемая строка
    :return: True в случае успешного прохождения проверки
    """
    try:
        if not isinstance(data, str):
            raise TypeError
        match = re.search(r'[^\w. -]', data)
        if match:
            raise ValueError
        else:
            # print("[OK]:{}".format(data))
            return True

    except ValueError as e:
        print("Value are not correct: {} is wrong".format(data))
        raise e
    except TypeError as e:
        print("Type is not correct: {} is {}".format(data, type(data)))
        raise e


def checkaddresses(country, city, streets):
    """
    Процедура проверки набора входных данных на допустимые символы в адресе

    :param country: проверяемая строка - название страны
    :param city: проверяемая строка - название города
    :param streets: проверяемая строка - название улицы
    :return: True в случае успешного прохождения проверки
    """
    try:
        checkinput(country)
        checkinput(city)
        for x in streets:
            checkinput(x)

        return True

    except (ValueError, TypeError) as e:
        print("The input data is wrong")
        raise e


def getaddressesfromjsonstring(jsonstr: str):
    """
    Процедура извлечения данных об адресе из строки формата JSON и проверки полученных данных на допустимые символы
    :param jsonstr: входящая json-строка
    :return: объект с данными об адресе {dict}, полученном в результате парсинга json-строки
    """

    data = json.loads(jsonstr)

    try:
        checkaddresses(data['Country'], data['City'], data['Streets'])
        return data

    except (ValueError, TypeError):
        print("Ошибка во входной json-строке:\n{}".format(data))
        return None


def loadaddressesfromjsonfile(fname=DATA_FILE):
    """
    Процедура извлечения данных об адресе из файла с данными формата JSON
    и проверки полученных данных на допустимые символы
    :param fname: имя файла с данными в формате json
    :return: объект с данными об адресе {dict}, полученном в результате парсинга json-строки из файла
    """
    with open(fname, encoding='utf8') as f:
        data = json.load(f)

    try:
        checkaddresses(data['Country'], data['City'], data['Streets'])
        return data

    except (ValueError, TypeError):
        print("Ошибка в json-строке файла:\n{}".format(data))
        return None


def getrandomaddress(data=None, country=None, city=None, streets=None):
    """
    Объект-генератор, генерирует случайные образом адрес из передаваемого набора данных о стране, городе и списка улиц
    :param data: объект с данными об адресе - словарь {'Country':'countryname', 'City':'cityname', 'Streets':[list]}
    Словарь входных данных может может принимать значение None, если входные данные передаются через переменные
    country, city, streets.
    Если словарь входных данных передан, то данные в переменных country, city, streets игнорируются
    :param country: строка с названием страны. Будет проигнорировано, если передан словарь data.
    :param city: строка с названием города. Будет проигнорировано, если передан словарь data.
    :param streets: список с названием улиц. Будет проигнорирован, если передан словарь data.
    :return: str , строка с полным случайным адресом, включающим номер дома, корпус и номер квартиры
    """

    try:
        if data is not None:
            country = data['Country']
            city = data['City']
            streets = data['Streets']
        elif (country is None) or (city is None) or (streets is None):
            raise ValueError
    except ValueError:
        print("Ошибка во входных параметрах функции-генератора")
        raise ValueError

    # print("Init data\nCountry:{}\nCity:{}\nStreets:{}".format(country, city, streets))
    counter = -1

    while True:
        counter += 1
        house = ', д.' + str(random.randint(1, 100))

        if random.randint(0, 9) == 0:
            # адреса с корпусами будем генерировать в 10 раз реже
            korp = ', корп.' + str(random.randint(1, 5))
        else:
            korp = ''
        flat = ', кв.' + str(random.randint(1, 100))
        yield country + ', ' + city + ', ' + random.choice(streets) + house + korp + flat


def testdecorate(keyword="test"):
    """
    Декоратор условного выполнения функции.

    :param keyword: ключевое значение параметра
    :return: Если при вызове декорированной функции значения хотя бы одного из аргументов было равно указанному,
    то функция не вызывается, а вместо нее в консоль выводится строка вида
    'Вызов функции {{name}} с параметрами {{список параметров}}', иначе - возвращается результат выполнения декорируемой
    функции
    """
    def testdecorator(func):
        def wrapper(*args, **kwargs):
            for x in args:
                if x == keyword:
                    return "Вызов функции {} с параметрами {}{}".format(func.__name__, args, kwargs)
            for x in kwargs:
                if kwargs[x] == keyword:
                    return "Вызов функции {} с параметрами {}{}".format(func.__name__, args, kwargs)

            return func(*args, **kwargs)

        return wrapper

    return testdecorator


@testdecorate()
def __test(a, b, c):
    """
    Тестовая функция для проверки работы декоратора
    :param a: int, 1-е слагаемое
    :param b: int, 2-е слагаемое
    :param c: int, 3-е слагаемое
    :return: сумма трёх слагаемых
    """
    return a + b + c


if __name__ == "__main__":

    """
    ТЕСТ-1
    Вариант генерации случайной адресов при уловии получения объекта об адресе из JSON - строки

    xd = getaddressesfromjsonstring(JSON_TEST_OK)
    gen = getrandomaddress(data=xd)
    print(next(gen))
    print(next(gen))
    """

    """
    ТЕСТ-2
    Вариант попытки получения объекта об адресе из JSON - строки С ОШИБКОЙ в адресах

    xd = getaddressesfromjsonstring(JSON_TEST_FAIL)
    gen = getrandomaddress(data=xd)
    print(next(gen))
    print(next(gen))
    """

    """
    ТЕСТ-3
    Вариант генерации случайной адресов при уловии получения объекта об адресов с передачей 
    входных данных не из json-строки или файла

    gen = getrandomaddress(country="Russia", city="SPb",
                           streets=["Моховая ул.", "бул. 1-й Пятилетки", "ул. Лёни Голикова"])
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
    """

    """
    ТЕСТ-4
    Вариант генерации случайных адресов при уловии получения объекта об адресах 
    с передачей входных данных файла с json-строкой
    """
    xd = loadaddressesfromjsonfile()
    gen = getrandomaddress(data=xd)
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))

    """
    Тестирование рвботы декоратора
    """
    print(__test(1, 3, "test"))
    print(__test(1, 3, 4, somedata="test"))
    print(__test(1, 3, 4))
