from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from fastapi.staticfiles import StaticFiles
from geopy.geocoders import Yandex
from contextlib import asynccontextmanager
from logger import logger
from bot.init_database import init_db



load_dotenv()
geolocator: Yandex = Yandex(api_key=os.getenv('API_KEY'))
api_key: str = os.getenv('API_KEY')

template: Jinja2Templates = Jinja2Templates(directory="app/static/templates")




@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    logger.info("Fastapi приложение и Бот запущены")
    yield


app: FastAPI = FastAPI(title='Карта', lifespan=lifespan)
app.mount("/app/static", StaticFiles(directory="app/static"), "static")


@app.get('/')
async def get_map(
    request: Request, 
    latitude: float,
    longitude: float,
    start_address: str,
    end_address: str
):
    return template.TemplateResponse(
        request=request,
        name='index.html',
        context={
            'api_key': api_key,
            'latitude': latitude,
            'longitude': longitude,
            'start_address': start_address,
            'end_address': end_address
        }
    )