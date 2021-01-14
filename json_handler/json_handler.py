import json
import os


def load_json_data(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


def load_jsonl_data(file_path):
    with open(file_path, 'r') as json_file:
        lines = list(json_file)
        return [json.loads(line) for line in lines]


def write_json_file(filename, data):
    _, ext = os.path.splitext(filename)
    filename = filename if ext == ".json" else f'{filename}.json'
    with open(filename, 'w') as out_file:
        json.dump(data, out_file, ensure_ascii=False, indent=2)