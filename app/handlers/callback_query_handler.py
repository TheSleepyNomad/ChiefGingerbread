from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, CallbackQuery
from app.config.config import START_LOGO
from app.database.methods.get import get_all_products, get_count_all_products
from json import loads as json_loads


# {\"method\":\"pagination\",\"NumberPage\":\"10\",\"CountPage\":\"10\"}

# btns
BTN_NEXT = InlineKeyboardButton('-->', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":\"s\",\"CountPage\":\"s\"}")
BTN_BACK = InlineKeyboardButton('<--', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":\"s\",\"CountPage\":\"s\"}")
BTN_MENU = InlineKeyboardButton('Вернуться в меню', callback_data='menu')
BTN_CURRENT_PAGE = InlineKeyboardButton('ТекСтр/Из', callback_data=' ')

# keyboard
CATALOG_MENU = InlineKeyboardMarkup().add(BTN_BACK, BTN_CURRENT_PAGE, BTN_NEXT).add(BTN_MENU)


async def show_catalog(query: CallbackQuery):
    await query.bot.answer_callback_query(query.id)
    request = query.data.split('_')
    print(request)
    if request[0] == 'menu':
       await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    elif "pagin" in request[0]:
        json_string = json_loads(request[0])
        page = int(json_string['PageNum'])
        count = json_string['CountPage']
        slicer = int(5 * page)
        print('строка json')
        print(json_string)



        
        products = get_all_products()

        markup = InlineKeyboardMarkup()
        for product in products[slicer - 5:slicer]:
                markup.add(InlineKeyboardButton(str(product), callback_data=' '))
        if page == 1:
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

    

def register_callback_query_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(show_catalog, text_contains='catalog')