"""
Implements JPEG compression corruption.

This file:
- takes a PIL image
- saves it to memory buffer
- Re-loads it with specified quality
- Returns degraded images

Just Image in -> image out
"""
import io
from PIL import Image
from .base_transform import BaseTransform

class JPEGTransform(BaseTransform):
    def __init__(self, quality: int = 75):
        # quality is an integer from 1 to 95
        self.quality = quality

    def apply(self, image: Image.Image) -> Image.Image:
        # JPEG doesn't support 'RGBA' (transparency), so we convert to RGB
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        # Create a virtual file in RAM
        buffer = io.BytesIO()
        
        # Save the image into that virtual file with the chosen quality
        image.save(buffer, format="JPEG", quality=self.quality)
        
        # Rewind the "file pointer" to the start so we can read it
        buffer.seek(0)
        
        # Return the new, compressed image object
        return Image.open(buffer)