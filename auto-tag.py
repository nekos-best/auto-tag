import sys
import os
import tags
import model

class AddAnimeTags:
    def __init__(self):
        self.model = model.DeepDanbooruModel()
        self.image_directory = None  # Store the image directory for later use

    def navigate_dir(self, path):
        if os.path.isdir(path):
            self.image_directory = path  # Set the image directory
            for root, _, files in os.walk(path):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    self.add_tags_to_image(file_path)
            # Save all image names and tags to JSON after processing all files
            if self.image_directory:
                json_file_path = os.path.join(self.image_directory, 'tags.json')
                tag.save_all_tags_to_json(json_file_path)
        else:
            self.add_tags_to_image(path)
            self.image_directory = os.path.dirname(path)  # Set the directory of the single image
            # Save the single image name and tags to JSON
            json_file_path = os.path.join(self.image_directory, 'tags.json')
            tag.save_all_tags_to_json(json_file_path)

    def add_tags_to_image(self, path):
        if sys.platform == 'win32':
            if not path.lower().endswith(('.jpg', '.jpeg')):
                print(f"{path} is not a JPEG, no EXIF data")
                return

        status, tags = self.model.classify_image(path)
        if status == 'success':
            tag.add_tags_to_memory(path, tags)
            print(f"{len(tags)} tags added.")
        else:
            print(f"Failed to process {path}")

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
    add_anime_tags.navigate_dir(sys.argv[1])
