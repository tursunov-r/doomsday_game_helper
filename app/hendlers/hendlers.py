from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from app.keyboards import role_buttons_builder as kb
from app.states.role_state import RoleState
from app.utils.utuls import RoleDefinition
from app.utils.translate import translate
from app.utils.pictures.get_pictures import get_pictures
from app.utils.bot_delete_message import bot_delete_message

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

    # достаём все id сообщений, которые бот отправлял ранее
    data = await state.get_data()
    bot_messages = data.get("bot_messages", [])

    # удаляем их
    for msg_id in bot_messages:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
        except Exception as e:
            print(f"Не удалось удалить сообщение {msg_id}: {e}")

    # очищаем список
    await state.update_data(bot_messages=[])

    # отправляем новое сообщение
    sent = await message.answer(
        "Укажите свою карту роли", reply_markup=kb.role_cart_keyboard()
    )

    # сохраняем id нового сообщения
    await state.update_data(bot_messages=[sent.message_id])
    await state.set_state(RoleState.role_cart)
    await state.clear()


@router.callback_query(RoleState.role_cart)
async def set_role(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer(f"")
    sent = await callback.message.answer(
        text=f"Укажите карту верности:",
        reply_markup=kb.fidelity_cart_keyboard(),
    )
    await state.update_data(role_cart=callback.data)
    await state.set_state(RoleState.fidelity_1)
    await bot_delete_message(state, sent)


@router.callback_query(RoleState.fidelity_1, F.data.in_(VALID_FIDELITY))
async def set_fidelity(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.delete()
    sent = await callback.message.answer(
        f"Укажите вторую карту верности",
        reply_markup=kb.fidelity_cart_keyboard(),
    )
    await state.update_data(fidelity_cart_1=callback.data)
    await state.set_state(RoleState.fidelity_2)
    await bot_delete_message(state, sent)


@router.callback_query(RoleState.fidelity_2, F.data.in_(VALID_FIDELITY))
async def set_fidelity(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer("")
    await state.update_data(fidelity_cart_2=callback.data)
    await state.set_state(RoleState.return_role)
    data = await state.get_data()
    role = RoleDefinition()
    role.add_cart(data["role_cart"])
    role.add_cart(data["fidelity_cart_1"])
    role.add_cart(data["fidelity_cart_2"])

    programs = data.get("program_fidelity", [])
    if programs:
        for p in programs:  # добавляем все карты программы в RoleDefinition
            role.add_cart(p)
        programs_text = "Программы верности: " + ", ".join(
            translate(p) for p in programs if translate(p)
        )
    else:
        programs_text = ""

    photo = FSInputFile(get_pictures(role.get_role))
    sent = await callback.message.answer_photo(
        photo=photo,
        caption=(f"{role.get_message(
                role=data["role_cart"],
                fidelity_1=data["fidelity_cart_1"],
                fidelity_2=data["fidelity_cart_2"],
                program=programs_text,
            )}"),
        reply_markup=kb.in_play_replace_role(),
    )
    await bot_delete_message(state, sent)


@router.callback_query(F.data == "change_fidelity")
async def change_fidelity(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.delete()
    sent = await callback.message.answer(
        "Укажите первую карту верности", reply_markup=kb.fidelity_cart_keyboard()
    )

    await state.set_state(RoleState.fidelity_1)
    await bot_delete_message(state, sent)


@router.callback_query(F.data == "program_fidelity")
async def program_fidelity(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.delete()
    sent = await callback.message.answer(
        "Укажите карту верности в программе", reply_markup=kb.fidelity_cart_keyboard()
    )
    # переводим в новое состояние выбора карты программы
    await state.set_state(RoleState.program_fidelity)
    await bot_delete_message(state, sent)


@router.callback_query(RoleState.program_fidelity, F.data.in_(VALID_FIDELITY))
async def add_program_fidelity(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("")
    data = await state.get_data()
    programs = data.get("program_fidelity", [])
    if not isinstance(programs, list):
        programs = []
    programs.append(callback.data)
    await state.update_data(program_fidelity=programs)

    # формируем роль заново
    role = RoleDefinition()
    role.add_cart(data["role_cart"])
    role.add_cart(data["fidelity_cart_1"])
    role.add_cart(data["fidelity_cart_2"])
    for p in programs:
        role.add_cart(p)

    programs_text = "Программы верности: " + ", ".join(
        translate(p) for p in programs if translate(p)
    )

    photo = FSInputFile(get_pictures(role.get_role))
    await callback.message.delete()
    sent = await callback.message.answer_photo(
        photo=photo,
        caption=(f"{role.get_message(
                role=data["role_cart"],
                fidelity_1=data["fidelity_cart_1"],
                fidelity_2=data["fidelity_cart_2"],
                program=programs_text,
            )}"),
        reply_markup=kb.if_set_fidelity(),
    )

    await state.set_state(RoleState.return_role)
    await bot_delete_message(state, sent)


@router.callback_query(F.data == "program_fidelity_remove")
async def remove_fidelity_program(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer("")
    await state.update_data(program_fidelity=[])

    data = await state.get_data()
    role = RoleDefinition()
    role.add_cart(data["role_cart"])
    role.add_cart(data["fidelity_cart_1"])
    role.add_cart(data["fidelity_cart_2"])

    # пересобираем роль без программ
    programs_text = "Программы верности: отсутствуют"

    photo = FSInputFile(get_pictures(role.get_role))
    sent = await callback.message.answer_photo(
        photo=photo,
        caption=(f"{role.get_message(
                role=data["role_cart"],
                fidelity_1=data["fidelity_cart_1"],
                fidelity_2=data["fidelity_cart_2"],
                program=programs_text,
            )}"),
        reply_markup=kb.in_play_replace_role(),
    )

    await state.set_state(RoleState.return_role)
    await bot_delete_message(state, sent)
