import json
import os
from os import path
import shutil
import sys
from typing import Union
from utils.argparser import ArgParser, ArgParentWrapper, ArgWrapper
from utils.pathutils import convert_to_api_reference_path, convert_to_pagedata_path, page_data_path, api_reference_path
from utils.sidebarutils import SidebarManager
from utils.templateutils import replace_thing_with_thing_from_template
from utils.typedatautils import update_json

import constructorgenerator
import eventgenerator
import fieldgenerator
import methodgenerator 
import constructorgenerator 
import operatorgenerator 
import propertygenerator
import typegenerator

command_line_args = []

def start(cl_args: list[str] = sys.argv):
    try:
        args = [ArgWrapper("-n", ["namespace"]),
                ArgWrapper("-c", ["class"])
        ]

        arg_parser = ArgParser(cl_args, args)

        for file in os.listdir(api_reference_path):
            full_path = path.join(api_reference_path, file)
            if path.isdir(full_path):
                shutil.rmtree(full_path)

        if arg_parser.parsed_args[0].exists:
            generate_types_in_namespace(path.join(page_data_path, arg_parser.parsed_args[0].params["namespace"]))
        elif arg_parser.parsed_args[1].exists:
            generate_type_in_namespace(path.join(page_data_path, arg_parser.parsed_args[0].params["namespace"], args.parsed_args[0].params["class"]))
        else:
            if path.isfile(path.join(api_reference_path, "_sidebar.md")):
                os.remove(path.join(api_reference_path, "_sidebar.md"))
            if path.isfile(path.join(page_data_path, "_sidebar.json")):
                os.remove(path.join(page_data_path, "_sidebar.json"))

            for namespace in os.listdir(page_data_path):
                namespace_path = path.join(page_data_path, namespace)
                generate_types_in_namespace(namespace_path)

                    
    except Exception as err:
        print(err.with_traceback())
        print("Failed to parse arguments\nYou likely just put them in the wrong order:"
        "\nglobalgenerator.py [-n namespace [-c class]] ")
        input("Press any key to exit")
        exit()

def generate_types_in_namespace(namespace_path: str):
    for class_ in os.listdir(namespace_path):
        class_path = path.join(namespace_path, class_)
        generate_type_in_namespace(class_path, class_)

def generate_type_in_namespace(class_path: str, class_: str):
    params = []
    member_path = ""
    
    member_path = path.join(class_path, "events")
    if path.isdir(member_path):
        for member in os.listdir(member_path):
            with open(path.join(member_path, member), encoding="utf-8") as json_file:
                params = json.load(json_file)
            eventgenerator.start(params)

    member_path = path.join(class_path, "fields")
    if path.isdir(member_path):
        for member in os.listdir(member_path):
            with open(path.join(member_path, member), encoding="utf-8") as json_file:
                params = json.load(json_file)
            fieldgenerator.start(params)
    
    member_path = path.join(class_path, "methods")
    if path.isdir(member_path):
        for member in os.listdir(member_path):
            with open(path.join(member_path, member), encoding="utf-8") as json_file:
                params = json.load(json_file)
            methodgenerator.start(params)
    
    member_path = path.join(class_path, "operators")
    if path.isdir(member_path):
        for member in os.listdir(member_path):
            with open(path.join(member_path, member), encoding="utf-8") as json_file:
                params = json.load(json_file)
            operatorgenerator.start(params)

    member_path = path.join(class_path, "properties")
    if path.isdir(member_path):
        for member in os.listdir(member_path):
            with open(path.join(member_path, member), encoding="utf-8") as json_file:
                params = json.load(json_file)
            propertygenerator.start(params)
    
    member_path = path.join(class_path, "constructors.md.json")
    if path.isfile(member_path):
        with open(path.join(member_path), encoding="utf-8") as json_file:
            params = json.load(json_file)
        constructorgenerator.start(params)
    
    member_path = path.join(class_path, f"{class_}.md.json")
    if path.isfile(member_path):
        with open(path.join(member_path), encoding="utf-8") as json_file:
            params = json.load(json_file)
        typegenerator.start(params)

if __name__ == "__main__":
    if len(command_line_args) == 1:
        start()
    else:
        start(command_line_args)