from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states import FillForm
from db.db import User

START_MESSAGE = "Привет! Для регистрации Вам необходимо ввести имя и электронную почту."
FILL_NAME = "Пожалуйста, введите имя"
FILL_MALE = "Пожалуйста, введите вашу почту"
WRONG_NAME = "То, что вы отправили не похоже на имя. Возможно вы использовали, цифры или пробелы\n\nПожалуйста, введите ваше имя\n\n"
SUCCESS = "Вы успешно зарегистрированы! Для добавления заметки нажмите /addnote. Чтобы посмотреть список заметок нажмите /mynotes"
WRONG_MAIL = "Вы ввели неверную почту, попробуйте еще раз."

router = Router()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext, user: User | None = None):
    await message.answer(START_MESSAGE)
    if user:
        await message.answer(SUCCESS)
    else:
        await state.set_state(FillForm.fill_name)
        await message.answer(FILL_NAME)


@router.message(StateFilter(FillForm.fill_name), F.text.isalpha())
async def fill_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FillForm.fill_mail)
    await message.answer(FILL_MALE)


@router.message(StateFilter(FillForm.fill_name))
async def warning_not_name(message: Message, state: FSMContext):
    await message.answer(WRONG_NAME)
