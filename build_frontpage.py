"""Render the V4 38-story, 10-region, 25-field Tuesday 24 November 2026 broadsheet to entry.png."""

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
    EPISTEMIC_SHORT,
    FIELD_COUNT,
    FOOTER_RIGHT,
    HERO_CARDS,
    KEY_NUMBERS,
    MAP_PINS,
    MID_CARDS,
    REGION_COLORS,
    REGIONS,
    SUBHEAD,
    TIMELINE_ANCHORS,
    BriefItem,
    CardItem,
    validate_dataset,
)
from svg_scenes import build_scenes, build_world_map_svg

REPO_DIR = Path(__file__).resolve().parent
OUTPUT_PNG = REPO_DIR / "entry.png"
MAX_PNG_BYTES = 270 * 1024

NUM_ACRONYM_RE = re.compile(r"(\$?\b\d[\d,\.%+–-]*(?:bn|m|k)?\b|\bM\d+\.\d+\b|\b[A-Z]{2,}\b)")


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


def format_brief_body(body: str, highlight: str) -> str:
    if highlight and highlight in body:
        before, after = body.split(highlight, 1)
        return (
            f'{escape(before)}<span class="b-hi">{escape(highlight)}</span>{escape(after)}'
        )
    return escape(body)


def format_date_check(text: str) -> str:
    marker = "Left out:"
    if marker in text:
        before, after = text.split(marker, 1)
        return (
            f'<span class="dc-lead">{escape(before)}</span>'
            f'<strong class="dc-excl">{marker}</strong>{escape(after)}'
        )
    return escape(text)


def render_card(card: CardItem, scenes: Dict[int, str], tier: str) -> str:
    reg_color = REGION_COLORS[card.region]
    epi_color = EPISTEMIC_COLORS[card.epistemic]
    cls = "hero-card" if tier == "hero" else "mid-card"
    return (
        f'<article class="card {cls}" style="border-top-color:{reg_color};">'
        f'  <div class="card-meta">'
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
    epi_color = EPISTEMIC_COLORS[item.epistemic]
    short_tag = EPISTEMIC_SHORT[item.epistemic]
    body_html = format_brief_body(item.body, item.highlight)
    return (
        f'<div class="b-row">'
        f'  <span class="b-num" style="background:{reg_color};">{item.num}</span>'
        f'  <span class="b-text"><strong class="b-lead">{escape(item.lead)}</strong> {body_html} '
        f'<span class="b-src">{escape(item.source)}</span></span>'
        f'  <span class="b-tag" style="background:{epi_color};">{short_tag}</span>'
        f'</div>'
    )


def build_html() -> str:
    total, counts = validate_dataset()
    scenes = build_scenes()
    world_map_svg = build_world_map_svg(MAP_PINS)

    region_chips_html = "".join(
        f'<div class="reg-chip" style="background:{r.color};">'
        f'<span class="reg-name">{escape(r.label)}</span>'
        f'<span class="reg-cnt">{counts[r.key]}</span>'
        f'</div>'
        for r in REGIONS
    )

    timeline_html = ' <span class="tl-sep">·</span> '.join(
        f'<span class="tl-item"><strong class="tl-time">{escape(t)}</strong> {escape(lbl)}</span>'
        for t, lbl in TIMELINE_ANCHORS
    )

    numbers_html = "".join(
        f'<div class="num-cell">'
        f'<span class="num-val">{escape(val)}</span>'
        f'<span class="num-lbl">{escape(lbl)}</span>'
        f'</div>'
        for val, lbl in KEY_NUMBERS
    )

    heroes_html = "".join(render_card(c, scenes, "hero") for c in HERO_CARDS)
    mids_html = "".join(render_card(c, scenes, "mid") for c in MID_CARDS)

    briefs_cols_html = "".join(
        '<div class="b-col">' + "".join(render_brief_row(b) for b in col) + "</div>"
        for col in BRIEF_COLUMNS
    )

    map_legend_html = "".join(
        f'<div class="ml-item">'
        f'<span class="ml-dot" style="background:{r.color};"></span>'
        f'<span class="ml-name">{escape(r.label)}</span>'
        f'<span class="ml-cnt">{counts[r.key]}</span>'
        f'</div>'
        for r in REGIONS
    )

    legend_items = [
        ("CONFIRMED", "2+ outlets"),
        ("OFFICIAL", "on record"),
        ("REPORTED", "one outlet"),
        ("CLAIM", "one side"),
        ("ONGOING", "unfolding"),
    ]
    legend_html = ' <span class="leg-dot">·</span> '.join(
        f'<span class="leg-item"><span class="leg-tag" style="background:{EPISTEMIC_COLORS[k]};">{k}</span> ({escape(v)})</span>'
        for k, v in legend_items
    )

    meta_right = (
        f"{total} DATED STORIES · {len(REGIONS)} REGIONS · {FIELD_COUNT} FIELDS · ALL FROM {EDITION_DATE_SHORT}"
    )

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
    padding: 5px 11px;
    display: flex;
    flex-direction: column;
    gap: 2.5px;
  }}

  /* Header band */
  .header-band {{
    display: flex;
    flex-direction: column;
    gap: 2px;
    flex-shrink: 0;
  }}
  .meta-bar {{
    height: 16px;
    background: #FAF8F3;
    border-bottom: 1.5px solid #0F172A;
    padding: 0 2px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .meta-left {{
    color: #991B1B;
    font-size: 9.6px;
    font-weight: 800;
    letter-spacing: 0.75px;
    text-transform: uppercase;
  }}
  .meta-right {{
    color: #1E293B;
    font-size: 9.6px;
    font-weight: 800;
    letter-spacing: 0.25px;
    text-transform: uppercase;
  }}
  .masthead {{
    text-align: center;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 39px;
    font-weight: 700;
    line-height: 1.0;
    letter-spacing: -0.4px;
    color: #020617;
  }}
  .subhead {{
    text-align: center;
    font-size: 11px;
    font-weight: 800;
    color: #991B1B;
    line-height: 1.14;
    letter-spacing: -0.1px;
    white-space: nowrap;
  }}
  .region-strip {{
    display: flex;
    gap: 3px;
    height: 17px;
  }}
  .reg-chip {{
    flex: 1;
    min-width: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2.5px;
    border-radius: 2px;
    color: #FFFFFF;
    font-size: 8.2px;
    font-weight: 800;
    letter-spacing: -0.12px;
    white-space: nowrap;
  }}
  .reg-cnt {{
    background: rgba(15, 23, 42, 0.28);
    padding: 0.5px 2.5px;
    border-radius: 2px;
    font-weight: 900;
    font-variant-numeric: tabular-nums;
  }}

  /* Light-Mode Chronological UTC Strip */
  .utc-strip {{
    height: 19px;
    background: #F3EFE6;
    border: 1px solid #D6CFC1;
    border-radius: 2px;
    padding: 0 7px 0 4px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .utc-badge {{
    background: #991B1B;
    color: #FFFFFF;
    font-size: 8.4px;
    font-weight: 900;
    padding: 1px 5px;
    border-radius: 2px;
    letter-spacing: 0.5px;
    flex-shrink: 0;
  }}
  .tl-items {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex: 1;
    font-size: 10.4px;
    font-weight: 600;
    color: #0F172A;
    white-space: nowrap;
  }}
  .tl-time {{
    color: #991B1B;
    font-weight: 900;
    font-variant-numeric: tabular-nums;
    margin-right: 1.5px;
  }}
  .tl-sep {{
    color: #94A3B8;
    font-weight: 900;
  }}

  /* High-Impact IN NUMBERS Bar */
  .numbers-bar {{
    height: 31px;
    background: #FFFFFF;
    border: 1px solid #D6CFC1;
    border-radius: 2px;
    display: flex;
    align-items: stretch;
    overflow: hidden;
    flex-shrink: 0;
  }}
  .numbers-badge {{
    background: #0F172A;
    color: #FACC15;
    font-size: 8.6px;
    font-weight: 900;
    letter-spacing: 0.5px;
    padding: 0 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-transform: uppercase;
    white-space: nowrap;
    flex-shrink: 0;
  }}
  .numbers-cells {{
    flex: 1;
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    min-width: 0;
  }}
  .num-cell {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-left: 1px solid #E5E0D5;
    padding: 1px 4px;
    min-width: 0;
    line-height: 1.02;
  }}
  .num-val {{
    font-size: 14px;
    font-weight: 900;
    color: #020617;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.25px;
    white-space: nowrap;
  }}
  .num-lbl {{
    font-size: 8.1px;
    font-weight: 600;
    color: #475569;
    white-space: nowrap;
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
    justify-content: space-between;
    gap: 4px;
    flex-shrink: 0;
  }}
  .kicker {{
    color: #334155;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.2px;
    white-space: nowrap;
    overflow: hidden;
    min-width: 0;
  }}
  .epi-badge {{
    color: #FFFFFF;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.25px;
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
    font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
    font-weight: 800;
    color: #0F172A;
  }}
  .hl-num {{
    font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
    font-weight: 900;
    font-variant-numeric: tabular-nums;
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
    font-size: 8.4px;
    border-top: 1px solid #ECE7DC;
    padding-top: 1.5px;
    white-space: nowrap;
  }}

  /* Top Tier — 3 Hero Lead Cards */
  .hero-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
    height: 212px;
    flex-shrink: 0;
  }}
  .hero-card {{
    background: #FFFDF9;
    border-top-width: 3.5px;
    padding: 3.5px 5px 3px 5px;
  }}
  .hero-card .card-meta {{
    height: 14px;
    margin-bottom: 2.5px;
  }}
  .hero-card .kicker {{
    font-size: 8.8px;
  }}
  .hero-card .epi-badge {{
    font-size: 7.4px;
    padding: 1px 4px;
  }}
  .hero-card .scene-wrap {{
    margin-bottom: 3.5px;
  }}
  .hero-svg {{
    height: 84px;
  }}
  .hero-card .headline {{
    font-size: 17.4px;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.15px;
    margin-bottom: 3px;
  }}
  .hero-card .deck {{
    font-size: 10.3px;
    line-height: 1.19;
  }}

  /* Middle Tier — 10 Sleek Open-Canvas Mid Cards (5x2 grid) */
  .mid-grid {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 5px;
    height: 306px;
    flex-shrink: 0;
  }}
  .mid-card {{
    background: #FFFFFF;
    padding: 2.5px 4px 2.5px 4px;
  }}
  .mid-card .card-meta {{
    height: 13px;
    margin-bottom: 2px;
  }}
  .mid-card .kicker {{
    font-size: 7.6px;
    letter-spacing: 0.1px;
  }}
  .mid-card .epi-badge {{
    font-size: 6.8px;
    padding: 0.8px 3px;
  }}
  .mid-card .scene-wrap {{
    margin-bottom: 2.5px;
  }}
  .mid-svg {{
    height: 50px;
  }}
  .mid-card .headline {{
    font-size: 12.7px;
    font-weight: 800;
    line-height: 1.12;
    letter-spacing: -0.15px;
    margin-bottom: 2px;
  }}
  .mid-card .deck {{
    font-size: 9.2px;
    line-height: 1.15;
  }}

  /* Lower Tier — 25 Briefs + World Locator Map */
  .lower-grid {{
    flex: 1;
    min-height: 0;
    display: grid;
    grid-template-columns: 1fr 274px;
    gap: 6px;
  }}
  .panel-box {{
    background: #FFFFFF;
    border: 1px solid #D6CFC1;
    border-top: 2.5px solid #0F172A;
    border-radius: 2px;
    padding: 4px 6px;
    display: flex;
    flex-direction: column;
    min-height: 0;
    overflow: hidden;
  }}
  .panel-hdr {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    border-bottom: 1px solid #E2DDD2;
    padding-bottom: 2px;
    margin-bottom: 3px;
    flex-shrink: 0;
  }}
  .panel-title {{
    font-size: 9.8px;
    font-weight: 900;
    letter-spacing: 0.35px;
    color: #0F172A;
    text-transform: uppercase;
  }}
  .panel-sub {{
    font-size: 8.2px;
    font-weight: 700;
    color: #475569;
  }}

  /* Left Panel: 25 upright single-line briefs (13 Col A + 12 Col B) */
  .briefs-cols {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 6px;
    flex: 1;
    min-height: 0;
  }}
  .b-col {{
    display: flex;
    flex-direction: column;
    gap: 1.8px;
    min-width: 0;
  }}
  .b-col:not(:first-child) {{
    padding-left: 6px;
    border-left: 1px solid #E2DDD2;
  }}
  .b-row {{
    display: flex;
    align-items: center;
    gap: 4px;
    height: 18px;
    line-height: 1.3;
    font-style: normal;
    font-size: 9.85px;
    letter-spacing: -0.1px;
    white-space: nowrap;
    overflow: hidden;
    border-bottom: 1px dotted #EAE5DA;
  }}
  .b-col .b-row:last-child {{
    border-bottom: none;
  }}
  .b-num {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 17px;
    height: 14px;
    border-radius: 2px;
    color: #FFFFFF;
    font-size: 8.2px;
    font-weight: 900;
    font-variant-numeric: tabular-nums;
    letter-spacing: 0;
    flex-shrink: 0;
  }}
  .b-text {{
    color: #0F172A;
    font-style: normal;
    white-space: nowrap;
    flex: 1;
    min-width: 0;
    overflow: hidden;
  }}
  .b-lead {{
    color: #020617;
    font-weight: 800;
    font-style: normal;
  }}
  .b-hi {{
    font-weight: 900;
    font-variant-numeric: tabular-nums;
    color: #020617;
  }}
  .b-src {{
    font-size: 8.8px;
    font-weight: 600;
    font-style: normal;
    color: #475569;
  }}
  .b-tag {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 15px;
    height: 13px;
    padding: 0 3px;
    border-radius: 2px;
    color: #FFFFFF;
    font-size: 7.4px;
    font-weight: 900;
    letter-spacing: 0.1px;
    flex-shrink: 0;
  }}

  /* Right Panel: World Locator Map + 2-column 10-region legend ONLY */
  .map-panel {{
    padding: 4px 5.5px;
  }}
  .world-map-wrap {{
    flex: 1;
    min-height: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 4px;
  }}
  .world-map-svg {{
    width: 100%;
    max-height: 100%;
    height: auto;
    display: block;
  }}
  .map-legend {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 3px 6px;
    padding-top: 4px;
    border-top: 1px solid #E2DDD2;
    flex-shrink: 0;
  }}
  .ml-item {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 8.2px;
    font-weight: 800;
    color: #1E293B;
    white-space: nowrap;
  }}
  .ml-dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
  }}
  .ml-name {{
    letter-spacing: 0.1px;
  }}
  .ml-cnt {{
    color: #020617;
    font-weight: 900;
    font-variant-numeric: tabular-nums;
  }}

  /* Exclusion Bar */
  .date-check {{
    background: #FEF2F2;
    border: 1.2px solid #DC2626;
    border-left: 4px solid #DC2626;
    border-radius: 2px;
    padding: 2.5px 7px;
    font-size: 9.3px;
    line-height: 1.2;
    font-weight: 600;
    color: #3B0707;
    flex-shrink: 0;
  }}
  .dc-tag {{
    display: inline-block;
    background: #DC2626;
    color: #FFFFFF;
    font-size: 7.8px;
    font-weight: 900;
    letter-spacing: 0.4px;
    padding: 0.8px 4px;
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
    font-size: 8.1px;
    color: #475569;
    flex-shrink: 0;
  }}
  .leg-group {{
    display: flex;
    align-items: center;
    gap: 3px;
    white-space: nowrap;
  }}
  .leg-item {{
    display: inline-flex;
    align-items: center;
    gap: 2.5px;
  }}
  .leg-tag {{
    color: #FFFFFF;
    font-size: 7.0px;
    font-weight: 900;
    padding: 0.8px 3px;
    border-radius: 2px;
    letter-spacing: 0.2px;
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
    <div class="utc-strip">
      <span class="utc-badge">UTC</span>
      <div class="tl-items">{timeline_html}</div>
    </div>
  </header>

  <section class="numbers-bar" aria-label="In numbers">
    <div class="numbers-badge">IN NUMBERS</div>
    <div class="numbers-cells">{numbers_html}</div>
  </section>

  <section class="hero-grid" aria-label="Top stories">
    {heroes_html}
  </section>

  <section class="mid-grid" aria-label="Regional highlights">
    {mids_html}
  </section>

  <section class="lower-grid" aria-label="More dated stories and locator map">
    <div class="panel-box briefs-panel">
      <div class="panel-hdr">
        <span class="panel-title">ALSO ON TUESDAY 24 NOVEMBER · 25 MORE STORIES</span>
        <span class="panel-sub">C 2+ · O official · R wire · CL claim · ON ongoing</span>
      </div>
      <div class="briefs-cols">
        {briefs_cols_html}
      </div>
    </div>

    <aside class="panel-box map-panel" aria-label="Where it happened">
      <div class="panel-hdr">
        <span class="panel-title">WHERE IT HAPPENED</span>
        <span class="panel-sub">Pins 1–13</span>
      </div>
      <div class="world-map-wrap">{world_map_svg}</div>
      <div class="map-legend">{map_legend_html}</div>
    </aside>
  </section>

  <aside class="date-check" aria-label="Date check">
    <span class="dc-tag">DATE CHECK</span>{format_date_check(DATE_CHECK_TEXT)}
  </aside>

  <footer class="footer-bar">
    <div class="leg-group">{legend_html}</div>
    <div class="footer-src">{escape(FOOTER_RIGHT)}</div>
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

  document.querySelectorAll('.hero-card, .mid-card, .panel-box, .numbers-bar, .utc-strip').forEach((el, idx) => {
    if (el.scrollHeight > el.clientHeight + 0.5) {
      errs.push(`Box #${idx + 1} (${el.className}) vertical overflow: scrollH=${el.scrollHeight} > clientH=${el.clientHeight}`);
    }
    if (el.scrollWidth > el.clientWidth + 0.5) {
      errs.push(`Box #${idx + 1} (${el.className}) horizontal overflow: scrollW=${el.scrollWidth} > clientW=${el.clientWidth}`);
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
    if (rect.height > 19.0) {
      errs.push(`Brief row #${idx + 1} height ${rect.height.toFixed(1)}px > 19px`);
    }
    if (row.scrollWidth > row.clientWidth + 0.5) {
      errs.push(`Brief row #${idx + 1} clipped: scrollW=${row.scrollWidth} > clientW=${row.clientWidth}`);
    }
    const txt = row.querySelector('.b-text');
    if (txt && txt.scrollWidth > txt.clientWidth + 0.5) {
      errs.push(`Brief text #${idx + 1} clipped: scrollW=${txt.scrollWidth} > clientW=${txt.clientWidth} (${txt.textContent.trim()})`);
    }
    const ratio = txt ? txt.scrollWidth / Math.max(1, txt.clientWidth) : 0;
    if (ratio > maxRowRatio) maxRowRatio = ratio;
  });

  document.querySelectorAll('svg.scene-svg').forEach((svg, idx) => {
    const vb = svg.viewBox.baseVal;
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
          if (minPad < 1.0) {
            errs.push(`SVG #${idx + 1} pill "${key}" text not strictly contained (minPad=${minPad.toFixed(2)}px; L=${padL.toFixed(1)} R=${padR.toFixed(1)} T=${padT.toFixed(1)} B=${padB.toFixed(1)})`);
          }
        }
      }
    });
  });

  const pins = Array.from(document.querySelectorAll('.map-pin')).map((el) => ({
    num: Number(el.getAttribute('data-pin')),
    x: Number(el.getAttribute('data-x')),
    y: Number(el.getAttribute('data-y')),
  }));
  let minPinDist = Infinity;
  for (let i = 0; i < pins.length; i++) {
    for (let j = i + 1; j < pins.length; j++) {
      const d = Math.hypot(pins[i].x - pins[j].x, pins[i].y - pins[j].y);
      if (d < minPinDist) minPinDist = d;
      if (d < 17.0) {
        errs.push(`Map pins #${pins[i].num} & #${pins[j].num} distance ${d.toFixed(1)} < 17`);
      }
    }
  }

  return {
    errs,
    docSize: [docEl.scrollWidth, docEl.scrollHeight],
    briefRows: document.querySelectorAll('.b-row').length,
    maxRowH: Number(maxRowH.toFixed(2)),
    maxRowRatio: Number(maxRowRatio.toFixed(3)),
    pinCount: pins.length,
    minPinDist: Number(minPinDist.toFixed(2)),
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
        f"max_row_h={audit['maxRowH']}px max_row_ratio={audit['maxRowRatio']} "
        f"pins={audit['pinCount']} min_pin_dist={audit['minPinDist']}"
    )
    print(f"Output: {OUTPUT_PNG} ({size_bytes} bytes / {size_kib:.2f} KiB, cap 270 KiB)")
    print(f"Preview (300x300): {preview_png}")

    if audit["errs"]:
        raise SystemExit(f"DOM audit failed with {len(audit['errs'])} error(s)")
    if size_bytes > MAX_PNG_BYTES:
        raise SystemExit(f"entry.png exceeds 270 KiB cap ({size_kib:.2f} KiB)")


if __name__ == "__main__":
    main()
