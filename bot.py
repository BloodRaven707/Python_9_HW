from aiogram.utils import executor

from create_bot import dp
import handlers
from logger import log


async def on_startup( _ ):
    await log( "bot" if __name__ == "__main__" else __name__, "on_startup", f"[+] Бот запущен" )


if __name__ == "__main__":
    handlers.register_handlers_client( dp )

    # skip_updates=True === Не отвечать на сообщения пришедшие когда был отключен
    executor.start_polling( dp, skip_updates=True, on_startup=on_startup )
