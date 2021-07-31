from os import path
from utils.argparser import ArgWrapper
from utils.htmlutils import convert_string_to_work_in_html, convert_string_to_work_in_id
from utils.pathutils import common_path

with open(path.join(common_path, "thingtemplate.md"), "r", encoding="utf-8") as template_file:
    thing_template = template_file.read()

with open(path.join(common_path, "thingwith2template.md"), "r", encoding="utf-8") as template_file:
    thing2_template = template_file.read()

with open(path.join(common_path, "table.md"), "r", encoding="utf-8") as table_file:
    table_template = table_file.read()

with open(path.join(common_path, "tablerow.md"), "r", encoding="utf-8") as table_row_file:
    table_row_template = table_row_file.read()

with open(path.join(common_path, "overloadtemplate.md"), "r", encoding="utf-8") as file_template_file:
    overload_template = file_template_file.read();  

def create_thing_from_template(data: ArgWrapper) -> str:
    thing_string = ""
    if not data.exists:
        return ""

    if isinstance(data.params, list):
        for param in data.params:
            thing_string += create_thing_from_template_single(param, data.template_keys) + "\n"
    else:
        thing_string += create_thing_from_template_single(data.params, data.template_keys) + "\n"

    return thing_string

def create_thing_from_template_single(data: dict, data_keys: list[str]) -> str:
    thing_string = ""
    if len(data) == 1:
        thing_string = data[data_keys[0]]
    elif len(data) == 2:
        thing_string = thing_template
        thing_string = thing_string.replace("{header}", data[data_keys[0]])
        thing_string = thing_string.replace("{description}", data[data_keys[1]])
    elif len(data) == 3:
        thing_string = thing2_template
        thing_string = thing_string.replace("{header}", data[data_keys[0]])
        thing_string = thing_string.replace("{header2}", data[data_keys[1]])
        thing_string = thing_string.replace("{description}", data[data_keys[2]])
    else:
        raise Exception("Template data length does not match any template")
    return thing_string

def replace_thing(data: ArgWrapper, orig: str, rs: str, rms: str, rf: str, rmf: str) -> str:
    if data.exists:
        orig = orig.replace(rs, rms)
    else:
        orig = orig.replace(rf, rmf)
    return orig

def replace_thing_with_thing_from_template(data: ArgWrapper, orig: str, rs: str, rf: str, rmf: str) -> str: #  naming things is hard ok
    return replace_thing(data, orig, rs, create_thing_from_template(data), rf, rmf)

def create_overload_table(args: ArgWrapper, page: str, global_data: dict, link_before_id: str) -> str:
    template = table_row_template
    table_rows = []

    overloads = []
    for data in args.params:
        overloads.append(create_method_overload(data))
        table_row = template
        table_row = table_row.replace("{linkbeforeid}", link_before_id)
        table_row = table_row.replace("{namecleaned}", convert_string_to_work_in_id(data["name"]))
        table_row = table_row.replace("{name}", convert_string_to_work_in_html(data["name"]))
        table_row = table_row.replace("{description}", data["description"])
        table_rows.append(table_row)

        global_data["names"].append(convert_string_to_work_in_html(data["name"]))
        global_data["descriptions"].append(data["description"])
        global_data["links"].append(link_before_id)
    
    table = table_template
    table = table.replace("{rows}", "\n".join(table_rows))
    page = page.replace("{overloadtable}", table)

    page = page.replace("{overloads}", "\n".join(overloads))
    return page

def create_method_overload(data: dict) -> str:
    template = overload_template
    
    template = template.replace("{name}", convert_string_to_work_in_html(data["name"]))
    template = template.replace("{description}", data["description"])
    template = template.replace("{declaration}", data["declaration"])
    template = template.replace("{appliesto}", data["applies_to"])

    template = replace_overload_things(data, template)
    return template

def replace_overload_things(data: dict, page: str) -> str:
    if "-r" in data:
        page = replace_thing_with_thing_from_template(data["-r"], page, "{returns}", "## Returns\n{returns}\n", "")
    else:
        page = page.replace("## Returns\n{returns}\n", "")
    page = replace_thing_with_thing_from_template(data["-tp"], page, "{typeparameters}", "## Type Parameters\n{typeparameters}\n", "")
    page = replace_thing_with_thing_from_template(data["-p"], page, "{parameters}", "## Parameters\n{parameters}\n", "")
    page = replace_thing_with_thing_from_template(data["-e"], page, "{exceptions}", "## Exceptions\n{exceptions}\n", "")
    page = replace_thing_with_thing_from_template(data["-ex"], page, "{examples}", "## Examples\n{examples}\n", "")
    page = replace_thing_with_thing_from_template(data["-re"], page, "{remarks}", "## Remarks\n{remarks}\n", "")
    return page