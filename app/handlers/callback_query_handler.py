from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, CallbackQuery
from app.config.config import START_LOGO
from app.database.methods.get import get_all_products, get_count_all_products, get_cart_by_user, get_selected_cart_item
from json import loads as json_loads
from app.database.methods.create import create_order_record, check_order_exist, update_order_record
from app.database.methods.delete import delele_user_cart, delete_selected_product_from_cart
from math import ceil
from app.database.methods.update import reduce_order_record
from app.database.methods.other import check_user_baket_exist
from app.handlers.command_handler import send_welcome_msg
from app.markup.markup import create_catalog_markup, create_cart_markup
from app.utils.utils import _get_data_from_json


async def show_catalog(query: CallbackQuery) -> None:
    await query.bot.answer_callback_query(query.id)
    await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.bot.send_message(query.from_user.id, text='Мы готовим...', reply_markup=create_catalog_markup(query))

async def back_to_menu(query: CallbackQuery) -> None:
    await query.bot.answer_callback_query(query.id)
    await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    await send_welcome_msg(query.message)


async def show_product_card(query: CallbackQuery) -> None:
    await query.bot.answer_callback_query(query.id)
    await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    request = query.data.split('_')
    json_string = json_loads(request[0])
    page = int(json_string['PageNum'])
    count = json_string['CountPage']
    product_id = json_string['prodId']
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Добавить в корзину', callback_data="{\"act\":\"add\",\"userId\":" + str(query.message.chat.id)+ ",\"prodId\":" + str(product_id)+"}"))\
        .add(InlineKeyboardButton(f'Посмотреть корзину', callback_data=" "))\
        .add(InlineKeyboardButton(f'Назад в каталог', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":" + str(page - 1)+ ",\"CountPage\":" + str(count)+"}"))
    
    await query.bot.send_message(query.from_user.id, text='Шаблон карточки', reply_markup=markup)


async def add_in_order(query: CallbackQuery) -> None:
    request = query.data.split('_')
    json_string = json_loads(request[0])
    user_id = json_string['userId']
    product_id = json_string['orderdId']
    if check_order_exist(product_id, user_id):
        update_order_record(product_id, user_id)
        await query.bot.answer_callback_query(query.id, text='Количество товаров увеличено', show_alert=True)
    else:
        create_order_record(product_id=product_id, user_telegram_id=user_id)
        await query.bot.answer_callback_query(query.id, text='Товар успешно добавлен', show_alert=True)


async def show_cart(query: CallbackQuery) -> None:
    await query.bot.answer_callback_query(query.id)
    await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.bot.send_message(query.from_user.id, text='7777', reply_markup=create_cart_markup(query))

async def delete_cart(query: CallbackQuery):
    if delele_user_cart(query.message.chat.id):
        await query.bot.answer_callback_query(query.id, text='Ваша корзина удалена!', show_alert=True)
        await query.bot.delete_message(query.message.chat.id, query.message.message_id)
        await send_welcome_msg(query.message)
    else:
        await query.bot.answer_callback_query(query.id, text='Произошла ошибка при удалении. Обратитесь к администратору', show_alert=True)


async def show_selected_item(query: CallbackQuery):
    await query.bot.answer_callback_query(query.id)
    await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    request = query.data.split('_')
    print(request)
    json_string = json_loads(request[0])
    selected_item_id = int(json_string['orderId'])
    page = int(json_string['PageNum'])
    count = json_string['CountPage']
    data = _get_data_from_json(query)
    selected_item = get_selected_cart_item(query.message.chat.id, data.order_id)
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Убрать из корзины', callback_data="{\"act\":\"reduce\",\"userId\":" + str(query.message.chat.id)+ ",\"orderdId\":" + str(selected_item[0].id) +"}"),
                                        InlineKeyboardButton('Удалить из корзины', callback_data="{\"act\":\"delItm\",\"userId\":" + str(query.message.chat.id)+ ",\"orderdId\":" + str(selected_item[0].id) +"}"),
                                        InlineKeyboardButton('Добавить в корзину', callback_data="{\"act\":\"add\",\"userId\":" + str(query.message.chat.id)+ ",\"orderdId\":" + str(selected_item[0].id) + "}"))\
        .add(InlineKeyboardButton(f'Назад в корзину', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":" + str(page - 1)+ ",\"CountPage\":" + str(count)+"}"))
    await query.bot.send_message(query.from_user.id, text='карточка выбранного из корзины товара', reply_markup=markup)

async def reduce_from_order(query: CallbackQuery):
    request = query.data.split('_')
    json_string = json_loads(request[0])
    selected_item_id = int(json_string['orderdId'])
    reduce_order_record(selected_item_id)
    await query.bot.answer_callback_query(query.id, text='Количество товаров уменьшено на 1', show_alert=True)


async def deleted_selected_item_from_order(query: CallbackQuery):
    request = query.data.split('_')
    json_string = json_loads(request[0])
    selected_item_id = int(json_string['prodId'])
    if delete_selected_product_from_cart(query.message.chat.id, selected_item_id):
        await query.bot.answer_callback_query(query.id, text='Товар убран из корзины', show_alert=True)
        await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    else:
        await query.bot.answer_callback_query(query.id, text='Произошла ошибка при удалении. Обратитесь к администратору', show_alert=True)


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