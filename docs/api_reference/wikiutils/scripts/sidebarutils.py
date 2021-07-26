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
from constants import api_reference_path

class SidebarManager:
    sample_object = {"link": "", "children": {}}
    sidebar = {}
    with open(path.join(api_reference_path, "_sidebar.json"), "r", encoding="utf-8") as sidebar_json:
        sidebar = json.load(sidebar_json)    

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
        cls._add_internal(class_, "constructors", name, should_save)
    
    @classmethod 
    def add_property(cls, class_: str, name: str, should_save: bool = True):
        cls._add_internal(class_, "properties", name, should_save)
            
    @classmethod 
    def add_method(cls, class_: str, name: str, should_save: bool = True):
        cls._add_internal(class_, "methods", name, should_save)
            
    @classmethod 
    def add_field(cls, class_: str, name: str, should_save: bool = True):
        cls._add_internal(class_, "fields", name, should_save)

    @classmethod 
    def add_operator(cls, class_: str, name: str, should_save: bool = True):
        cls._add_internal(class_, "operators", name, should_save)

    @classmethod
    def _add_internal(cls, class_: str, type_: str, name: str, should_save: bool = True):
        class_ = class_.lower()
        type_ = type_.lower()
        name = name.lower()

        if class_ not in cls.sidebar:
            cls.sidebar[class_] = copy.deepcopy(cls.sample_object)
            class_child = cls.sidebar[class_]
        else:
            class_child = cls.sidebar[class_]

        if type_ not in class_child:
            type_child = copy.deepcopy(cls.sample_object)
            class_child["children"][type_] = type_child
        else:
            type_child = class_child[type_]

        if name not in type_child:
            name_child = copy.deepcopy(cls.sample_object)
            type_child["children"][name] = name_child
        else:
            name_child = type_child[name]

        if name_child["link"] == "":
            name_child["link"] = path.join(class_, type_, name + ".md")
        
        if should_save:
            cls.save()

    @classmethod
    def save(cls):
        with open(path.join(api_reference_path, "_sidebar.md"), "w", encoding="utf-8") as sidebar_json:
            cls._write_recursive(sidebar_json, cls.sidebar)
        with open(path.join(api_reference_path, "_sidebar.json"), "w", encoding="utf-8") as sidebar_json:
            json.dump(cls.sidebar, sidebar_json, indent=4)
                
    
    @classmethod
    def _write_recursive(cls, fp, children: dict, layer: int = 0):
        for key, value in children.items():
            link = value["link"]
            if link == "":
                fp.write(f"{layer * '  '}- {key}\n")
            else:
                fp.write(f"{layer * '  '}- [{key}]({link})\n")
            cls._write_recursive(fp, value["children"], layer + 1)      
