import random


from aiogram import types, Dispatcher



import bot_data
import candies
from logger import log
from user import users, check_user
from user_kb import kb


# #
# Сделать потом нормальное меню, вместо текущей версии
# #


# /start и некоторые другие
async def command_start( message: types.Message ):
    user_id = message.from_user.id
    await log( "handlers", "command_start", f"{ user_id }: { message.text }" )

    user_name = message.from_user.full_name
    if await check_user( user_id, "game_mode" ) == True:
        await message.answer( f"{ user_name }, сначала выйдите из игры > /stop" )
    await message.answer( f"{ user_name }{ bot_data.main_menu }", reply_markup=kb )


# async def candies( message: types.Message ):  # /candies game
#   if len( message.text.split() ) == 1 or message.text.split()[1] == game:
#
#   if message.text.split()[1] == rules:
#       await message.answer( f"{ bot_data.rules }" )


# Обработчик /candies_game # Переделать на /candies game - вызов с параметром
async def candies_game( message: types.Message ):  # /candies game
    user_id = message.from_user.id
    await log( __name__, "candies_game", f"{ user_id }: { message.text }" )

    if await check_user( user_id, "game_mode" ) == False:
        users[ user_id ][ "game_mode" ] = True  # candies_mode = True
        await candies.new_game( message )
    elif message.text.isdigit():
        if await candies.player( message ):
            users[ user_id ][ "game_mode" ] = False
    else:
        await message.answer( "Вы должны взять не менее 1 и не более 28 конфет..." )


# Обработчик /candies_rules  # Переделать на /candies rules - вызов с параметром
async def candies_rules( message: types.Message ):
    user_id = message.from_user.id
    await log( __name__, "candies_rules", f"{ user_id }: { message.text }" )

    await message.answer( f"{ bot_data.rules }", reply_markup=kb  )


# Выход из режима игры
async def stop_game( message: types.Message ):
    user_id = message.from_user.id
    await log( __name__, "stop_game", f"{ user_id }: { message.text }" )

    if await check_user( user_id, "game_mode" ) == True:
        users[ user_id ][ "game_mode" ] = False

        await message.answer( "Жаль, что ты уже уходишь 😢...", reply_markup=kb )
        await command_start( message )

    else:
        await message.answer( "Вы сейчас не играете в игру...", reply_markup=kb )


# Обработчик всех сообщений
async def not_command( message: types.Message ):
    user_id = message.from_user.id
    await log( __name__, "not_command", f"{ user_id }: { message.text }" )

    if await check_user( user_id, "game_mode" ) == True and message.text.isdigit(): # if candies_mode:
        await candies_game( message )
    else:
        await message.answer( f"Я пока не умею обрабатывать: \"{message.text}\"" )


# Регистрируем handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler( command_start, commands=[ "start", "старт", "help", "помощь", "menu", "меню" ] )

    dp.register_message_handler( candies_game,  commands=[ "candies_game", "candies", "sweets", "конфеты", "game", "игра", "играть" ] )
    dp.register_message_handler( candies_rules, commands=[ "candies_rules", "rules", "правила" ] )

    dp.register_message_handler( stop_game,     commands=[ "stop", "стоп", "выйти" ] )

    dp.register_message_handler( not_command )
