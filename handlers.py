import random


from aiogram import types, Dispatcher


import bot_data
import candies


# #
# Давить меню (общее меня) через BotFather... если будет больше функционала...
# Добавить обычное меню... если будет больше функционала...
#
# #

game_mode = False


# /start и некоторые другие
async def command_start( message: types.Message ):
    global game_mode
    if game_mode:
        await message.answer( f"{ message.from_user.full_name }, сначала выйдите из игры > /stop" )
    await message.answer( f"{ message.from_user.full_name }, { bot_data.main_menu }" )


# /candies_rules
async def candies_rules( message: types.Message ):
    name = message.from_user.full_name
    await message.answer( f"{ bot_data.rules }" )


# /candies
async def candies_game( message: types.Message ):
    global game_mode
    user = message.from_user.full_name
    if not game_mode:
        game_mode = True # candies_mode = True
        await candies.new_game( message )

    else:
        await candies.player( message )


async def stop_game( message: types.Message ):
    global game_mode
    if game_mode:
        game_mode = False
        # if candies_mode:
        # candies_mode = False
        candies.candies = 140
        candies.move = ""
    await message.answer( "Жаль, что ты уже уходишь 😢..." )
    await command_start( message )


async def not_command( message: types.Message ):
    global game_mode
    if game_mode and message.text.isdigit(): # if candies_mode:
        await candies_game( message )
    else:
        await message.answer( f"Я пока не умею обрабатывать: \"{message.text}\"" )


# Регистрируем handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler( command_start, commands=[ "start", "старт", "help", "помощь", "menu", "меню" ] )

    dp.register_message_handler( candies_game,  commands=[ "candies_game", "candies", "sweets", "конфеты", "game", "игра", "играть" ] )
    dp.register_message_handler( candies_rules, commands=[ "candies_rules", "rules", "правила" ] )

    dp.register_message_handler( stop_game,     commands=[ "stop", "стоп" ] )

    dp.register_message_handler( not_command )
