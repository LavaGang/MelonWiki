import json
import os
from os import path

def update_json(class_path: str, type_: str, data: dict):
    json_path = path.join(class_path, "member_data.json")
    if not path.isfile(json_path):
        with open(json_path, "w", encoding="utf-8") as global_data_file:
            json.dump({type_: {"names": [], "descriptions": [], "links": []}}, global_data_file, indent=4)

    with open(json_path, "r", encoding="utf-8") as global_data_file:
        global_data = json.load(global_data_file)

    if type_ not in global_data:
        global_data[type_] = {"names": [], "descriptions": [], "links": []}

    type_data = global_data[type_]

    for i in range(len(data["names"])):
        name = data["names"][i]
        description = data["descriptions"][i]
        link = data["links"][i]
        try:
            index = type_data["names"].index(name)
            type_data["names"][index] = name
            type_data["descriptions"][index] = description
            type_data["links"][index] = link
        except ValueError:
            type_data["names"].append(name)
            type_data["descriptions"].append(description)
            type_data["links"].append(link)

    with open(json_path, "w", encoding="utf-8") as global_data_file:
        json.dump(global_data, global_data_file, indent=4)