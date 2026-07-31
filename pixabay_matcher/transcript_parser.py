"""Parse a transcript file into segments for image matching.

Supports plain .txt (paragraph/sentence based, no timing) and
.srt / .vtt (timestamped subtitle formats).
"""
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Segment:
    index: int
    text: str
    start: str = ""
    end: str = ""


_SRT_BLOCK_RE = re.compile(
    r"(\d+)\s*\n(\d{2}:\d{2}:\d{2}[,.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,.]\d{3})\s*\n(.*?)(?=\n\s*\n|\Z)",
    re.DOTALL,
)


def parse_srt_or_vtt(content: str) -> list[Segment]:
    segments = []
    for match in _SRT_BLOCK_RE.finditer(content):
        idx, start, end, text = match.groups()
        clean_text = " ".join(line.strip() for line in text.strip().splitlines())
        segments.append(Segment(index=int(idx), text=clean_text, start=start, end=end))
    return segments


def parse_plain_text(content: str) -> list[Segment]:
    # Split on blank lines first (paragraphs); fall back to sentence splitting
    # for a single unbroken block of text.
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", content) if p.strip()]
    if len(paragraphs) <= 1:
        sentences = re.split(r"(?<=[.!?])\s+", content.strip())
        paragraphs = [s.strip() for s in sentences if s.strip()]

    return [Segment(index=i + 1, text=p) for i, p in enumerate(paragraphs)]


def parse_transcript(path: str) -> list[Segment]:
    file_path = Path(path)
    content = file_path.read_text(encoding="utf-8")

    if file_path.suffix.lower() in (".srt", ".vtt"):
        segments = parse_srt_or_vtt(content)
        if segments:
            return segments

    return parse_plain_text(content)
