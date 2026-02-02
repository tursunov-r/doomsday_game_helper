from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, message

from app.keyboards import role_buttons_builder as kb
from app.states.role_state import RoleState
from app.utils.utuls import RoleDefinition
from app.utils.translate import translate
from app.utils.pictures.get_pictures import get_pictures
from app.utils.mission import mission

router = Router()
VALID_FIDELITY = {
    "people",
    "machine",
    "outcast",
    "people_x2",
    "machine_x2",
    "outcast_x2",
}


@router.message(F.text.lower() == "определить мою роль")
async def set_role_cart(message: types.Message, state: FSMContext):
    await message.delete()
    sent = await message.answer(
        "Укажите свою карту роли", reply_markup=kb.role_cart_keyboard()
    )
    await state.update_data(bot_message_id=sent.message_id)
    await state.set_state(RoleState.role_cart)


@router.callback_query(RoleState.role_cart)
async def set_role(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(f"")
    await callback.bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=f"Укажите карту верности:",
        reply_markup=kb.fidelity_cart_keyboard(),
    )
    await state.update_data(role_cart=callback.data)
    await state.set_state(RoleState.fidelity_1)


@router.callback_query(RoleState.fidelity_1, F.data.in_(VALID_FIDELITY))
async def set_fidelity(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.delete()
    await callback.message.answer(
        f"Укажите вторую карту верности",
        reply_markup=kb.fidelity_cart_keyboard(),
    )
    await state.update_data(fidelity_cart_1=callback.data)
    await state.set_state(RoleState.fidelity_2)


@router.callback_query(RoleState.fidelity_2, F.data.in_(VALID_FIDELITY))
async def set_fidelity(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.update_data(fidelity_cart_2=callback.data)
    await state.set_state(RoleState.return_role)
    data = await state.get_data()
    role = RoleDefinition()
    role.add(data["role_cart"])
    role.add(data["fidelity_cart_1"])
    role.add(data["fidelity_cart_2"])
    program_fidelity = data.get("program_fidelity")
    if program_fidelity and program_fidelity in VALID_FIDELITY:
        role.add(program_fidelity)
    photo = FSInputFile(get_pictures(role.get_role))
    await callback.message.answer_photo(
        photo=photo,
        caption=(
            f"Ваши карты:\n"
            f"Роль: {translate(data['role_cart'])}\n"
            f"Верность: 1 - {translate(data['fidelity_cart_1'])}, "
            f"2 - {translate(data['fidelity_cart_2'])}\n"
            f"Команда: {translate(role.get_role)}\n"
            f"Цель: {mission(role.get_role)}"
        ),
        reply_markup=kb.in_play_replace_role(),
    )


@router.callback_query(F.data == "change_fidelity")
async def change_fidelity(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.delete()
    await callback.message.answer(
        "Укажите первую карту верности", reply_markup=kb.fidelity_cart_keyboard()
    )

    await state.set_state(RoleState.fidelity_1)


@router.callback_query(F.data == "program_fidelity")
async def program_fidelity(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.delete()
    await callback.message.answer(
        f"Укажите карту верности в программе", reply_markup=kb.fidelity_cart_keyboard()
    )
    await state.update_data(program_fidelity=callback.data)
    await state.set_state(RoleState.fidelity_2)
