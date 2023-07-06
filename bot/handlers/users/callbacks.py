import json
from aiogram.types import CallbackQuery,FSInputFile, ReplyKeyboardRemove, Message
from aiogram import Bot
from keyboards.reply.reply_keyboards import get_reply_keyboard
from states.states import orderStates
from keyboards.reply.reply_keyboards import get_location_keyboard, get_number_keyboard
from loader import bot, goods, tech_chat
from utils.callbackdata import *
from aiogram.fsm.context import FSMContext
from keyboards.inline.inline_keyboards import *
from .message import check_favs
from connectors.db_funct import create_order,del_from_fav,create_user,add_to_cart,check_cartTable, clean_cart_db,clean_cart_product,add_to_fav,check_favTable
import pandas as pd
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")
import datetime
import ast
from pytz import timezone



#ВЫЗОВ ПОДКАТЕГОРИЙ
async def category_call(call: CallbackQuery, bot: Bot,callback_data: Category):
    photo = FSInputFile('photos/NataliyaPhoto.jpg')
    create_user(call.message.chat.id, call.message.chat.first_name)
    df_goods = goods.loc[goods['Категория']==callback_data.name].reset_index(drop=True)
    if (str(goods.loc[goods['Категория']==callback_data.name]['Подкатегория'].unique()[0]))!='nan':
        list_but = goods.loc[goods['Категория']==callback_data.name]['Подкатегория'].unique().tolist()
        ikb_catalogue = subcategory_buttons(list_but,(1,))
    elif (str(goods.loc[goods['Категория']==callback_data.name]['Наименовние по каталогу'].unique()[0]))!='nan':
        ikb_catalogue = product_buttons(df_goods,(1,))
    else:
        await call.answer('Пока нет товаров в данной категории')
        ikb_catalogue = subcategory_buttons(['пусто'],(1,))
        return
    await bot.send_photo(chat_id= call.message.chat.id,
                        photo=photo,
                        caption=callback_data.name,
                        reply_markup=ikb_catalogue)
    text = callback_data.name
    await call.answer(text)

#ВЫЗОВ ТОВАРОВ
async def subcategory_call(call: CallbackQuery, bot: Bot,callback_data: Subcat):
    photo = FSInputFile('photos/NataliyaPhoto.jpg')
    df_goods = goods.loc[goods['Подкатегория']==callback_data.name].reset_index(drop=True)
    ikb_catalogue = product_buttons(df_goods,(1,))
    await bot.send_photo(chat_id= call.message.chat.id,
                        photo=photo,
                        caption=str(call.message.caption) + '\\'+ str(callback_data.name),
                        reply_markup=ikb_catalogue)
    text = callback_data.name
    await call.answer(text)

#ПРОСМОТР ТОВАРА
async def product_call(call: CallbackQuery, bot: Bot,callback_data: Product):
    cat_cap = call.message.caption
    if not cat_cap:
        cat_cap=''
    good = goods.loc[goods['Артикул']==callback_data.id]
    cart_data = pd.DataFrame(check_cartTable(call.message.chat.id), columns=['userid', 'itemid', 'weight','itemsum'])
    if not cart_data.empty:
        cart_exist = True
    else: 
        cart_exist = False
    print(good.reset_index(drop=True)['Артикул'][0])
    photo = good.reset_index(drop=True)['Фото товара'][0]
    price = good.reset_index(drop=True)['Цена за 1 кг.'][0]
    title = good.reset_index(drop=True)['Наименовние по каталогу'][0]
    volume = good.reset_index(drop=True)['Объем'][0]
    weight = float(str(good.reset_index(drop=True)['Заказ от'][0]).replace(',','.'))
    sumprice = float(str(weight).replace(',','.')) * float(price)
    ikb_catalogue = product_detail_buttons(good, weight,sumprice,cart_exist)
    await bot.send_photo(chat_id= call.message.chat.id,
                        photo=photo,
                        caption=cat_cap + '\n\n' +title + ' '+ str(price)+ '₽ за '+str(volume),
                        reply_markup=ikb_catalogue)
    await call.answer(title)

#ДОБАВИТЬ ВЕС\ШТ
async def add_button(call: CallbackQuery, callback_data: AddProduct):
    good = goods.loc[goods['Артикул']==callback_data.id]
    cart_data = pd.DataFrame(check_cartTable(call.message.chat.id), columns=['userid', 'itemid', 'weight','itemsum'])
    if not cart_data.empty:
        cart_exist = True
    else: 
        cart_exist = False
    step = good.reset_index(drop=True)['Шаг заказа'][0]
    price = good.reset_index(drop=True)['Цена за 1 кг.'][0]
    weight = callback_data.weight + float(step)
    sumprice = callback_data.sumprice + (price*step)
    await call.message.edit_reply_markup(reply_markup=product_detail_buttons(good=good, weight=weight, sumprice=sumprice,cart_exist=cart_exist))

#УБАВИТЬ ВЕС\ШТ
async def delete_button(call: CallbackQuery, callback_data: DelProduct):
    good = goods.loc[goods['Артикул']==callback_data.id]
    cart_data = pd.DataFrame(check_cartTable(call.message.chat.id), columns=['userid', 'itemid', 'weight','itemsum'])
    if not cart_data.empty:
        cart_exist = True
    else: 
        cart_exist = False
    step = good.reset_index(drop=True)['Шаг заказа'][0]
    price = good.reset_index(drop=True)['Цена за 1 кг.'][0]
    if callback_data.weight > float(str(good.reset_index(drop=True)['Заказ от'][0]).replace(',','.')):
        weight = callback_data.weight - float(step)
        sumprice = callback_data.sumprice - (price*step)
        await call.message.edit_reply_markup(reply_markup=product_detail_buttons(good=good, weight=weight, sumprice=sumprice, cart_exist=cart_exist))
    else:
        await call.answer('Минимальный заказ от '+ str(good.reset_index(drop=True)['Заказ от'][0])+' ' +good.reset_index(drop=True)['Объем'][0])


###################################
#ДОБАВИТЬ В КОРЗИНУ
async def addcart_button(call: CallbackQuery, callback_data: AddCart):
    create_user(call.message.chat.id, call.message.chat.first_name)
    add_to_cart(call.message.chat.id, callback_data.id, callback_data.weight, callback_data.sumprice)
    cart_exist = True
    good = goods.loc[goods['Артикул']==callback_data.id]
    price = good.reset_index(drop=True)['Цена за 1 кг.'][0]
    weight = float(str(good.reset_index(drop=True)['Заказ от'][0]).replace(',','.'))
    sumprice = float(str(weight).replace(',','.')) * float(price)
    ikb_catalogue = product_detail_buttons(good, weight,sumprice,cart_exist)
    try:
        await call.message.edit_reply_markup(reply_markup=ikb_catalogue)
    except:
        pass
    await call.answer('Товар добавлен в коризну')

#ОЧИСТКА КОРИЗИНЫ
async def clean_cart(call: CallbackQuery):
    cart_data = pd.DataFrame(check_cartTable(call.message.chat.id), columns=['userid', 'itemid', 'weight','itemsum'])
    if not cart_data.empty:
        cart_exist = True
        await bot.send_message(chat_id= call.message.chat.id,
            text='Выберите действие на кнопке ниже👇',
            reply_markup=three_inline_buttons(['Удалить одну позицию','Очистить всё','К корзине'],(1,2,)))
        await call.answer('Очистка корзины')
    else: 
        await call.answer('Корзина пуста')

#ОЧИСТКА КОРИЗИНЫ УДАЛЕНИЕ ОДНОЙ ПОЗИЦИИ №1
async def clean_one(call: CallbackQuery):
    cart_data = pd.DataFrame(check_cartTable(call.message.chat.id), columns=['userid', 'itemid', 'weight','itemsum'])
    if not cart_data.empty:
        df2 = cart_data[['itemid','weight','itemsum']].groupby('itemid').sum().reset_index()
        goods_df = goods.loc[goods['Артикул'].isin(df2['itemid'].tolist())].reset_index(drop=True)
        await bot.send_message(chat_id= call.message.chat.id,
        text='Выберите продукт для удаления на кнопках ниже',
        reply_markup=del_cart_product(goods_df,(1,)))
        await call.answer('Удаление одной позиции')
    else: 
        await call.answer('Корзина пуста')

#ОЧИСТКА КОРИЗИНЫ УДАЛЕНИЕ ОДНОЙ ПОЗИЦИИ №2
async def clean_two(call: CallbackQuery, callback_data: DelCartProduct):
    clean_cart_product(call.message.chat.id, callback_data.id)
    good = goods.loc[goods['Артикул']==callback_data.id]
    title = good.reset_index(drop=True)['Наименовние по каталогу'][0]
    await bot.send_message(chat_id= call.message.chat.id,
            text='Продукт  "'+ str(title) + '"  удален',
            reply_markup=three_inline_buttons(['Удалить одну позицию','Очистить всё','К корзине', 'Оформить'],(1,2,)))
    await call.answer()
    
#ОЧИСТКА КОРИЗИНЫ ПОЛНОЕ УДАЛЕНИЕ
async def clean_cart_full(call: CallbackQuery):
    clean_cart_db(call.message.chat.id)
    await bot.send_message(chat_id= call.message.chat.id,
            text='Корзина полностью очищена',
            reply_markup=three_inline_buttons(['К каталогу','К корзине'],(1,)))
    await call.answer('Корзина очищена')


################################
#ДОБАВИТЬ В ИЗБРАННОЕ
async def addfav_button(call: CallbackQuery, callback_data: AddFav):
    create_user(call.message.chat.id, call.message.chat.first_name)
    fav_data = pd.DataFrame(check_favTable(call.message.chat.id), columns=['userid', 'itemid'])
    if not fav_data.empty:
        favs = fav_data.loc[fav_data['itemid']==callback_data.id]
        if not favs.empty:
            await call.answer('Этот товар уже добавлен в ваши избранные')
        else:
            add_to_fav(call.message.chat.id, callback_data.id) 
            await call.answer('Товар добавлен в избранное')
    else:
        add_to_fav(call.message.chat.id, callback_data.id) 
        await call.answer('Товар добавлен в избранное')

#ОЧИСТКА ИЗБРАННОГО УДАЛЕНИЕ ОДНОЙ ПОЗИЦИИ №1
async def clean_favs(call: CallbackQuery):
    favs_data = pd.DataFrame(check_favTable(call.message.chat.id), columns=['userid', 'itemid'])
    if not favs_data.empty:
        df_goods =goods.loc[goods['Артикул'].isin(favs_data['itemid'].tolist())].reset_index(drop=True)
        ikb_favs = del_favs_product(df_goods,(1,))
        await call.message.answer(text='Выберете продукт для удаления на кнопках ниже👇',
                            reply_markup=ikb_favs)
    else:
        ikb_cart = three_inline_buttons(['К каталогу',],(1,))
        await call.message.answer(text='В избранном пусто, чтобы добавить товар в избранное, перейдите в карточку товара и нажмите "В избранное"',
                            reply_markup=ikb_cart)
        
#ОЧИСТКА ИЗБРАННОГО УДАЛЕНИЕ ОДНОЙ ПОЗИЦИИ №2
async def clean_favs_two(call: CallbackQuery, callback_data: DelFavsProduct):
    del_from_fav(call.message.chat.id, callback_data.id)
    good = goods.loc[goods['Артикул']==callback_data.id]
    title = good.reset_index(drop=True)['Наименовние по каталогу'][0]
    await bot.send_message(chat_id= call.message.chat.id,
            text='Продукт  "'+ str(title) + '" удален',
            reply_markup=three_inline_buttons(['Избранные','К каталогу','Корзина'],(1,2,)))
    await call.answer()

############################
#ОФОРМЛЕНИЕ

async def neworder_canlcel(call, state: FSMContext):
    if type(call) == CallbackQuery:
        await call.answer()
        call=call.message
    await bot.send_message(chat_id= call.chat.id,
            text='Оформление отменено',
            reply_markup=three_inline_buttons(['Избранные','К каталогу','Корзина'],(1,2,)))
    await state.clear()


async def neworder_shipments(call: CallbackQuery , state: FSMContext):
    shipments_list = goods.loc[( goods['Категория']=='Доставка')].reset_index(drop=True)
    text_msg=''
    for i in range(len(shipments_list)):
        title = shipments_list['Наименовние по каталогу'][i]
        price = shipments_list['Цена за 1 кг.'][i]
        text_msg +='🔹' + title + str('  🫰Цена: ') + str(price) + ';\n'
    await bot.send_message(chat_id= call.message.chat.id,
                  text=f'Варианты доставки:\n{text_msg}Выберите тип доставки на кнопках ниже',
                  reply_markup=shipments_buttons(shipments_list))
    await state.set_state(orderStates.shipment)
    await call.answer()

async def neworder_adress(call: CallbackQuery , state: FSMContext):
    # print(call.data)
    await call.answer()
    ship_product = goods.loc[goods['Артикул']==int(call.data)].reset_index(drop=True)[['Наименовние по каталогу', 'Цена за 1 кг.']]
    cart_data = pd.DataFrame(check_cartTable(call.message.chat.id), columns=['userid', 'itemid', 'weight','itemsum'])
    if not cart_data.empty:
        df2 = cart_data[['itemid','weight','itemsum']].groupby('itemid').sum().reset_index()
        await state.update_data(products = str(df2.to_dict(orient='list')))
        await state.update_data(shipment = str(ship_product['Наименовние по каталогу'][0]) + str(' За ') +str(ship_product['Цена за 1 кг.'][0]))
        text_msg='Ваши товары: \n'
        res_sum = float(ship_product['Цена за 1 кг.'][0])
        for i in range(len(df2)):
            good = goods.loc[goods['Артикул']==df2['itemid'][i]]
            title = good.reset_index(drop=True)['Наименовние по каталогу'][0]
            volume = good.reset_index(drop=True)['Объем'][0]
            text_msg +='🔹' + title + str('  ⚖️Вес: ') + str(df2['weight'][i]) +' '+str(volume) + str('  🫰Сумма: ') + str(df2['itemsum'][i]) + ';\n'
            res_sum += df2['itemsum'][i]
        text_msg += '____________________________________\n\n Выбрана доставка {} за {} \n\nСумма с учетом доставки: {}'.format(ship_product['Наименовние по каталогу'][0], ship_product['Цена за 1 кг.'][0], str(res_sum)+' ₽')
        await call.message.answer(text=text_msg)
        if int(call.data) == 520:
            await call.message.answer(text='Супер, наш адрес Такая-то улица дом 4, запиши, чтоб не потерять', reply_markup=get_reply_keyboard(['Записал!']))
            await state.set_state(orderStates.number)
        else:
            kb = get_location_keyboard()
            await bot.send_message(chat_id= call.message.chat.id,
                        text='Отлично!⭐️\nКуда доставим?📍\nМожешь нажать на кнопку "Геолокация" чтобы поделиться своим местоположением или просто отправь свой адрес в сообщении🙃\nСкопировать пример: `г. Москва, ул. Чистопрудный бульвар, дом 6, квартира 20`',
                        reply_markup=kb, parse_mode='Markdown')
            await state.set_state(orderStates.number)
    else:
        ikb_cart = three_inline_buttons(['К каталогу',],(1,))
        await call.message.answer(text='Корзина пуста', reply_markup=ikb_cart)


async def neworder_number(msg: Message, state: FSMContext):
    if msg.location:
        location = geolocator.reverse(str(msg.location.latitude)+","+str(msg.location.longitude))
    else:
        location = msg.text
    await state.update_data(adress = location)
    kb = get_number_keyboard()
    await bot.send_message(chat_id= msg.chat.id,
                text='Почти всё!😇\nОсталось указать номер телефона📱\nМожешь нажать на кнопку "Контакт" чтобы поделиться текущим номером, если хочешь указать другой номер для связи просто отправь его в сообщении',
                reply_markup=kb)
      
    await state.set_state(orderStates.send_order)

async def neworder_send(msg: Message, state: FSMContext):
    if msg.contact:
        phone = msg.contact.phone_number
    else:
        phone = msg.text
    await state.update_data(phone = phone)
    data = await state.get_data()
    today = datetime.datetime.now(timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')
    df_ord_goods = pd.DataFrame(eval(data['products']))
    create_order(msg.chat.username, msg.chat.id, str(data['products']), str(today), str(data['adress']), str(data['phone']), str(data['shipment']))
    order_goods = goods.loc[goods['Артикул'].isin(df_ord_goods['itemid'].tolist())].reset_index(drop=True)[['Наименовние по каталогу', 'Цена за 1 кг.']]
    text_goods = ''
    res_sum=float(data['shipment'].split(' За ')[1])
    for i in range(len(order_goods)):
        text_goods+=str('--') + order_goods['Наименовние по каталогу'][i] + str(' Количество: ')+ str(df_ord_goods['weight'][i]) + str(' Сумма: ') + str(df_ord_goods['itemsum'][i]) + str('\n')
        res_sum+=float(df_ord_goods['itemsum'][i])
    try:
        await bot.send_message(tech_chat, f"✉ | Новый заказ\nОт: {msg.chat.username}\nТовары:\n`{text_goods}`\nДоставка: `{data['shipment']}`\nАдрес: `{data['adress']}`\nТелефон: `{data['phone']}`\nОбщая сумма заказа: `{res_sum}`\n\n📝 Чтобы ответить на вопрос введите `/ответ {msg.chat.id} Ваш ответ`", parse_mode='Markdown')
    except:
        await bot.send_message(tech_chat, f"✉ | Новый заказ\nОт: {msg.chat.username}\nТовары:\n`{text_goods}`\nДоставка: `{data['shipment']}`\nАдрес: `{data['adress']}`\nТелефон: `{data['phone']}`\nОбщая сумма заказа: `{res_sum}`\n\n📝 Чтобы ответить на вопрос введите `/ответ {msg.chat.id} Ваш ответ`")
    await msg.answer(f"Ваш заказ создан и ожидает оплаты\nПеревод по номеру 89991112233 Сбербанк Проверкин П.А, сумма {res_sum}\nМодератор проверит его и свяжется с вами✅", reply_markup=ReplyKeyboardRemove())
    await state.clear()
### КОНЕЦ ФУНКЦИЙ ЗАКАЗА ###
    





#ОБРАТНО
async def back(call: CallbackQuery, bot: Bot):
    photo = FSInputFile('photos/NataliyaPhoto.jpg')
    if str(call.message.reply_markup.inline_keyboard[0][0]).startswith("text='-'"):
        g_cat = (call.message.caption).split('\n\n')[0].split('\\')
        if len(g_cat)>1:
            df_goods = goods.loc[goods['Подкатегория']==g_cat[1]].reset_index(drop=True)
            ikb_catalogue = product_buttons(df_goods,(1,))
            cap = str(call.message.caption).split('\n\n')[0]
        elif '\n' not in str(call.message.caption):
            await check_favs(call)
            await call.answer('Избранные')
            return
        else:
            df_goods = goods.loc[goods['Категория']==g_cat[0]].reset_index(drop=True)
            ikb_catalogue = product_buttons(df_goods,(1,))
            cap = str(call.message.caption).split('\n\n')[0].split('\\')[0]
    elif len((call.message.caption).split('\\'))>1:
        g = goods.loc[goods['Категория']==str(call.message.caption).split('\\')[0]]['Подкатегория'].unique()
        list_but =g.tolist()
        ikb_catalogue = subcategory_buttons(list_but,(1,))
        cap = str(call.message.caption).split('\\')[0]
    else:
        list_but = goods['Категория'].unique().tolist()[:-2]
        ikb_catalogue = category_buttons(list_but,(2,1,1,1,1,1,1,2,1,1,2,1,))
        cap='Привет! 🙂\nС Вами Наталья и мой новый ассистент - бот 🤖 Market Buyer 👩🏼‍🌾\nТеперь это Ваш личный помощник для заказа свежих и вкусных продуктов 🍒\n\nСмело наполняйте корзину 🧺 и оформляйте заказы себе и близким, ведь доставка свежих и вкусных продуктов доступна по всей Москве и не только ))'
    await bot.send_photo(chat_id= call.message.chat.id,
                    photo=photo,
                    caption=cap,
                    reply_markup=ikb_catalogue)
    await call.answer(call.message.text)