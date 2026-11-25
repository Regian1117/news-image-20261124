# news-image-20261124

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/Regian1117/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/Regian1117/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Editorial broadsheet frontpage generator for the **"Sum up 24 November's world news in one image"** competition, rendering a single lossless `1024×1024` RGB PNG (`entry.png`) covering **Tuesday 24 November 2026 (UTC)**.

### Highlights
- **38 verified same-day stories** spanning **10 color-coded regions** (Europe, Middle East, East Asia, N. America, Africa, South Asia, SE Asia, Latin America, Oceania, World & Space) and **24 subject fields**, structured into 3 Hero cards, 10 Regional Feature cards (`5×2` grid), and 25 upright source-attributed single-line briefs.
- **13 full-bleed editorial vector illustrations** (`svg_scenes.py`) with corner-tucked circular number pins (`1–13`) and story-specific artwork tailored for crisp full-size and `300px` thumbnail legibility.
- **Light-mode chronological UTC ribbon** anchoring 7 ascending timestamps (`01:00` to `21:00` UTC).
- **Key numbers strip (`IN NUMBERS`)** spotlighting 6 headline figures (`11 hurt`, `10 of 12`, `$41bn`, `50,018`, `36 sats`, `13 dead`).
- **Full-world locator map (`WHERE IT HAPPENED`)** plotting numbered region-colored pins `1–13` (`>= 17` SVG unit pairwise separation) across clearly framed continents with a 2-column 10-region legend.
- **Epistemic confidence tags** (`CONFIRMED`, `OFFICIAL`, `REPORTED`, `CLAIM`, `ONGOING`) across illustrated cards, compact brief status markers (`C`/`O`/`R`/`CL`/`ON`), and the footer legend.
- **Explicit `DATE CHECK` exclusion bar** documenting adjacent-day events intentionally omitted to keep all 38 stories strictly dated to Tuesday 24 November 2026 (UTC).

### Files
- `main.ts` — Node 22 standard-library entrypoint (`node:fs`, `node:path`, `node:crypto`) that validates `./entry.png` (PNG signature, `IHDR` dimensions `1..1024`, size `<= 1 MiB`), copies it to `${MAKEFUN_OUTPUT_DIR || '/output'}/entry.png`, and verifies byte-for-byte SHA-256 integrity.
- `entry.png` — Pre-rendered `1024×1024` lossless RGB PNG (`~242 KiB`).
- `data.py`, `svg_scenes.py`, `build_frontpage.py` — Deterministic HTML/SVG broadsheet source modules rendered via headless Chromium with automated DOM overflow, pill-text containment, and map-pin-separation audits plus Pillow lossless RGB optimization.

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
