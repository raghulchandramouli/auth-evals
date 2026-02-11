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