from aiogram import types
from loader import dp,bot,ADMIN, HELP_COMMAND, goods, tech_chat
from aiogram.utils.chat_action import ChatActionSender
from connectors.db_funct import create_user,check_cartTable,check_favTable,check_orders
from keyboards.reply.reply_keyboards import get_reply_keyboard
from keyboards.inline.inline_keyboards import category_buttons,three_inline_buttons, favs_buttons
import pandas as pd

# @dp.message_handler(commands=['catalogue'])
# @dp.message_handler(Text(equals='Главное меню'))

#админ функция ответа
async def otvet(msg: types.Message):
    chat_id = str(msg.text).split(' ')[1]
    answer = ''
    answer_raw = str(msg.text).split(' ')[2:]
    photo1 = types.InputMediaPhoto(type='photo', media=types.FSInputFile(r'photos/example1.jpg'), caption='Пример копирования')
    photo2 = types.InputMediaPhoto(type='photo', media=types.FSInputFile(r'photos/example2.jpg'), caption='Пример отправки')
    media=[photo2,photo1]
    await bot.send_media_group(chat_id, media)
    for w in answer_raw:
        answer += w + ' '
    try:
        await bot.send_message(chat_id, f"✉ Новое уведомление!\nОтвет от тех.поддержки:\n\n`{str(answer)}`\n\n📝 Чтобы ответить введите `/допинфо Ваш ответ`",parse_mode='Markdown')
    except:
        await bot.send_message(chat_id, f"✉ Новое уведомление!\nОтвет от тех.поддержки:\n\n`{str(answer)}`\n\n📝 Чтобы ответить введите `/допинфо Ваш ответ`")
    await msg.reply('✅ Ответ отправлен пользователю!')


#клиент функция доп_инфы
async def dop_data(msg: types.Message):
    answer = ''
    answer_raw = str(msg.text).split(' ')[1:]
    for w in answer_raw:
        answer += w + ' '
    try:
        await bot.send_message(tech_chat, f"✉ | Уточнение\nОт: {msg.chat.username}\n\nТекст:\n\n`{str(answer)}`\n\n📝 Чтобы ответить введите `/ответ {msg.chat.id} Ваш ответ`", parse_mode='Markdown')
    except:
        await bot.send_message(tech_chat, f"✉ | Уточнение\nОт: {msg.chat.username}\n\nТекст:\n\n`{str(answer)}`\n\n📝 Чтобы ответить введите `/ответ {msg.chat.id} Ваш ответ`")
    await msg.answer(f"Уточнение отправлено, спасибо!✅")


async def process_main_menu_command(msg):
    if type(msg) == types.CallbackQuery:
        await msg.answer()
        msg=msg.message   
    create_user(msg.from_user.id, msg.from_user.first_name)
    photo = types.FSInputFile('photos/NataliyaPhoto.jpg')
    list_but = goods['Категория'].unique().tolist()[:-2]
    ikb_catalogue = category_buttons(list_but,(2,2,1,1,1,1,1,1,2,1,1,2,1,))
    await bot.send_photo(chat_id= msg.chat.id,
                        photo=photo,
                        caption='Привет! 🙂\nС Вами Наталья и мой новый ассистент - бот 🤖 Market Buyer 👩🏼‍🌾\nТеперь это Ваш личный помощник для заказа свежих и вкусных продуктов 🍒\n\nСмело наполняйте корзину 🧺 и оформляйте заказы себе и близким, ведь доставка свежих и вкусных продуктов доступна по всей Москве и не только ))',
                        reply_markup=ikb_catalogue)
    # await msg.answer('Каталог', reply_markup=ikb_catalogue)
    await msg.delete()

# @dp.message_handler(commands=['help'])
async def process_help_command(msg: types.Message):
    if str(msg.from_user.id) in ADMIN:
        kb_admin = get_reply_keyboard(['Добавить товар', 'Изменить товар', 'Удалить товар'],(2,1))
        await msg.answer('Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре', reply_markup=kb_admin)
    else:
        kb = get_reply_keyboard(['Главное меню',],(1,))
        await msg.answer(HELP_COMMAND, parse_mode='HTML',reply_markup=kb)
        await msg.delete()

# @dp.message_handler(commands=['cart'])
async def check_cart(msg):
    if type(msg) == types.CallbackQuery:
        await msg.answer()
        msg=msg.message        
    photo = "http://allboxes.ru/wp-content/uploads/2015/12/korzina.jpg"
    cart_data = pd.DataFrame(check_cartTable(msg.chat.id), columns=['userid', 'itemid', 'weight','itemsum'])
    if not cart_data.empty:
        df2 = cart_data[['itemid','weight','itemsum']].groupby('itemid').sum().reset_index()
        text_msg='Ваши товары: \n'
        res_sum = 0
        for i in range(len(df2)):
            good = goods.loc[goods['Артикул']==df2['itemid'][i]]
            title = good.reset_index(drop=True)['Наименовние по каталогу'][0]
            volume = good.reset_index(drop=True)['Объем'][0]
            text_msg +='🔹' + title + str('  ⚖️Вес: ') + str(df2['weight'][i]) +' '+str(volume) + str('  🫰Сумма: ') + str(df2['itemsum'][i]) + ';\n'
            res_sum += df2['itemsum'][i]
        text_msg += '____________________________________\n Общая сумма покупок: {}'.format(str(res_sum)+' ₽')
        ikb_cart = three_inline_buttons(['Оформить','К каталогу','Редактировать'],(1,2,))
        await msg.answer_photo(
                            photo=photo,
                            caption=text_msg,
                            reply_markup=ikb_cart)
        # await msg.answer(text=text_msg)
    else:
        ikb_cart = three_inline_buttons(['К каталогу',],(1,))
        await msg.answer_photo(
                            photo=photo,
                            caption='Корзина пуста, скорее к покупкам',
                            reply_markup=ikb_cart)
        await msg.answer(text='Корзина пуста')


# @dp.message_handler(commands=['order'])
async def check_userorder(msg):
    if type(msg) == types.CallbackQuery:
        await msg.answer()
        msg=msg.message        
    data_orders = pd.DataFrame(check_orders(msg.chat.id), columns= ['order_id','user_name', 'user_id', 'listids', 'date', 'adress', 'phone', 'shipment'])
    # print(data_orders)
    if not data_orders.empty:
        df2 = data_orders.sort_values(by='date',ascending=False).reset_index()[:3]
        text_msg='Ваши заказы: \n'
        for i in range(len(df2)):
            df_temp = pd.DataFrame(eval(df2['listids'][i]))
            goodsdf = goods.loc[goods['Артикул'].isin(df_temp['itemid'].tolist())]
            title = goodsdf.reset_index(drop=True)['Наименовние по каталогу'].tolist()
            title_str =''
            for t in title:
                title_str+=str(t)+ str(', ')
            text_msg +='🔹 Заказ: ' + title_str + str('  Дата: ') + str(df2['date'][i]) +'\n'
        ikb_cart = three_inline_buttons(['К каталогу','К корзине'],(1,))
        await msg.answer(text=text_msg, reply_markup=ikb_cart)
    else:
        ikb_cart = three_inline_buttons(['К каталогу','К корзине'],(1,))
        await msg.answer(text='Вы ещё ничего не заказали', reply_markup=ikb_cart)


# @dp.message_handler(commands=['description'])
async def process_descr_command(msg):
    if type(msg) == types.CallbackQuery:
        await msg.answer()
        msg=msg.message
    async with ChatActionSender.upload_video(chat_id=msg.chat.id):
        await msg.answer(text='Отправка видео🎦')
        video = types.FSInputFile(r".\media\IMG_0399.mp4")
        print(video)
        await bot.send_video(caption='Добрый день!\n\nУ нас на канале много новеньких:) Мы очень этому рады и хотим кому-то рассказать, а кому-то напомнить о том, чем занимается Market Buyer и в чем наша особенность💚',
                       chat_id=msg.chat.id, video=video, width=720, height=1280)
        await msg.delete()

async def check_favs(msg):
    if type(msg) == types.CallbackQuery:
        await msg.answer()
        msg=msg.message        
    favs_data = pd.DataFrame(check_favTable(msg.chat.id), columns=['userid', 'itemid'])
    if not favs_data.empty:
        df_goods =goods.loc[goods['Артикул'].isin(favs_data['itemid'].tolist())].reset_index(drop=True)
        ikb_favs = favs_buttons(df_goods,(1,))
        await msg.answer(text='Избранные👇',
                            reply_markup=ikb_favs)
    else:
        ikb_cart = three_inline_buttons(['К каталогу',],(1,))
        await msg.answer(text='В избранном пусто, чтобы добавить товар в избранное, перейдите в карточку товара и нажмите "В избранное"',
                            reply_markup=ikb_cart)



