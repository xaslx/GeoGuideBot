from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from bot.src.repository.establishments_repository import EstablishmentRepository
from bot.src.handlers.admin_filter import AdminProtect
from bot.src.states.establishments import AddEstablishmentState
from sqlalchemy.ext.asyncio import AsyncSession
from bot.src.schemas.establishment import EstablishmentSchemaIn



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




@admin_router.message(AdminProtect(), StateFilter(default_state), Command('add_establishment'))
async def add_new_establishment(message: Message, state: FSMContext):
    await message.answer(
        'Введите название ресторана\n'
        'Или команду /cancel - чтобы отменить'
    )
    await state.set_state(AddEstablishmentState.title)



@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.title), F.text)
async def add_title(message: Message, state: FSMContext):
    await state.update_data({'title': message.text})
    await state.set_state(AddEstablishmentState.description)
    await message.answer(
        'Теперь введите описание ресторана\n'
        'Или команду /cancel - чтобы отменить'
    )


@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.title), ~F.text)
async def add_title_warning(message: Message):
    await message.answer(
        'Отправьте название ресторана\n'
    )


@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.description), F.text)
async def add_description(message: Message, state: FSMContext):
    await state.update_data({'description': message.text})
    await state.set_state(AddEstablishmentState.address)
    await message.answer(
        'Теперь введите адрес\n'
        'Или команду /cancel - чтобы отменить'
    )


@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.description), ~F.text)
async def add_description_warning(message: Message):
    await message.answer(
        'Введите описание\n'
    )


@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.address), F.text)
async def add_address(message: Message, state: FSMContext):
    await state.update_data({'address': message.text})
    await state.set_state(AddEstablishmentState.photo_url)
    await message.answer(
        'Теперь добавьте фото\n'
        'Или команду /cancel - чтобы отменить'
    )


@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.address), ~F.text)
async def add_address_warning(message: Message):
    await message.answer('Введите адрес')


@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.photo_url), F.photo)
async def add_photo(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data({'photo_url': message.photo[-1].file_id})
    res: dict = await state.get_data()
    new_establishment: EstablishmentSchemaIn = EstablishmentSchemaIn(**res)
    await EstablishmentRepository.add(session=session, **new_establishment.model_dump())
    await message.answer('Ресторан успешно добавлен')
    await state.clear()



@admin_router.message(AdminProtect(), StateFilter(AddEstablishmentState.photo_url), ~F.photo)
async def add_photo_warning(message: Message):
    await message.answer('Отправьте фото')


@admin_router.message(AdminProtect(), StateFilter(default_state), Command('ahelp'))
async def admins_cmd(message: Message):
    await message.answer(
        'Команды для администрации:\n'
        '/add_establishment - добавить новый ресторан\n'
        '/del_establishment - удалить ресторан'
    )
