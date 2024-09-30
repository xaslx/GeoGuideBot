from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from fastapi.staticfiles import StaticFiles
from geopy.geocoders import Yandex


load_dotenv()
geolocator: Yandex = Yandex(api_key=os.getenv('API_KEY'))
api_key: str = os.getenv('API_KEY')

template: Jinja2Templates = Jinja2Templates(directory="app/static/templates")

app: FastAPI = FastAPI(title='Карта')
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