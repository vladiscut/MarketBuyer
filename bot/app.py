import asyncio
from aiogram.filters import Command
from loader import dp, bot
from utils.set_bot_commands import set_default_commands
from states.states import orderStates
from connectors.db_funct import create_table_user, create_table_cart, create_table_favorite, create_table_orders
from handlers.users.message import *
from handlers.users.callbacks import *
from aiogram import F
from utils.callbackdata import Category
import logging

logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(bot)
    print('Bot Started!')

async def start():
    create_table_user()
    create_table_cart()
    create_table_favorite()
    create_table_orders()

    dp.startup.register(on_startup)
    dp.message.register(otvet,Command(commands=['ответ']))
    dp.message.register(dop_data,Command(commands=['допинфо']))

    #ЗАКАЗЫ
    dp.message.register(check_userorder,Command(commands=['orders']))
    dp.callback_query.register(check_userorder, F.data.startswith('checkuserorder'))
  

    #КАТАЛОГ
    dp.message.register(process_main_menu_command,Command(commands=['catalogue', 'start']))
    dp.message.register(process_main_menu_command,F.text=='Главное меню')
    dp.callback_query.register(process_main_menu_command, F.data.startswith('К каталогу'))

    #КОРЗИНА    
    dp.message.register(check_cart,Command(commands=['cart']))
    dp.callback_query.register(check_cart, F.data.startswith('gocart'))
    dp.callback_query.register(check_cart, F.data.startswith('К корзине'))
    dp.callback_query.register(check_cart, F.data.startswith('Корзина'))

    #ИЗБРАННОЕ
    dp.message.register(check_favs,Command(commands=['favs']))
    dp.callback_query.register(check_favs, F.data.startswith('Избранные'))
    dp.callback_query.register(clean_favs, F.data.startswith('Изменить'))
    dp.callback_query.register(clean_favs_two, DelFavsProduct.filter())

    #ОПИСАНИЕ
    dp.message.register(process_descr_command,Command(commands=['description']))
    dp.callback_query.register(process_descr_command,F.data.startswith('О нас'))

    #ОФОРМЛЕНИЕ
    dp.callback_query.register(neworder_shipments,F.data.startswith('Оформить'))
    dp.callback_query.register(neworder_canlcel,F.data.startswith('Отмена оформления'))
    dp.message.register(neworder_canlcel,F.text=='Отмена оформления')
    dp.callback_query.register(neworder_adress,orderStates.shipment)
    dp.message.register(neworder_number,orderStates.number)
    dp.message.register(neworder_send,orderStates.send_order)

    dp.callback_query.register(clean_cart, F.data.startswith('Редактировать'))
    dp.callback_query.register(clean_one, F.data.startswith('Удалить одну позицию'))
    dp.callback_query.register(back, F.data.startswith('Обратно'))
    dp.callback_query.register(clean_cart_full, F.data.startswith('Очистить всё'))
    dp.callback_query.register(category_call, Category.filter())
    dp.callback_query.register(clean_two, DelCartProduct.filter())
    dp.callback_query.register(subcategory_call, Subcat.filter())
    dp.callback_query.register(product_call, Product.filter())
    dp.callback_query.register(add_button, AddProduct.filter())
    dp.callback_query.register(delete_button, DelProduct.filter())
    dp.callback_query.register(addcart_button, AddCart.filter())
    dp.callback_query.register(addfav_button, AddFav.filter())
    # try:
    await dp.start_polling(bot, skip_updates=True)
    # finally:
    #     await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())

