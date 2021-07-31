import json
import os
from os import path
import sys
from typing import Union
from utils.argparser import ArgParser, ArgParentWrapper, ArgWrapper
from utils.htmlutils import convert_string_to_work_in_id
from utils.pathutils import convert_to_api_reference_path, convert_to_pagedata_path, join_and_verify, types_path
from utils.sidebarutils import SidebarManager
from utils.templateutils import replace_thing_with_thing_from_template, table_row_template, table_template
from utils.typedatautils import update_json


command_line_args = ["-e", "TestNamespace", "Test", "Struct", "This is a test description", "public static struct Test", "object->fuck", "doesn't apply to anything",
                     "-ex",
                         "This is an example in usage, a very good one",
]

with open(path.join(types_path, "typetemplate.md"), "r", encoding="utf-8") as file_template_file:
    type_template = file_template_file.read(); 

def start(cl_args: list[str] = sys.argv):
    try:
        args = [ArgWrapper("-e", ["namespace", "class", "class_type", "description", "declaration", "inheritance", "applies_to"]),
                ArgWrapper("-ex", ["Example"]),
        ]

        arg_parser = ArgParser(cl_args, args)
    except Exception as err:
        print(err.with_traceback())
        print("Failed to parse arguments\nYou likely just put them in the wrong order:"
        "\ntypegenerator.py -t namespace class class_type type_description type_declaration inheritance applies_to [-ex example_description]")
        input("Press any key to exit")
        exit()

    print(f"Page generated successfully at path: " + create_type_page(arg_parser))

def create_type_page(args: ArgParser):
    page = type_template

    base_args = args.parsed_args[0].params
    namespace = base_args["namespace"]
    class_ = base_args["class"]
    description = base_args["description"]

    page = page.replace("{class}", class_)
    page = page.replace("{classtype}", base_args["class_type"])
    page = page.replace("{typenamespace}", namespace)
    page = page.replace("{typedescription}", description)
    page = page.replace("{typedeclaration}", base_args["declaration"])
    page = page.replace("{inheritance}", base_args["inheritance"])
    page = page.replace("{appliesto}", base_args["applies_to"])

    page = replace_thing_with_thing_from_template(args.parsed_args[1], page, "{examples}", "## Examples\n{examples}\n", "")

    type_data_path = convert_to_pagedata_path(namespace, class_)
    page_data_path = path.join(join_and_verify(type_data_path), class_ + ".md.json")
    full_path = path.join(convert_to_api_reference_path(namespace, class_), class_ + ".md")

    with open(path.join(type_data_path, "member_data.json"), encoding="utf-8") as member_data_file:
        member_data = json.load(member_data_file)

    page = fill_in_table(namespace, class_, member_data, page)


    with open(full_path, "w", encoding="utf-8") as page_file:
        page_file.write(page)
    with open(page_data_path, "w", encoding="utf-8") as cl_arg_file:
        json.dump(args.args, cl_arg_file, indent=4)

    SidebarManager.add_type(namespace, class_)

    return full_path

def fill_in_table(namespace: str, class_: str, member_data: dict, page: str) -> str:    
    for member in SidebarManager._desired_member_order:
        if member.lower() not in member_data:
            page = page.replace(f"<h2 id=\"{member.lower()}\">{member}</h2>\n{{{member.lower()}}}\n", "")
            continue
        else:
            v = member_data[member.lower()]
        
        rows = []
        for name, description, link in zip(v["names"], v["descriptions"], v["links"]):
            row = table_row_template
            row = row.replace("{linkbeforeid}", link)
            row = row.replace("{namecleaned}", convert_string_to_work_in_id(name))
            row = row.replace("{name}", name)
            row = row.replace("{description}", description)
            rows.append(row)
        
        page = page.replace(f"{{{member.lower()}}}", table_template.replace("{rows}", "\n".join(rows)))

    return page

if __name__ == "__main__":
    if len(command_line_args) == 1:
        start()
    else:
        start(command_line_args)