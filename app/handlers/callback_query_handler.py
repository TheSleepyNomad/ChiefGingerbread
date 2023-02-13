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
from app.markup.markup import create_catalog_markup, create_cart_markup, create_selected_item_markup, create_product_card_markup
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
    await query.bot.send_message(query.from_user.id, text='Шаблон карточки', reply_markup=create_product_card_markup(query))


async def add_in_order(query: CallbackQuery) -> None:
    data = _get_data_from_json(query)

    # if user increases the quantity of products from the cart
    if data.order_id:
        update_order_record(data.order_id, data.user_id, from_cart=True)
        await query.bot.answer_callback_query(query.id, text='Количество товаров увеличено', show_alert=True)

    # if user select product and try add them from catalog
    elif data.product_id:

        # if user already add product before -> update quantity
        if check_order_exist(data.product_id, data.user_id):
            update_order_record(data.product_id, data.user_id)
            await query.bot.answer_callback_query(query.id, text='Количество товаров увеличено', show_alert=True)

        else:
            create_order_record(product_id=data.product_id, user_telegram_id=data.user_id)
            await query.bot.answer_callback_query(query.id, text='Товар успешно добавлен', show_alert=True)



async def show_cart(query: CallbackQuery) -> None:
    await query.bot.answer_callback_query(query.id)
    await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.bot.send_message(query.from_user.id, text='7777', reply_markup=create_cart_markup(query))

async def delete_cart(query: CallbackQuery) -> None:
    if delele_user_cart(query.message.chat.id):
        await query.bot.answer_callback_query(query.id, text='Ваша корзина удалена!', show_alert=True)
        await query.bot.delete_message(query.message.chat.id, query.message.message_id)
        await send_welcome_msg(query.message)
    else:
        await query.bot.answer_callback_query(query.id, text='Произошла ошибка при удалении. Обратитесь к администратору', show_alert=True)


async def show_selected_item(query: CallbackQuery) -> None:
    await query.bot.answer_callback_query(query.id)
    await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.bot.send_message(query.from_user.id, text='карточка выбранного из корзины товара', reply_markup=create_selected_item_markup(query))

async def reduce_from_order(query: CallbackQuery) -> None:
    data = _get_data_from_json(query)
    if reduce_order_record(data.order_id):
        await query.bot.answer_callback_query(query.id, text='Количество товаров уменьшено на 1', show_alert=True)
    else:
        await query.bot.answer_callback_query(query.id, text='Нельзя убавить. Всего 1 штука в корзине', show_alert=True)


async def deleted_selected_item_from_order(query: CallbackQuery) -> None:
    data = _get_data_from_json(query)
    if delete_selected_product_from_cart(query.message.chat.id, data.order_id):
        await query.bot.answer_callback_query(query.id, text='Товар убран из корзины', show_alert=True)
        await query.bot.delete_message(query.message.chat.id, query.message.message_id)
        #! Запрос пустой
        await query.bot.send_message(query.from_user.id, text='7777', reply_markup=create_cart_markup(query))
    else:
        await query.bot.answer_callback_query(query.id, text='Произошла ошибка при удалении. Обратитесь к администратору', show_alert=True)


def register_callback_query_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(show_catalog, text_contains='catalog')
    dp.register_callback_query_handler(show_product_card, text_contains='card')
    dp.register_callback_query_handler(back_to_menu, text_contains='menu')
    dp.register_callback_query_handler(show_cart, text_contains='cart')
    dp.register_callback_query_handler(delete_cart, text_contains='delete_backet')
    dp.register_callback_query_handler(show_selected_item, text_contains='item')
    dp.register_callback_query_handler(add_in_order, text_contains='add')
    dp.register_callback_query_handler(reduce_from_order, text_contains='reduce')
    dp.register_callback_query_handler(deleted_selected_item_from_order, text_contains='delItm')