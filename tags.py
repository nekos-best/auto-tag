import os
import json

all_tags = {}

def add_tags_to_memory(file_path, tag_list):
    try:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        all_tags[base_name] = tag_list
    except Exception as e:
        print(f"Error adding tags to memory: {e}")

def save_all_tags_to_json(json_file='tags.json'):
    try:
        with open(json_file, 'w') as f:
            json.dump(all_tags, f, indent=4)
        print(f"All tags saved to JSON file: {json_file}")
    except Exception as e:
        print(f"Error saving tags to JSON file: {e}")
