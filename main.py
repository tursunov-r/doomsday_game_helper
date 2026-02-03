import asyncio
import types

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from app.configs.config import BOT_TOKEN
from app.keyboards import role_buttons_builder as kb
from app.hendlers.hendlers import router as role_router

BOT = Bot(token=BOT_TOKEN)
dp = Dispatcher()
routers = [
    role_router,
]


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        'Здравствуйте! Я Ваш персональный помощник по игре "Судный день"\n',
        reply_markup=kb.main_keyboard(),
    )


async def main():
    for router in routers:
        dp.include_router(router)
    await dp.start_polling(BOT)


if __name__ == "__main__":
    asyncio.run(main())
