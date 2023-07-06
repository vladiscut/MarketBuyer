from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage


import pandas as pd

token = 'your_token'

ADMIN = ['admin_id',]
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
