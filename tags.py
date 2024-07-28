import os
import json

tags = {}

def load_to_memory(file_path, tag_list, character_list):
    try:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        tags[file_name] = {
            "tags": tag_list,
            "characters": character_list
        }
    except Exception as e:
        print(f"Error adding tags and characters to memory: {e}")

def save_to_json(json_file='tags.json'):
    try:
        with open(json_file, 'w') as f:
            json.dump(tags, f, indent=4)
    except Exception as e:
        print(f"Error saving tags and characters to JSON file: {e}")
