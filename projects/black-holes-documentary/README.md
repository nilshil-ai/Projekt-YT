# Black Holes Documentary — Pixabay Visual Package

Editorial B-roll/image plan for the "what is a black hole" explainer
transcript, plus the actual assets downloaded from Pixabay for each beat.

- `transcript.txt` — the source script.
- `editing_plan.md` — the full shot list: 66 beats, each with an estimated
  timestamp, transcript excerpt, recommended visual, type (video/image),
  Pixabay search keywords, editorial notes, and the actual downloaded
  file + Pixabay source link.
- `manifest.json` — the same data in machine-readable form.
- `scripts/beats.py` — the curated beat definitions (text, visual,
  type, keywords, notes) used to drive the fetch.
- `scripts/fetch.py` — downloads the best-matching Pixabay hit for each
  beat (reads `PIXABAY_API_KEY` from the environment). A handful of beats
  were manually re-picked afterward to fix bad keyword collisions and
  duplicate assets — see `fix_note` in `manifest.json` for the ones that
  changed from the script's first automatic pick.
- `downloads/` (gitignored) — the actual downloaded media, created by
  running `scripts/fetch.py`.

Timestamps assume ~150 words/minute narration; re-sync against the real
voiceover once recorded.
