from app.utils.translate import translate


class RoleDefinition:
    def __init__(self):
        self.__carts = []

    def add(self, cart: str):
        self.__carts.append(cart)

    def __clear(self):
        self.__carts = []

    @property
    def get_role(self):
        people = self.__carts.count("people") + (self.__carts.count("people_x2") * 2)
        machine = self.__carts.count("machine") + (self.__carts.count("machine_x2") * 2)
        outcast = self.__carts.count("outcast") + (self.__carts.count("outcast_x2") * 2)
        print(people, machine, outcast)

        if "always_people" in self.__carts:
            return "people"
        elif "always_machine" in self.__carts:
            return "machine"
        elif "always_outcast" in self.__carts:
            return "outcast"
        elif people > machine and people > outcast:
            return "people"
        elif machine > people and machine > outcast:
            return "machine"
        elif outcast > people and outcast > machine:
            return "outcast"
        else:
            return "outcast"

    def get_fidelity_cards(self) -> list[str]:
        """Вернуть список всех карт верности (без роли)."""
        fidelity_keys = {
            "people",
            "people_x2",
            "machine",
            "machine_x2",
            "outcast",
            "outcast_x2",
        }
        return [c for c in self.__carts if c in fidelity_keys]

    def fidelity_text(self) -> str:
        """Вернуть строку со всеми картами верности, переведёнными."""
        cards = self.get_fidelity_cards()
        if not cards:
            return "Нет карт верности"
        return ", ".join(translate(c) for c in cards if translate(c))
