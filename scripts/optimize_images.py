"""Generate responsive WebP copies; originals remain the editable masters.

Optional dependency: python -m pip install Pillow==13.0.0
Run from any directory: python scripts/optimize_images.py
"""

from pathlib import Path

from PIL import Image, ImageOps


ASSETS = Path(__file__).resolve().parents[1] / "dist" / "assets"


def main():
    original_bytes = 0
    full_size_bytes = 0
    for name in ("prosthesis", "workshop"):
        source = ASSETS / f"{name}.png"
        original_bytes += source.stat().st_size
        with Image.open(source) as image:
            image = ImageOps.exif_transpose(image).convert("RGB")
            for width in (640, 1024, 1536):
                size = (width, round(image.height * width / image.width))
                resized = image.resize(size, Image.Resampling.LANCZOS)
                target = ASSETS / f"{name}-{width}.webp"
                resized.save(target, "WEBP", quality=82, method=6)
                count = target.stat().st_size
                if width == 1536:
                    full_size_bytes += count
                print(f"{target.name}: {size[0]}x{size[1]}, {count:,} bytes")
    print(f"Full-size pair: {original_bytes:,} -> {full_size_bytes:,} bytes "
          f"({1 - full_size_bytes / original_bytes:.1%} smaller)")


if __name__ == "__main__":
    main()
