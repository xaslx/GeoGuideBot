from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from geopy.geocoders import Yandex
import os
from bot.src.repository.user_repository import UserRepository
from bot.src.repository.sqlalchemy_repositroy import SQLAlchemyRepository
from bot.src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from bot.src.states.location import LocationState
from bot.src.keyboards.keyboards import keyboard


user_router: Router = Router()
api_key: str = os.getenv('API_KEY')
geolocator: Yandex = Yandex(api_key=api_key)


@user_router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, session: AsyncSession):
    user: User = await UserRepository.find_one_or_none(session=session, user_id=message.from_user.id)
    if not user:
        await UserRepository.add(session=session)
    await message.answer('Выбери', reply_markup=keyboard)
    


@user_router.message(StateFilter(default_state), F.text == 'Рестораны')
async def get_restaurants(message: Message):
    await message.answer(
        'вот так',
        reply_markup=ReplyKeyboardRemove()
    )
    
    

@user_router.message(Command('location'), StateFilter(default_state))
async def cmd_location(message: Message, state: FSMContext):
    await message.answer(
        f'Отправь свою геопозцию'
    )
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(LocationState.location)


@user_router.message(StateFilter(LocationState.location), F.location)
async def get_location(message: Message, state: FSMContext):
    pass
    

@user_router.message(StateFilter(LocationState.location), ~F.location)
async def get_location_warning(message: Message):
    await message.answer('Вы должны отправить вашу геопозицию.')

