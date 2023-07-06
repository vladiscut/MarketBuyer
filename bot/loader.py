from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage


import pandas as pd

token = '6294662417:AAGod-P17bTNJya4UuOAqOag2VyHAs4Fh54'

ADMIN = ['344150886',]
tech_chat = '-961118755'


HELP_COMMAND = """
<b>/help</b> - <em>список комманд</em>
<b>/start</b> - <em>запуск</em>
<b>/description</b> - <em>описание</em>
"""

goods = pd.read_excel(r'Каталог Сайт.xlsx')
goods = goods.loc[goods['ДОСТУПНОСТЬ (Y/N)']=='Y'].reset_index(drop=True)

bot = Bot(token=token, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher()
