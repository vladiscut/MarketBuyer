from aiogram import types

async def set_default_commands(bot):
    commands=[
            types.BotCommand(command = "catalogue", description= "📖 Каталог"),
            types.BotCommand(command = "cart", description= "🛒 Корзина"),
            types.BotCommand(command = "favs", description= "❤️ Избранное"),
            types.BotCommand(command = "orders", description= "📦 Заказы"),
            types.BotCommand(command = "description", description= "⭐️ Немного о нас"),

        ]
    await bot.set_my_commands(commands)
