"""Match and download Pixabay images for each segment of a transcript.

Usage:
    python main.py --transcript path/to/transcript.txt --output-dir images/

The Pixabay API key is read from the PIXABAY_API_KEY environment variable
(or a .env file in this directory) — never pass it as a CLI argument, since
that would leak it into your shell history.
"""
import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from transcript_parser import parse_transcript
from keyword_extractor import extract_query
from pixabay_client import search_images, download_image, PixabayError


def slugify(text: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in text)[:40].strip("_") or "image"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transcript", required=True, help="Path to transcript (.txt, .srt, or .vtt)")
    parser.add_argument("--output-dir", default="downloaded_images", help="Where to save images")
    parser.add_argument("--images-per-segment", type=int, default=1)
    parser.add_argument("--min-words", type=int, default=3, help="Skip segments shorter than this many words")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("PIXABAY_API_KEY")
    if not api_key:
        print("Error: set PIXABAY_API_KEY in your environment or a .env file.", file=sys.stderr)
        sys.exit(1)

    segments = parse_transcript(args.transcript)
    print(f"Parsed {len(segments)} segment(s) from {args.transcript}")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    for seg in segments:
        if len(seg.text.split()) < args.min_words:
            continue

        query = extract_query(seg.text)
        print(f"[segment {seg.index}] query: '{query}' — text: {seg.text[:60]}...")

        try:
            hits = search_images(query, api_key, per_page=args.images_per_segment)
        except PixabayError as e:
            print(f"  ! Pixabay error for segment {seg.index}: {e}", file=sys.stderr)
            continue

        if not hits:
            print(f"  ! No results for '{query}'")
            continue

        for i, hit in enumerate(hits):
            filename = f"seg{seg.index:04d}_{slugify(query)}_{i}.jpg"
            dest_path = out_dir / filename
            download_image(hit["largeImageURL"], str(dest_path))
            manifest.append({
                "segment": seg.index,
                "start": seg.start,
                "end": seg.end,
                "text": seg.text,
                "query": query,
                "file": filename,
                "pixabay_page": hit.get("pageURL"),
            })
            print(f"  -> saved {filename}")

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nDone. {len(manifest)} image(s) downloaded. Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
