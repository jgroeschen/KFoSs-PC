import configparser


def read_config(section: str,
                key: str) -> str:
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config.get(section, key)


def write_config(section: str,
                 key: str,
                 value: str) -> None:
    config = configparser.ConfigParser()
    config.read('config.ini')
    if config.has_section(section):
        pass
    else:
        config.add_section(section)
    config.set(section, key, value)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def read_list(section: str,
              key: str) -> list:
    config = configparser.ConfigParser()
    config.read('config.ini')
    list = config.get(section, key)
    list = list[1:-1]
    list = list.split(',')
    list = [e.strip() for e in list]
    list = [e[1:-1] for e in list]
    return list