import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

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
        'Здравствуйте! Я Ваш персональный помощник по игре "Судный день"\n'
        "В я могу помочь Вам посчитать ваши карты верности и роли"
        "что бы определить на чьей стороне вы играете и вам не пришлось"
        "считать все это в голове.\n"
        "Вы можете спокойно продолжать наслаждаться игрой",
        reply_markup=kb.main_keyboard(),
    )


async def main():
    for router in routers:
        dp.include_router(router)
    await dp.start_polling(BOT)


if __name__ == "__main__":
    asyncio.run(main())
