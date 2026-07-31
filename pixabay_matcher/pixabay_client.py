"""Thin wrapper around the Pixabay image search/download API."""
import time
import requests

API_URL = "https://pixabay.com/api/"


class PixabayError(Exception):
    pass


def search_images(query: str, api_key: str, per_page: int = 3, image_type: str = "photo") -> list[dict]:
    params = {
        "key": api_key,
        "q": query,
        "image_type": image_type,
        "safesearch": "true",
        "per_page": max(per_page, 3),  # Pixabay requires per_page >= 3
        "order": "popular",
    }

    for attempt in range(3):
        response = requests.get(API_URL, params=params, timeout=15)
        if response.status_code == 429:
            time.sleep(2 ** attempt)
            continue
        if response.status_code != 200:
            raise PixabayError(f"Pixabay API error {response.status_code}: {response.text[:200]}")
        return response.json().get("hits", [])[:per_page]

    raise PixabayError("Pixabay API rate limit exceeded after retries")


def download_image(url: str, dest_path: str) -> None:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    with open(dest_path, "wb") as f:
        f.write(response.content)
