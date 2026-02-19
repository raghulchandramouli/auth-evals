"""
Build unified metadata CSV from arbitrarily nested folder or any strcture it may matter

Usage:
    Python build.py \
        --input-root <path/to/data> \
        --output-path <path/to/output.csv> \
        --source my_dataset \
        --split test \
        --compression none

Label inference (default):
    - if any path segment contains `fake` -> label 1
    - else if any path segment contains `real` -> label 0
    - else image is skipped (raises strict error), will be adding a mode of control
"""

from __future__ import annotations

import argparse, csv
from pathlib import Path
from typing import Iterable, Optional

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.bmp', ',tif', '.tiff', '.webp'}

def is_image(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in IMAGE_EXTS

def infer_label_from_path(path: Path) -> Optional[int]:
    parts = [p.lower() for p in path.parts]
    if any('fake' in p for p in parts):
        return 1
    if any('real' in p for p in parts):
        return 0
    return None

def infer_generator_from_path(path: Path) -> str:
    # The Inference will view() content from this path
    known = ['sdxl', 'dalle', 'midjourney', 'gan', 'stable-diffusion', 'flux']
    parts = [p.lower() for p in path.parts]
    
    for part in parts:
        for name in known:
            if name in part:
                return name
            
    return 'unknown'

def walk_images(root : Path) -> Iterable[Path]:
    for p in root.rglob('*'):
        if is_image(p):
            yield p
            
def build_rows(
    input_root    : Path,
    source        : str,
    split         : str,
    compression   : str,
    strict_labels : bool,
) -> list[dict]:
    
    rows: list[dict] = []
    skipped = 0
    
    for img_path in walk_images(input_root):
        rel   = img_path.relative_to(input_root)
        label = infer_label_from_path(rel)
        
        if label is None:
            if strict_label:
                raise ValueError(f'Could not infer label for {rel}')
             
            skipped += 1
            continue
        
        rows.append(
            {
                'image_path'  : str(img_path.resolve()),
                'label'       : label,
                'generator'   : infer_generator_from_path(rel),
                'source'      : source,
                'split'       : split,
                'compression' : compression,
            }
        )
        
    if skipped:
        print(f'Skipped {skipped} images due to missing labels')
    return rows

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Build metadata CSV from image directory'
    )
    
    parser.add_argument('--input-root', required=True, type=Path)
    parser.add_argument('--output-csv', required=True, type=Path)
    parser.add_argument('--source', default='unknown-dataset')
    parser.add_argument('--split', default='test')
    parser.add_argument('--compression', default='none')
    parser.add_argument(
        '--strict-labels',
        action='store_true',
        help='Raise error if label cannot be inferred'
    )

    args = parser.parse_args()
    input_root = args.input_root.resolve()
    output_csv = args.output_csv.resolve()
    
    if not input_root.exiest() or not input_root.is_dir():
        raise FileNotFoundError(f'Input root not found or not a directory: {input_root}')
    
    rows = build_rows(
        input_root    = input_root,
        source        = args.source,
        split         = args.split,
        compression   = args.compression,
        strict_labels = args.strict_labels,
    )
    
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open('w', newline="", encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['image_path', 'label', 'generator', 'source', 'split', 'compression']
        )
        writer.writeheader()
        writer.writerows(rows)
        
    print(f'Wrote {len(rows)} rows to {output_csv}')
    
if __name__ == '__main__':
    main()

