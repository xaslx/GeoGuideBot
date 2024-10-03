from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, WebAppInfo
from geopy.geocoders import Yandex
import os
from bot.src.repository.user_repository import UserRepository
from bot.src.repository.sqlalchemy_repositroy import SQLAlchemyRepository
from bot.src.handlers.admin_filter import AdminProtect
from bot.src.keyboards.inline_keyboards import add_establishment
from bot.src.utils.token import create_session_token





admin_router: Router = Router()




@admin_router.message(AdminProtect(), StateFilter(default_state), Command('apanel'))
async def admins_cmd(message: Message):
    await message.answer('Команды для администрации')



@admin_router.message(AdminProtect(), StateFilter(default_state), Command('add_establishment'))
async def add_new_establishment(message: Message):
    token: str = create_session_token({'user_id': str(message.from_user.id)})
    await message.answer('Добавление нового заведения', reply_markup=add_establishment(token=token))