class RoleDefinition:
    def __init__(self):
        self.__carts = []

    def add(self, cart):
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
