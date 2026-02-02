from aiogram.fsm.state import State, StatesGroup


class RoleState(StatesGroup):
    role_cart = State()
    fidelity_1 = State()
    fidelity_2 = State()
    return_role = State()
    program_fidelity = State()
