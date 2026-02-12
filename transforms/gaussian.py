"""
Applies Gaussian Blur

This file:
- Uses PIL ImageFilter
- Applies blur with specified radius
- Returns blurred Image

Simulate:
- Camera lensing
- Lens defects
- Focus issues

"""
from PIL import Image,ImageFilter
from .base_transform import BaseTransform

class GaussianBlurTransform(BaseTransform):
    def __init__(self, radius: float):
        self.radius = radius

    # Applies Gaussian blur to the input image using the specified radius.       
    def apply(self, image: Image.Image) -> Image.Image:
        return image.filter(ImageFilter.GaussianBlur(self.radius))

