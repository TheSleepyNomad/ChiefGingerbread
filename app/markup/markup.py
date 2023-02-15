from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from app.database.methods.get import get_count_all_products, get_cart_by_user, get_all_products, get_selected_cart_item
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
    markup = InlineKeyboardMarkup()

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
    markup = InlineKeyboardMarkup()

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
        # init our pagination
        for product in products[slicer - 5:slicer]:
            print(product)
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
                InlineKeyboardButton('Оплатить', callback_data='payment'))
        
    return markup
    

def create_selected_item_markup(query: CallbackQuery) -> InlineKeyboardMarkup:
    print(query.data)
    data = _get_data_from_json(query)
    selected_item = get_selected_cart_item(query.message.chat.id, data.order_id)
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Убрать из корзины', callback_data="{\"act\":\"reduce\",\"userId\":" + str(query.message.chat.id)+ ",\"orderId\":" + str(selected_item[0].id) +"}"),
                                        InlineKeyboardButton('Удалить из корзины', callback_data="{\"act\":\"delItm\",\"userId\":" + str(query.message.chat.id)+ ",\"orderId\":" + str(selected_item[0].id) +"}"),
                                        InlineKeyboardButton('Добавить в корзину', callback_data="{\"act\":\"add\",\"userId\":" + str(query.message.chat.id)+ ",\"orderId\":" + str(selected_item[0].id) + "}"))\
        .add(InlineKeyboardButton(f'Назад в корзину', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":" + str(data.page - 1)+ ",\"CountPage\":" + str(data.count_page)+"}"))
    return markup

def create_product_card_markup(query: CallbackQuery) -> InlineKeyboardMarkup:
    data = _get_data_from_json(query)
    user_products_count = ceil(len(get_cart_by_user(query.message.chat.id)) / 5)
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Добавить в корзину', callback_data="{\"act\":\"add\",\"userId\":" + str(query.message.chat.id)+ ",\"prodId\":" + str(data.product_id)+"}"))
    if user_products_count:
        markup.add(InlineKeyboardButton('Посмотреть корзину', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":\"1\",\"CountPage\":" + str(user_products_count) + "}"))
    markup.add(InlineKeyboardButton(f'Назад в каталог', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":" + str(data.page - 1)+ ",\"CountPage\":" + str(data.count_page)+"}"))
    return markup