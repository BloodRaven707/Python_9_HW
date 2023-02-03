from os.path import isfile

from datetime import datetime


# Главный логгер
async def log( module_name, function_name, info ):
    date = datetime.today().date()
    time = datetime.today().time()

    data = f"{ date } { time } | { function_name } | { info }\n"

    if not isfile( f"logs\\{ module_name }.log" ):
        with open( f"logs\\{ module_name }.log", "w", encoding="UTF-8") as file:
            file.write( data )
    else:
        with open( f"logs\\{ module_name }.log", "a", encoding="UTF-8") as file:
            file.write( data )
