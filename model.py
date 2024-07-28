import sys
import os
import numpy as np
from PIL import Image
import tensorflow as tf


class DeepDanbooruModel:
    MODEL_PATH = "./model/model-resnet_custom_v3.h5"
    TAGS_PATH = "./model/tags.txt"
    IMAGE_SIZE = (512, 512)
    THRESHOLD = 0.4

    def __init__(self):
        self.model = self.load_model()
        self.tags = self.load_tags()

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
            print('Tags loaded successfully.')
        except Exception as e:
            print(f'Failed to load tags. Error: {e}')
            sys.exit()

        return tags

    @staticmethod
    def model_not_found_error(path: str):
        print(f'File not found at {path}')
        print('Please download the required file from https://github.com/KichangKim/DeepDanbooru')
        sys.exit()

    def classify_image(self, image_path: str) -> tuple[str, list[str]]:
        try:
            image = self.load_image(image_path)
        except IOError:
            return 'fail', []

        results = self.model.predict(np.array([image])).reshape(self.tags.shape[0])
        result_tags = self.get_result_tags(results)

        return 'success', list(result_tags.keys())

    def load_image(self, image_path: str) -> np.ndarray:
        image = Image.open(image_path).convert('RGB').resize(self.IMAGE_SIZE)
        return np.array(image) / 255.0

    def get_result_tags(self, results: np.ndarray) -> dict[str, float]:
        return {self.tags[i]: results[i] for i in range(len(self.tags)) if results[i] > self.THRESHOLD}
