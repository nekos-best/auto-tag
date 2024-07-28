import os
import sys
import numpy as np
from PIL import Image
import tensorflow as tf


class DeepDanbooruModel:
    THRESHOLD = 0.75 # Increase this to achieve more accurate results or decrease it for less accurate results.
    METADATA_PATH = "./tags/metadata.txt" # Modify the tags you prefer to display exclusively.
    CHARACTERS_PATH = "./tags/characters.txt" # Modify the characters you prefer to display exclusively.

    # Do not change the paths or settings below here.
    MODEL_PATH = "./model/model-resnet_custom_v3.h5"
    TAGS_PATH = "./model/tags.txt"
    IMAGE_SIZE = (512, 512)

    def __init__(self):
        self.model = self.load_model()
        self.tags = self.load_tags()
        self.characters = self.load_characters()
        self.metadata_tags = self.load_metadata_tags()

    def load_model(self) -> tf.keras.Model:
        print('Loading model...')
        if not os.path.exists(self.MODEL_PATH):
            self.model_not_found_error(self.MODEL_PATH)

        try:
            model = tf.keras.models.load_model(self.MODEL_PATH, compile=False)
            print('Model loaded successfully.')
        except Exception as e:
            print(f'Failed to load the model. Error: {e}')
            sys.exit()

        return model

    def load_tags(self) -> np.ndarray:
        if not os.path.exists(self.TAGS_PATH):
            self.model_not_found_error(self.TAGS_PATH)

        try:
            with open(self.TAGS_PATH, 'r') as tags_stream:
                tags = np.array([tag.strip() for tag in tags_stream if tag.strip()])
            print(f'Tags loaded successfully.')
        except Exception as e:
            print(f'Failed to load tags. Error: {e}')
            sys.exit()

        return tags

    def load_characters(self) -> set:
        if not os.path.exists(self.CHARACTERS_PATH):
            self.model_not_found_error(self.CHARACTERS_PATH)

        try:
            with open(self.CHARACTERS_PATH, 'r') as characters_stream:
                characters = {character.strip() for character in characters_stream if character.strip()}
            print(f'Characters loaded successfully. Number of characters: {len(characters)}')
        except Exception as e:
            print(f'Failed to load characters. Error: {e}')
            sys.exit()

        return characters

    def load_metadata_tags(self) -> set:
        if not os.path.exists(self.METADATA_PATH):
            self.model_not_found_error(self.METADATA_PATH)

        try:
            with open(self.METADATA_PATH, 'r') as metadata_stream:
                metadata_tags = {tag.strip() for tag in metadata_stream if tag.strip()}
            print(f'Metadata tags loaded successfully. Number of metadata tags: {len(metadata_tags)}')
        except Exception as e:
            print(f'Failed to load metadata tags. Error: {e}')
            sys.exit()

        return metadata_tags

    @staticmethod
    def model_not_found_error(path: str):
        print(f'File not found at {path}')
        print('Please download the required file from https://github.com/KichangKim/DeepDanbooru')
        sys.exit()

    def classify_image(self, image_path: str) -> tuple[str, list[str], list[str]]:
        try:
            image = self.load_image(image_path)
        except IOError:
            return 'fail', [], []

        results = self.model.predict(np.array([image]))

        if results.shape[1] != self.tags.shape[0]:
            print("Mismatch between model output and number of tags!")
            return 'fail', [], []

        result_tags = self.get_result_tags(results.reshape(-1))

        tags = [tag for tag in result_tags.keys() if tag in self.metadata_tags]
        characters = [tag for tag in result_tags.keys() if tag in self.characters]

        return 'success', tags, characters

    def load_image(self, image_path: str) -> np.ndarray:
        image = Image.open(image_path).convert('RGB').resize(self.IMAGE_SIZE)
        return np.array(image) / 255.0

    def get_result_tags(self, results: np.ndarray) -> dict[str, float]:
        return {self.tags[i]: results[i] for i in range(len(self.tags)) if results[i] > self.THRESHOLD}
