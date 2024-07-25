import json
import os

# Global variable to store all tags in memory
all_tags = {}

def add_tags_to_memory(file_path, tag_list):
    """
    Adds tags to a global dictionary to be saved in a single JSON file.
    """
    # Remove the file extension
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    all_tags[base_name] = tag_list

def save_all_tags_to_json(json_file='tags.json'):
    """
    Saves all collected tags to a single JSON file.
    """
    with open(json_file, 'w') as f:
        json.dump(all_tags, f, indent=4)
    print(f"All tags saved to JSON file: {json_file}")