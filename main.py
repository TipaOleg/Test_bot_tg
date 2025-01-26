from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData
import asyncio


with open('Key', 'r') as file:
    API = file.read().strip()

bot = Bot(token=API)
dp = Dispatcher(storage=MemoryStorage())
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рассчитать')],
        [KeyboardButton(text='Информация')]
    ],
    resize_keyboard=True
)
inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text="Формулы расчета", callback_data='formulas')]
    ]
)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message(Command(commands=['start']))
async def start(message: Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью. Выберите действие:', reply_markup=main_keyboard)

@dp.message(lambda message: message.text == 'Рассчитать')
async def main_menu(message: Message):
    await message.answer('Выберите опцию', reply_markup=inline_keyboard)

@dp.message(lambda message: message.text == 'Информация')
async def info(message: Message):
    await message.answer('Это бот для улучшения вашего здоровья.')

@dp.callback_query(lambda call: call.data == 'formulas')
async def get_formulas(call: CallbackQuery):
    await call.message.answer('Формула Миффлина-Сан Жеора: 10*вес + 6.25*рост - 5*возраст + 5')
    await call.answer()

@dp.callback_query(lambda call: call.data == 'calories')
async def set_age(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите свой возраст')
    await state.set_state(UserState.age)
    await call.answer()

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
