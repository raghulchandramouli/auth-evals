"""
Defines the interface contract.

This file:
- Creates an abstract base class
- Forces every transform to implement `.apply(image)`
- Standarsizes behaviour

Why?
- so evaluator can treat all transforms the same way.

Just pure structure
"""
from abc import ABC, abstractmethod
from PIL import image
class BaseTransform(ABC):

    # Every transform must implement this method
    @abstractmethod
    def apply(self, image: image.image) -> image.image:
        pass