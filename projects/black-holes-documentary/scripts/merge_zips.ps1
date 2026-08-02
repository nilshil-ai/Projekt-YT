# Merge all 18 black_holes_visuals_partN.zip files into one folder (Windows).
#
# How to use:
#   1. Put this file in the same folder as all 18 downloaded
#      black_holes_visuals_part*.zip files.
#   2. Right-click merge_zips.ps1 -> "Run with PowerShell"
#      (if Windows blocks it, right-click -> Properties -> check "Unblock" -> OK, then try again)
#   3. All 66 files land in a new folder called "black_holes_visuals"
#      right next to the zips, named 001_... through 066_... matching cut_list.md.
#
# Uses only Expand-Archive, built into Windows 10/11 — nothing to install.

$ErrorActionPreference = "Stop"
$outDir = Join-Path $PSScriptRoot "black_holes_visuals"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$zips = Get-ChildItem -Path $PSScriptRoot -Filter "black_holes_visuals_part*.zip"
if ($zips.Count -eq 0) {
    Write-Host "No black_holes_visuals_part*.zip files found next to this script."
    exit
}

$total = 0
foreach ($zip in $zips) {
    Expand-Archive -Path $zip.FullName -DestinationPath $outDir -Force
    Write-Host "Extracted $($zip.Name)"
}

$total = (Get-ChildItem -Path $outDir -File).Count
Write-Host ""
Write-Host "Done. $total files merged into $outDir"
Write-Host "Open that folder, sort by Name, select all, and drag them onto the CapCut timeline."
