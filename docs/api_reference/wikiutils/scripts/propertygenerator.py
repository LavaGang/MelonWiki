import json
import os
from os import path
import sys
from typing import Union
from argparser import ArgParser, ArgParentWrapper, ArgWrapper
from constants import api_reference_path, common_path, properties_path
from globaldatautils import update_json
from htmlutils import convert_string_to_work_in_html, convert_string_to_work_in_link
from sidebarutils import SidebarManager
from templateutils import replace_thing_with_thing_from_template


command_line_args = ["-p", "Test", "aaaaa", "This is a test description", "public static int TestProperty { get; }", "doesn't apply to anything",
                     "-pv", "`int`", "some test thingy that returns int",
                     "-e", 
                        "`shootmeexception`", "asjdfa;lksjd;lakjdf",
                     "-e",
                        "nullrefexception", "lol what no my code works perfecrtly",
                     "-ex",
                         "This is an example in usage, a very good one",
                     "-re",
                         "this is a remark yes yes"
]


def start(cl_args: list[str] = sys.argv):
    try:
        args = [ArgWrapper("-p", ["class", "name", "description", "declaration", "applies_to"]),
                ArgWrapper("-pv", ["type", "description"]), 
                ArgWrapper("-e", ["type", "description"], True), 
                ArgWrapper("-ex", ["Example"]),
                ArgWrapper("-re", ["Remarks"])
        ]

        arg_parser = ArgParser(cl_args, args)
    except Exception as err:
        print(err.with_traceback())
        print("Failed to parse arguments\nYou likely just put them in the wrong order:"
        "\npropertygenerator.py -p class property_name property_description property_declaration applies_to [-pv property_value_type property_value_description] [[-e exception_type description ...]] [-ex example_description] [-re remark_description]")
        input("Press any key to exit")
        exit()

    print(f"Page generated successfully at path: " + create_property_page(arg_parser))

def create_property_page(args: ArgParser):
    page = ""
    with open(path.join(properties_path, "propertytemplate.md"), "r", encoding="utf-8") as file_template_file:
        page = file_template_file.read();  

    base_method_args = args.parsed_args[0].params
    page = page.replace("{class}", base_method_args["class"])
    page = page.replace("{propertyname}", convert_string_to_work_in_html(base_method_args["name"]))
    page = page.replace("{propertydescription}", base_method_args["description"])
    page = page.replace("{propertydeclaration}", base_method_args["declaration"])
    page = page.replace("{appliesto}", base_method_args["applies_to"])

    page = replace_thing_with_thing_from_template(args.parsed_args[1], page, "{propertyvalue}", "## Property Value\n{propertyvalue}\n", "")
    page = replace_thing_with_thing_from_template(args.parsed_args[2], page, "{exceptions}", "## Exceptions\n{exceptions}\n", "")
    page = replace_thing_with_thing_from_template(args.parsed_args[3], page, "{examples}", "## Examples\n{examples}\n", "")
    page = replace_thing_with_thing_from_template(args.parsed_args[4], page, "{remarks}", "## Remarks\n{remarks}\n", "")

    final_path_folder = path.join(api_reference_path, base_method_args["class"].lower(), "properties")

    data = {"names": [], "descriptions": []}
    data["names"].append(args.parsed_args[0].params["name"])
    data["descriptions"].append(args.parsed_args[0].params["description"])
    update_json(final_path_folder, "properties", data)

    final_path = path.join(final_path_folder, base_method_args["name"].lower() + ".md")
    with open(final_path, "w", encoding="utf-8") as page_file:
        page_file.write(page)
    with open(final_path + ".json", "w", encoding="utf-8") as cl_arg_file:
        json.dump(args.args, cl_arg_file)

    SidebarManager.add_property(base_method_args["class"], base_method_args["name"])

    return final_path

if __name__ == "__main__":
    if len(command_line_args) == 1:
        start()
    else:
        start(command_line_args)