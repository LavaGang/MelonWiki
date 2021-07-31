import json
import os
from os import path
import sys
from typing import Union
from utils.argparser import ArgParser, ArgParentWrapper, ArgWrapper
from utils.htmlutils import convert_string_to_work_in_html
from utils.pathutils import convert_to_api_reference_path, convert_to_pagedata_path, join_and_verify, operators_path
from utils.sidebarutils import SidebarManager
from utils.templateutils import replace_thing_with_thing_from_template
from utils.typedatautils import update_json


command_line_args = ["-op", "TestNamespace", "Test", "TestOperator", "TestOperator(string, object)", "This is a test description", "public static int TestOperator(string thingy, object thingy2)", "doesn't apply to anything",
                     "-r", "`int`", "some test thingy that returns int",
                     "-p",
                         "string", "thingy", "this is a string parameter, \"i dunno what to say\"",
                     "-p",
                         "object", "thing2", "this is an object parameter. yes this naming is confused",
                     "-e",
                         "ArgumentNullException", "throws then either of the arguments are null",
                     "-e",
                         "ArgumentException", "throws when the operator feels like it"
]

with open(path.join(operators_path, "operatortemplate.md"), "r", encoding="utf-8") as file_template_file:
    operator_template = file_template_file.read();   

def start(cl_args: list[str] = sys.argv):
    try:
        args = [ArgWrapper("-op", ["namespace", "class", "name", "name_with_params", "description", "declaration", "applies_to"]),
                ArgWrapper("-r", ["type", "description"]), 
                ArgWrapper("-p", ["type", "name", "description"], True),
                ArgWrapper("-e", ["type", "description"], True),
                ArgWrapper("-ex", ["Example"]),
                ArgWrapper("-re", ["Remarks"])
        ]

        arg_parser = ArgParser(cl_args, args)
    except Exception as err:
        print(err.with_traceback())
        print("Failed to parse arguments\nYou likely just put them in the wrong order:"
        "\noperatorgenerator.py -op namespace class operator_name operator_description operator_declaration applies_to [-r return_type return_description] [[-p parameter_type parameter_name description ...]] [[-e exception_type description ...]] [-ex example_description] [-re remark_description]")
        input("Press any key to exit")
        exit()

    print(f"Page generated successfully at path: " + create_operator_page(arg_parser))

def create_operator_page(args: ArgParser):
    page = operator_template 

    base_args = args.parsed_args[0].params
    namespace = base_args["namespace"]
    class_ = base_args["class"]
    name = base_args["name"]
    description = base_args["description"]

    page = page.replace("{class}", class_)
    page = page.replace("{namespace}", namespace)
    page = page.replace("{operatorname}", convert_string_to_work_in_html(base_args["name_with_params"]))
    page = page.replace("{operatordescription}", description)

    type_data_path = convert_to_pagedata_path(namespace, class_)
    page_data_path = path.join(join_and_verify(type_data_path, "operators"), name.lower() + ".md.json")
    full_path = path.join(convert_to_api_reference_path(namespace, class_, "operators"), name.lower() + ".md")

    page = page.replace("{operatordeclaration}", base_args["declaration"])
    page = page.replace("{appliesto}", base_args["applies_to"])

    page = replace_thing_with_thing_from_template(args.parsed_args[1], page, "{returns}", "## Returns\n{returns}\n", "")
    page = replace_thing_with_thing_from_template(args.parsed_args[2], page, "{parameters}", "## Parameters\n{parameters}\n", "")
    page = replace_thing_with_thing_from_template(args.parsed_args[3], page, "{exceptions}", "## Exceptions\n{exceptions}\n", "")
    page = replace_thing_with_thing_from_template(args.parsed_args[4], page, "{examples}", "## Examples\n{examples}\n", "")
    page = replace_thing_with_thing_from_template(args.parsed_args[5], page, "{remarks}", "## Remarks\n{remarks}\n", "")

    data = {"names": [name], "descriptions": [description], "links": [f"{namespace.lower()}/{class_.lower()}/operators/{name.lower()}"]}
    update_json(type_data_path, "operators", data)
    
    with open(full_path, "w", encoding="utf-8") as page_file:
        page_file.write(page)
    with open(page_data_path, "w", encoding="utf-8") as cl_arg_file:
        json.dump(args.args, cl_arg_file, indent=4)

    SidebarManager.add_operator(namespace, class_, name)
    
    return full_path

if __name__ == "__main__":
    if len(command_line_args) == 1:
        start()
    else:
        start(command_line_args)

