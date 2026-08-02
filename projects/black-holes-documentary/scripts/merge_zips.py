"""
Merge all 18 black_holes_visuals_partN.zip files into one common folder.

Usage:
    1. Put this script in the same folder as all 18 downloaded
       black_holes_visuals_part*.zip files (from Claude's chat attachments).
    2. Run:  python3 merge_zips.py
    3. All 66 files land in a new folder called "black_holes_visuals/",
       named 001_... through 066_... matching cut_list.md.

No file will be overwritten or duplicated — every asset has a unique
numeric prefix (001-066), so extracting all parts into the same folder
is always safe.
"""
import glob
import os
import zipfile

OUT_DIR = "black_holes_visuals"

def main():
    zips = sorted(glob.glob("black_holes_visuals_part*.zip"))
    if not zips:
        print("No black_holes_visuals_part*.zip files found in this folder.")
        return

    os.makedirs(OUT_DIR, exist_ok=True)
    total = 0
    for zpath in zips:
        with zipfile.ZipFile(zpath) as z:
            z.extractall(OUT_DIR)
            total += len(z.namelist())
        print(f"Extracted {zpath}")

    print(f"\nDone. {total} files merged into ./{OUT_DIR}/")

if __name__ == "__main__":
    main()
