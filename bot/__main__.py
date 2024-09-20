import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import ConnectionPool, Redis

from bot.config import Config, load_config
from bot.handlers import router
from bot.middlewares.middleware import CheckUserMiddleware, DBSessionMiddleware
from db.create_pool import create_pool

CHECK_INTERVAL = 60


async def main():
    logging.basicConfig(level=logging.INFO)
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token)
    redis: Redis = Redis(
        connection_pool=ConnectionPool(
            host=config.redis_db.redis_host,
            port=config.redis_db.redis_port,
            db=config.redis_db.redis_db,
        )
    )

    dp: Dispatcher = Dispatcher(
        name="main_dispatcher",
        storage=RedisStorage(redis=redis),
        config=config,
    )
    session_pool = await create_pool()
    dp.message.middleware(DBSessionMiddleware(session_pool))
    dp.message.middleware(CheckUserMiddleware())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
