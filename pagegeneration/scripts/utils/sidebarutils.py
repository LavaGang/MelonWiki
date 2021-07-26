"""
Sample sidebar object

"name": {
    "link": "link",
    "children": []
}
"""

import copy
import json
from os import path
from typing import Union
from utils.pathutils import api_reference_path, page_data_path

class SidebarManager:
    sample_object = {"link": "", "children": {}}
    sidebar = {}

    json_path = path.join(page_data_path, "_sidebar.json")
    md_path = path.join(api_reference_path, "_sidebar.md")

    if not path.isfile(json_path):
        with open(json_path, "w", encoding="utf-8") as sidebar_json:
            json.dump({}, sidebar_json)

    with open(json_path, "r", encoding="utf-8") as sidebar_json:
        sidebar = json.load(sidebar_json)  

    _desired_member_order = ["Constructor", "Fields", "Properties", "Methods", "Operators"]  

    @classmethod
    def add_introduction(cls, class_: str, should_save: bool = True):
        class_ = class_.lower()

        if class_ not in cls.sidebar:
            cls.sidebar[class_] = copy.deepcopy(cls.sample_object)
            class_child = cls.sidebar[class_]
        else:
            class_child = cls.sidebar[class_]

        if class_ not in class_child:
            intro_child = copy.deepcopy(cls.sample_object)
            class_child["children"][class_] = intro_child
        else:
            intro_child = class_child["children"]
        
        if intro_child["link"] == "":
            intro_child["link"] = path.join(class_, class_ + ".md")
        
        if should_save:
            cls.save()

    @classmethod 
    def add_constructor(cls, class_: str, name: str, should_save: bool = True):
        cls._add_internal(class_, "Constructors", name, should_save)
    
    @classmethod 
    def add_field(cls, class_: str, name: str, should_save: bool = True):
        cls._add_internal(class_, "Fields", name, should_save)

    @classmethod 
    def add_property(cls, class_: str, name: str, should_save: bool = True):
        cls._add_internal(class_, "Properties", name, should_save)
            
    @classmethod 
    def add_method(cls, class_: str, name: str, should_save: bool = True):
        cls._add_internal(class_, "Methods", name, should_save)

    @classmethod 
    def add_operator(cls, class_: str, name: str, should_save: bool = True):
        cls._add_internal(class_, "Operators", name, should_save)

    @classmethod
    def _add_internal(cls, class_: str, type_: str, name: str, should_save: bool = True):
        if class_ not in cls.sidebar:
            cls.sidebar[class_] = copy.deepcopy(cls.sample_object)
            class_child = cls.sidebar[class_]["children"]
        else:
            class_child = cls.sidebar[class_]["children"]

        if type_ not in class_child:
            type_child = copy.deepcopy(cls.sample_object)
            class_child[type_] = type_child
        else:
            type_child = class_child[type_]

        if name not in type_child["children"]:
            name_child = copy.deepcopy(cls.sample_object)
            type_child["children"][name] = name_child
        else:
            name_child = type_child["children"][name]

        if name_child["link"] == "":
            name_child["link"] = "/".join([class_.lower(), type_.lower(), name.lower() + ".md"])
        
        if should_save:
            cls.save()

    @classmethod
    def save(cls):
        cls.sort_sidebar()
        with open(cls.md_path, "w", encoding="utf-8") as sidebar_json:
            cls._write_recursive(sidebar_json, cls.sidebar)
        with open(cls.json_path, "w", encoding="utf-8") as sidebar_json:
            json.dump(cls.sidebar, sidebar_json, indent=4)


    @classmethod
    def sort_sidebar(cls):
        cls.sidebar = {k: cls._sort_member_types(v) if isinstance(v, dict) else v
                       for k, v in sorted(cls.sidebar.items())}

    @classmethod
    def _sort_member_types(cls, member: dict) -> dict:
        ordered = {}
        member_children = member["children"]
        for member_order in cls._desired_member_order:
            if member_order in member_children:
                ordered[member_order] = dict(sorted(cls._sort_members(member_children.pop(member_order)).items()))
        member_children.update(ordered)
        return member
    
    @classmethod
    def _sort_members(cls, member: dict) -> dict:
        member["children"] = dict(sorted(member["children"].items()))
        return member


    @classmethod
    def _write_recursive(cls, fp, children: dict, layer: int = 0):
        for key, value in children.items():
            link = value["link"]
            if link == "":
                fp.write(f"{layer * '  '}- {key}\n")
            else:
                fp.write(f"{layer * '  '}- [{key}]({link})\n")
            cls._write_recursive(fp, value["children"], layer + 1)      
