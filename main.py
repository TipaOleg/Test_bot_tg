from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os
import asyncio

# Чтение API токена
with open('Key', 'r') as file:
    API = file.read().strip()

bot = Bot(token=API)
dp = Dispatcher(storage=MemoryStorage())

# Главная клавиатура
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рассчитать')],
        [KeyboardButton(text='Информация')],
        [KeyboardButton(text='Купить')]
    ],
    resize_keyboard=True
)

# Клавиатура продуктов
product_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product2', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product3', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product4', callback_data='product_buying')],
    ]
)

# Состояния пользователя
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Обработка команды /start
@dp.message(Command(commands=['start']))
async def start(message: Message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью. Выберите действие:', reply_markup=main_keyboard)

# Обработка нажатия кнопки "Рассчитать"
@dp.message(lambda message: message.text == 'Рассчитать')
async def main_menu(message: Message):
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
            [InlineKeyboardButton(text="Формулы расчета", callback_data='formulas')]
        ]
    )
    await message.answer('Выберите опцию', reply_markup=inline_keyboard)

# Обработка нажатия кнопки "Информация"
@dp.message(lambda message: message.text == 'Информация')
async def info(message: Message):
    await message.answer('Это бот для улучшения вашего здоровья.')

# Обработка выбора "Формулы расчета"
@dp.callback_query(lambda call: call.data == 'formulas')
async def get_formulas(call: CallbackQuery):
    await call.message.answer('Формула Миффлина-Сан Жеора: 10*вес + 6.25*рост - 5*возраст + 5')
    await call.answer()

# Начало расчета калорий
@dp.callback_query(lambda call: call.data == 'calories')
async def set_age(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите свой возраст:')
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
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()

    calories = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5
    await message.answer(f'Ваша норма калорий: {calories:.2f} ккал в день.')
    await state.clear()

# Обработка нажатия кнопки "Купить"
@dp.message(lambda message: message.text == 'Купить')
async def get_buying_list(message: Message):
    products = [
        {'name': 'Product1', 'desc': 'описание 1', 'price': 100, 'image': 'images/product1.jpg'},
        {'name': 'Product2', 'desc': 'описание 2', 'price': 200, 'image': 'images/product2.jpg'},
        {'name': 'Product3', 'desc': 'описание 3', 'price': 300, 'image': 'images/product3.jpg'},
        {'name': 'Product4', 'desc': 'описание 4', 'price': 400, 'image': 'images/product4.jpg'}
    ]

    for product in products:
        text = f"Название: {product['name']} | Описание: {product['desc']} | Цена: {product['price']} руб."
        image_path = product['image']

        if not os.path.exists(image_path):
            await message.answer(f"Ошибка: файл {image_path} не найден!")
            continue

        await message.answer_photo(FSInputFile(image_path), caption=text)

    await message.answer("Выберите продукт для покупки:", reply_markup=product_inline_keyboard)

@dp.callback_query(lambda call: call.data == 'product_buying')
async def send_confirm_message(call: CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

# Обработка всех остальных сообщений
@dp.message()
async def all_message(message: Message):
    await message.answer('Введите команду /start, чтобы начать общение.')

# Основная функция
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
