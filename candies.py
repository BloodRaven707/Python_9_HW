from random import choice, randint

from aiogram import types

import bot_data

# #
# Добавить кнопки: 1 и 28 для выбора конфет
# Добавить кнопки: /rules (правила) и /stop_game (выход)
# Доработка бота - для более сложной логики...
# #

candies = {}


async def new_game( message: types.Message ) -> int:
    global candies, move
    user = message.from_user.full_name
    candies[ user ] = {}
    candies[ user ][ "count" ] = 140
    candies[ user ][ "move" ] = choice( [True, False] )
    await message.answer( f"{ user }, игра началась..." \
                          f"Для выхода введите > /stop" )
    if candies[ user ][ "move" ] == True:
        await message.answer( f"На столе лежит { candies[ user ][ 'count' ] } конфет{ declension( candies[ user ][ 'count' ] )[ 0 ] }\n" \
                              f"{ user }, сколько конфет возьмете вы? " )
    else:
        await bot( message )


async def player( message: types.Message ):
    taken = ""
    user = message.from_user.full_name
    while True:
        taken = message.text
        if taken.isdigit():
            taken = int( taken )
            if taken > candies[ user ][ "count" ]:
                await message.answer( f"Вы хотите взять { taken } конфет{ declension( taken )[ 0 ] }, "
                                      f"но на столе всего { candies[ user ][ 'count' ] } конфет{ declension( taken )[ 0 ] }.\n"
                                      f"Возьми поменьше, не жадничай 😃" )

            elif taken < 1 or taken > 28:
                if candies[ user ][ "count" ] > 28: # > 29
                    await message.answer( "Вы должны взять не менее 1 и не более 28 конфет..." )
                else:
                    await message.answer( "Помните победит тот кто возьмет последние конфеты..." )
                    # await message.answer( "Помните взяв последнюю конфету вы проиграете..." ) для другого режима
            else:
                break

    if await check_win(message, "player", taken):
        return

    await message.answer( f"Вы берете { taken } конфет{ declension( taken )[ 1 ] }\n" \
                          f"На столе осталось { candies[ user ][ 'count' ] } "
                          f"конфет{ declension( candies[ user ][ 'count' ] )[ 0 ] }." )

    await bot( message )


async def bot( message: types.Message ):
    user = message.from_user.full_name
    taken = 0
    if candies[ user ][ "count" ] <= 28: # 29 для другого режима
        taken = candies[ user ][ "count" ] # 29 -1 для другого режима
    else:
        taken = randint( 1, 28 )

    if await check_win( message, "Бот", taken ):
        return

    await message.answer( f"Бот берет { taken } конфет{ declension( taken )[ 1 ] }\n" \
                          f"На столе осталось { candies[ user ][ 'count' ] } "
                          f"конфет{ declension( candies[ user ][ 'count' ] )[ 0 ] }." )

    await message.answer( f"{ user }, сколько конфет возьмете вы?" )


async def check_win( message: types.Message, player: str, taken: int ) -> bool:
    global candies
    user = message.from_user.full_name
    candies[ user ][ "count" ] -= taken

    if candies[ user ][ "count" ] == 0:
        if player == "player":
            await message.answer( f"Вы берете { taken } конфет{ declension( taken )[ 1 ] }\n" \
                                  f"\nКонфет больше нет! "
                                  f"\n{ user } позравляю, вы победили...🤓"
                                  f"\n\nЕще разок? > /candies_game")
        else:
            await message.answer( f"Конфет больше нет! Выиграл бот! 😎\n"
                                  f"Как насчет реванша?:) > /candies_game")

        return True
    else:
        return False


def declension( count: int ) -> str:    # Спасибо Елене за идею...
    count_str = str( count )
    count_len = len( count_str )

    if count_len == 1:
        if count in [ 2, 3, 4 ]:
            return "ы", "ы"
        elif count == 1:
            return "а", "а"

    elif count_str[ -2 ] != "1":
        if count_str[ -1 ] in [ "2", "3", "4" ]:
            return "ы", "ы"
        elif count_str[ -1 ] in [ "1" ]:
            return "y" "а"
    return "", ""
