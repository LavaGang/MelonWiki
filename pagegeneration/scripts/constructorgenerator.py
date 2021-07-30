import json
import os
from os import path
import sys
from typing import Union
from utils.argparser import ArgParser, ArgParentWrapper, ArgWrapper
from utils.htmlutils import convert_string_to_work_in_html, convert_string_to_work_in_id
from utils.pathutils import convert_to_api_reference_path, convert_to_pagedata_path, join_and_verify, constructors_path
from utils.sidebarutils import SidebarManager
from utils.templateutils import create_overload_table, replace_overload_things, replace_thing_with_thing_from_template
from utils.typedatautils import update_json


# Constructor with no overloads
command_line_args = ["-cg", "TestNamespace", "Test", "This is a test description", 
                     "-c", "public static Test<T, T1>(string thingy, object thingy2)", "doesn't apply to anything",
                        "-tp", 
                            "T", "type param 1",
                        "-tp",
                            "T1", "type paramasfasdfasdfasdfas 2, i know its confusing",
                        "-p",
                            "string", "thingy", "this is a string parameter, \"i dunno what to say\"",
                        "-p",
                            "object", "thing2", "this is an object parameter. yes this naming is confused",
                        "-e",
                            "ArgumentNullException", "throws then either of the arguments are null",
                        "-e",
                            "ArgumentException", "throws when the constructor feels like it"
]

# Constructor with overloads
command_line_args = ["-cg", "TestNamespace", "Test", "This is a test description", 
                     "-co", "Test<T, T1>(string, object)", "this is a test description of the first overload", "public static int Test<T, T1>(string thingy, object thingy2)", "doesn't apply to anything",
                        "-tp", 
                            "`T`", "type param 1",
                        "-tp",
                            "`T1`", "type paramasfasdfasdfasdfas 2, i know its confusing",
                        "-p",
                            "`string`", "thingy", "this is a string parameter, \"i dunno what to say\"",
                        "-p",
                            "`object`", "thing2", "this is an object parameter. yes this naming is confused",
                        "-e",
                            "ArgumentNullException", "throws then either of the arguments are null",
                        "-e",
                            "ArgumentException", "throws when the constructor feels like it",
                        "-ex",
                            "This is an example in usage, a very good one",
                        "-re",
                            "this is a remark yes yes",
                     "-co", "Test<T>(string, object)", "This is a test description of the second overload", "public static int Test<T>(string thingy, object thingy2)", "doesn't apply to anything",
                        "-tp", 
                            "`T`", "type param 1",
                        "-p",
                            "`string`", "thingy", "this is a string parameter, \"i dunno what to say\"",
                        "-p",
                            "`object`", "thing2", "this is an object parameter. yes this naming is confused",
                        "-e",
                            "ArgumentNullException", "throws then either of the arguments are null",
                        "-e",
                            "ArgumentException", "throws when the constructor feels like it",
                        "-re",
                            "this is a remark yes yes",
]

with open(path.join(constructors_path, "constructortemplate.md"), "r", encoding="utf-8") as file_template_file:
    constructor_template = file_template_file.read();   

with open(path.join(constructors_path, "constructortemplatewithoverload.md"), "r", encoding="utf-8") as file_template_file:
    constructor_with_overload_template = file_template_file.read();  

def start(cl_args: list[str] = sys.argv):
    try:
        args = [ArgWrapper("-cg", ["namespace", "class", "description"]),
                ArgParentWrapper("-c", ["declaration", "applies_to", 
                                        ArgWrapper("-tp", ["name", "description"], True),
                                        ArgWrapper("-p", ["type", "name", "description"], True),
                                        ArgWrapper("-e", ["type", "description"], True),
                                        ArgWrapper("-ex", ["Example"]),
                                        ArgWrapper("-re", ["Remarks"])]),
                ArgParentWrapper("-co", ["name", "description", "declaration", "applies_to", 
                                         ArgWrapper("-tp", ["name", "description"], True),
                                         ArgWrapper("-p", ["type", "name", "description"], True),
                                         ArgWrapper("-e", ["type", "description"], True),
                                         ArgWrapper("-ex", ["Example"]),
                                         ArgWrapper("-re", ["Remarks"])], 
                                 True)
        ]

        arg_parser = ArgParser(cl_args, args)
    except Exception as err:
        print(err.with_traceback())
        print("Failed to parse arguments\nYou likely just put them in the wrong order:"
        "\nconstructorgenerator.py -cg namespace class constructor_description {-c name constructor_declaration applies_to [[-tp type_parameter_name description ...]] [[-p parameter_type parameter_name description ...]] [[-e exception_type description ...]] [-ex example_description] [-re remark_description]"
        " | [-co overload_name overload_declaration overload_applies_to [[-tp type_parameter_name description ...]] [[-p parameter_type parameter_name description ...]] [[-e exception_type description ...]] [-ex example_description] [-re remark_description] ...]}")
        input("Press any key to exit")
        exit()

    print(f"Page generated successfully at path: " + create_constructor_page(arg_parser))

def create_constructor_page(args: ArgParser):
    page = ""
    
    if args.parsed_args[1].exists:
        page = constructor_template 
    else:
        page = constructor_with_overload_template

    base_args = args.parsed_args[0].params
    namespace = base_args["namespace"]
    class_ = base_args["class"]

    page = page.replace("{class}", class_)
    page = page.replace("{namespace}", namespace)
    page = page.replace("{constructordescription}", base_args["description"])

    type_data_path = convert_to_pagedata_path(namespace, class_)
    page_data_path = path.join(join_and_verify(type_data_path), "constructors.md.json")
    full_path = path.join(convert_to_api_reference_path(class_), "constructors.md")

    data = {"names": [], "descriptions": []}
    if args.parsed_args[1].exists:
        page = create_constructor_page_no_overloads(args, data, page)
    else:
        page = create_constructor_page_with_overloads(args, data, page)

    update_json(type_data_path, "constructors", data)
    
    with open(full_path, "w", encoding="utf-8") as page_file:
        page_file.write(page)
    with open(page_data_path, "w", encoding="utf-8") as cl_arg_file:
        json.dump(args.args, cl_arg_file, indent=4)

    SidebarManager.add_constructor(namespace, class_)
    
    return full_path

def create_constructor_page_no_overloads(args: ArgParser, data: dict, page: str) -> str:
    parent_arg = args.parsed_args[1]

    data["names"].append(args.parsed_args[0].params["class"])
    data["descriptions"].append(args.parsed_args[0].params["description"])

    params = parent_arg.params
    page = page.replace("{constructordeclaration}", params["declaration"])
    page = page.replace("{appliesto}", params["applies_to"])

    page = replace_overload_things(params, page)
    return page

def create_constructor_page_with_overloads(args: ArgParser, global_data: dict, page: str) -> str:
    class_ = args.parsed_args[0].params["class"]
    page = create_overload_table(args.parsed_args[2], page, global_data, f"{class_.lower()}/constructors")
    return page


if __name__ == "__main__":
    if len(command_line_args) == 1:
        start()
    else:
        start(command_line_args)

