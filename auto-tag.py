import sys
import os
import time
from tags import add_tags_to_memory, save_all_tags_to_json
from model import DeepDanbooruModel

class AddAnimeTags:
    def __init__(self):
        self.model = DeepDanbooruModel()
        self.image_directory = None

    def navigate_directory(self, path: str):
        start_time = time.time()

        if os.path.isdir(path):
            self.image_directory = path
            for root, _, files in os.walk(path):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    self.classify_and_add_tags(file_path)
            self.save_tags()
        else:
            self.classify_and_add_tags(path)
            self.image_directory = os.path.dirname(path)
            self.save_tags()

        total_time = time.time() - start_time
        print(f"Total operation time: {total_time:.2f} seconds")

    def classify_and_add_tags(self, path: str):
        image_start_time = time.time()

        status, tags = self.model.classify_image(path)
        if status == 'success':
            add_tags_to_memory(path, tags)
            image_time = time.time() - image_start_time
            num_tags = len(tags)
            print(f"[Success] [{image_time:.2f} seconds] [{num_tags} tags added] [{path}]")
        else:
            image_time = time.time() - image_start_time
            print(f"[Failed] [{image_time:.2f} seconds] [No tags] [{path}]")

    def save_tags(self):
        if self.image_directory:
            json_file_path = os.path.join(self.image_directory, 'tags.json')
            save_all_tags_to_json(json_file_path)
            print(f"Tags saved to {json_file_path}")

def parse_args():
    if len(sys.argv) < 2:
        print("Usage: python auto-tag-anime.py <path>")
        sys.exit()

    if not os.path.exists(sys.argv[1]):
        print('Path does not exist')
        sys.exit()

if __name__ == "__main__":
    parse_args()
    add_anime_tags = AddAnimeTags()
    add_anime_tags.navigate_directory(sys.argv[1])
