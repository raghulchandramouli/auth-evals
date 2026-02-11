from abc import ABC, abstractmethod
from PIL import Image

class BaseInferencer(ABC):
    
    @abstractmethod
    def predict(self, image: Image.Image) -> dict:
        """
        Use : Predicts the probability of the Image being real or Fake.
        
        Args: 
            image (Image.Image) : The image to predict.
        Returns:
            dict: A dictionary containing the probability of the image being real or fake.
        """
        
        pass