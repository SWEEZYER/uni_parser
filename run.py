import logging
import asyncio
from os import getenv
from dotenv import load_dotenv
import time
from aiogram import Bot, Dispatcher

from handlers import router
from aiogram.fsm.storage.memory import MemoryStorage


# Загрузка переменных окружения
load_dotenv()
TOKEN = getenv("BOT_TOKEN")  # Получение токена бота
# ADMIN_IDS = list(map(int, getenv("ADMIN_ID", "").split(","))) if getenv("ADMIN_ID") else []
#
# if not TOKEN:
#     raise ValueError("Токен бота (BOT_TOKEN) не найден в .env файле!")
#
# if not ADMIN_IDS:
#     logging.warning("Не указаны идентификаторы администраторов (ADMIN_ID).")

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()  # Используем хранилище состояний в памяти
dp = Dispatcher(storage=storage)


# # Передача admin_ids в контекст диспетчера
# dp["admin_ids"] = ADMIN_IDS

async def main():
    """Основная функция для запуска бота."""
    dp.include_router(router)
    await dp.start_polling(bot)


def times():
    """Функция для получения текущего времени в формате MM-DD | HH:MM."""
    time_time = time.time()
    local_time = time.localtime(time_time)
    return time.strftime("%m-%d | %H:%M", local_time)


if __name__ == "__main__":
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)

    try:
        print(f"\nБот начал работу!\n   {times()}\n")
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\nБот завершил работу!\n   {times()}\n")