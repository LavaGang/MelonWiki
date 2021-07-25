from os import path
from argparser import ArgWrapper
from constants import common_path

def create_thing_from_template(data: ArgWrapper) -> str:
    thing_string = ""
    if isinstance(data.params, list):
        for param in data.params:
            thing_string += create_thing_from_template_single(param, data.template_keys)
    else:
        thing_string += create_thing_from_template_single(param, data.template_keys)

    return thing_string

def create_thing_from_template_single(data: dict, data_keys: list[str]) -> str:
    thing_string = ""
    if len(data) == 2:
        with open(path.join(common_path, "thingtemplate.md"), "r", encoding="utf-8") as template_file:
            thing_string = template_file.read()
        thing_string = thing_string.replace("{header}", data[data_keys[0]])
        thing_string = thing_string.replace("{description}", data[data_keys[1]])
    elif len(data) == 3:
        with open(path.join(common_path, "thingwith2template.md"), "r", encoding="utf-8") as template_file:
            thing_string = template_file.read()
        thing_string = thing_string.replace("{header}", data[data_keys[0]])
        thing_string = thing_string.replace("{header2}", data[data_keys[1]])
        thing_string = thing_string.replace("{description}", data[data_keys[2]])
    else:
        raise Exception("Template data length does not match any template")
    return thing_string
