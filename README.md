# 🀄 Top 100 Chinese Characters — Flashcards

A study set for the 100 most common Chinese characters, built end-to-end with [Claude Code](https://claude.com/claude-code). It comes in two forms:

1. **A standalone web flashcard app** (`index.html`) — open it in any browser, nothing to install.
2. **An Anki deck** (`chinese-flashcards.apkg`) — import into Anki for spaced-repetition review on any device, with audio.

🌐 **Live site:** **https://subiqian.github.io/chinese-flashcards/**

## What's on each card

| Field | Example |
|---|---|
| Character (hanzi) | 好 |
| Pinyin | hǎo / hào |
| Meaning | good; like |
| Frequency rank | #71 of 100 |
| Two example words | 你好 (nǐ hǎo, "hello"), 好吃 (hǎochī, "delicious") |

The Anki deck also includes **audio** for the character and both example words.

## The files

| File | Purpose |
|---|---|
| `index.html` | Self-contained web app — flip through all 100 cards in the browser. Uses the LXGW WenKai calligraphy font for beautiful character rendering. |
| `chinese-flashcards.apkg` | Importable Anki deck: 100 cards + ~300 audio clips, with a custom-styled card template (calligraphy font, color-coded pinyin). |
| `generate_anki_deck.py` | Builds the `.apkg` from the curated word list. |

## How the audio is made

No paid TTS API — the audio is generated **locally and for free** using macOS's built-in `say` command with the Mandarin voice **Tingting**, then converted to AAC/`.m4a` with `afconvert`. Three clips per card (the character + both example words).

## Built with Claude Code

The whole set was created interactively with Claude Code:

- Curated the **top-100 character list** with pinyin, meanings, frequency ranks, and two natural example words each (including tricky multi-reading characters like 为, 得, 着)
- Wrote the **`genanki` generator** with a custom card template — calligraphy font, large hanzi, color-coded pinyin, and a clean two-column example layout
- Added **per-card audio** generated from macOS text-to-speech (no API keys, no cost)
- Built a matching **standalone HTML app** so the same deck can be studied in a browser without Anki

## Using it

- **Web:** visit **https://subiqian.github.io/chinese-flashcards/** (or open `index.html` locally).
- **Anki:** install [Anki](https://apps.ankiweb.net/), then **File → Import → `chinese-flashcards.apkg`**. Audio plays automatically on the answer side.

## Regenerating the deck

```bash
pip3 install genanki
python3 generate_anki_deck.py
```

Audio clips are cached in `_anki_audio/`, so re-runs only generate what's missing. Requires macOS (for the `say` and `afconvert` commands).
