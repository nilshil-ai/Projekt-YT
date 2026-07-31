# Pixabay Transcript Image Matcher

Downloads Pixabay images that match each segment of a video transcript,
so you can drop them straight into your editing timeline.

## Setup

```bash
cd pixabay_matcher
pip install -r requirements.txt
cp .env.example .env
# edit .env and paste your Pixabay API key
```

## Usage

```bash
python main.py --transcript path/to/transcript.txt --output-dir images/
```

Supports plain `.txt` transcripts (split into paragraphs/sentences) and
timestamped `.srt`/`.vtt` files (split by subtitle cue).

Output:
- One or more images per segment, saved to `--output-dir`
- `manifest.json` in that folder mapping each segment (text, timestamp,
  search query used) to its downloaded file and Pixabay source page

## Options

- `--images-per-segment` (default 1): how many images to download per segment
- `--min-words` (default 3): skip segments shorter than this many words
