"""
Turn a text PDF into an image-only "scanned" PDF for OCR testing.

Each page is rendered to a grey image, rotated slightly, blurred and sprinkled
with specks, then saved as a PDF with no text layer.

Usage:
    python3 make_scan.py input.pdf output.pdf

Needs: pdftoppm (poppler) and Pillow (pip install pillow)
"""
import glob
import random
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageFilter

DPI = 150          # scan resolution; real office scans are often 200-300
MAX_TILT = 0.8     # degrees of random rotation per page
BLUR = 0.6         # Gaussian blur radius
SPECK_RATE = 400   # one speck per this many pixels


def main(src: str, dst: str, seed: int = 3):
    random.seed(seed)  # same seed = same "scan" every time
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", str(DPI), "-gray", "-png", src, f"{tmp}/p"], check=True)
        pages = []
        for f in sorted(glob.glob(f"{tmp}/p-*.png")):
            im = Image.open(f).convert("L")
            im = im.rotate(random.uniform(-MAX_TILT, MAX_TILT), fillcolor=255, resample=Image.BICUBIC)
            im = im.filter(ImageFilter.GaussianBlur(BLUR))
            px = im.load()
            w, h = im.size
            for _ in range(w * h // SPECK_RATE):
                px[random.randrange(w), random.randrange(h)] = random.choice([90, 140, 200])
            pages.append(im.convert("RGB"))
    pages[0].save(dst, save_all=True, append_images=pages[1:], resolution=DPI)
    print(f"Saved {len(pages)} page(s) to {Path(dst).name}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
