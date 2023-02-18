from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, CallbackQuery, LabeledPrice
from app.config.config import START_LOGO
from app.database.methods.get import get_all_products, get_count_all_products, get_cart_by_user, get_selected_cart_item, get_product_by_id, get_product_quantity_from_cart
from json import loads as json_loads
from app.database.methods.create import create_order_record, check_order_exist, update_order_record
from app.database.methods.delete import delele_user_cart, delete_selected_product_from_cart
from math import ceil
from app.database.methods.update import reduce_order_record
from app.database.methods.other import check_user_baket_exist
from app.handlers.command_handler import send_welcome_msg
from app.markup.markup import create_catalog_markup, create_cart_markup, create_selected_item_markup, create_product_card_markup, create_start_markup, create_invoice_markup
from app.utils.utils import _get_data_from_json
from app.misc.data import MsgTemplate


async def show_catalog(query: CallbackQuery) -> None:
    await query.bot.answer_callback_query(query.id)
    await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.bot.send_message(query.from_user.id, text='Мы готовим...', reply_markup=create_catalog_markup(query))

async def back_to_menu(query: CallbackQuery) -> None:
    await query.bot.answer_callback_query(query.id)
    await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    await send_welcome_msg(query.message)


async def show_product_card(query: CallbackQuery) -> None:
    """
    This function is responsible for showing product card
    """
    # collecting data from database and query
    data = _get_data_from_json(query)
    product = get_product_by_id(data.product_id)
    # send answer and delete last msg
    await query.bot.answer_callback_query(query.id)
    await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    # send product card with img
    with open(product.img_path, 'rb') as img:
        await query.bot.send_photo(query.from_user.id, photo=InputFile(img), caption=MsgTemplate.product_card_msg.format(name=product.name,title=product.title,price=product.price), reply_markup=create_product_card_markup(query), parse_mode='HTML')


async def add_in_order(query: CallbackQuery) -> None:
    """
    This function is responsible for adding a product and updating its quantity in the cart
    """
    data = _get_data_from_json(query)
    old_caption = query.message.caption
    # if user increases the quantity of products from the cart
    if data.order_id:
        update_order_record(data.order_id, data.user_id, from_cart=True)
        await query.bot.answer_callback_query(query.id, text='Количество товаров увеличено', show_alert=True)

    # if user select product and try add them from catalog
    elif data.product_id:
        user_products_count = ceil(len(get_cart_by_user(query.message.chat.id)) / 5)
        # if dont have products in cart yet, but wanna add
        # save markup and insert new button after first button
        if len(query.message.reply_markup.inline_keyboard) < 3:
            query.message.reply_markup.inline_keyboard.insert(1, [InlineKeyboardButton('Посмотреть корзину', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":\"1\",\"CountPage\":" + str(user_products_count) + "}")])
        # if user already add product before -> update quantity
        if check_order_exist(data.product_id, data.user_id):
            # update quantity in order
            update_order_record(data.product_id, data.user_id)
            # collect current product quantity
            quantity = get_product_quantity_from_cart(data.user_id, data.product_id)
            # delete last string in caption. 
            # find penult string and replace all after her
            caption = old_caption.replace(old_caption[(old_caption.find('руб.') + 4):], '\nСейчас в корзине: {} шт.'.format(quantity))
            # send answer and new caption
            await query.bot.answer_callback_query(query.id, text='Количество товаров увеличено', show_alert=True)
            await query.bot.edit_message_caption(chat_id=query.message.chat.id, message_id=query.message.message_id, caption=caption, reply_markup=query.message.reply_markup)

        # if user add product in cart first time
        else:
            create_order_record(product_id=data.product_id, user_telegram_id=data.user_id)
            quantity = get_product_quantity_from_cart(data.user_id, data.product_id)
            # send answer and new caption
            await query.bot.answer_callback_query(query.id, text='Товар успешно добавлен', show_alert=True)
            await query.bot.edit_message_caption(chat_id=query.message.chat.id, 
                                                 message_id=query.message.message_id, 
                                                 caption=query.message.caption + '\nСейчас в корзине: {} шт.'.format(quantity), 
                                                 reply_markup=query.message.reply_markup)



async def show_cart(query: CallbackQuery) -> None:
    print(query.data)
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
    data = _get_data_from_json(query)
    selected_item = get_selected_cart_item(query.message.chat.id, data.order_id)
    await query.bot.answer_callback_query(query.id)
    await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    with open(selected_item[0].img, 'rb') as img:
        await query.bot.send_photo(query.from_user.id, 
                                   photo=InputFile(img), 
                                   caption=MsgTemplate.product_card_msg.format(name=selected_item[0].name,
                                                                               title=selected_item[0].name,
                                                                               price=selected_item[0].price), 
                                                                               reply_markup=create_selected_item_markup(query), 
                                                                               parse_mode='HTML')

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
        await query.bot.send_message(query.from_user.id, text='7777', reply_markup=create_start_markup(query.message.chat.id))
    else:
        await query.bot.answer_callback_query(query.id, text='Произошла ошибка при удалении. Обратитесь к администратору', show_alert=True)


async def payment_process_query(query: CallbackQuery) -> None:
    # get user cart and products
    products = get_cart_by_user(query.message.chat.id)
    prices = []
    # fill prices list
    for product in products:
        prices.append(LabeledPrice(label=product.name, amount=int(product.price)*100))

    await query.bot.answer_callback_query(query.id)
    await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.bot.send_invoice(chat_id=query.message.chat.id,
                                 title='Оплата покупки',
                                 description='Описание',
                                 provider_token='1744374395:TEST:5b88879c3684482b9133',
                                 currency='RUB',
                                 prices=prices,
                                 start_parameter='time-machine-example',
                                 payload='test',
                                 reply_markup=create_invoice_markup())


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
    dp.register_callback_query_handler(payment_process_query, text_contains='payment')