users = {}
# users[ user_id ][ "game_mode" ] = False  # Значение по умолчанию


# Проверка данных у пользователя
async def check_user( user_id: dict, key: str ):

    # Задаем значения по умолчанию
    if not user_id in users:
        users[ user_id ] = {}
        if key == "game_mode":
            users[ user_id ][ key ] = False

    return users[ user_id ][ key ]
