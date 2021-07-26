import json
import os
from os import path
import sys
from typing import Union
from utils.argparser import ArgParser, ArgParentWrapper, ArgWrapper
from utils.htmlutils import convert_string_to_work_in_html, convert_string_to_work_in_link
from utils.pathutils import convert_to_api_reference_path, convert_to_pagedata_path, fields_path, join_and_verify
from utils.sidebarutils import SidebarManager
from utils.templateutils import replace_thing_with_thing_from_template
from utils.typedatautils import update_json


command_line_args = ["-f", "Test", "TestField", "This is a test description", "public static const int TestConstant = 1;", "doesn't apply to anything",
                     "-fv", "`int`",
                     "-ex",
                         "This is an example in usage, a very good one",
                     "-re",
                         "this is a remark yes yes"
]

with open(path.join(fields_path, "fieldtemplate.md"), "r", encoding="utf-8") as file_template_file:
    field_template = file_template_file.read(); 

def start(cl_args: list[str] = sys.argv):
    try:
        args = [ArgWrapper("-f", ["class", "name", "description", "declaration", "applies_to"]),
                ArgWrapper("-fv", ["type"]), 
                ArgWrapper("-ex", ["Example"]),
                ArgWrapper("-re", ["Remarks"])
        ]

        arg_parser = ArgParser(cl_args, args)
    except Exception as err:
        print(err.with_traceback())
        print("Failed to parse arguments\nYou likely just put them in the wrong order:"
        "\nfieldgenerator.py -f class field_name field_description field_declaration applies_to [-fv field_type] [-ex example_description] [-re remark_description]")
        input("Press any key to exit")
        exit()

    print(f"Page generated successfully at path: " + create_field_page(arg_parser))

def create_field_page(args: ArgParser):
    page = field_template

    base_method_args = args.parsed_args[0].params
    class_ = base_method_args["class"]
    name = base_method_args["name"]
    description = base_method_args["description"]

    page = page.replace("{class}", class_)
    page = page.replace("{fieldname}", convert_string_to_work_in_html(name))
    page = page.replace("{fielddescription}", description)
    page = page.replace("{fielddeclaration}", base_method_args["declaration"])
    page = page.replace("{appliesto}", base_method_args["applies_to"])

    page = replace_thing_with_thing_from_template(args.parsed_args[1], page, "{fieldvalue}", "## Field Value\n{fieldvalue}\n", "")
    page = replace_thing_with_thing_from_template(args.parsed_args[2], page, "{examples}", "## Examples\n{examples}\n", "")
    page = replace_thing_with_thing_from_template(args.parsed_args[3], page, "{remarks}", "## Remarks\n{remarks}\n", "")

    type_data_path = convert_to_pagedata_path(class_)
    page_data_path = path.join(join_and_verify(type_data_path, "fields"), name.lower() + ".md.json")
    full_path = path.join(convert_to_api_reference_path(class_, "fields"), name.lower() + ".md")

    data = {"names": [], "descriptions": []}
    data["names"].append(name)
    data["descriptions"].append(description)
    update_json(type_data_path, "fields", data)

    with open(full_path, "w", encoding="utf-8") as page_file:
        page_file.write(page)
    with open(page_data_path, "w", encoding="utf-8") as cl_arg_file:
        json.dump(args.args, cl_arg_file)

    SidebarManager.add_field(class_, name)

    return full_path

if __name__ == "__main__":
    if len(command_line_args) == 1:
        start()
    else:
        start(command_line_args)