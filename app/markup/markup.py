from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from app.database.methods.get import get_count_all_products, get_cart_by_user, get_all_products
from app.database.methods.other import check_user_baket_exist
from math import ceil
from json import loads as json_loads
from app.utils.utils import _get_data_from_json

def create_start_markup(user_id: int) -> InlineKeyboardMarkup:
    count_products = get_count_all_products()
    count = ceil(count_products / 5)
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('На сайт', callback_data='web_site'))
    markup.add(InlineKeyboardButton('Процесс готовки', callback_data='description'))
    markup.add(InlineKeyboardButton('Каталог', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":\"1\",\"CountPage\":"+ str(count) +"}"))
    if check_user_baket_exist(user_id):
        user_products_count = ceil(len(get_cart_by_user(user_id)) / 5)
        markup.add(InlineKeyboardButton('Корзина', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":\"1\",\"CountPage\":" + str(user_products_count) + "}"))

    return markup

def create_catalog_markup(query: CallbackQuery) -> InlineKeyboardMarkup:
    request = query.data.split('_')
    if "pagin" in request[0]:
        products = get_all_products()
        data = _get_data_from_json(query)
        markup = InlineKeyboardMarkup()

        # init our pagination
        for product in products[data.slicer - 5:data.slicer]:
                item = json_loads(str(product))
                markup.add(InlineKeyboardButton(item['name'], callback_data="{\"page\":\"card\",\"prodId\":" + str(item['id']) + ",\"PageNum\":" + str(data.page + 1)+ ",\"CountPage\":" + str(data.count_page)+"}"))
        
        if data.page == 1:
            if data.count_page <= 1:
                markup.add(
                    InlineKeyboardButton('<--', callback_data=" "),
                    InlineKeyboardButton(f'{data.page}/{data.count_page}', callback_data=" "),
                    InlineKeyboardButton('-->', callback_data=" "),
                )
            else:
                markup.add(
                    InlineKeyboardButton('<--', callback_data=" "),
                    InlineKeyboardButton(f'{data.page}/{data.count_page}', callback_data=" "),
                    InlineKeyboardButton('-->', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":" + str(data.page + 1)+ ",\"CountPage\":" + str(data.count_page)+"}"),
                )

        elif data.page == data.count_page:
            markup.add(
                InlineKeyboardButton('<--', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":" + str(data.page - 1)+ ",\"CountPage\":" + str(data.count_page)+"}"),
                InlineKeyboardButton(f'{data.page}/{data.count_page}', callback_data=" "),
                InlineKeyboardButton('-->', callback_data=" "),
            )

        else:
            markup.add(
                InlineKeyboardButton('<--', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":" + str(data.page - 1)+ ",\"CountPage\":" + str(data.count_page)+"}"),
                InlineKeyboardButton(f'{data.page}/{data.count_page}', callback_data=" "),
                InlineKeyboardButton('-->', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":" + str(data.page + 1)+ ",\"CountPage\":" + str(data.count_page)+"}"),
            )

        markup.add(InlineKeyboardButton('Вернуться в меню', callback_data='menu'))
        return markup
    

def create_cart_markup(query: CallbackQuery) -> InlineKeyboardMarkup:
    request = query.data.split('_')

    if 'pagin' in request[0]:
        # get user cart
        products = get_cart_by_user(query.message.chat.id)
        data = _get_data_from_json(query)
        print(data)

        json_string = json_loads(request[0])
        page = int(json_string['PageNum'])
        count = json_string['CountPage']

        # set slicer for List[Products]
        slicer = int(5 * page)

        # set new markup with products name
        markup = InlineKeyboardMarkup()

        # init our pagination
        for product in products[slicer - 5:slicer]:
            markup.add(InlineKeyboardButton(f'{product.name} | Кол-во {product.quantity} | Цена {product.price} руб.', callback_data="{\"page\":\"item\",\"orderId\":" + str(product.id) + ",\"PageNum\":" + str(data.page + 1)+ ",\"CountPage\":" + str(data.count_page)+"}"))
        

        if data.page == 1:
            if data.count_page <= 1:
                markup.add(
                    InlineKeyboardButton('<--', callback_data=" "),
                    InlineKeyboardButton(f'{data.page}/{data.count_page}', callback_data=" "),
                    InlineKeyboardButton('-->', callback_data=" "),
                )
            else:
                markup.add(
                        InlineKeyboardButton('<--', callback_data=" "),
                        InlineKeyboardButton(f'{data.page}/{data.count_page}', callback_data=" "),
                        InlineKeyboardButton('-->', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":" + str(data.page + 1)+ ",\"CountPage\":" + str(data.count_page)+"}"),
                    )

        elif page == count:
            markup.add(
                InlineKeyboardButton('<--', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":" + str(data.page - 1)+ ",\"CountPage\":" + str(data.count_page)+"}"),
                InlineKeyboardButton(f'{data.page}/{data.count_page}', callback_data=" "),
                InlineKeyboardButton('-->', callback_data=" "),
            )

        else:
            markup.add(
                InlineKeyboardButton('<--', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":" + str(data.page - 1)+ ",\"CountPage\":" + str(data.count_page)+"}"),
                InlineKeyboardButton(f'{data.page}/{data.count_page}', callback_data=" "),
                InlineKeyboardButton('-->', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":" + str(data.page + 1)+ ",\"CountPage\":" + str(data.count_page)+"}"),
            )

        markup.add(InlineKeyboardButton('Вернуться в меню', callback_data='menu'),
                InlineKeyboardButton('Очистить корзину', callback_data='delete_backet'),
                InlineKeyboardButton('Оплатить', callback_data=' '))
        return markup