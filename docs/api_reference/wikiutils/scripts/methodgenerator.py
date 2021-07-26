import json
import os
from os import path
import sys
from typing import Union
from argparser import ArgParser, ArgParentWrapper, ArgWrapper
from constants import api_reference_path, common_path, methods_path
from globaldatautils import update_json
from htmlutils import convert_string_to_work_in_html, convert_string_to_work_in_link
from sidebarutils import SidebarManager
from templateutils import replace_thing_with_thing_from_template

# Method with no overloads
command_line_args = ["-mg", "Test", "TestMethod<T, T1>(string, object)", "This is a test description", 
                     "-m", "public static int TestMethod<T, T1>(string thingy, object thingy2)", "doesn't apply to anything",
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
command_line_args = ["-mg", "Test", "TestMethod", "This is a test description", 
                     "-mo", "TestMethod<T, T1>(string, object)", "this is a test description of the first overload", "public static int TestMethod<T, T1>(string thingy, object thingy2)", "doesn't apply to anything",
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
                     "-mo", "TestMethod<T>(string, object)", "This is a test description of the second overload", "public static int TestMethod<T>(string thingy, object thingy2)", "doesn't apply to anything",
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


def start(cl_args: list[str] = sys.argv):
    try:
        args = [ArgWrapper("-mg", ["class", "name", "description"]),
                ArgParentWrapper("-m", ["declaration", "applies_to", 
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
        "\nmethodgenerator.py -mg class method_name method_description {-m method_declaration applies_to [-r return_type return_description] [[-tp type_parameter_name description ...]] [[-p parameter_type parameter_name description ...]] [[-e exception_type description ...]] [-ex example_description] [-re remark_description]"
        " | [-mo overload_name overload_declaration overload_applies_to [-r return_type return_description] [[-tp type_parameter_name description ...]] [[-p parameter_type parameter_name description ...]] [[-e exception_type description ...]] [-ex example_description] [-re remark_description] ...]}")
        input("Press any key to exit")
        exit()

    print(f"Page generated successfully at path: " + create_method_page(arg_parser))

def create_method_page(args: ArgParser):
    page = ""
    
    if args.parsed_args[1].exists:
        with open(path.join(methods_path, "methodtemplate.md"), "r", encoding="utf-8") as file_template_file:
            page = file_template_file.read();    
    else:
        with open(path.join(methods_path, "methodtemplatewithoverload.md"), "r", encoding="utf-8") as file_template_file:
            page = file_template_file.read();  

    base_method_args = args.parsed_args[0].params
    page = page.replace("{class}", base_method_args["class"])
    page = page.replace("{methodname}", convert_string_to_work_in_html(base_method_args["name"]))
    page = page.replace("{methoddescription}", base_method_args["description"])

    data = {"names": [], "descriptions": []}
    if args.parsed_args[1].exists:
        page = create_method_page_no_overloads(args, data, page)
    else:
        page = create_method_page_with_overloads(args, data, page)

    final_path_folder = path.join(api_reference_path, base_method_args["class"].lower(), "methods")
    update_json(final_path_folder, "methods", data)
    
    final_path = path.join(final_path_folder, base_method_args["name"].lower() + ".md")
    with open(final_path, "w", encoding="utf-8") as page_file:
        page_file.write(page)
    with open(final_path + ".json", "w", encoding="utf-8") as cl_arg_file:
        json.dump(args.args, cl_arg_file)

    SidebarManager.add_method(base_method_args["class"], base_method_args["name"])
    
    return final_path

def create_method_page_no_overloads(args: ArgParser, data: dict, page: str) -> str:
    parent_arg = args.parsed_args[1]

    data["names"].append(args.parsed_args[0].params["name"])
    data["descriptions"].append(args.parsed_args[0].params["description"])

    params = parent_arg.params
    page = page.replace("{methoddeclaration}", params["declaration"])
    page = page.replace("{appliesto}", params["applies_to"])

    page = replace_overload_things(params, page)
    return page

def create_method_page_with_overloads(args: ArgParser, global_data: dict, page: str) -> str:
    table_row_template = ""
    table_rows = []
    with open(path.join(methods_path, "overloadtablerow.md"), "r", encoding="utf-8") as table_row_file:
        table_row_template = table_row_file.read()

    overloads = []
    for data in args.parsed_args[2].params:
        overloads.append(create_method_overload(data, overloads))

        table_row = table_row_template
        table_row = table_row.replace("{classlower}", args.parsed_args[0].params["class"].lower())
        table_row = table_row.replace("{namelower}", args.parsed_args[0].params["name"].lower())
        table_row = table_row.replace("{namecleaned}", convert_string_to_work_in_link(data["name"]))
        table_row = table_row.replace("{name}", convert_string_to_work_in_html(data["name"]))
        table_row = table_row.replace("{description}", data["description"])
        table_rows.append(table_row)

        global_data["names"].append(convert_string_to_work_in_html(data["name"]))
        global_data["descriptions"].append(data["description"])

    table = ""
    with open(path.join(methods_path, "overloadtable.md"), "r", encoding="utf-8") as table_file:
        table = table_file.read()
    table = table.replace("{rows}", "\n".join(table_rows))
    page = page.replace("{overloadtable}", table)

    page = page.replace("{overloads}", "\n".join(overloads))
    return page

def create_method_overload(data: dict, page: str) -> str:
    template = ""
    with open(path.join(methods_path, "overloadtemplate.md"), "r", encoding="utf-8") as file_template_file:
        template = file_template_file.read();  
    
    template = template.replace("{methodname}", convert_string_to_work_in_html(data["name"]))
    template = template.replace("{methoddescription}", data["description"])
    template = template.replace("{methoddeclaration}", data["declaration"])
    template = template.replace("{appliesto}", data["applies_to"])

    template = replace_overload_things(data, template)
    return template

def replace_overload_things(data: dict, page: str) -> str:
    page = replace_thing_with_thing_from_template(data["-r"], page, "{returns}", "## Returns\n{returns}\n", "")
    page = replace_thing_with_thing_from_template(data["-tp"], page, "{typeparameters}", "## Type Parameters\n{typeparameters}\n", "")
    page = replace_thing_with_thing_from_template(data["-p"], page, "{parameters}", "## Parameters\n{parameters}\n", "")
    page = replace_thing_with_thing_from_template(data["-e"], page, "{exceptions}", "## Exceptions\n{exceptions}\n", "")
    page = replace_thing_with_thing_from_template(data["-ex"], page, "{examples}", "## Examples\n{examples}\n", "")
    page = replace_thing_with_thing_from_template(data["-re"], page, "{remarks}", "## Remarks\n{remarks}\n", "")
    return page

if __name__ == "__main__":
    if len(command_line_args) == 1:
        start()
    else:
        start(command_line_args)

