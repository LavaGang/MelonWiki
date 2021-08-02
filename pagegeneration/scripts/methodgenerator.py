import json
import os
from os import path
import sys
from typing import Union
from utils.argparser import ArgParser, ArgParentWrapper, ArgWrapper
from utils.htmlutils import convert_string_to_work_in_html, convert_string_to_work_in_id
from utils.pathutils import convert_to_api_reference_path, convert_to_pagedata_path, join_and_verify, methods_path
from utils.sidebarutils import SidebarManager
from utils.templateutils import create_overload_table, replace_overload_things, replace_thing_with_thing_from_template
from utils.typedatautils import update_json


# Method with no overloads
command_line_args = ["methodgenerator.py", "-mg", "TestNamespace", "Test", "TestMethod", "This is a test description", 
                     "-m", "TestMethod<T, T1>(string, object)", "public static int TestMethod<T, T1>(string thingy, object thingy2)", "doesn't apply to anything",
                        "-r", "`int`", "some test thingy that returns int",
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
                            "ArgumentException", "throws when the method feels like it"
]

# Method with overloads
command_line_args = ["methodgenerator.py", "-mg", "TestNamespace", "Test", "Die", "This is a test description", 
                     "-mo", "Die<T, T1>(string, object)", "this is a test description of the first overload", "public static int TestMethod<T, T1>(string thingy, object thingy2)", "doesn't apply to anything",
                        "-r", "`int`", "some test thingy that returns int",
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
                            "ArgumentException", "throws when the method feels like it",
                        "-ex",
                            "This is an example in usage, a very good one",
                        "-re",
                            "this is a remark yes yes",
                     "-mo", "Die<T>(string, object)", "This is a test description of the second overload", "public static int TestMethod<T>(string thingy, object thingy2)", "doesn't apply to anything",
                        "-r", "`int`", "some test thingy that returns int",
                        "-tp", 
                            "`T`", "type param 1",
                        "-p",
                            "`string`", "thingy", "this is a string parameter, \"i dunno what to say\"",
                        "-p",
                            "`object`", "thing2", "this is an object parameter. yes this naming is confused",
                        "-e",
                            "ArgumentNullException", "throws then either of the arguments are null",
                        "-e",
                            "ArgumentException", "throws when the method feels like it",
                        "-re",
                            "this is a remark yes yes",
]

with open(path.join(methods_path, "methodtemplate.md"), "r", encoding="utf-8") as file_template_file:
    method_template = file_template_file.read();   

with open(path.join(methods_path, "methodtemplatewithoverload.md"), "r", encoding="utf-8") as file_template_file:
    method_with_overload_template = file_template_file.read();  

def start(cl_args: list[str] = sys.argv):
    try:
        args = [ArgWrapper("-mg", ["namespace", "class", "name", "description"]),
                ArgParentWrapper("-m", ["name", "declaration", "applies_to", 
                                        ArgWrapper("-r", ["type", "description"]), 
                                        ArgWrapper("-tp", ["name", "description"], True),
                                        ArgWrapper("-p", ["type", "name", "description"], True),
                                        ArgWrapper("-e", ["type", "description"], True),
                                        ArgWrapper("-ex", ["Example"]),
                                        ArgWrapper("-re", ["Remarks"])]),
                ArgParentWrapper("-mo", ["name", "description", "declaration", "applies_to", 
                                         ArgWrapper("-r", ["type", "description"]), 
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
        "\nmethodgenerator.py -mg namespace class method_name method_description {-m name method_declaration applies_to [-r return_type return_description] [[-tp type_parameter_name description ...]] [[-p parameter_type parameter_name description ...]] [[-e exception_type description ...]] [-ex example_description] [-re remark_description]"
        " | [-mo overload_name overload_declaration overload_applies_to [-r return_type return_description] [[-tp type_parameter_name description ...]] [[-p parameter_type parameter_name description ...]] [[-e exception_type description ...]] [-ex example_description] [-re remark_description] ...]}")
        input("Press any key to exit")
        exit()

    print(f"Page generated successfully at path: " + create_method_page(arg_parser))

def create_method_page(args: ArgParser):
    page = ""
    
    if args.parsed_args[1].exists:
        page = method_template 
    else:
        page = method_with_overload_template

    base_args = args.parsed_args[0].params
    namespace = base_args["namespace"]
    class_ = base_args["class"]
    name = base_args["name"]

    page = page.replace("{class}", class_)
    page = page.replace("{namespace}", namespace)
    page = page.replace("{methoddescription}", base_args["description"])

    type_data_path = convert_to_pagedata_path(namespace, class_)
    page_data_path = path.join(join_and_verify(type_data_path, "methods"), name.lower() + ".md.json")
    full_path = path.join(convert_to_api_reference_path(namespace, class_, "methods"), name.lower() + ".md")

    data = {"names": [], "descriptions": [], "links": []}
    if args.parsed_args[1].exists:
        page = create_method_page_no_overloads(args, data, page)
    else:
        page = create_method_page_with_overloads(args, data, page)

    update_json(type_data_path, "methods", data)
    
    with open(full_path, "w", encoding="utf-8") as page_file:
        page_file.write(page)
    with open(page_data_path, "w", encoding="utf-8") as cl_arg_file:
        json.dump(args.args, cl_arg_file, indent=4)

    SidebarManager.add_method(namespace, class_, name)
    
    return full_path

def create_method_page_no_overloads(args: ArgParser, data: dict, page: str) -> str:
    parent_arg = args.parsed_args[1]

    page = page.replace("{methodname}", convert_string_to_work_in_html(args.parsed_args[1].params["name"]))

    data["names"].append(args.parsed_args[0].params["name"])
    data["descriptions"].append(args.parsed_args[0].params["description"])

    params = parent_arg.params
    page = page.replace("{methoddeclaration}", params["declaration"])
    page = page.replace("{appliesto}", params["applies_to"])

    page = replace_overload_things(params, page)
    return page

def create_method_page_with_overloads(args: ArgParser, global_data: dict, page: str) -> str:
    namespace = args.parsed_args[0].params["namespace"]
    class_ = args.parsed_args[0].params["class"]
    name = args.parsed_args[0].params["name"]
    page = page.replace("{methodname}", convert_string_to_work_in_html(name))
    page = create_overload_table(args.parsed_args[2], page, global_data, f"{namespace.lower()}/{class_.lower()}/methods/{name.lower()}")
    return page

if __name__ == "__main__":
    if len(command_line_args) == 1:
        start()
    else:
        start(command_line_args)

