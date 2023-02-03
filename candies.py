from random import choice, randint

from aiogram import types

import bot_data
from logger import log
from user_kb import kbs

# #
# Добавить кнопки: 1 и 28 для выбора конфет
# Добавить кнопки: /rules (правила) и /stop_game (выход)
# Доработка бота - для более сложной логики...
# #

_module_name = "candies"
users_candies = {}


# Запуск новой игры
async def new_game( message: types.Message ) -> int:
    user_id = message.from_user.id
    await log( __name__, "new_game", f"{ user_id }: { message.text }" )

    users_candies[ user_id ] = {}
  # users_candies[ user_id ][ "start_count" ] = 300
  # users_candies[ user_id ][ "max_taken" ] = 30
    users_candies[ user_id ][ "count" ] = 140

    user_name = message.from_user.full_name
    await message.answer( f"{ user_name }, игра началась..." \
                          f"Для выхода введите > /stop" )
    if choice( [True, False] ) == True:
        await message.answer( f"На столе лежит { users_candies[ user_id ][ 'count' ] } " \
                              f"конфет{ declension( users_candies[ user_id ][ 'count' ] )[ 0 ] }\n" \
                              f"{ user_name }, сколько конфет возьмете вы?", reply_markup=kbs )
    else:
        await bot( message )


# Ход игрока
async def player( message: types.Message ) -> bool:
    user_id = message.from_user.id
    await log( __name__, "player", f"{ user_id }: { message.text }" )

    while True:
        taken = message.text
        if taken.isdigit():
            taken = int( taken )
            if taken > users_candies[ user_id ][ "count" ]:
                await message.answer( f"Вы хотите взять { taken } конфет{ declension( taken )[ 0 ] }, "
                                      f"но на столе всего { users_candies[ user_id ][ 'count' ] } " \
                                      f"конфет{ declension( taken )[ 0 ] }.\n"
                                      f"Возьми поменьше, не жадничай 😃", reply_markup=kbs )
                return False
            elif taken < 1 or taken > 28:
                if users_candies[ user_id ][ "count" ] > 28: # > 29
                    await message.answer( "Вы должны взять не менее 1 и не более 28 конфет...", reply_markup=kbs )
                else:
                    await message.answer( "Помните победит тот кто возьмет последние конфеты...", reply_markup=kbs )
                    # await message.answer( "Помните взяв последнюю конфету вы проиграете..." ) для другого режима
                return False
            else:
                break

    if await check_win( message, "player", taken ):
        await log( __name__, "player", f"{ user_id }: Победил" )
        return True

    await message.answer( f"Вы берете { taken } конфет{ declension( taken )[ 1 ] }\n" \
                          f"На столе осталось { users_candies[ user_id ][ 'count' ] } "
                          f"конфет{ declension( users_candies[ user_id ][ 'count' ] )[ 0 ] }." )

    return await bot( message )


# Ход бота
async def bot( message: types.Message ) -> bool:
    user_id = message.from_user.id

    user_name = message.from_user.full_name
    if users_candies[ user_id ][ "count" ] <= 28: # 29 для другого режима
        taken = users_candies[ user_id ][ "count" ] # 29 -1 для другого режима
    else:
        taken = randint( 1, 28 )

    if await check_win( message, "Бот", taken ):
        await log( __name__, "player", f"{ user_id }: Проиграл" )
        return True

    await message.answer( f"Бот берет { taken } конфет{ declension( taken )[ 1 ] }\n" \
                          f"На столе осталось { users_candies[ user_id ][ 'count' ] } "
                          f"конфет{ declension( users_candies[ user_id ][ 'count' ] )[ 0 ] }." )

    await message.answer( f"{ user_name }, сколько конфет возьмете вы?", reply_markup=kbs )
    return False


# Проверка...
async def check_win( message: types.Message, player: str, taken: int ) -> bool:
    user_id = message.from_user.id

    user_name = message.from_user.full_name
    users_candies[ user_id ][ "count" ] -= taken

    if users_candies[ user_id ][ "count" ] == 0:
        if player == "player":
            await message.answer( f"Вы берете { taken } конфет{ declension( taken )[ 1 ] }\n" \
                                  f"\nКонфет больше нет! "
                                  f"\n{ user_name } позравляю, вы победили...🤓"
                                  f"\n\nЕще разок? > /candies_game")
        else:
            await message.answer( f"Бот берет { taken } конфет{ declension( taken )[ 1 ] }\n" \
                                  f"Конфет больше нет! Выиграл бот! 😎\n"
                                  f"Как насчет реванша?:) > /candies_game")

        return True
    else:
        return False


# Частичная реализация склонений для русских слов, для полноценной рализиции нужен словарь с категориями или система анализа
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
