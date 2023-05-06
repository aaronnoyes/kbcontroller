import configparser


def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def get_modifiers(config):
    modifiers = {}

    modifiers["shift"] = config.get("modifiers", "shift")
    modifiers["ctrl"] = config.get("modifiers", "ctrl")
    modifiers["alt"] = config.get("modifiers", "alt")
    modifiers["mode"] = config.get("modifiers", "mode")

    return modifiers


def main():
    print("config.py")


if __name__ == "__main__":
    main()
