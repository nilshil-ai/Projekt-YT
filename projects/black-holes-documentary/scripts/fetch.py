import json
import os
import re
import sys
import time

import requests

from beats import BEATS

API_KEY = os.environ["PIXABAY_API_KEY"]
IMG_API = "https://pixabay.com/api/"
VID_API = "https://pixabay.com/api/videos/"
WPM = 150.0
WPS = WPM / 60.0

OUT_DIR = "downloads"
os.makedirs(OUT_DIR, exist_ok=True)


def fmt_ts(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(round(seconds % 60))
    if s == 60:
        m += 1
        s = 0
    return f"{m:02d}:{s:02d}"


def slugify(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_")[:50] or "clip"


def search_image(query):
    params = dict(key=API_KEY, q=query, image_type="photo", safesearch="true",
                  per_page=6, order="popular")
    for attempt in range(3):
        r = requests.get(IMG_API, params=params, timeout=20)
        if r.status_code == 429:
            time.sleep(2 ** attempt)
            continue
        r.raise_for_status()
        return r.json().get("hits", [])
    return []


def search_video(query):
    params = dict(key=API_KEY, q=query, safesearch="true", per_page=6, order="popular")
    for attempt in range(3):
        r = requests.get(VID_API, params=params, timeout=20)
        if r.status_code == 429:
            time.sleep(2 ** attempt)
            continue
        r.raise_for_status()
        return r.json().get("hits", [])
    return []


def download(url, dest):
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    with open(dest, "wb") as f:
        f.write(r.content)
    return os.path.getsize(dest)


def try_keywords(beat_type, keywords):
    """Try each keyword phrase in turn (most specific first), fall back
    to shorter/looser queries if nothing is found."""
    tried = []
    for kw in keywords:
        tried.append(kw)
        hits = search_video(kw) if beat_type == "Video" else search_image(kw)
        if hits:
            return kw, hits
    # Fallback: single most generic word from the first keyword phrase
    fallback = keywords[0].split()[0]
    if fallback not in tried:
        hits = search_video(fallback) if beat_type == "Video" else search_image(fallback)
        if hits:
            return fallback, hits
    return None, []


results = []
cum_words = 0.0

for i, beat in enumerate(BEATS, start=1):
    n_words = len(beat["text"].split())
    start = cum_words / WPS
    cum_words += n_words
    end = cum_words / WPS

    used_query, hits = try_keywords(beat["type"], beat["keywords"])

    entry = {
        "index": i,
        "start": fmt_ts(start),
        "end": fmt_ts(end),
        "text": beat["text"],
        "visual": beat["visual"],
        "type": beat["type"],
        "keywords": beat["keywords"],
        "notes": beat["notes"],
        "query_used": used_query,
        "downloaded": False,
    }

    if hits:
        hit = hits[0]
        if beat["type"] == "Video":
            video_files = hit.get("videos", {})
            file_info = video_files.get("medium") or video_files.get("small") or video_files.get("tiny")
            if file_info:
                ext = "mp4"
                fname = f"{i:03d}_{slugify(used_query)}.{ext}"
                dest = os.path.join(OUT_DIR, fname)
                try:
                    size = download(file_info["url"], dest)
                    entry.update(downloaded=True, file=fname, file_size=size,
                                 pixabay_page=hit.get("pageURL"), pixabay_id=hit.get("id"),
                                 tags=hit.get("tags"))
                except Exception as e:
                    entry["error"] = str(e)
        else:
            url = hit.get("largeImageURL") or hit.get("webformatURL")
            if url:
                fname = f"{i:03d}_{slugify(used_query)}.jpg"
                dest = os.path.join(OUT_DIR, fname)
                try:
                    size = download(url, dest)
                    entry.update(downloaded=True, file=fname, file_size=size,
                                 pixabay_page=hit.get("pageURL"), pixabay_id=hit.get("id"),
                                 tags=hit.get("tags"))
                except Exception as e:
                    entry["error"] = str(e)
    else:
        entry["error"] = "no hits found for any keyword variant"

    results.append(entry)
    status = "OK" if entry["downloaded"] else "MISS"
    print(f"[{i:03d}/{len(BEATS)}] {status:4s} type={beat['type']:5s} query='{used_query}' -> {entry.get('file','')}")

with open("manifest.json", "w") as f:
    json.dump(results, f, indent=2)

n_ok = sum(1 for r in results if r["downloaded"])
print(f"\nDone: {n_ok}/{len(results)} downloaded successfully.")
