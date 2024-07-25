import sys
import os
import numpy as np
import tensorflow as tf
import PIL
import h5py

class DeepDanbooruModel:
    def __init__(self):
        self.model = self.load_model()

    def load_model(self):
        print('Loading model...')
        model_path = "./model/model-resnet_custom_v3.h5"
        if not os.path.exists(model_path):
            print(f'Model file not found at {model_path}')
            print('Please download it from https://github.com/KichangKim/DeepDanbooru')
            sys.exit()

        try:
            # Directly load the model using the file path
            model = tf.keras.models.load_model(model_path, compile=False)
        except Exception as e:
            print(f'Failed to load the model. Error: {e}')
            sys.exit()

        tags_path = "./model/tags.txt"
        if not os.path.exists(tags_path):
            print(f'Tags file not found at {tags_path}')
            sys.exit()

        with open(tags_path, 'r') as tags_stream:
            self.tags = np.array([tag.strip() for tag in tags_stream if tag.strip()])

        print('Model loaded successfully. Tags added.')
        return model

    def classify_image(self, image_path):
        try:
            image = np.array(PIL.Image.open(image_path).convert('RGB').resize((512, 512))) / 255.0
        except IOError:
            return 'fail', []

        results = self.model.predict(np.array([image])).reshape(self.tags.shape[0])
        result_tags = {}
        for i in range(len(self.tags)):
            if results[i] > 0.4:
                result_tags[self.tags[i]] = results[i]

        return 'success', list(result_tags.keys())
