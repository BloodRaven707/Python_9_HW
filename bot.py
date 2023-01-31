from aiogram.utils import executor


from create_bot import dp
import handlers


async def on_startup(_):
    print("[+] Бот запущен")


if __name__ == "__main__":
    handlers.register_handlers_client(dp)


    # Не отвечать на сообщения пришедшие когда был отключен
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
