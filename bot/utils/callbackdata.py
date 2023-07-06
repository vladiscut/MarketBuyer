from aiogram.filters.callback_data import CallbackData

class Category(CallbackData,prefix = 'cat'):
    name: str

class Subcat(CallbackData, prefix = 'subcat'):
    name: str

class Product(CallbackData, prefix = 'product'):
    id: int

class AddProduct(CallbackData, prefix = 'add'):
    id: int
    weight: float
    sumprice: float

class DelProduct(CallbackData, prefix = 'del'):
    id: int
    weight: float
    sumprice: float

class AddCart(CallbackData, prefix = 'cart'):
    id: int
    weight: float
    sumprice: float

class DelCartProduct(CallbackData, prefix = 'delcartproduct'):
    id: int

class AddFav(CallbackData,prefix='addfav'):
    id:int

class DelFavsProduct(CallbackData, prefix = 'delfavsproduct'):
    id: int