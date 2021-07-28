import json
import os
from os import path
import sys
from typing import Union
from utils.argparser import ArgParser, ArgParentWrapper, ArgWrapper
from utils.htmlutils import convert_string_to_work_in_html
from utils.pathutils import convert_to_api_reference_path, convert_to_pagedata_path, events_path, join_and_verify
from utils.sidebarutils import SidebarManager
from utils.templateutils import replace_thing_with_thing_from_template
from utils.typedatautils import update_json


command_line_args = ["-e", "Test", "TestEvent", "This is a test description", "public static event Action TestEvent;", "doesn't apply to anything",
                     "-fv", "`Action`",
                     "-ex",
                         "This is an example in usage, a very good one",
                     "-re",
                         "this is a remark yes yes"
]

with open(path.join(events_path, "eventtemplate.md"), "r", encoding="utf-8") as file_template_file:
    event_template = file_template_file.read(); 

def start(cl_args: list[str] = sys.argv):
    try:
        args = [ArgWrapper("-e", ["class", "name", "description", "declaration", "applies_to"]),
                ArgWrapper("-fv", ["type"]), 
                ArgWrapper("-ex", ["Example"]),
                ArgWrapper("-re", ["Remarks"])
        ]

        arg_parser = ArgParser(cl_args, args)
    except Exception as err:
        print(err.with_traceback())
        print("Failed to parse arguments\nYou likely just put them in the wrong order:"
        "\neventgenerator.py -e class event_name event_description event_declaration applies_to [-et event_type] [-ex example_description] [-re remark_description]")
        input("Press any key to exit")
        exit()

    print(f"Page generated successfully at path: " + create_event_page(arg_parser))

def create_event_page(args: ArgParser):
    page = event_template

    base_args = args.parsed_args[0].params
    class_ = base_args["class"]
    name = base_args["name"]
    description = base_args["description"]

    page = page.replace("{class}", class_)
    page = page.replace("{eventname}", convert_string_to_work_in_html(name))
    page = page.replace("{eventdescription}", description)
    page = page.replace("{eventdeclaration}", base_args["declaration"])
    page = page.replace("{appliesto}", base_args["applies_to"])

    page = replace_thing_with_thing_from_template(args.parsed_args[1], page, "{eventtype}", "## Event Type\n{eventtype}\n", "")
    page = replace_thing_with_thing_from_template(args.parsed_args[2], page, "{examples}", "## Examples\n{examples}\n", "")
    page = replace_thing_with_thing_from_template(args.parsed_args[3], page, "{remarks}", "## Remarks\n{remarks}\n", "")

    type_data_path = convert_to_pagedata_path(class_)
    page_data_path = path.join(join_and_verify(type_data_path, "events"), name.lower() + ".md.json")
    full_path = path.join(convert_to_api_reference_path(class_, "events"), name.lower() + ".md")

    data = {"names": [name], "descriptions": [description]}
    update_json(type_data_path, "events", data)

    with open(full_path, "w", encoding="utf-8") as page_file:
        page_file.write(page)
    with open(page_data_path, "w", encoding="utf-8") as cl_arg_file:
        json.dump(args.args, cl_arg_file, indent=4)

    SidebarManager.add_event(class_, name)

    return full_path

if __name__ == "__main__":
    if len(command_line_args) == 1:
        start()
    else:
        start(command_line_args)