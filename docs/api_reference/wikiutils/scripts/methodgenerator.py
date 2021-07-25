import os
from os import path
import sys
from typing import Union
from argparser import ArgParser, ArgWrapper
from commontemplateutils import create_thing_from_template
from constants import api_reference_path, common_path, methods_path

command_line_args = ["-m", "Test", "TestMethod", "This is a test description", "public static int TestMethod<T, T1>(string thingy, object thingy2)", "doesn't apply to anything",
                     "-r", "`int`", "some test thingy that returns int",
                     "-tp", 
                        "T", "type param 1",
                        "T1", "type param 2, i know its confusing",
                     "-p",
                        "string", "thingy", "this is a string parameter, \"i dunno what to say\"",
                        "object", "thing2", "this is an object parameter. yes this naming is confused",
                     "-e",
                        "ArgumentNullException", "throws then either of the arguments are null",
                        "ArgumentException", "throws when the method feels like it"
                    ]

def start(cl_args: list[str] = sys.argv):
    try:
        args = [ArgWrapper("-m", ["class", "name", "description", "declaration", "applies_to"]), 
                ArgWrapper("-r", ["type", "description"]), 
                ArgWrapper("-tp", ["name", "description"], True),
                ArgWrapper("-p", ["type", "name", "description"], True),
                ArgWrapper("-e", ["type", "description"], True)]

        arg_parser = ArgParser(cl_args, args)
    except:
        print("Failed to parse arguments\nYou likely just put them in the wrong order:"
        "\nmethodgenerator.py -m method_dir method_name method_description method_declaration applies_to [-r return_type return_description] [-tp [type_parameter_name description ...]] [-p [parameter_type parameter_name description ...]] [-e [exception_type description ...]]")
        input("Press any key to exit")

    print(f"Page generated successfully at path: " + create_method_page(arg_parser))
        

def create_method_page(args: ArgParser):
    page = ""
    with open(path.join(methods_path, "methodtemplate.md"), "r", encoding="utf-8") as file_template_file:
        page = file_template_file.read();    

    base_method_args = args.parsed_args[0].params
    page = page.replace("{class}", base_method_args["class"])
    page = page.replace("{methodname}", base_method_args["name"])
    page = page.replace("{methoddescription}", base_method_args["description"])
    page = page.replace("{methoddeclaration}", base_method_args["declaration"])
    page = page.replace("{appliesto}", base_method_args["applies_to"])

    if args.parsed_args[1].exists:
        return_args = args.parsed_args[1].params
        page = page.replace("{returntype}", return_args["type"])
        page = page.replace("{returndescription}", return_args["description"])
    else:
        page = page.replace("## Returns\n{returntype}\n{returndescription}\n\n", "")

    if args.parsed_args[2].exists:
        page = page.replace("{typeparameters}", create_thing_from_template(args.parsed_args[2]))
    else:
        page = page.replace("## Type Parameters\n{typeparameters}\n", "")

    if args.parsed_args[3].exists:
        page = page.replace("{parameters}", create_thing_from_template(args.parsed_args[3]))
    else:
        page = page.replace("## Parameters\n{parameters}\n", "")

    if args.parsed_args[4].exists:
        page = page.replace("{exceptions}", create_thing_from_template(args.parsed_args[4]))
    else:
        page = page.replace("## Exceptions\n{exceptions}\n", "")

    final_path = path.join(api_reference_path, base_method_args["class"].lower(), "methods", base_method_args["name"].lower() + ".md")
    with open (final_path, "w", encoding="utf-8") as page_file:
        page_file.write(page)
    return final_path

if __name__ == "__main__":
    if len(command_line_args) == 1:
        start()
    else:
        start(command_line_args)

