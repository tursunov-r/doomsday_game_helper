from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def main_keyboard():
    buttons = ("Определить мою роль",)

    keyboard = ReplyKeyboardBuilder()
    for button in buttons:
        keyboard.add(KeyboardButton(text=button))
    return keyboard.adjust(1).as_markup(resize_keyboard=True)


def role_cart_keyboard():
    buttons = (
        ("👨‍🎤человек", "people"),
        ("всегда человек", "always_people"),
        ("🦾машины", "machine"),
        ("всегда машина", "always_machine"),
        ("🐺изгой", "outcast"),
        ("всегда изгой", "always_outcast"),
    )
    keyboard = InlineKeyboardBuilder()
    for button in buttons:
        keyboard.add(
            InlineKeyboardButton(text=button[0], callback_data=button[1])
        )
    return keyboard.adjust(2).as_markup()


def fidelity_cart_keyboard():
    buttons = (
        ("👨‍🎤человек", "people"),
        ("🦾машины", "machine"),
        ("🐺изгои", "outcast"),
        ("👨‍🎤человек x2", "people_x2"),
        ("🦾машины x2", "machine_x2"),
        ("🐺изгои x2", "outcast_x2"),
    )
    keyboard = InlineKeyboardBuilder()
    for button in buttons:
        keyboard.add(
            InlineKeyboardButton(text=button[0], callback_data=button[1])
        )
    return keyboard.adjust(3).as_markup()


def in_play_replace_role():
    buttons = (
        ("Смена верности", "change_fidelity"),
        ("Программа верности", "program_fidelity"),
    )
    keyboard = InlineKeyboardBuilder()
    for button in buttons:
        keyboard.add(
            InlineKeyboardButton(text=button[0], callback_data=button[1])
        )
    return keyboard.adjust(1).as_markup()


def if_set_fidelity():
    buttons = (
        ("Смена верности", "change_fidelity"),
        ("Программа верности", "program_fidelity"),
        ("Сбросить программы", "program_fidelity_remove"),
    )
    keyboard = InlineKeyboardBuilder()
    for button in buttons:
        keyboard.add(
            InlineKeyboardButton(text=button[0], callback_data=button[1])
        )
    return keyboard.adjust(1).as_markup()
