import json

def read_json(file_path:str) -> dict:
    """Takes in a json file path and returns it's contents"""
    with open(file_path, "r") as json_file:
        content = json.load(json_file)
    return content

def store_json(data:dict, file_path:str):
    """Takes in a python dict and stores it as a .json file"""
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)
        data = {}
data["temp"] = t
data["humidity"] = h

store_json(data, "C:/Users/HP/Downloads/project-1DT032-main.zip/project-1DT032-main/project.json")