from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  # , ReplyKeyboardRemove


kb = ReplyKeyboardMarkup(resize_keyboard=True)
# kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) # на 1 раз
kbs = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('/Меню')
b2 = KeyboardButton('/Конфеты')


# kb_client.add(b1).add(b2).add(b3)     # На отдельных строках
# kb_client.add(b1, b2).insert(b3)        # В одну строку
# kb_client.row(b4, b5)                   # В одну строку
kb.add(b1, b2)
kbs.add(KeyboardButton('/Выйти'))