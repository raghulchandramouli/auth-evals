"""
What happens here?

Resize image to fixed resolution.

This file:
- Takes Image
- Resizes to (size, size)
- Returns resized image

Simulation:
- platform downscaling
- Distribution shift
"""
from PIL import Image
from .base_transform import BaseTransform

class ResizeTransform(BaseTransform):
    def __init__(self, size: int = 224):
        # We store the target size (height and width will be the same)
        self.size = (size, size)

    def apply(self, image: Image.Image) -> Image.Image:
        # Resizes the image to the target size. 
        # Image.LANCZOS is a high-quality downsampling filter.
        return image.resize(self.size, Image.LANCZOS)
      