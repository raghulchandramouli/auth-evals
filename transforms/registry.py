"""
What happens here?

- It takes in string
- Parse it
- Instantiates correct transform class
- Returns transformed objects

Example:
- Map 'clean' -> None
- Map 'jpeg, q=70' -> JPEGTransform(70)
- Map 'blur, q=1.5' -> GaussianTransform(1.5)
- Map 'resize, size=224' -> ResizeTransform(224)


"""
# Import the actual classes from your other files
from .gaussian import GaussianBlurTransform
from .jpeg import JPEGTransform
from .resize import ResizeTransform

# Mapping 'nicknames' to the actual Classes
TRANSFORM_REGISTRY = {
    "blur": GaussianBlurTransform,
    "jpeg": JPEGTransform,
    "resize": ResizeTransform
}

def get_transform(name: str, **kwargs):
    """
    Factory function to fetch and initialize a transform.
    Args:
        name: The string key (e.g., "blur")
        **kwargs: The parameters for that specific transform (e.g., radius=2.0)
    """
    # 1. Look up the class in the dictionary
    transform_class = TRANSFORM_REGISTRY.get(name.lower())
    
    # 2. If the class exists, create an instance with the provided arguments
    if transform_class:
        return transform_class(**kwargs)
    
    # 3. If it doesn't exist, return None or handle the error
    return None