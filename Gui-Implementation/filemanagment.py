from pathlib import Path
import csv
import json
import os


PROFILES_PATH = "profiles"

class Result():
    def __init__(self, id, json_path, csv_path, output = [], settings = {}):
        self.id = id
        self.json_path = json_path
        self.csv_path = csv_path
        self.output = output
        self.settings = settings

def get_id_of_folder(file_name: str):
    return int(os.path.basename(file_name).replace("profile_", ""))

def read_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def read_csv_file(file_path):
    matrix = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            matrix.append(row)
    return matrix

def count_files():
    i = 0

    folder = Path(PROFILES_PATH)

    for file in folder.iterdir():
        if file.is_file():
            i += 1
    return i 

def list_of_results(include_output,include_settings):
    folder = Path(PROFILES_PATH)

    results = []

    for profile in folder.iterdir():
        if not profile.is_file():
            id = get_id_of_folder(profile.as_posix())
            output = []
            settings = {}
            if include_output:
                output = read_csv_file(f"{profile.as_posix()}/output.csv")
            if include_settings:
                settings = read_json_file(f"{profile.as_posix()}/settings.json")
            result = Result(id,json_path=f"{profile.as_posix()}/settings.json", csv_path=f"{profile.as_posix()}/output.csv",output=output, settings=settings)
            results.append(result)

    return results

def get_latest_id():
    max_id = -1

    folder = Path(PROFILES_PATH)

    for profile in folder.iterdir():
        if not profile.is_file():
            id = get_id_of_folder(profile.name)
            if id > max_id:
                max_id = id
    return max_id