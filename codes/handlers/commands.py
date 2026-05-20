from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
import random
import asyncio
from codes.states.save_fsm import Form, GameState

router = Router()

def reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=
        [[KeyboardButton(text='🔄 Заполнить анкету заново')],
        [KeyboardButton(text='🎮 Игры')]],
        resize_keyboard=True
    )
    return keyboard


def inline_keyboard_form():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Подтвердить анкету', callback_data='✅ confirm_anketa')],
            [InlineKeyboardButton(text='Удалить анкету', callback_data='❌ cancel_anketa')],
        ],
    )
    return keyboard

def inline_keyboard_games():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Рандомайзер чисел', callback_data='🤔 random')],
            [InlineKeyboardButton(text='Орел и Решка', callback_data='🪙 coin')],
            [InlineKeyboardButton(text='Бросок кубика', callback_data='🎲 dice')],
            [InlineKeyboardButton(text='Все игры', callback_data='🎮 all_games')],
        ],
        resize_keyboard=True
    )
    return keyboard

async def generate_number():
    await asyncio.sleep(1)
    return random.randint(1, 100)

async def generate_coin():
    await asyncio.sleep(1)
    return random.choice(['Орёл', 'Решка'])

async def generate_dice():
    await asyncio.sleep(1)
    return random.randint(1, 6)

@router.callback_query(lambda c: c.data == '✅ confirm_anketa')
async def confirm_anketa(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get('name', 'Друг')
    surname = data.get('surname')
    age = data.get('age')
    city = data.get('city')
    await callback.message.answer(f'Ваше имя и фамилия: {name} {surname}\nВаш возраст: {age}\nВаш город: {city}\nВаша анкета подтверждена!')
    await callback.answer()

@router.callback_query(lambda c: c.data == '❌ cancel_anketa')
async def cancel_anketa(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Ваша анкета удалена!')
    await callback.answer()

@router.callback_query(lambda c: c.data == '🤔 random')
async def randomizer(callback: CallbackQuery, state: FSMContext):
    await asyncio.sleep(1)
    name = (await state.get_data()).get('name', 'Друг')
    await state.clear()

    number = random.randint(1, 100)

    await state.set_state(GameState.number)
    await state.update_data(number=number)

    await callback.message.answer(f'{name} угадай число от 1 до 100!')
    await callback.answer()

@router.message(GameState.number)
async def check_number(message: Message, state: FSMContext):
    data = await state.get_data()
    number = data.get('number')

    if number is None:
        await message.answer("Игра не найдена. Начни заново 🎮")
        return

    try:
       user_guess = int(message.text)
    except ValueError:
        await message.answer('Введи число!')
        return

    if 1 <= user_guess <= 100:
        if user_guess == number:
            await message.answer('🎉 Правильно!')
            await state.clear()
        elif user_guess < number:
            await message.answer('📉 Больше')
        else:
            await message.answer('📈 Меньше')
    else:
        await message.answer('Введи число в диапазоне от 1 до 100!')

@router.callback_query(lambda c: c.data == '🪙 coin')
async def random_coin(callback: CallbackQuery, state: FSMContext):
    await asyncio.sleep(1)
    await state.clear()
    l = ['Орел', 'Решка']
    coin = random.choice(l)

    await state.set_state(GameState.coin)
    await state.update_data(coin=coin)

    await callback.message.answer('Угадай, Орел или Решка?')
    await callback.answer()

@router.message(GameState.coin)
async def check_coin(message: Message, state: FSMContext):
    data = await state.get_data()
    coin = data.get('coin')

    if coin is None:
        return

    user_guess = message.text.strip().capitalize()

    if user_guess == coin:
        await message.answer('🎉 Угадал!')
        await state.clear()
    else:
        await message.answer('К сожалению, Вы не угадали\nПопробуйте еще раз!')

@router.callback_query(lambda c: c.data == '🎲 dice')
async def random_dice(callback: CallbackQuery, state: FSMContext):
    await asyncio.sleep(1)
    name = (await state.get_data()).get('name', 'Друг')
    await state.clear()

    dice = random.randint(1, 6)

    await state.set_state(GameState.dice)
    await state.update_data(dice=dice)

    await callback.message.answer(f'{name} Угадай число от 1 до 6!(В будущем добавлю сам кубик для игры!)')
    await callback.answer()

@router.message(GameState.dice)
async def check_dice(message: Message, state: FSMContext):
    data = await state.get_data()
    dice = data.get('dice')

    if dice is None:
        await message.answer('Игра не найдена. Начни заново 🎮!')
        return
    try:
        user_guess = int(message.text)
    except ValueError:
        await message.answer('Введи цифру!')
        return

    if 1 <= user_guess <= 6:
        if user_guess == dice:
            await message.answer('🎉 Угадал!')
        elif user_guess < dice:
            await message.answer('📉 Больше!')
        else:
            await message.answer('📈 Меньше!')
    else:
        await message.answer('Введи цифру от 1 до 6!')


@router.callback_query(lambda c: c.data == '🎮 all_games')
async def all_games(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    number, coin, dice = await asyncio.gather(
        generate_number(),
        generate_coin(),
        generate_dice(),
    )

    await callback.message.answer(
        f'🔢 Number: {number}\n'
        f'🪙 Coin: {coin}\n'
        f'🎲 Dice: {dice}'
    )
    await callback.answer()

@router.message(F.text == '🔄 Заполнить анкету заново')
async def restart_form(message: Message, state: FSMContext):
    await state.clear()

    await message.answer('Начинаем заново!\nКак вас зовут?', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.name)

@router.message(F.text == '🎮 Игры')
async def play_games(message:Message, state: FSMContext):
    name = (await state.get_data()).get('name', 'Друг')
    await message.answer(f'{name} давай поиграем в игру?\nКакую игру ты предпочитаешь поиграть?', reply_markup=inline_keyboard_games())

@router.message(Command('start'))
async def start_form(message: Message, state: FSMContext):
    await message.answer('Привет, Как вас зовут?')
    await state.set_state(Form.name)

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
    name = data.get('name')
    surname = data.get('surname')
    age = data.get('age')
    city = data.get('city')

    await message.answer(f'Ваше имя и фамилия: {name} {surname}\nВаш возраст: {age}\nВаш город: {city}\nЕсли вы хотите подвердить или удалить, то воспользуйтесь кнопками!', reply_markup=inline_keyboard_form())
    await message.answer('Если вы хотите заполнить заново или поиграть в игры, то воспользуйтесь кнопками в меню!', reply_markup=reply_keyboard())


