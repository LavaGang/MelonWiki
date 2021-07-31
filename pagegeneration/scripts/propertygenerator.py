import json
import os
from os import path
import sys
from typing import Union
from utils.argparser import ArgParser, ArgParentWrapper, ArgWrapper
from utils.htmlutils import convert_string_to_work_in_html
from utils.pathutils import convert_to_api_reference_path, convert_to_pagedata_path, join_and_verify, properties_path
from utils.sidebarutils import SidebarManager
from utils.templateutils import replace_thing_with_thing_from_template
from utils.typedatautils import update_json


command_line_args = ["-p", "TestNamespace", "A", "a", "This is a test description", "public static int TestProperty { get; }", "doesn't apply to anything",
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

with open(path.join(properties_path, "propertytemplate.md"), "r", encoding="utf-8") as file_template_file:
    property_template = file_template_file.read();  

def start(cl_args: list[str] = sys.argv):
    try:
        args = [ArgWrapper("-p", ["namespace", "class", "name", "description", "declaration", "applies_to"]),
                ArgWrapper("-pv", ["type", "description"]), 
                ArgWrapper("-e", ["type", "description"], True), 
                ArgWrapper("-ex", ["Example"]),
                ArgWrapper("-re", ["Remarks"])
        ]

        arg_parser = ArgParser(cl_args, args)
    except Exception as err:
        print(err.with_traceback())
        print("Failed to parse arguments\nYou likely just put them in the wrong order:"
        "\npropertygenerator.py -p namespace class property_name property_description property_declaration applies_to [-pv property_value_type property_value_description] [[-e exception_type description ...]] [-ex example_description] [-re remark_description]")
        input("Press any key to exit")
        exit()

    print(f"Page generated successfully at path: " + create_property_page(arg_parser))

def create_property_page(args: ArgParser):
    page = property_template

    base_args = args.parsed_args[0].params
    namespace = base_args["namespace"]
    class_ = base_args["class"]
    name = base_args["name"]
    description = base_args["description"]

    page = page.replace("{class}", class_)
    page = page.replace("{namespace}", namespace)
    page = page.replace("{propertyname}", convert_string_to_work_in_html(name))
    page = page.replace("{propertydescription}", base_args["description"])
    page = page.replace("{propertydeclaration}", base_args["declaration"])
    page = page.replace("{appliesto}", base_args["applies_to"])

    page = replace_thing_with_thing_from_template(args.parsed_args[1], page, "{propertyvalue}", "## Property Value\n{propertyvalue}\n", "")
    page = replace_thing_with_thing_from_template(args.parsed_args[2], page, "{exceptions}", "## Exceptions\n{exceptions}\n", "")
    page = replace_thing_with_thing_from_template(args.parsed_args[3], page, "{examples}", "## Examples\n{examples}\n", "")
    page = replace_thing_with_thing_from_template(args.parsed_args[4], page, "{remarks}", "## Remarks\n{remarks}\n", "")

    type_data_path = convert_to_pagedata_path(namespace, class_)
    page_data_path = path.join(join_and_verify(type_data_path, "properties"), name.lower() + ".md.json")
    full_path = path.join(convert_to_api_reference_path(namespace, class_, "properties"), name.lower() + ".md")

    data = {"names": [name], "descriptions": [description], "links": [f"{namespace.lower()}/{class_.lower()}/properties/{name.lower()}"]}
    update_json(type_data_path, "properties", data)

    with open(full_path, "w", encoding="utf-8") as page_file:
        page_file.write(page)
    with open(page_data_path, "w", encoding="utf-8") as cl_arg_file:
        json.dump(args.args, cl_arg_file, indent=4)

    SidebarManager.add_property(namespace, class_, name)

    return full_path

if __name__ == "__main__":
    if len(command_line_args) == 1:
        start()
    else:
        start(command_line_args)