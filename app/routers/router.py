from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from geopy.geocoders import Yandex
import os




template: Jinja2Templates = Jinja2Templates(directory="app/static/templates")
api_key: str = os.getenv('API_KEY')
geolocator: Yandex = Yandex(api_key=api_key)



router: APIRouter = APIRouter('/')




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