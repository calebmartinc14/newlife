"""Generate responsive WebP copies of the real-world reference photographs.

Optional dependency: python -m pip install Pillow==13.0.0
Run from any directory: python scripts/optimize_images.py
Use --download to import verified originals and refresh the local JPEG masters.
Sources, attribution, and image licenses are documented in docs/ASSET_CREDITS.md.
"""

import argparse
import hashlib
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageOps


ASSETS = Path(__file__).resolve().parents[1] / "dist" / "assets"
PHOTOS = {
    "prosthesis-use": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Hailey_Dawson_first_pitch_at_Orioles_Park%2C_August_2015.jpg",
        "sha1": "ec5b004f844e5b77fc0ad67eba6b63251c9c69e1",
        "crop": (0.52, 0.22, 1.0, 0.70),
    },
    "prosthesis-team": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/1/1d/Danny_Letain_et_l%27equipe_d%27ingenieur.jpg",
        "sha1": "8857c60866ba1a10810bd1a0c72f14cdf2965e22",
    },
}


def import_photo(name, metadata):
    request = Request(metadata["url"], headers={
        "User-Agent": "NewLife3D/1.0 (https://github.com/calebmartinc14/newlife; photo import)",
    })
    with urlopen(request, timeout=60) as response:
        data = response.read()
    # Match the source revision recorded by Wikimedia Commons, not a changed file.
    if hashlib.sha1(data).hexdigest() != metadata["sha1"]:
        raise ValueError(f"Source checksum changed for {name}; review the source before importing")
    with Image.open(BytesIO(data)) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        if "crop" in metadata:
            left, top, right, bottom = metadata["crop"]
            image = image.crop((
                round(left * image.width), round(top * image.height),
                round(right * image.width), round(bottom * image.height),
            ))
        image = ImageOps.fit(image, (1536, 1024), Image.Resampling.LANCZOS)
        image.save(ASSETS / f"{name}.jpg", "JPEG", quality=90, optimize=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="Import the licensed reference photos")
    args = parser.parse_args()
    if args.download:
        for name, metadata in PHOTOS.items():
            import_photo(name, metadata)
    original_bytes = 0
    full_size_bytes = 0
    for name in PHOTOS:
        source = ASSETS / f"{name}.jpg"
        original_bytes += source.stat().st_size
        print(f"{source.name}: {source.stat().st_size:,} bytes")
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
