from fastapi import FastAPI
from dotenv import load_dotenv
import os
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from logger import logger
from init_database import init_db
from bot.run import on_startup, handle_web_hook
from app.routers import router



load_dotenv()





@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await on_startup()
    logger.info("Fastapi приложение и Бот запущены")
    yield


app: FastAPI = FastAPI(title='Карта', lifespan=lifespan)
app.mount("/app/static", StaticFiles(directory="app/static"), "static")
app.add_route(f"/{os.getenv('TOKEN_BOT')}", handle_web_hook, methods=["POST"])
app.include_router(router)

