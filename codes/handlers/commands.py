from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from codes.states.save_fsm import Form
router = Router()

@router.message(Command('start'))
async def start_form(message: Message, state: FSMContext):
    await message.answer('Привет, Как вас зовут?')
    await state.set_state(Form.name)

@router.message(Command('cancel'))
async def cancel_form(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Анкета удалена!')

@router.message(Form.name, F.text)
async def form_name(message: Message, state: FSMContext):
    name = message.text

    if not name.isalpha():
        await message.answer('Введите корректное имя!')
        return

    await state.update_data(name=name)

    await message.answer('Классное имя! Фамилия?')
    await state.set_state(Form.surname)

@router.message(Form.surname, F.text)
async def form_surname(message: Message, state: FSMContext):
    surname = message.text
    if not surname.isalpha():
        await message.answer('Введите корректную фамилию!')
        return

    await state.update_data(surname=surname)

    await message.answer('Сколько вам лет?')
    await state.set_state(Form.age)

@router.message(Form.age, F.text)
async def form_age(message: Message, state: FSMContext):
    age = message.text

    if not age.isdigit():
        await message.answer('Введите корректный возраст!')
        return

    await state.update_data(age=age)
    await message.answer('Круто! Двигаемся дальше\nВ каком городе ты живешь?')
    await state.set_state(Form.city)

@router.message(Form.city, F.text)
async def form_city(message: Message, state: FSMContext):
    city = message.text
    await state.update_data(city=city)

    data = await state.get_data()
    name = data['name']
    surname = data['surname']
    age = data['age']
    city = data['city']

    await message.answer(f'Ваше имя и фамилия: {name} {surname}\nВаш возраст: {age}\nВаш город: {city}')
    await state.clear()



