from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio

from pyexpat.errors import messages

with open('Key', 'r') as file:
    API = file.read().strip()

bot = Bot(token=API)
dp = Dispatcher(storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message(Command(commands=['start']))
async def start(message: Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

@dp.message(Command(commands=['Calories']))
async def set_age(message: Message, state: FSMContext):
    await message.answer('Ввудите свой возраст:')
    await state.set_state(UserState.age)

@dp.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await state.set_state(UserState.growth)

@dp.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await state.set_state(UserState.weight)

@dp.message(UserState.weight)
async def send_colories(message: Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()

    calories = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5

    await message.answer(f'Ваша норма калорий: {calories:.2f} ккал в день.')
    await state.clear()

@dp.message()
async def all_message(message: Message):
    await message.answer('Введите команду /start, чтобы начать общение.')

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
