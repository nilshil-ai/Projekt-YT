"""Turn a transcript segment's text into a short Pixabay search query."""
import re

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then", "so", "of", "to", "in",
    "on", "at", "by", "for", "with", "about", "against", "between", "into",
    "through", "during", "before", "after", "above", "below", "from", "up",
    "down", "is", "are", "was", "were", "be", "been", "being", "have", "has",
    "had", "do", "does", "did", "will", "would", "shall", "should", "can",
    "could", "may", "might", "must", "this", "that", "these", "those", "i",
    "you", "he", "she", "it", "we", "they", "them", "his", "her", "its",
    "our", "your", "their", "what", "which", "who", "whom", "as", "not",
    "no", "there", "here", "when", "where", "why", "how", "all", "each",
    "just", "also", "very", "really", "even", "now", "than", "too", "such",
    "one", "two", "three", "some", "more", "most", "other", "into", "over",
}

# Small bias list for a space-themed channel — nudges extraction toward
# on-topic terms when a segment mentions them. Edit freely for your niche.
PRIORITY_TERMS = {
    "space", "galaxy", "galaxies", "star", "stars", "planet", "planets",
    "nebula", "moon", "sun", "solar", "orbit", "astronaut", "rocket",
    "telescope", "universe", "asteroid", "comet", "black hole", "nasa",
    "spacecraft", "satellite", "mars", "jupiter", "saturn", "venus",
    "mercury", "neptune", "uranus", "pluto", "milky way", "supernova",
    "cosmos", "gravity", "meteor", "eclipse", "spacex", "iss",
}


def _candidate_phrases(text: str) -> list[str]:
    # Capitalized multi-word phrases (e.g. "Milky Way", "James Webb") first.
    phrases = re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b", text)
    return [p.lower() for p in phrases]


def extract_query(text: str, max_words: int = 3) -> str:
    text_lower = text.lower()

    for phrase in PRIORITY_TERMS:
        if " " in phrase and phrase in text_lower:
            return phrase

    phrases = _candidate_phrases(text)
    if phrases:
        return phrases[0]

    words = re.findall(r"[a-zA-Z']+", text_lower)
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]

    if not words:
        return text_lower.strip()[:50] or "space"

    def score(word: str) -> tuple:
        return (word in PRIORITY_TERMS, len(word))

    ranked = sorted(set(words), key=score, reverse=True)
    return " ".join(ranked[:max_words])
