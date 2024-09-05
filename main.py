import logging
import asyncio, logging, sys

from aiogram import Bot, Dispatcher, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import TG_TOKEN
from routers.admin import router as admin_router 
from routers.users import router as users_router 
from routers.channel import router as channel_router 

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TG_TOKEN,
    default=DefaultBotProperties(
    parse_mode=ParseMode.HTML,
    ))

dp = Dispatcher()


async def main() -> None:
    dp.include_routers(
        # admin_router,
        users_router,
        channel_router
        )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    
