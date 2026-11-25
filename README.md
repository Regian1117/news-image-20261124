# news-image-20261124

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/Regian1117/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/Regian1117/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Editorial broadsheet frontpage generator for the **"Sum up 24 November's world news in one image"** competition, rendering a single lossless `1024×1024` RGB PNG (`entry.png`) covering **Tuesday 24 November 2026 (UTC)**.

### Highlights
- **38 verified same-day stories** spanning **10 color-coded regions** (Europe, Middle East, East Asia, N. America, Africa, South Asia, SE Asia, Latin America, Oceania, World & Space) and **25 subject fields** (including currency markets via Iran's record rial slide), structured into 3 warm-tinted Hero lead cards, 10 sleek open-canvas Mid cards (`5×2` grid), and 25 upright source-attributed single-line briefs.
- **Decluttered editorial header & high-impact typography** — warm newsprint hairline masthead bar, Georgia `39px` masthead paired with crisp bold sans-serif card headlines for distortion-free `300px` thumbnail OCR, light-mode UTC chronological ribbon (`01:00`–`21:00` UTC), and an upgraded `31px` `IN NUMBERS` bar (`14px` tabular-nums values: `11 hurt`, `10 of 12`, `$41bn`, `50,018`, `36 sats`, `13 dead`).
- **Two-tier editorial vector artwork** (`svg_scenes.py`) — 3 full-bleed Hero illustrations (`314×86`) and 10 open-canvas full-width Mid scenes (`186×50`) with corner pins (`1–13`) and compact top-right badge tags.
- **Full-world locator map (`WHERE IT HAPPENED`)** plotting region-colored circular pins `1–13` (`>= 17` SVG unit pairwise separation) across high-contrast continents with a tightly grouped inline 2-column 10-region legend.
- **Epistemic confidence tags** (`CONFIRMED`, `OFFICIAL`, `REPORTED`, `CLAIM`, `ONGOING`) across cards, brief status markers (`C`/`O`/`R`/`CL`/`ON`), and the footer legend.
- **Explicit `DATE CHECK` exclusion bar** (`9.3px` semibold) documenting adjacent-day events omitted to keep all 38 stories strictly dated to Tuesday 24 November 2026 (UTC).

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
