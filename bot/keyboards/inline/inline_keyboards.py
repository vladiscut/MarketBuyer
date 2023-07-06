from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbackdata import *
import pandas as pd

def del_cart_product(goods, row_width:tuple):
    ikb = InlineKeyboardBuilder()
    for i in range(len(goods)):
        ikb.button(text = str(goods['Наименовние по каталогу'][i]),
                   callback_data=DelCartProduct(id=str(goods['Артикул'][i])))
    ikb.button(text = "К корзине",callback_data='К корзине')
    ikb.adjust(*row_width)
    return ikb.as_markup()

def shipments_buttons(goods):
    ikb = InlineKeyboardBuilder()
    for i in range(len(goods)):
        ikb.button(text = str(goods['Наименовние по каталогу'][i]),
                   callback_data=str(goods['Артикул'][i]))
    ikb.button(text = "Отменить оформление",callback_data='Отмена оформления')
    ikb.adjust(1)
    return ikb.as_markup()

def three_inline_buttons(list_but:list, row_width:tuple):
    ikb = InlineKeyboardBuilder()
    for b in list_but:
        ikb.button(text = str(b),callback_data=str(b))
    ikb.adjust(*row_width)
    return ikb.as_markup()

def category_buttons(list_but:list, row_width:tuple):
    ikb = InlineKeyboardBuilder()
    ikb.button(text = '🛒 Корзина', callback_data='Корзина')
    ikb.button(text = '⭐️ О нас', callback_data='О нас')
    ikb.button(text = '❤️ Избранное', callback_data='Избранные')
    ikb.button(text = '📦 Заказы', callback_data='checkuserorder')
    for b in list_but:
        ikb.button(text = str(b),callback_data=Category(name=str(b)[:28]))
    ikb.button(text = '🙎‍♀️ Поддержка', url='https://t.me/ManagerMarketBuyer_bot')    
    ikb.adjust(*row_width)
    return ikb.as_markup()

def subcategory_buttons(list_but:list, row_width:tuple):
    ikb = InlineKeyboardBuilder()
    for b in list_but:
        ikb.button(text = str(b),callback_data=Subcat(name=str(b)[:28]))
    ikb.button(text = "Обратно 🔙",callback_data='Обратно')
    ikb.adjust(*row_width)
    return ikb.as_markup()

def product_buttons(goods:pd.DataFrame, row_width:tuple):
    ikb = InlineKeyboardBuilder()
    for i in range(len(goods)):
        ikb.button(text = str(goods['Наименовние по каталогу'][i]),
                   callback_data=Product(id=str(goods['Артикул'][i])))
    ikb.button(text = "Обратно 🔙",callback_data='Обратно')
    ikb.adjust(*row_width)
    return ikb.as_markup()

def favs_buttons(goods:pd.DataFrame, row_width:tuple):
    ikb = InlineKeyboardBuilder()
    for i in range(len(goods)):
        ikb.button(text = str(goods['Наименовние по каталогу'][i]),
                   callback_data=Product(id=str(goods['Артикул'][i])))
    ikb.button(text = "Изменить 🔧",callback_data='Изменить')
    ikb.button(text = "К каталогу 📖",callback_data='К каталогу')
    ikb.adjust(*row_width)
    return ikb.as_markup()

def del_favs_product(goods, row_width:tuple):
    ikb = InlineKeyboardBuilder()
    for i in range(len(goods)):
        ikb.button(text = str(goods['Наименовние по каталогу'][i]),
                   callback_data=DelFavsProduct(id=str(goods['Артикул'][i])))
    ikb.button(text = "К избранному",callback_data='Избранные')
    ikb.adjust(*row_width)
    return ikb.as_markup()

def product_detail_buttons(good:pd.DataFrame, weight:float, sumprice:float, cart_exist:bool):
    ikb = InlineKeyboardBuilder()
    volume = good.reset_index(drop=True)['Объем'][0]
    itemid = good.reset_index(drop=True)['Артикул'][0]
    ikb.button(text = '-',callback_data=DelProduct(id=itemid, weight=weight,sumprice=sumprice))
    ikb.button(text = str(round(weight,2))+' '+str(volume) ,callback_data='weight')
    ikb.button(text = '+',callback_data=AddProduct(id=itemid, weight=weight,sumprice=sumprice))
    ikb.button(text = 'Добавить в корзину за {}₽'.format(sumprice),callback_data=AddCart(id=itemid, weight=weight,sumprice=sumprice))
    ikb.button(text = 'В избранное',callback_data=AddFav(id=itemid))
    ikb.button(text = "Обратно 🔙",callback_data='Обратно')
    if cart_exist:
        ikb.button(text = "Перейти в корзину",callback_data='gocart')
    ikb.adjust(3,1,1,2)
    return ikb.as_markup()

    # if cart_exist:
    #     ib6_azer = InlineKeyboardButton (text = 'Перейти в корзину'.format(weight, price),callback_data='cart')
    #     ikb_azer.add(ib1_azer,ib2_azer,ib3_azer).add(ib6_azer,ib4_azer).add(ib5_azer)
    # else:
    ikb_azer.add(ib1_azer,ib2_azer,ib3_azer).add(ib4_azer).add(ib5_azer)

    return ikb_azer