# inferencers/dummy_inferencer.py

import random
from PIL import Image
from .base_inferencer import BaseInferencer

class DummyInferencer(BaseInferencer):
    
    def predict(self, image: Image.Image):
        
        fake_prob = random.random()
        
        return {
            'real_prob' : 1 - fake_prob,
            'fake_prob' : fake_prob
        }