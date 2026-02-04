def mission(command):
    if command == "people":
        return "Убейте всех машин и изгоев. Верните господство людям"
    elif command == "machine":
        return (
            "Найти и уничтожить все человечество. "
            "Изгои могут остаться в живых."
        )
    else:
        return "Убить людей, убить машин, выжить"
