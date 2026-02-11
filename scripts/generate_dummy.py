import os
import numpy as np
from PIL import Image
import pandas as pd

os.makedirs('databunch/dummy/images', exist_ok=True)

rows = []
for i in range(20):
    
    # generate random noise construction of RBG
    img = (np.random.rand(256, 256, 3) * 255).astype('uint8')
    image = Image.fromarray(img)
    
    path = f'databunch/dummy/images/img_{i}.jpg'
    image.save(path)
    
    label = np.random.randint(0, 2)
    
    rows.append({
        "image_path" : path,
        "label" : label,
        "generator" : "dummy_gen" if label == 1 else 'real',
        "source" : "dummy",
        "split" : "test",
        "compression" : "none"
    })

df = pd.DataFrame(rows)
df.to_csv('databunch/dummy/metadata.csv', index=False)

print(f"Dummy data generated and saved to databunch/dummy/metadata.csv")