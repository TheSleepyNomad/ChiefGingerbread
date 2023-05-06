from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Btn:
    menu = '\U0001F9FE' + ' Меню'
    cart = '\U0001F6D2' + ' Корзина'
    catalog = '\U0001F3F7' + ' Каталог'
    pay_card = '\U0001F4B3' + ' Оплатить'
    web_site = '\U0001F310' + ' На сайт'
    video = '\U0001F39E' + ' Процесс готовки'
    delete_backet = '\U0000274C' + ' Очистить корзину'
