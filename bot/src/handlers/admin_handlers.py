from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, WebAppInfo
from geopy.geocoders import Yandex
import os
from bot.src.repository.user_repository import UserRepository
from bot.src.repository.establishments_repository import EstablishmentRepository
from bot.src.handlers.admin_filter import AdminProtect
from bot.src.utils.token import create_session_token
from bot.src.states.establishments import AddEstablishmentState
from bot.src.keyboards.keyboards import get_category_for_new_establishment
from sqlalchemy.ext.asyncio import AsyncSession




admin_router: Router = Router()



@admin_router.message(AdminProtect(), Command(commands="cancel"), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text="Отменять нечего.\n\n" "Отправьте команду /add_establishment")


@admin_router.message(AdminProtect(), Command(commands="cancel"), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text="Вы отменили добавление нового заведения\n\n"
        "Чтобы снова перейти к добавлению - "
        "отправьте команду /add_establishment"
    )
    await state.clear()


@admin_router.message(AdminProtect(), StateFilter(default_state), Command('apanel'))
async def admins_cmd(message: Message):
    await message.answer('Команды для администрации')



@admin_router.message(AdminProtect(), StateFilter(default_state), Command('add_establishment'))
async def add_new_establishment(message: Message, state: FSMContext):
    await message.answer(
        'Выберите в какую категорию добавить новое заведение',
        reply_markup=get_category_for_new_establishment()
    )
    await state.set_state(AddEstablishmentState.type_id)



@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.type_id), F.text.in_(('кафе', 'ресторан')))
async def add_establishment_category(message: Message, state: FSMContext):
    type_id: int = 1 if message.text == 'ресторан' else 2
    await state.update_data({'type_id': type_id})
    await message.answer('Теперь введите название заведения', reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddEstablishmentState.title)


@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.type_id), ~F.text.in_(('кафе', 'ресторан')))
async def add_establishment_warning(message: Message):
    await message.answer('Можно выбрать только "кафе" или "ресторан"')


@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.title), F.text)
async def add_title(message: Message, state: FSMContext):
    await state.update_data({'title': message.text})
    await state.set_state(AddEstablishmentState.description)
    await message.answer('Теперь введите описание заведения')


@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.title), ~F.text)
async def add_title_warning(message: Message):
    await message.answer('Отправьте название заведения')



@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.description), F.text)
async def add_description(message: Message, state: FSMContext):
    await state.update_data({'description': message.text})
    await state.set_state(AddEstablishmentState.address)
    await message.answer('Теперь введите адрес')


@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.description), ~F.text)
async def add_description_warning(message: Message):
    await message.answer('Введите описание')


@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.address), F.text)
async def add_address(message: Message, state: FSMContext):
    await state.update_data({'address': message.text})
    await state.set_state(AddEstablishmentState.photo_url)
    await message.answer('Теперь добавьте фото')


@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.address), ~F.text)
async def add_address_warning(message: Message):
    await message.answer('Введите адрес')


@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.photo_url), F.photo)
async def add_address(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data({'photo_url': message.photo[-1].file_id})
    await message.answer_photo('Отлично, заведение добавлено!')



@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.photo_url), ~F.photo)
async def add_address_warning(message: Message):
    await message.answer('Отправьте фото')