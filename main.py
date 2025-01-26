from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

with open('Key', 'r') as file:
    API = file.read().strip()

bot = Bot(token=API)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command(commands=['start']))
async def start(message: Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

@dp.message()
async def all_message(message: Message):
    await message.answer('Введите команду /start, чтобы начать общение.')

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
