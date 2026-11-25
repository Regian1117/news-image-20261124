"""Render the 39-story Tuesday 24 November 2026 world-news broadsheet to entry.png."""

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

NUM_ACRONYM_RE = re.compile(r"(\$?\b\d[\d,\.%+–-]*(?:bn|m|k)?\b|\b[A-Z]{2,}\b)")


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
    world_map_svg = build_world_map_svg(MAP_PINS)

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

    pin_key_html = "".join(
        f'<span class="pk-item">'
        f'<span class="pk-num" style="background:{REGION_COLORS[p.region]};">{p.num}</span>'
        f'<span class="pk-place">{escape(p.place)}</span>'
        f'</span>'
        for p in MAP_PINS
    )

    map_legend_html = "".join(
        f'<span class="ml-item">'
        f'<span class="ml-dot" style="background:{r.color};"></span>'
        f'<span class="ml-name">{escape(r.key)}</span>'
        f'<span class="ml-cnt">{counts[r.key]}</span>'
        f'</span>'
        for r in REGIONS
    )

    legend_items = [
        ("CONFIRMED", "2+ outlets"),
        ("OFFICIAL", "on record"),
        ("REPORTED", "single wire"),
        ("CLAIM", "one side"),
    ]
    legend_html = ' <span class="leg-dot">·</span> '.join(
        f'<span class="leg-item"><span class="leg-tag" style="background:{EPISTEMIC_COLORS[k]};">{k}</span> = {escape(v)}</span>'
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
    padding: 5px 12px;
    display: flex;
    flex-direction: column;
    gap: 3.5px;
  }}

  /* Header band */
  .header-band {{
    display: flex;
    flex-direction: column;
    gap: 2.5px;
    flex-shrink: 0;
  }}
  .meta-bar {{
    height: 18px;
    background: #0F172A;
    padding: 0 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 2px;
  }}
  .meta-left {{
    color: #FACC15;
    font-size: 10.2px;
    font-weight: 900;
    letter-spacing: 0.85px;
    text-transform: uppercase;
  }}
  .meta-right {{
    color: #F8FAFC;
    font-size: 9.4px;
    font-weight: 800;
    letter-spacing: 0.35px;
    text-transform: uppercase;
  }}
  .masthead {{
    text-align: center;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 38px;
    font-weight: 700;
    line-height: 1.0;
    letter-spacing: -0.4px;
    color: #020617;
    padding-top: 1px;
  }}
  .subhead {{
    text-align: center;
    font-size: 11px;
    font-weight: 800;
    color: #991B1B;
    line-height: 1.15;
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
    gap: 3.5px;
    border-radius: 2px;
    color: #FFFFFF;
    font-size: 8.2px;
    font-weight: 800;
    letter-spacing: 0.12px;
    white-space: nowrap;
  }}
  .reg-cnt {{
    background: rgba(15, 23, 42, 0.28);
    padding: 0.5px 3px;
    border-radius: 2px;
    font-weight: 900;
  }}
  .utc-ribbon {{
    height: 18px;
    background: #0F172A;
    padding: 0 7px;
    border-radius: 2px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .utc-badge {{
    background: #F59E0B;
    color: #0F172A;
    font-size: 8.4px;
    font-weight: 900;
    padding: 1px 4.5px;
    border-radius: 2px;
    letter-spacing: 0.5px;
    flex-shrink: 0;
  }}
  .tl-items {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex: 1;
    gap: 4px;
  }}
  .tl-item {{
    color: #E2E8F0;
    font-size: 9.0px;
    font-weight: 600;
    white-space: nowrap;
  }}
  .tl-time {{
    color: #FACC15;
    font-weight: 900;
    margin-right: 1.5px;
  }}

  /* THE DAY IN NUMBERS bar */
  .numbers-bar {{
    height: 29px;
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
    font-size: 8.4px;
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
    line-height: 1.05;
  }}
  .num-val {{
    font-size: 11.4px;
    font-weight: 900;
    color: #020617;
    letter-spacing: -0.2px;
    white-space: nowrap;
  }}
  .num-lbl {{
    font-size: 8.0px;
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
    gap: 3.5px;
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
    letter-spacing: 0.15px;
    white-space: nowrap;
    overflow: hidden;
    flex: 1;
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
    padding-top: 1.5px;
    white-space: nowrap;
  }}

  /* Top Tier — 3 Hero Cards */
  .hero-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 7px;
    height: 190px;
    flex-shrink: 0;
  }}
  .hero-card {{
    padding: 4px 6px 3.5px 6px;
  }}
  .hero-card .card-meta {{
    height: 16px;
    margin-bottom: 3px;
  }}
  .hero-card .num-badge {{
    width: 16px;
    height: 16px;
    font-size: 9.5px;
  }}
  .hero-card .kicker {{
    font-size: 8.6px;
  }}
  .hero-card .epi-badge {{
    font-size: 7.5px;
    padding: 1px 3.8px;
  }}
  .hero-card .scene-wrap {{
    margin-bottom: 3.5px;
  }}
  .hero-svg {{
    height: 65px;
  }}
  .hero-card .headline {{
    font-size: 15.0px;
    line-height: 1.1;
    margin-bottom: 2.5px;
  }}
  .hero-card .deck {{
    font-size: 10.6px;
    line-height: 1.2;
  }}
  .hero-card .card-src {{
    font-size: 8.3px;
  }}

  /* Section header */
  .sec-hdr {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    border-bottom: 1.5px solid #0F172A;
    padding-bottom: 1px;
    flex-shrink: 0;
  }}
  .sec-title {{
    font-size: 10.4px;
    font-weight: 900;
    letter-spacing: 0.6px;
    color: #0F172A;
    text-transform: uppercase;
  }}
  .sec-sub {{
    font-size: 9.0px;
    font-weight: 600;
    color: #475569;
  }}

  /* Middle Tier — 8 Feature Cards */
  .mid-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 5px;
    height: 296px;
    flex-shrink: 0;
  }}
  .mid-card {{
    padding: 3.5px 4px 3px 4px;
  }}
  .mid-card .card-meta {{
    height: 14px;
    margin-bottom: 2.5px;
    gap: 3px;
  }}
  .mid-card .num-badge {{
    width: 14px;
    height: 14px;
    font-size: 8.5px;
  }}
  .mid-card .kicker {{
    font-size: 7.8px;
    letter-spacing: 0.08px;
  }}
  .mid-card .epi-badge {{
    font-size: 7.0px;
    padding: 1px 3.2px;
  }}
  .mid-card .scene-wrap {{
    margin-bottom: 2.5px;
  }}
  .mid-svg {{
    height: 46px;
  }}
  .mid-card .headline {{
    font-size: 12.2px;
    line-height: 1.1;
    margin-bottom: 2px;
  }}
  .mid-card .deck {{
    font-size: 9.8px;
    line-height: 1.18;
  }}
  .mid-card .card-src {{
    font-size: 8.0px;
  }}

  /* Lower Tier — 28 Briefs + World Locator Map */
  .lower-grid {{
    flex: 1;
    min-height: 0;
    display: grid;
    grid-template-columns: 1fr 240px;
    gap: 6px;
  }}
  .panel-box {{
    background: #FFFFFF;
    border: 1px solid #D6CFC1;
    border-top: 2.5px solid #0F172A;
    border-radius: 2px;
    padding: 4px 6.5px;
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
    letter-spacing: 0.4px;
    color: #0F172A;
    text-transform: uppercase;
  }}
  .panel-sub {{
    font-size: 8.4px;
    font-weight: 700;
    color: #475569;
  }}

  /* Left Panel: 2 cols x 14 single-line rows */
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
    height: 16.0px;
    line-height: 1;
    font-size: 10.2px;
    letter-spacing: -0.12px;
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
    width: 14px;
    height: 13.5px;
    border-radius: 2px;
    color: #FFFFFF;
    font-size: 8.0px;
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
    font-size: 7.2px;
    font-weight: 900;
    padding: 1px 3px;
    border-radius: 2px;
    flex-shrink: 0;
  }}

  /* Right Panel: World Locator Map + Pin Key + Region Legend */
  .map-panel {{
    padding: 4px 5.5px;
  }}
  .world-map-wrap {{
    line-height: 0;
    flex-shrink: 0;
    margin-bottom: 4px;
  }}
  .world-map-svg {{
    width: 100%;
    height: auto;
    display: block;
  }}
  .pin-key {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2.5px 4px;
    padding: 3.5px 0;
    border-top: 1px solid #ECE7DC;
    border-bottom: 1px solid #ECE7DC;
    margin-bottom: 4px;
    flex-shrink: 0;
  }}
  .pk-item {{
    display: inline-flex;
    align-items: center;
    gap: 3px;
    font-size: 8.1px;
    font-weight: 700;
    color: #1E293B;
    white-space: nowrap;
    min-width: 0;
  }}
  .pk-num {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 12.5px;
    height: 12.5px;
    border-radius: 50%;
    color: #FFFFFF;
    font-size: 7.4px;
    font-weight: 900;
    flex-shrink: 0;
  }}
  .pk-place {{
    overflow: hidden;
  }}
  .map-legend {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2px 5px;
    margin-top: auto;
  }}
  .ml-item {{
    display: inline-flex;
    align-items: center;
    gap: 3px;
    font-size: 7.9px;
    font-weight: 700;
    color: #334155;
    white-space: nowrap;
  }}
  .ml-dot {{
    width: 6.5px;
    height: 6.5px;
    border-radius: 50%;
    flex-shrink: 0;
  }}
  .ml-name {{
    flex: 1;
    min-width: 0;
  }}
  .ml-cnt {{
    color: #020617;
    font-weight: 900;
  }}

  /* Exclusion Bar */
  .date-check {{
    background: #FEF2F2;
    border: 1.2px solid #DC2626;
    border-left: 4px solid #DC2626;
    border-radius: 2px;
    padding: 2.5px 7px;
    font-size: 8.7px;
    line-height: 1.22;
    font-weight: 500;
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
    font-size: 8.2px;
    color: #475569;
    flex-shrink: 0;
  }}
  .leg-group {{
    display: flex;
    align-items: center;
    gap: 3.5px;
    white-space: nowrap;
  }}
  .leg-item {{
    display: inline-flex;
    align-items: center;
    gap: 2.5px;
  }}
  .leg-tag {{
    color: #FFFFFF;
    font-size: 7.2px;
    font-weight: 900;
    padding: 0.8px 3.2px;
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
    <div class="utc-ribbon">
      <span class="utc-badge">UTC</span>
      <div class="tl-items">{timeline_html}</div>
    </div>
  </header>

  <section class="numbers-bar" aria-label="The day in numbers">
    <div class="numbers-badge">IN NUMBERS</div>
    <div class="numbers-cells">{numbers_html}</div>
  </section>

  <section class="hero-grid" aria-label="Top stories">
    {heroes_html}
  </section>

  <div class="sec-hdr">
    <span class="sec-title">THE DAY IN 8 MORE</span>
    <span class="sec-sub">Courts, markets, space, climate, war &amp; tech across 6 regions</span>
  </div>

  <section class="mid-grid" aria-label="Regional highlights">
    {mids_html}
  </section>

  <section class="lower-grid" aria-label="More dated stories and locator map">
    <div class="panel-box briefs-panel">
      <div class="panel-hdr">
        <span class="panel-title">ALSO ON TUESDAY 24 NOVEMBER — 28 MORE DATED STORIES</span>
        <span class="panel-sub">9 regions matched by color</span>
      </div>
      <div class="briefs-cols">
        {briefs_cols_html}
      </div>
    </div>

    <aside class="panel-box map-panel" aria-label="Where it happened">
      <div class="panel-hdr">
        <span class="panel-title">WHERE IT HAPPENED</span>
        <span class="panel-sub">Pins 1–11</span>
      </div>
      <div class="world-map-wrap">{world_map_svg}</div>
      <div class="pin-key">{pin_key_html}</div>
      <div class="map-legend">{map_legend_html}</div>
    </aside>
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

  document.querySelectorAll('.hero-card, .mid-card, .panel-box, .numbers-bar').forEach((el, idx) => {
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
    if (rect.height > 18.0) {
      errs.push(`Brief row #${idx + 1} height ${rect.height.toFixed(1)}px > 18px`);
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
    const artLimit = isHero ? 104.0 : 64.0;
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
      if (d < 20.0) {
        errs.push(`Map pins #${pins[i].num} & #${pins[j].num} distance ${d.toFixed(1)}px < 20px`);
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
        f"pins={audit['pinCount']} min_pin_dist={audit['minPinDist']}px"
    )
    print(f"Output: {OUTPUT_PNG} ({size_bytes} bytes / {size_kib:.2f} KiB, cap 270 KiB)")
    print(f"Preview (300x300): {preview_png}")

    if audit["errs"]:
        raise SystemExit(f"DOM audit failed with {len(audit['errs'])} error(s)")
    if size_bytes > MAX_PNG_BYTES:
        raise SystemExit(f"entry.png exceeds 270 KiB cap ({size_kib:.2f} KiB)")


if __name__ == "__main__":
    main()
