from json import JSONDecodeError
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from logger import logger
from bot.src.handlers.user_handlers import user_router
from bot.src.handlers.admin_handlers import admin_router
import os
from fastapi import Request, Response
from bot.src.middleware import DbMiddleware
from database import async_session_maker




TOKEN_BOT: str = os.getenv('TOKEN_BOT')
web_hook: str = f"/{TOKEN_BOT}"
WEBHOOK_URL: str = os.getenv('WEBHOOK_URL')
bot: Bot = Bot(TOKEN_BOT, default=DefaultBotProperties(parse_mode="HTML"))
dp: Dispatcher = Dispatcher()


async def set_webhook():
    webhook_url: str = f'{WEBHOOK_URL}{web_hook}'
    await bot.set_webhook(webhook_url, allowed_updates=["callback_query", "message"])


async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    await set_webhook()
    

async def on_shutdown():
    await bot.session.close()

async def handle_web_hook(request: Request):
    url: str = str(request.url)
    index: str = url.rfind("/")
    token: str = url[index + 1 :]
    if token == TOKEN_BOT:
        try:
            request_data = await request.json()
            update = types.Update(**request_data)
            await dp.feed_webhook_update(bot, update)
            return Response()
        except JSONDecodeError:
            logger.error("Ошибка декодирования Json")
    else:
        return Response(status_code=403)


dp.include_router(user_router)
dp.include_router(admin_router)
dp.startup.register(on_startup)
dp.startup.register(on_shutdown)
dp.update.middleware.register(DbMiddleware(async_session_maker))
