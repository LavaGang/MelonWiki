import json
import os
from os import path

def update_json(class_path: str, type_: str, data: dict):
    json_path = path.join(class_path, "member_data.json")
    if not path.isfile(json_path):
        with open(json_path, "w", encoding="utf-8") as global_data_file:
            json.dump({type_: {"names": [], "descriptions": []}}, global_data_file)

    with open(json_path, "r", encoding="utf-8") as global_data_file:
        global_data = json.load(global_data_file)

    if type_ not in global_data:
        global_data[type_] = {"names": [], "descriptions": []}

    for name in data["names"]:
        if name in global_data[type_]["names"]:
            return

    global_data[type_]["names"].extend(data["names"])
    global_data[type_]["descriptions"].extend(data["descriptions"])
    
    with open(json_path, "w", encoding="utf-8") as global_data_file:
        json.dump(global_data, global_data_file)