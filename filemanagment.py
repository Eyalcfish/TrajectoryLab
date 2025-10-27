from pathlib import Path
import csv
import json


SETTINGS_PATH = "/home/eyalc/Projects/TrajectoryLab/TrajectoryLab/settings"
OUTPUT_PATH = "/home/eyalc/Projects/TrajectoryLab/TrajectoryLab/shooting-sim-output"

class Result():
    def __init__(self, id, json_path, csv_path, output = [], settings = {}):
        self.id = id
        self.json_path = json_path
        self.csv_path = csv_path
        self.output = output
        self.settings = settings

def get_id_of_file(file_name: str):
    return int(file_name.replace("shots_", "").replace("data_", "").replace(".csv", "").replace(".json", ""))

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

    folder = Path(OUTPUT_PATH)

    for file in folder.iterdir():
        if file.is_file():
            i += 1
    return i 

def list_of_results(include_output,include_settings):
    folder = Path(OUTPUT_PATH)

    results = []

    for file in folder.iterdir():
        if file.is_file():
            csv_name = file.name
            id = get_id_of_file(csv_name)
            json_name = "No Json Found"
            if Path(f"{SETTINGS_PATH}/data_{id}.json").is_file():
                json_name = f"data_{id}.json"
            output = []
            settings = {}
            if include_output:
                output = read_csv_file(f"{OUTPUT_PATH}/{csv_name}")
            if include_settings and json_name != "No Json Found":
                settings = read_json_file(f"{SETTINGS_PATH}/{json_name}")
            result = Result(id,json_path=f"{SETTINGS_PATH}/{json_name}", csv_path=f"{OUTPUT_PATH}/{csv_name}",output=output, settings=settings)
            results.append(result)

    return results

def get_result_by_id(id, include_output, include_settings):
    csv_path = f"{OUTPUT_PATH}/shots_{id}.csv"
    json_path = f"{SETTINGS_PATH}/data_{id}.json"
    output = []
    settings = {}
    if include_output:
        output = read_csv_file(csv_path)
    if include_settings and Path(json_path).is_file():
        settings = read_json_file(json_path)
    result = Result(id, json_path=json_path, csv_path=csv_path, output=output, settings=settings)
    return result

def get_latest_id():
    max_id = -1

    folder = Path(OUTPUT_PATH)

    for file in folder.iterdir():
        if file.is_file():
            id = get_id_of_file(file.name)
            if id > max_id:
                max_id = id
    return max_id