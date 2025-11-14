from pathlib import Path
import csv
import json

PROFILES_PATH = Path("profiles")

class Result:
    """Data class for a simulation result."""
    def __init__(self, id, json_path, csv_path, output=None, settings=None):
        self.id = id
        self.json_path = json_path
        self.csv_path = csv_path
        self.output = output if output is not None else []
        self.settings = settings if settings is not None else {}

    def __str__(self):
        return f"Result(id={self.id}, json_path={self.json_path}, csv_path={self.csv_path})"

def _get_id_from_path(path: Path):
    """Extracts the profile ID from a path."""
    try:
        return int(path.name.replace("profile_", ""))
    except (ValueError, AttributeError):
        return -1

def _read_json(path: Path):
    """Reads a JSON file and returns its content."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file {path}: {e}")
        return None

def _read_csv(path: Path):
    """Reads a CSV file and returns its content as a list of lists."""
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            return list(reader)
    except FileNotFoundError as e:
        print(f"Error reading CSV file {path}: {e}")
        return []

def list_of_results(include_output=False, include_settings=False):
    """
    Scans the profiles directory and returns a list of Result objects.
    """
    if not PROFILES_PATH.is_dir():
        return []

    results = []
    for profile_dir in PROFILES_PATH.iterdir():
        if profile_dir.is_dir():
            profile_id = _get_id_from_path(profile_dir)
            if profile_id == -1:
                continue

            settings_path = profile_dir / "settings.json"
            output_path = profile_dir / "output.csv"
            
            output = _read_csv(output_path) if include_output else []
            settings = _read_json(settings_path) if include_settings else {}

            results.append(Result(profile_id, settings_path, output_path, output, settings))
            
    return sorted(results, key=lambda r: r.id)

def get_latest_id():
    """Gets the highest profile ID from the profiles directory."""
    if not PROFILES_PATH.is_dir():
        return -1
        
    max_id = -1
    for profile_dir in PROFILES_PATH.iterdir():
        if profile_dir.is_dir():
            profile_id = _get_id_from_path(profile_dir)
            if profile_id > max_id:
                max_id = profile_id
    return max_id
