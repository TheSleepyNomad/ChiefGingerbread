from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, CallbackQuery
from app.config.config import START_LOGO
from app.database.methods.get import get_all_products, get_count_all_products, get_cart_by_user, get_selected_cart_item
from json import loads as json_loads
from app.database.methods.create import create_order_record
from app.database.methods.delete import delele_user_cart, delete_selected_product_from_cart
from math import ceil

# {\"method\":\"pagination\",\"NumberPage\":\"10\",\"CountPage\":\"10\"}

# btns
# ! delete in future
BTN_NEXT = InlineKeyboardButton('-->', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":\"s\",\"CountPage\":\"s\"}")
BTN_BACK = InlineKeyboardButton('<--', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":\"s\",\"CountPage\":\"s\"}")

# * migrate in config file
BTN_MENU = InlineKeyboardButton('Вернуться в меню', callback_data='menu')
BTN_CURRENT_PAGE = InlineKeyboardButton('ТекСтр/Из', callback_data=' ')

# keyboard
CATALOG_MENU = InlineKeyboardMarkup().add(BTN_BACK, BTN_CURRENT_PAGE, BTN_NEXT).add(BTN_MENU)


async def show_catalog(query: CallbackQuery) -> None:
    await query.bot.answer_callback_query(query.id)
    # get our data
    request = query.data.split('_')

    if request[0] == 'menu':
       await query.bot.delete_message(query.message.chat.id, query.message.message_id)

    elif "pagin" in request[0]:
        # parse our callback from query
        json_string = json_loads(request[0])
        page = int(json_string['PageNum'])
        count = json_string['CountPage']

        # set slicer for List[Products]
        slicer = int(5 * page)
        products = get_all_products()

        # set new markup with products name
        markup = InlineKeyboardMarkup()

        # init our pagination
        for product in products[slicer - 5:slicer]:
                item = json_loads(str(product))
                markup.add(InlineKeyboardButton(item['name'], callback_data="{\"page\":\"card\",\"id\":" + str(item['id']) + ",\"PageNum\":" + str(page + 1)+ ",\"CountPage\":" + str(count)+"}"))
        
        if count == 1 or count == 0:
            markup.add(
                InlineKeyboardButton('<--', callback_data=" "),
                InlineKeyboardButton(f'{page}/1', callback_data=" "),
                InlineKeyboardButton('-->', callback_data=" "),
            )
            await query.bot.send_message(query.from_user.id, text='Мы готовим...', reply_markup=markup)


        elif page == 1:
            markup.add(
                InlineKeyboardButton('<--', callback_data=" "),
                InlineKeyboardButton(f'{page}/{count}', callback_data=" "),
                InlineKeyboardButton('-->', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":" + str(page + 1)+ ",\"CountPage\":" + str(count)+"}"),
            )

        elif page == count:
            markup.add(
                InlineKeyboardButton('<--', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":" + str(page - 1)+ ",\"CountPage\":" + str(count)+"}"),
                InlineKeyboardButton(f'{page}/{count}', callback_data=" "),
                InlineKeyboardButton('-->', callback_data=" "),
            )

        else:
            markup.add(
                InlineKeyboardButton('<--', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":" + str(page - 1)+ ",\"CountPage\":" + str(count)+"}"),
                InlineKeyboardButton(f'{page}/{count}', callback_data=" "),
                InlineKeyboardButton('-->', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":" + str(page + 1)+ ",\"CountPage\":" + str(count)+"}"),
            )

        markup.add(BTN_MENU)
        await query.bot.send_message(query.from_user.id, text='Мы готовим...', reply_markup=markup)

async def back_to_menu(query: CallbackQuery) -> None:
    await query.bot.answer_callback_query(query.id)
    # pass


async def show_product_card(query: CallbackQuery) -> None:
    await query.bot.answer_callback_query(query.id)

    request = query.data.split('_')
    json_string = json_loads(request[0])
    page = int(json_string['PageNum'])
    count = json_string['CountPage']
    product_id = json_string['id']
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Добавить в корзину', callback_data="{\"act\":\"add\",\"userId\":" + str(query.message.from_user.id)+ ",\"prodId\":" + str(product_id)+"}"))\
        .add(InlineKeyboardButton(f'Посмотреть корзину', callback_data=" "))\
        .add(InlineKeyboardButton(f'Назад в каталог', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":" + str(page - 1)+ ",\"CountPage\":" + str(count)+"}"))
    
    await query.bot.send_message(query.from_user.id, text='Шаблон карточки', reply_markup=markup)


async def add_in_order(query: CallbackQuery) -> None:
    request = query.data.split('_')
    json_string = json_loads(request[0])
    user_id = json_string['userId']
    product_id = json_string['prodId']
    create_order_record(product_id=product_id, user_telegram_id=user_id)
    print('check db!')
    await query.bot.answer_callback_query(query.id, text='Товар успешно добавлен', show_alert=True)


async def show_cart(query: CallbackQuery) -> None:
    await query.bot.answer_callback_query(query.id)
    # get our data from button
    request = query.data.split('_')

    if 'pagin' in request[0]:
        # get user cart
        products = get_cart_by_user(query.message.from_user.id)

        json_string = json_loads(request[0])
        page = int(json_string['PageNum'])
        count = json_string['CountPage']

        # set slicer for List[Products]
        slicer = int(5 * page)

        # set new markup with products name
        markup = InlineKeyboardMarkup()

        # init our pagination
        for product in products[slicer - 5:slicer]:
            print(product)
            markup.add(InlineKeyboardButton(f'{product.name} | Кол-во {product.quantity} | Цена {product.price} руб.', callback_data="{\"page\":\"item\",\"id\":" + str(product.id) + ",\"PageNum\":" + str(page + 1)+ ",\"CountPage\":" + str(count)+"}"))
        
        if count == 1 or count == 0:
            markup.add(
                InlineKeyboardButton('<--', callback_data=" "),
                InlineKeyboardButton(f'{page}/1', callback_data=" "),
                InlineKeyboardButton('-->', callback_data=" "),
            )
            await query.bot.send_message(query.from_user.id, text='22227777', reply_markup=markup)

        elif page == 1:
            markup.add(
                InlineKeyboardButton('<--', callback_data=" "),
                InlineKeyboardButton(f'{page}/{count}', callback_data=" "),
                InlineKeyboardButton('-->', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":" + str(page + 1)+ ",\"CountPage\":" + str(count)+"}"),
            )

        elif page == count:
            markup.add(
                InlineKeyboardButton('<--', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":" + str(page - 1)+ ",\"CountPage\":" + str(count)+"}"),
                InlineKeyboardButton(f'{page}/{count}', callback_data=" "),
                InlineKeyboardButton('-->', callback_data=" "),
            )

        else:
            markup.add(
                InlineKeyboardButton('<--', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":" + str(page - 1)+ ",\"CountPage\":" + str(count)+"}"),
                InlineKeyboardButton(f'{page}/{count}', callback_data=" "),
                InlineKeyboardButton('-->', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":" + str(page + 1)+ ",\"CountPage\":" + str(count)+"}"),
            )

        markup.add(BTN_MENU,
                InlineKeyboardButton('Очистить корзину', callback_data='delete_backet'),
                InlineKeyboardButton('Оплатить', callback_data=' '))
        
        await query.bot.send_message(query.from_user.id, text='7777', reply_markup=markup)

async def delete_cart(query: CallbackQuery):
    if delele_user_cart(query.message.from_user.id):
        await query.bot.answer_callback_query(query.id, text='Ваша корзина удалена!', show_alert=True)

        count_products = get_count_all_products()
        count = ceil(count_products / 5)
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton('На сайт', callback_data='web_site'))
        markup.add(InlineKeyboardButton('Процесс готовки', callback_data='description'))
        markup.add(InlineKeyboardButton('Каталог', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":\"1\",\"CountPage\":"+ str(count) +"}"))
        await query.bot.send_message(query.from_user.id, text='7777', reply_markup=markup)

async def show_selected_item(query: CallbackQuery):
    await query.bot.answer_callback_query(query.id)
    request = query.data.split('_')
    json_string = json_loads(request[0])
    selected_item_id = int(json_string['id'])
    page = int(json_string['PageNum'])
    count = json_string['CountPage']
    print(request[0])
    selected_item = get_selected_cart_item(query.message.from_user.id, selected_item_id)
    print(selected_item)
    #* Проработать кнопки
    #* Написать парсе реквеста
    #* Написать функцию уменьшение и удаления
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Убрать из корзины', callback_data="{\"act\":\"reduce\",\"userId\":" + str(query.message.from_user.id)+ ",\"prodId\":" + str(selected_item[0].id) +"}"),
                                        InlineKeyboardButton('Удалить из корзины', callback_data="{\"act\":\"delItm\",\"userId\":" + str(query.message.from_user.id)+ ",\"prodId\":" + str(selected_item[0].id) +"}"),
                                        InlineKeyboardButton('Добавить в корзину', callback_data="{\"act\":\"add\",\"userId\":" + str(query.message.from_user.id)+ ",\"prodId\":" + str(selected_item[0].id) + "}"))\
        .add(InlineKeyboardButton(f'Назад в корзину', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":" + str(page - 1)+ ",\"CountPage\":" + str(count)+"}"))
    await query.bot.send_message(query.from_user.id, text='карточка выбранного из корзины товара', reply_markup=markup)

async def reduce_from_order(query: CallbackQuery):
    await query.bot.answer_callback_query(query.id)
    pass


async def deleted_selected_item_from_order(query: CallbackQuery):
    print('we are here')
    request = query.data.split('_')
    print(request[0])
    pass
    json_string = json_loads(request[0])
    selected_item_id = int(json_string['prodId'])
    if delete_selected_product_from_cart(query.message.from_user.id, selected_item_id):
        await query.bot.answer_callback_query(query.id, text='Товар убран из корзины', show_alert=True)
    await query.bot.answer_callback_query(query.id)
    # after refactoring write markup for showing cart again


def register_callback_query_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(show_catalog, text_contains='catalog')
    dp.register_callback_query_handler(show_product_card, text_contains='card')
    dp.register_callback_query_handler(back_to_menu, text_contains='menu')
    dp.register_callback_query_handler(show_cart, text_contains='cart')
    dp.register_callback_query_handler(delete_cart, text_contains='delete_backet')
    dp.register_callback_query_handler(show_selected_item, text_contains='item')
    dp.register_callback_query_handler(add_in_order, text_contains='add')
    dp.register_callback_query_handler(reduce_from_order, text_contains='reduce')
    dp.register_callback_query_handler(deleted_selected_item_from_order, text_contains='delItm')