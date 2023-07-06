from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_location_keyboard():
    rp_keyboard_builder = ReplyKeyboardBuilder()
    # for but in list_but:
    rp_keyboard_builder.button(text='Геолокация',request_location=True)
    rp_keyboard_builder.button(text='Отмена оформления')
    # print(*row)
    return rp_keyboard_builder.as_markup(resize_keyboard=True,selective =True,one_time_keyboard=True)

def get_number_keyboard():
    rp_keyboard_builder = ReplyKeyboardBuilder()
    # for but in list_but:
    rp_keyboard_builder.button(text='Контакт',request_contact=True)
    rp_keyboard_builder.button(text='Отмена оформления')
    # print(*row)
    return rp_keyboard_builder.as_markup(resize_keyboard=True,selective =True,one_time_keyboard=True)

def get_reply_keyboard(list_but:list):
    rp_keyboard_builder = ReplyKeyboardBuilder()
    for but in list_but:
        rp_keyboard_builder.button(text=(but))
    # print(*row)
    return rp_keyboard_builder.as_markup(resize_keyboard=True,selective =True,one_time_keyboard=True)
    

def one_button(but):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton(text=but)
    kb.add(b1)
    return kb

def three_buttons(list_but):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    b1= KeyboardButton(list_but[0])
    b2 = KeyboardButton(list_but[1])
    b3 = KeyboardButton(list_but[2])

    kb.add(b1,b2).add(b3)


def towers(list_but):
    keyboard_inline_buttons = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for b in list_but:
        keyboard_inline_buttons.insert(b)
    return keyboard_inline_buttons
