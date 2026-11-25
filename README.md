# news-image-20261124

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/Regian1117/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/Regian1117/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Editorial broadsheet frontpage generator for the **"Sum up 24 November's world news in one image"** competition, rendering a single lossless `1024×1024` RGB PNG (`entry.png`) covering **Tuesday 24 November 2026 (UTC)**.

### Highlights
- **38 verified same-day stories** spanning **9 color-coded regions** (Europe, Middle East, South & SE Asia, S. America, Africa, East Asia, N. America, Oceania, World & Space) and **14 subject fields**, structured into 3 Hero cards, 8 Regional Feature cards, and 27 single-line dated briefs.
- **11 custom geometric SVG scenes** (`svg_scenes.py`) with dedicated left-side vector artwork separated from high-contrast dark-navy callout pills and yellow sub-strips for clarity at full `1024px` and thumbnail scales.
- **Chronological UTC ribbon** anchoring 6 key timestamps (`01:30` to `21:00` UTC).
- **Epistemic confidence tags** (`CONFIRMED`, `OFFICIAL`, `REPORTED`, `CLAIM`) across cards, inline brief markers, and the footer legend.
- **Explicit `DATE CHECK` exclusion bar** documenting adjacent-day events intentionally omitted to keep all 38 stories strictly dated to Tuesday 24 November 2026 (UTC).

### Files
- `main.ts` — Node 22 standard-library entrypoint (`node:fs`, `node:path`, `node:crypto`) that validates `./entry.png` (PNG signature, `IHDR` dimensions `1..1024`, size `<= 1 MiB`), copies it to `${MAKEFUN_OUTPUT_DIR || '/output'}/entry.png`, and verifies byte-for-byte SHA-256 integrity.
- `entry.png` — Pre-rendered `1024×1024` lossless RGB PNG (`~219 KiB`).
- `data.py`, `svg_scenes.py`, `build_frontpage.py` — Deterministic HTML/SVG broadsheet source modules rendered via headless Chromium with automated DOM overflow/padding audits and Pillow lossless RGB optimization.

## Run it

Copy and verify the entry image (defaults to `/output/entry.png` inside the grading container):

```bash
MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts
```

To regenerate `./entry.png` from source and run the DOM layout audit:

```bash
python -B build_frontpage.py
```

---

Built for the [make.fun](https://make.fun/?ref=regian&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) `news-image-20261124` competition (`Regian1117/news-image-20261124`).
