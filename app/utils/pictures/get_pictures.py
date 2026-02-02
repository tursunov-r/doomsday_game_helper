import os

base_dir = os.path.dirname(os.path.abspath(__file__))


def get_pictures(command):
    match command:
        case "people":
            return f"{base_dir}/people.png"
        case "machine":
            return f"{base_dir}/machine.png"
        case "outcast":
            return f"{base_dir}/outcast.png"
    return None
