def translate(data: str) -> str:
    translate = {
        "people": "Человек",
        "people_x2": "Человек x2",
        "machine": "Машина",
        "machine_x2": "Машина x2",
        "outcast": "Изгой",
        "outcast_x2": "Изгой x2",
        "always_people": "Всегда человек",
        "always_machine": "Всегда машина",
        "always_outcast": "Всегда изгой",
    }

    return translate[data] if data in translate.keys() else None
