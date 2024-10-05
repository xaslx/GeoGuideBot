from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from geopy.geocoders import Yandex
import os
from bot.src.utils.token import valid_token
import os



template: Jinja2Templates = Jinja2Templates(directory="app/static/templates")
api_key: str = os.getenv('API_KEY')
geolocator: Yandex = Yandex(api_key=api_key)
ADMINS: list[str] = os.getenv('ADMINS_ID').split(',')


router: APIRouter = APIRouter(prefix='', tags=['Main router'])




@router.get('/')
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



