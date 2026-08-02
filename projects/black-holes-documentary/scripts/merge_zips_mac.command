#!/bin/bash
# Merge all 18 black_holes_visuals_partN.zip files into one folder (Mac).
#
# How to use:
#   1. Put this file in the same folder as all 18 downloaded
#      black_holes_visuals_part*.zip files.
#   2. Double-click merge_zips_mac.command
#      (if Mac blocks it: right-click -> Open -> Open, once, to approve it)
#   3. All 66 files land in a new folder called "black_holes_visuals"
#      right next to the zips, named 001_... through 066_... matching cut_list.md.
#
# Uses only "unzip", already built into macOS — nothing to install.

cd "$(dirname "$0")"
mkdir -p black_holes_visuals

shopt -s nullglob
zips=(black_holes_visuals_part*.zip)
if [ ${#zips[@]} -eq 0 ]; then
    echo "No black_holes_visuals_part*.zip files found next to this script."
    read -p "Press Enter to close..."
    exit 1
fi

for z in "${zips[@]}"; do
    unzip -o -q "$z" -d black_holes_visuals
    echo "Extracted $z"
done

count=$(ls black_holes_visuals | wc -l | tr -d ' ')
echo ""
echo "Done. $count files merged into ./black_holes_visuals"
echo "Open that folder, sort by Name, select all, and drag them onto the CapCut timeline."
read -p "Press Enter to close..."
