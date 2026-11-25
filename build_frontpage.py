"""Render the 1024x1024 Tuesday 24 November 2026 world-news broadsheet to entry.png."""

from __future__ import annotations

import os
import re
import tempfile
from html import escape
from pathlib import Path
from typing import Dict, List

from PIL import Image
from playwright.sync_api import Browser, Playwright, sync_playwright

from data import (
    BRIEF_COLUMNS,
    DATE_CHECK_TEXT,
    EDITION_DATE,
    EDITION_DATE_SHORT,
    EPISTEMIC_COLORS,
    FIELD_COUNT,
    FOOTER_SOURCES,
    HERO_CARDS,
    MID_CARDS,
    REGION_COLORS,
    REGIONS,
    SUBHEAD,
    TIMELINE_ANCHORS,
    BriefItem,
    CardItem,
    validate_dataset,
)
from svg_scenes import build_scenes

REPO_DIR = Path(__file__).resolve().parent
OUTPUT_PNG = REPO_DIR / "entry.png"
MAX_PNG_BYTES = 275 * 1024

NUM_ACRONYM_RE = re.compile(r"(\b\d[\d,\.%+–-]*\b|\b[A-Z]{2,}\b)")


def style_headline(text: str) -> str:
    """Wrap numbers and acronyms in bold sans-serif 900-weight spans."""
    parts: List[str] = []
    last = 0
    for m in NUM_ACRONYM_RE.finditer(text):
        parts.append(escape(text[last : m.start()]))
        parts.append(f'<span class="hl-num">{escape(m.group(0))}</span>')
        last = m.end()
    parts.append(escape(text[last:]))
    return "".join(parts)


def format_date_check(text: str) -> str:
    """Highlight the 'Left out:' boundary inside the DATE CHECK bar."""
    marker = "Left out:"
    if marker in text:
        before, after = text.split(marker, 1)
        return f'<span class="dc-lead">{escape(before)}</span><strong class="dc-excl">{marker}</strong>{escape(after)}'
    return escape(text)


def render_card(card: CardItem, scenes: Dict[int, str], tier: str) -> str:
    reg_color = REGION_COLORS[card.region]
    epi_color = EPISTEMIC_COLORS[card.epistemic]
    cls = "hero-card" if tier == "hero" else "mid-card"
    return (
        f'<article class="card {cls}" style="border-top-color:{reg_color};">'
        f'  <div class="card-meta">'
        f'    <span class="num-badge" style="background:{reg_color};">{card.num}</span>'
        f'    <span class="kicker">{escape(card.kicker)}</span>'
        f'    <span class="epi-badge" style="background:{epi_color};">{escape(card.epistemic)}</span>'
        f'  </div>'
        f'  <div class="scene-wrap">{scenes[card.scene_id]}</div>'
        f'  <h2 class="headline">{style_headline(card.headline)}</h2>'
        f'  <p class="deck">{escape(card.deck)}</p>'
        f'  <div class="card-src">{escape(card.sources)}</div>'
        f'</article>'
    )


def render_brief_row(item: BriefItem) -> str:
    reg_color = REGION_COLORS[item.region]
    badge_html = ""
    if item.show_badge:
        epi_color = EPISTEMIC_COLORS[item.epistemic]
        badge_html = f'<span class="inline-claim" style="background:{epi_color};">{escape(item.epistemic)}</span>'
    return (
        f'<div class="b-row">'
        f'  <span class="b-num" style="background:{reg_color};">{item.num}</span>'
        f'  <span class="b-text"><strong class="b-lead">{escape(item.lead)}</strong> {escape(item.body)}</span>'
        f'  {badge_html}'
        f'</div>'
    )


def build_html() -> str:
    total, counts = validate_dataset()
    scenes = build_scenes()

    region_chips_html = "".join(
        f'<div class="reg-chip" style="background:{r.color};">'
        f'<span class="reg-name">{escape(r.label)}</span>'
        f'<span class="reg-cnt">{counts[r.key]}</span>'
        f'</div>'
        for r in REGIONS
    )

    timeline_html = "".join(
        f'<span class="tl-item"><strong class="tl-time">{escape(t)}</strong> {escape(lbl)}</span>'
        for t, lbl in TIMELINE_ANCHORS
    )

    heroes_html = "".join(render_card(c, scenes, "hero") for c in HERO_CARDS)
    mids_html = "".join(render_card(c, scenes, "mid") for c in MID_CARDS)

    briefs_cols_html = "".join(
        '<div class="b-col">' + "".join(render_brief_row(b) for b in col) + "</div>"
        for col in BRIEF_COLUMNS
    )

    legend_items = [
        ("CONFIRMED", "2+ outlets"),
        ("OFFICIAL", "on record"),
        ("REPORTED", "single wire/local"),
        ("CLAIM", "one side's word"),
    ]
    legend_html = ' <span class="leg-dot">·</span> '.join(
        f'<span class="leg-item"><span class="leg-tag" style="background:{EPISTEMIC_COLORS[k]};">{k}</span> = {escape(v)}</span>'
        for k, v in legend_items
    )

    meta_right = f"{total} DATED STORIES · {len(REGIONS)} REGIONS · {FIELD_COUNT} FIELDS · ALL FROM {EDITION_DATE_SHORT}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>{escape(EDITION_DATE)} — World News Broadsheet</title>
<style>
  *, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  html, body {{
    width: 1024px;
    height: 1024px;
    overflow: hidden;
    background: #FAF8F3;
    color: #0F172A;
    font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  .page {{
    width: 1024px;
    height: 1024px;
    overflow: hidden;
    background: #FAF8F3;
    padding: 6px 12px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  /* Header band */
  .header-band {{
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}
  .meta-bar {{
    height: 20px;
    background: #0F172A;
    padding: 0 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 2px;
  }}
  .meta-left {{
    color: #FACC15;
    font-size: 10.6px;
    font-weight: 900;
    letter-spacing: 0.85px;
    text-transform: uppercase;
  }}
  .meta-right {{
    color: #F8FAFC;
    font-size: 9.6px;
    font-weight: 800;
    letter-spacing: 0.35px;
    text-transform: uppercase;
  }}
  .masthead {{
    text-align: center;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 42px;
    font-weight: 700;
    line-height: 1.02;
    letter-spacing: -0.4px;
    color: #0F172A;
    padding-top: 2px;
  }}
  .subhead {{
    text-align: center;
    font-size: 11.4px;
    font-weight: 800;
    color: #991B1B;
    line-height: 1.18;
    letter-spacing: -0.18px;
    white-space: nowrap;
  }}
  .region-strip {{
    display: flex;
    gap: 3px;
    height: 19px;
  }}
  .reg-chip {{
    flex: 1;
    min-width: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    border-radius: 2px;
    color: #FFFFFF;
    font-size: 8.3px;
    font-weight: 800;
    letter-spacing: 0.15px;
    white-space: nowrap;
  }}
  .reg-cnt {{
    background: rgba(15, 23, 42, 0.28);
    padding: 0.5px 3.5px;
    border-radius: 2px;
    font-weight: 900;
  }}
  .utc-ribbon {{
    height: 20px;
    background: #0F172A;
    padding: 0 7px;
    border-radius: 2px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
  }}
  .utc-badge {{
    background: #F59E0B;
    color: #0F172A;
    font-size: 8.8px;
    font-weight: 900;
    padding: 1.5px 5px;
    border-radius: 2px;
    letter-spacing: 0.5px;
    flex-shrink: 0;
  }}
  .tl-items {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex: 1;
    gap: 6px;
  }}
  .tl-item {{
    color: #E2E8F0;
    font-size: 9.4px;
    font-weight: 600;
    white-space: nowrap;
  }}
  .tl-time {{
    color: #FACC15;
    font-weight: 900;
    margin-right: 2px;
  }}

  /* Shared card styling */
  .card {{
    background: #FFFFFF;
    border: 1px solid #D6CFC1;
    border-top-width: 3px;
    border-radius: 2px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    min-width: 0;
  }}
  .card-meta {{
    display: flex;
    align-items: center;
    gap: 4px;
    flex-shrink: 0;
  }}
  .num-badge {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    color: #FFFFFF;
    font-weight: 900;
    flex-shrink: 0;
  }}
  .kicker {{
    color: #334155;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.2px;
    white-space: nowrap;
    overflow: hidden;
    flex: 1;
    min-width: 0;
  }}
  .epi-badge {{
    color: #FFFFFF;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    border-radius: 2px;
    flex-shrink: 0;
  }}
  .scene-wrap {{
    flex-shrink: 0;
    line-height: 0;
  }}
  .scene-svg {{
    display: block;
    width: 100%;
  }}
  .headline {{
    font-family: Georgia, 'Times New Roman', serif;
    font-weight: 700;
    color: #020617;
  }}
  .hl-num {{
    font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
    font-weight: 900;
    font-size: 0.94em;
    letter-spacing: -0.2px;
    color: #020617;
  }}
  .deck {{
    color: #1E293B;
    font-weight: 500;
  }}
  .card-src {{
    margin-top: auto;
    color: #64748B;
    font-weight: 600;
    border-top: 1px solid #ECE7DC;
    padding-top: 2px;
    white-space: nowrap;
  }}

  /* Top Tier — 3 Hero Cards */
  .hero-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    height: 210px;
    flex-shrink: 0;
  }}
  .hero-card {{
    padding: 5px 6px 4px 6px;
  }}
  .hero-card .card-meta {{
    height: 17px;
    margin-bottom: 4px;
  }}
  .hero-card .num-badge {{
    width: 17px;
    height: 17px;
    font-size: 10px;
  }}
  .hero-card .kicker {{
    font-size: 8.8px;
  }}
  .hero-card .epi-badge {{
    font-size: 7.8px;
    padding: 1.5px 4px;
  }}
  .hero-card .scene-wrap {{
    margin-bottom: 4px;
  }}
  .hero-svg {{
    height: 78px;
  }}
  .hero-card .headline {{
    font-size: 15.8px;
    line-height: 1.11;
    margin-bottom: 3px;
  }}
  .hero-card .deck {{
    font-size: 11px;
    line-height: 1.22;
  }}
  .hero-card .card-src {{
    font-size: 8.6px;
  }}

  /* Section header */
  .sec-hdr {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    border-bottom: 1.5px solid #0F172A;
    padding-bottom: 1.5px;
    flex-shrink: 0;
  }}
  .sec-title {{
    font-size: 10.8px;
    font-weight: 900;
    letter-spacing: 0.6px;
    color: #0F172A;
    text-transform: uppercase;
  }}
  .sec-sub {{
    font-size: 9.2px;
    font-weight: 600;
    color: #475569;
  }}

  /* Middle Tier — 8 Regional Feature Cards */
  .mid-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 6px;
    height: 340px;
    flex-shrink: 0;
  }}
  .mid-card {{
    padding: 4px 4px 3px 4px;
  }}
  .mid-card .card-meta {{
    height: 15px;
    margin-bottom: 3px;
    gap: 3px;
  }}
  .mid-card .num-badge {{
    width: 15px;
    height: 15px;
    font-size: 8.8px;
  }}
  .mid-card .kicker {{
    font-size: 7.9px;
    letter-spacing: 0.1px;
  }}
  .mid-card .epi-badge {{
    font-size: 7.2px;
    padding: 1px 3.5px;
  }}
  .mid-card .scene-wrap {{
    margin-bottom: 3px;
  }}
  .mid-svg {{
    height: 52px;
  }}
  .mid-card .headline {{
    font-size: 12.8px;
    line-height: 1.12;
    margin-bottom: 2.5px;
  }}
  .mid-card .deck {{
    font-size: 10.2px;
    line-height: 1.19;
  }}
  .mid-card .card-src {{
    font-size: 8.2px;
  }}

  /* Lower Tier — 27 More Dated Stories */
  .briefs-box {{
    flex: 1;
    min-height: 0;
    background: #FFFFFF;
    border: 1px solid #D6CFC1;
    border-top: 2.5px solid #0F172A;
    border-radius: 2px;
    padding: 5px 7px 5px 7px;
    display: flex;
    flex-direction: column;
  }}
  .briefs-hdr {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    border-bottom: 1px solid #E2DDD2;
    padding-bottom: 3px;
    margin-bottom: 4px;
    flex-shrink: 0;
  }}
  .briefs-title {{
    font-size: 10.2px;
    font-weight: 900;
    letter-spacing: 0.45px;
    color: #0F172A;
    text-transform: uppercase;
  }}
  .briefs-sub {{
    font-size: 8.8px;
    font-weight: 600;
    color: #475569;
  }}
  .briefs-cols {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
    flex: 1;
    min-height: 0;
  }}
  .b-col {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-width: 0;
  }}
  .b-col:not(:first-child) {{
    padding-left: 6px;
    border-left: 1px solid #E2DDD2;
  }}
  .b-row {{
    display: flex;
    align-items: center;
    gap: 3.5px;
    height: 17.8px;
    line-height: 1;
    font-size: 10.9px;
    letter-spacing: -0.32px;
    white-space: nowrap;
    overflow: hidden;
    border-bottom: 1px dotted #E5E0D5;
  }}
  .b-col .b-row:last-child {{
    border-bottom: none;
  }}
  .b-num {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 14.5px;
    height: 14.5px;
    border-radius: 2px;
    color: #FFFFFF;
    font-size: 8.2px;
    font-weight: 900;
    letter-spacing: 0;
    flex-shrink: 0;
  }}
  .b-text {{
    color: #0F172A;
    white-space: nowrap;
  }}
  .b-lead {{
    color: #020617;
    font-weight: 800;
  }}
  .inline-claim {{
    display: inline-flex;
    align-items: center;
    color: #FFFFFF;
    font-size: 7.4px;
    font-weight: 900;
    letter-spacing: 0.2px;
    padding: 1.5px 3.5px;
    border-radius: 2px;
    flex-shrink: 0;
    margin-left: 1px;
  }}

  /* Exclusion Bar */
  .date-check {{
    background: #FEF2F2;
    border: 1.2px solid #DC2626;
    border-left: 4px solid #DC2626;
    border-radius: 2px;
    padding: 3px 7px;
    font-size: 9.0px;
    line-height: 1.24;
    font-weight: 500;
    color: #3B0707;
    flex-shrink: 0;
  }}
  .dc-tag {{
    display: inline-block;
    background: #DC2626;
    color: #FFFFFF;
    font-size: 8.0px;
    font-weight: 900;
    letter-spacing: 0.4px;
    padding: 1px 4.5px;
    border-radius: 2px;
    margin-right: 5px;
    vertical-align: 0.5px;
  }}
  .dc-lead {{
    font-weight: 700;
    color: #0F172A;
  }}
  .dc-excl {{
    color: #B91C1C;
    font-weight: 900;
  }}

  /* Footer bar */
  .footer-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 8.4px;
    color: #475569;
    padding-top: 1px;
    flex-shrink: 0;
  }}
  .leg-group {{
    display: flex;
    align-items: center;
    gap: 4px;
    white-space: nowrap;
  }}
  .leg-item {{
    display: inline-flex;
    align-items: center;
    gap: 3px;
  }}
  .leg-tag {{
    color: #FFFFFF;
    font-size: 7.3px;
    font-weight: 900;
    padding: 1px 3.5px;
    border-radius: 2px;
    letter-spacing: 0.25px;
  }}
  .leg-dot {{
    color: #94A3B8;
  }}
  .footer-src {{
    font-weight: 700;
    color: #334155;
    white-space: nowrap;
  }}
</style>
</head>
<body>
<div class="page">
  <header class="header-band">
    <div class="meta-bar">
      <span class="meta-left">THE WORLD IN ONE DAY</span>
      <span class="meta-right">{escape(meta_right)}</span>
    </div>
    <h1 class="masthead">{escape(EDITION_DATE)}</h1>
    <div class="subhead">{escape(SUBHEAD)}</div>
    <div class="region-strip">{region_chips_html}</div>
    <div class="utc-ribbon">
      <span class="utc-badge">UTC</span>
      <div class="tl-items">{timeline_html}</div>
    </div>
  </header>

  <section class="hero-grid" aria-label="Top stories">
    {heroes_html}
  </section>

  <div class="sec-hdr">
    <span class="sec-title">THE DAY IN 8 MORE</span>
    <span class="sec-sub">Regional &amp; thematic highlights across 6 regions</span>
  </div>

  <section class="mid-grid" aria-label="Regional highlights">
    {mids_html}
  </section>

  <section class="briefs-box" aria-label="27 more dated stories">
    <div class="briefs-hdr">
      <span class="briefs-title">ALSO ON TUESDAY 24 NOVEMBER — 27 MORE DATED STORIES</span>
      <span class="briefs-sub">9 regions matched by color · every item verified to Tue 24 Nov 2026</span>
    </div>
    <div class="briefs-cols">
      {briefs_cols_html}
    </div>
  </section>

  <aside class="date-check" aria-label="Date check">
    <span class="dc-tag">DATE CHECK</span>{format_date_check(DATE_CHECK_TEXT)}
  </aside>

  <footer class="footer-bar">
    <div class="leg-group">{legend_html}</div>
    <div class="footer-src">{escape(FOOTER_SOURCES)}</div>
  </footer>
</div>
</body>
</html>
"""


def launch_browser(p: Playwright) -> Browser:
    errors: List[str] = []
    for kwargs in ({}, {"channel": "msedge"}, {"channel": "chrome"}):
        try:
            return p.chromium.launch(headless=True, **kwargs)
        except Exception as exc:
            errors.append(f"{kwargs or 'default'}: {exc}")
    raise RuntimeError("Failed to launch Chromium:\n" + "\n".join(errors))


DOM_AUDIT_JS = """() => {
  const errs = [];
  const docEl = document.documentElement;
  if (docEl.scrollWidth > 1024 || docEl.scrollHeight > 1024) {
    errs.push(`Document overflow: ${docEl.scrollWidth}x${docEl.scrollHeight}`);
  }
  const page = document.querySelector('.page');
  if (page && (page.scrollWidth > 1024 || page.scrollHeight > 1024)) {
    errs.push(`Page overflow: ${page.scrollWidth}x${page.scrollHeight}`);
  }

  document.querySelectorAll('.hero-card, .mid-card').forEach((card, idx) => {
    if (card.scrollHeight > card.clientHeight + 0.5) {
      errs.push(`Card #${idx + 1} vertical overflow: scrollH=${card.scrollHeight} > clientH=${card.clientHeight}`);
    }
    if (card.scrollWidth > card.clientWidth + 0.5) {
      errs.push(`Card #${idx + 1} horizontal overflow: scrollW=${card.scrollWidth} > clientW=${card.clientWidth}`);
    }
  });

  const subhead = document.querySelector('.subhead');
  if (subhead && subhead.scrollWidth > subhead.clientWidth + 0.5) {
    errs.push(`Subhead overflow: scrollW=${subhead.scrollWidth} > clientW=${subhead.clientWidth}`);
  }

  document.querySelectorAll('.reg-chip').forEach((chip, idx) => {
    if (chip.scrollWidth > chip.clientWidth + 0.5) {
      errs.push(`Region chip #${idx + 1} overflow: ${chip.textContent.trim()}`);
    }
  });

  let maxRowH = 0;
  let maxRowRatio = 0;
  document.querySelectorAll('.b-row').forEach((row, idx) => {
    const rect = row.getBoundingClientRect();
    if (rect.height > maxRowH) maxRowH = rect.height;
    if (rect.height > 20.0) {
      errs.push(`Brief row #${idx + 1} height ${rect.height.toFixed(1)}px > 20px`);
    }
    if (row.scrollWidth > row.clientWidth + 0.5) {
      errs.push(`Brief row #${idx + 1} clipped: scrollW=${row.scrollWidth} > clientW=${row.clientWidth} (${row.textContent.trim()})`);
    }
    const ratio = row.scrollWidth / Math.max(1, row.clientWidth);
    if (ratio > maxRowRatio) maxRowRatio = ratio;
  });

  document.querySelectorAll('svg.scene-svg').forEach((svg, idx) => {
    const vb = svg.viewBox.baseVal;
    const isHero = svg.classList.contains('hero-svg');
    const artLimit = isHero ? 108.0 : 68.0;
    const art = svg.querySelector('.scene-art');
    if (art) {
      const ab = art.getBBox();
      if (ab.x + ab.width > artLimit + 0.5) {
        errs.push(`SVG #${idx + 1} art crosses x=${artLimit}: right=${(ab.x + ab.width).toFixed(1)}`);
      }
    }
    svg.querySelectorAll('text').forEach((txt) => {
      const tb = txt.getBBox();
      if (tb.x < vb.x || tb.y < vb.y || (tb.x + tb.width) > (vb.x + vb.width) || (tb.y + tb.height) > (vb.y + vb.height)) {
        errs.push(`SVG #${idx + 1} text out of bounds: "${txt.textContent}"`);
      }
      const key = txt.getAttribute('data-pill-for');
      if (key) {
        const pill = svg.querySelector(`rect[data-pill="${key}"]`);
        if (pill) {
          const pb = pill.getBBox();
          const padL = tb.x - pb.x;
          const padR = (pb.x + pb.width) - (tb.x + tb.width);
          const padT = tb.y - pb.y;
          const padB = (pb.y + pb.height) - (tb.y + tb.height);
          const minPad = Math.min(padL, padR, padT, padB);
          if (minPad < 3.0) {
            errs.push(`SVG #${idx + 1} pill "${key}" padding ${minPad.toFixed(2)}px < 3px (L=${padL.toFixed(1)} R=${padR.toFixed(1)} T=${padT.toFixed(1)} B=${padB.toFixed(1)})`);
          }
        }
      }
    });
  });

  return {
    errs,
    docSize: [docEl.scrollWidth, docEl.scrollHeight],
    briefRows: document.querySelectorAll('.b-row').length,
    maxRowH: Number(maxRowH.toFixed(2)),
    maxRowRatio: Number(maxRowRatio.toFixed(3)),
  };
}"""


def main() -> None:
    html = build_html()
    raw_png = Path(tempfile.gettempdir()) / "news_frontpage_raw_20261124.png"
    preview_png = Path(tempfile.gettempdir()) / "news_frontpage_preview_300_20261124.png"

    with sync_playwright() as p:
        browser = launch_browser(p)
        try:
            page = browser.new_page(viewport={"width": 1024, "height": 1024}, device_scale_factor=1)
            page.set_content(html, wait_until="load")
            page.evaluate("() => document.fonts ? document.fonts.ready : Promise.resolve()")
            audit = page.evaluate(DOM_AUDIT_JS)
            page.screenshot(path=str(raw_png), type="png", clip={"x": 0, "y": 0, "width": 1024, "height": 1024})
        finally:
            browser.close()

    with Image.open(raw_png) as img:
        rgb = img.convert("RGB")
        assert rgb.size == (1024, 1024), f"Expected 1024x1024, got {rgb.size}"
        rgb.save(OUTPUT_PNG, format="PNG", optimize=True, compress_level=9)
        thumb = rgb.resize((300, 300), Image.Resampling.LANCZOS)
        thumb.save(preview_png, format="PNG", optimize=True, compress_level=9)

    try:
        os.remove(raw_png)
    except OSError:
        pass

    size_bytes = OUTPUT_PNG.stat().st_size
    size_kib = size_bytes / 1024.0
    print(f"DOM errs={audit['errs']}")
    print(
        f"DOM stats: doc={audit['docSize']} brief_rows={audit['briefRows']} "
        f"max_row_h={audit['maxRowH']}px max_row_ratio={audit['maxRowRatio']}"
    )
    print(f"Output: {OUTPUT_PNG} ({size_bytes} bytes / {size_kib:.2f} KiB, cap 275 KiB)")
    print(f"Preview (300x300): {preview_png}")

    if audit["errs"]:
        raise SystemExit(f"DOM audit failed with {len(audit['errs'])} error(s)")
    if size_bytes > MAX_PNG_BYTES:
        raise SystemExit(f"entry.png exceeds 275 KiB cap ({size_kib:.2f} KiB)")


if __name__ == "__main__":
    main()
