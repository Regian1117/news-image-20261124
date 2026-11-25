"""V4 editorial SVG scenes (3 Hero 314x86, 10 open-canvas Mid 186x50) and full-world locator map."""

from __future__ import annotations

from html import escape
from typing import Dict, List

from data import HERO_CARDS, MAP_PINS, MID_CARDS, REGION_COLORS, MapPin

FONT_SANS = "'Segoe UI', Arial, Helvetica, sans-serif"


def _corner_pin(num: int, region: str) -> str:
    color = REGION_COLORS[region]
    fsize = "9.2" if num >= 10 else "10.2"
    return (
        f'<g class="card-pin">'
        f'<circle cx="13" cy="13" r="9.5" fill="{color}" stroke="#FFFFFF" stroke-width="1.5"/>'
        f'<text x="13" y="16.4" text-anchor="middle" font-family="{FONT_SANS}" '
        f'font-size="{fsize}" font-weight="900" fill="#FFFFFF">{num}</text>'
        f'</g>'
    )


def _pill(
    pid: str,
    x: float,
    y: float,
    w: float,
    h: float,
    fill: str,
    text: str,
    text_fill: str,
    font_size: float,
    rx: float = 3.0,
    stroke: str = "",
    stroke_w: float = 1.0,
    letter_spacing: float = 0.2,
    y_text: float | None = None,
    font_weight: int = 900,
) -> str:
    stroke_attr = f' stroke="{stroke}" stroke-width="{stroke_w}"' if stroke else ""
    cx = x + w / 2.0
    ty = y_text if y_text is not None else (y + h * 0.5 + font_size * 0.405)
    return (
        f'<rect class="callout-pill" data-pill="{pid}" x="{x}" y="{y}" width="{w}" height="{h}" '
        f'rx="{rx}" fill="{fill}"{stroke_attr}/>'
        f'<text class="callout-text" data-pill-for="{pid}" x="{cx:.1f}" y="{ty:.1f}" '
        f'text-anchor="middle" font-family="{FONT_SANS}" font-size="{font_size}" '
        f'font-weight="{font_weight}" letter-spacing="{letter_spacing}" fill="{text_fill}">{escape(text)}</text>'
    )


def _wrap_hero(num: int, region: str, bg: str, frame: str, body: str, label: str) -> str:
    return (
        f'<svg class="scene-svg hero-svg" viewBox="0 0 314 90" width="314" height="90" '
        f'preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{escape(label)}">'
        f'<rect x="0.5" y="0.5" width="313" height="89" rx="3" fill="{bg}" stroke="{frame}" stroke-width="1"/>'
        f'{body}'
        f'{_corner_pin(num, region)}'
        f'</svg>'
    )


def _wrap_mid(num: int, region: str, bg: str, frame: str, body: str, label: str) -> str:
    return (
        f'<svg class="scene-svg mid-svg" viewBox="0 0 186 50" width="186" height="50" '
        f'preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{escape(label)}">'
        f'<rect x="0.5" y="0.5" width="185" height="49" rx="2.5" fill="{bg}" stroke="{frame}" stroke-width="1"/>'
        f'{body}'
        f'{_corner_pin(num, region)}'
        f'</svg>'
    )


def build_scenes() -> Dict[int, str]:
    card_regions: Dict[int, str] = {c.num: c.region for c in HERO_CARDS + MID_CARDS}
    scenes: Dict[int, str] = {}

    # #1 Hero (314x90): Full Arabian Peninsula map (#DCEEF9 ocean, #EFC8A5 land) + burning Riyadh tower + 11 HURT / HODEIDAH HIT
    body_1 = (
        '<rect x="1" y="1" width="312" height="88" rx="2.5" fill="#DCEEF9"/>'
        # Arabian Peninsula landmass
        '<path d="M 16,1 L 130,1 L 154,15 L 182,42 L 188,61 L 166,79 L 122,89 L 48,89 L 30,61 L 14,30 Z" '
        'fill="#EFC8A5" stroke="#B45309" stroke-width="1.1"/>'
        '<path d="M 38,15 L 122,15 L 160,46 L 140,75 L 64,75 Z" fill="#F5D9BC" opacity="0.65"/>'
        # Clear labels well separated from pin #1 (13,13), arc, and tower
        f'<text x="86" y="25" text-anchor="middle" font-family="{FONT_SANS}" font-size="8.4" '
        'font-weight="900" letter-spacing="0.45" fill="#78350F">SAUDI ARABIA</text>'
        f'<text x="64" y="81" text-anchor="middle" font-family="{FONT_SANS}" font-size="8.4" '
        'font-weight="900" letter-spacing="0.45" fill="#9A3412">YEMEN</text>'
        # Burning Riyadh tower silhouette on right side of landmass
        '<rect x="122" y="44" width="11" height="28" fill="#475569"/>'
        '<polygon points="136,72 136,21 147,14 156,23 156,72" fill="#1E293B"/>'
        '<rect x="140" y="28" width="3.5" height="4.5" fill="#93C5FD"/>'
        '<rect x="147" y="28" width="3.5" height="4.5" fill="#FDE68A"/>'
        '<rect x="140" y="38" width="3.5" height="4.5" fill="#93C5FD"/>'
        '<rect x="147" y="38" width="3.5" height="4.5" fill="#93C5FD"/>'
        '<rect x="140" y="48" width="3.5" height="4.5" fill="#FDE68A"/>'
        '<rect x="159" y="41" width="12" height="31" fill="#334155"/>'
        # Red dashed trajectory arc from Yemen to Riyadh tower
        '<path d="M 94,77 Q 112,40 143,28" fill="none" stroke="#DC2626" stroke-width="2.3" stroke-dasharray="4 2.2"/>'
        '<circle cx="94" cy="77" r="3" fill="#B91C1C"/>'
        # Fire burst on tower
        '<polygon points="146,17 149,23 156,21 152,28 159,32 151,34 153,41 146,35 140,40 142,33 134,30 141,26 140,19 144,23" fill="#DC2626"/>'
        '<polygon points="146,22 148,26 152,25 150,29 153,32 149,32 149,35 146,33 143,34 144,31 141,30 144,28 143,24 145,26" fill="#FACC15"/>'
        + _pill("p1", 196, 15, 108, 28, "#991B1B", "11 HURT", "#FFFFFF", 13.4, rx=3.5, stroke="#450A0A", stroke_w=0.9)
        + _pill("p2", 196, 49, 108, 27, "#FFFFFF", "HODEIDAH HIT", "#9A3412", 10.6, rx=3.0, stroke="#B45309", stroke_w=1.2)
    )
    scenes[1] = _wrap_hero(1, card_regions[1], "#DCEEF9", "#B45309", body_1, "Riyadh tower strike 11 hurt, Hodeidah hit")

    # #2 Hero (314x90): Neoclassical courthouse columns on #EDE9FE + tilted wooden gavel + GUILTY / 10 OF 12
    body_2 = (
        '<rect x="1" y="66" width="312" height="23" fill="#DDD6FE" opacity="0.72"/>'
        '<polygon points="81,11 22,30 140,30" fill="#5B21B6" stroke="#1E1B4B" stroke-width="1.3"/>'
        '<circle cx="81" cy="22" r="3.2" fill="#FDE047"/>'
        '<rect x="24" y="30" width="114" height="4.5" fill="#312E81"/>'
        '<rect x="29" y="34.5" width="10" height="35" fill="#FFFFFF" stroke="#6D28D9" stroke-width="1.1"/>'
        '<rect x="49" y="34.5" width="10" height="35" fill="#FFFFFF" stroke="#6D28D9" stroke-width="1.1"/>'
        '<rect x="69" y="34.5" width="10" height="35" fill="#FFFFFF" stroke="#6D28D9" stroke-width="1.1"/>'
        '<rect x="89" y="34.5" width="10" height="35" fill="#FFFFFF" stroke="#6D28D9" stroke-width="1.1"/>'
        '<rect x="109" y="34.5" width="10" height="35" fill="#FFFFFF" stroke="#6D28D9" stroke-width="1.1"/>'
        '<rect x="125" y="34.5" width="8" height="35" fill="#FFFFFF" stroke="#6D28D9" stroke-width="1.1"/>'
        '<rect x="20" y="69.5" width="122" height="4.5" fill="#4C1D95"/>'
        '<rect x="15" y="74" width="132" height="6" rx="1" fill="#1E1B4B"/>'
        '<rect x="147" y="70" width="38" height="8.5" rx="2" fill="#4C1D95" stroke="#1E1B4B" stroke-width="1.2"/>'
        '<g transform="rotate(-32 162 42)">'
        '<rect x="148" y="28" width="27" height="14.5" rx="2.5" fill="#78350F" stroke="#0F172A" stroke-width="1.3"/>'
        '<rect x="150.5" y="27" width="4" height="16.5" rx="1" fill="#FDE047"/>'
        '<rect x="168.5" y="27" width="4" height="16.5" rx="1" fill="#FDE047"/>'
        '<rect x="159" y="42.5" width="5.2" height="27" rx="1.5" fill="#92400E" stroke="#0F172A" stroke-width="1"/>'
        '</g>'
        + _pill("p1", 196, 15, 108, 28, "#7F1D1D", "GUILTY", "#FFFFFF", 13.6, rx=3.5, stroke="#450A0A", stroke_w=0.9)
        + _pill("p2", 196, 49, 108, 27, "#1E1B4B", "10 OF 12", "#FFFFFF", 12.6, rx=3.0, stroke="#6D28D9", stroke_w=1.0, letter_spacing=0.6, font_weight=800)
    )
    scenes[2] = _wrap_hero(2, card_regions[2], "#EDE9FE", "#7C3AED", body_2, "Huawei guilty 10 of 12 counts")

    # #3 Hero (314x90): Shanghai Pudong skyline + Oriental Pearl Tower + magnifying-glass portrait + UNDER PROBE / CHEN JINING
    body_3 = (
        '<rect x="1" y="64" width="312" height="25" fill="#FECACA" opacity="0.72"/>'
        # Shanghai Pudong skyline
        '<rect x="22" y="48" width="12" height="32" fill="#64748B"/>'
        '<line x1="47" y1="13" x2="47" y2="80" stroke="#334155" stroke-width="2.2"/>'
        '<polygon points="47,55 38,80 42,80 47,63 52,80 56,80" fill="#334155"/>'
        '<circle cx="47" cy="31" r="5.5" fill="#B91C1C" stroke="#1E293B" stroke-width="1"/>'
        '<circle cx="47" cy="50" r="7.5" fill="#B91C1C" stroke="#1E293B" stroke-width="1"/>'
        '<polygon points="64,80 68,16 77,12 82,80" fill="#1E293B"/>'
        '<rect x="86" y="28" width="15" height="52" fill="#334155"/>'
        '<rect x="89.5" y="33" width="8" height="4.5" fill="#FEE2E2"/>'
        '<rect x="104" y="45" width="11" height="35" fill="#475569"/>'
        # Circular magnifying-glass portrait
        '<circle cx="144" cy="42" r="23.5" fill="#FFFFFF" stroke="#0F172A" stroke-width="3.2"/>'
        '<circle cx="144" cy="42" r="19.5" fill="#FEF2F2" stroke="#DC2626" stroke-width="1" stroke-dasharray="3 2"/>'
        '<circle cx="144" cy="35.5" r="7" fill="#1E293B"/>'
        '<path d="M 130,57 C 130,47 136,44 144,44 C 152,44 158,47 158,57 Z" fill="#1E293B"/>'
        '<polygon points="142,45 146,45 145,54 144,56 143,54" fill="#DC2626"/>'
        '<line x1="161" y1="59" x2="175" y2="77" stroke="#0F172A" stroke-width="5.5" stroke-linecap="round"/>'
        '<line x1="161" y1="59" x2="175" y2="77" stroke="#B91C1C" stroke-width="2.2" stroke-linecap="round"/>'
        + _pill("p1", 188, 15, 116, 28, "#991B1B", "UNDER PROBE", "#FFFFFF", 12.2, rx=3.5, stroke="#450A0A", stroke_w=0.9)
        + _pill("p2", 188, 49, 116, 27, "#FFFFFF", "CHEN JINING", "#0F172A", 11.4, rx=3.0, stroke="#991B1B", stroke_w=1.2)
    )
    scenes[3] = _wrap_hero(3, card_regions[3], "#FEE2E2", "#DC2626", body_3, "Shanghai party chief Chen Jining under probe")

    # #4 Mid (186x50): Darkened Ukrainian apartment skyline with smoke plumes, dawn explosion burst + 9 KILLED
    body_4 = (
        '<rect x="1" y="38" width="184" height="11" fill="#CBD5E1" opacity="0.72"/>'
        # Smoke plumes
        '<circle cx="56" cy="18" r="8" fill="#64748B" opacity="0.48"/>'
        '<circle cx="67" cy="12" r="6.5" fill="#475569" opacity="0.4"/>'
        '<circle cx="80" cy="10" r="5" fill="#94A3B8" opacity="0.35"/>'
        '<circle cx="144" cy="30" r="6" fill="#64748B" opacity="0.32"/>'
        # Darkened Ukrainian apartment skyline across full width
        '<rect x="14" y="29" width="18" height="20" fill="#334155"/>'
        '<rect x="18" y="33" width="3" height="3" fill="#CBD5E1"/>'
        '<rect x="24" y="33" width="3" height="3" fill="#FDE047"/>'
        '<rect x="36" y="20" width="22" height="29" fill="#0F172A"/>'
        '<rect x="40" y="25" width="3.5" height="3.5" fill="#93C5FD"/>'
        '<rect x="47" y="25" width="3.5" height="3.5" fill="#FDE047"/>'
        '<rect x="40" y="33" width="3.5" height="3.5" fill="#CBD5E1"/>'
        '<rect x="47" y="33" width="3.5" height="3.5" fill="#CBD5E1"/>'
        '<rect x="62" y="25" width="20" height="24" fill="#1E293B"/>'
        '<rect x="66" y="30" width="3" height="3" fill="#FDE047"/>'
        '<rect x="73" y="30" width="3" height="3" fill="#CBD5E1"/>'
        '<rect x="86" y="28" width="22" height="21" fill="#334155"/>'
        '<rect x="91" y="33" width="3" height="3" fill="#CBD5E1"/>'
        '<rect x="98" y="33" width="3" height="3" fill="#93C5FD"/>'
        '<rect x="112" y="31" width="24" height="18" fill="#1E293B"/>'
        '<rect x="117" y="36" width="3" height="3" fill="#FDE047"/>'
        '<rect x="125" y="36" width="3" height="3" fill="#CBD5E1"/>'
        '<rect x="140" y="29" width="20" height="20" fill="#0F172A"/>'
        '<rect x="145" y="34" width="3" height="3" fill="#93C5FD"/>'
        '<rect x="152" y="34" width="3" height="3" fill="#CBD5E1"/>'
        '<rect x="163" y="34" width="15" height="15" fill="#475569"/>'
        # Dawn explosion burst
        '<polygon points="52,13 55,19 62,18 57,23 61,27 54,26 52,31 50,25 44,25 48,21 46,16 50,18" fill="#DC2626"/>'
        '<polygon points="52,17 54,20 57,20 55,22 57,25 53,24 52,26 51,23 48,23 50,21 49,19 51,20" fill="#FACC15"/>'
        + _pill("p1", 110, 5, 70, 20, "#991B1B", "9 KILLED", "#FFFFFF", 11.4, rx=2.5, stroke="#450A0A", stroke_w=0.8)
    )
    scenes[4] = _wrap_mid(4, card_regions[4], "#E2E8F0", "#64748B", body_4, "Ukraine strikes 9 killed")

    # #5 Mid (186x50): Open-canvas sky-blue #DBEAFE + capsule + conical flask + top-right $41BN
    body_5 = (
        '<rect x="1" y="39" width="184" height="10" fill="#BFDBFE" opacity="0.7"/>'
        # Tilted purple/white pharmaceutical capsule left-center
        '<g transform="rotate(-28 54 27)">'
        '<rect x="30" y="18" width="48" height="18" rx="9" fill="#FFFFFF" stroke="#1E1B4B" stroke-width="1.5"/>'
        '<path d="M 54,18 L 69,18 A 9,9 0 0,1 69,36 L 54,36 Z" fill="#6D28D9"/>'
        '<line x1="54" y1="18" x2="54" y2="36" stroke="#1E1B4B" stroke-width="1.3"/>'
        '<rect x="36" y="21" width="12" height="2.8" rx="1.4" fill="#DBEAFE"/>'
        '</g>'
        # Conical Erlenmeyer flask center-right
        '<path d="M 101,15 L 101,25 L 90,44 L 122,44 L 111,25 L 111,15 Z" '
        'fill="#FFFFFF" stroke="#1E3A8A" stroke-width="1.4" stroke-linejoin="round"/>'
        '<path d="M 95,35 L 117,35 L 122,44 L 90,44 Z" fill="#0D9488" opacity="0.85"/>'
        '<line x1="98" y1="15" x2="114" y2="15" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round"/>'
        '<circle cx="104" cy="39" r="1.6" fill="#CCFBF1"/>'
        '<circle cx="109" cy="41" r="1.2" fill="#CCFBF1"/>'
        # Subtle molecular accent dots right
        '<circle cx="144" cy="36" r="3" fill="#6D28D9" opacity="0.35"/>'
        '<circle cx="158" cy="32" r="2.2" fill="#0284C7" opacity="0.4"/>'
        '<line x1="146" y1="35" x2="156" y2="32.5" stroke="#3B82F6" stroke-width="1" opacity="0.45"/>'
        + _pill("p1", 114, 4, 66, 21, "#0F172A", "$41BN", "#FFFFFF", 12.5, rx=2.8)
    )
    scenes[5] = _wrap_mid(5, card_regions[5], "#DBEAFE", "#60A5FA", body_5, "Sanofi $41bn buyout")

    # #6 Mid (186x50): Pure bull green rally on left (x=10..95) + stacked DOW 50,018 & NASDAQ -1.5% on right
    body_6 = (
        '<line x1="10" y1="16" x2="95" y2="16" stroke="#1E293B" stroke-width="0.8"/>'
        '<line x1="10" y1="29" x2="95" y2="29" stroke="#1E293B" stroke-width="0.8"/>'
        '<line x1="10" y1="43" x2="95" y2="43" stroke="#334155" stroke-width="1"/>'
        # Ascending green vertical bars (dark-to-bright emerald #16A34A -> #4ADE80)
        '<rect x="13" y="36" width="8" height="7" rx="1" fill="#16A34A" opacity="0.65"/>'
        '<rect x="26" y="32" width="8" height="11" rx="1" fill="#16A34A" opacity="0.75"/>'
        '<rect x="39" y="29" width="8" height="14" rx="1" fill="#22C55E" opacity="0.8"/>'
        '<rect x="52" y="23" width="8" height="20" rx="1" fill="#22C55E" opacity="0.85"/>'
        '<rect x="65" y="18" width="8" height="25" rx="1" fill="#4ADE80" opacity="0.88"/>'
        '<rect x="78" y="12" width="8" height="31" rx="1" fill="#4ADE80" opacity="0.92"/>'
        # Soft green area fill under pure bull rally line
        '<polygon points="12,42 29,34 43,31 56,23 69,18 88,9 88,43 12,43" fill="#22C55E" opacity="0.22"/>'
        # Crisp upward rally polyline + bright arrowhead + peak dot
        '<polyline points="12,42 29,34 43,31 56,23 69,18 88,9" fill="none" stroke="#4ADE80" '
        'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
        '<polygon points="94,6 83,7 89,14" fill="#4ADE80"/>'
        '<circle cx="88" cy="9" r="2.8" fill="#BBF7D0"/>'
        + _pill("p1", 100, 4, 80, 18, "#15803D", "DOW 50,018", "#FFFFFF", 9.6, rx=2.5, letter_spacing=0.15, font_weight=800)
        + _pill("p2", 100, 25, 80, 17, "#B91C1C", "NASDAQ -1.5%", "#FFFFFF", 8.5, rx=2.5, letter_spacing=0.1, font_weight=800)
    )
    scenes[6] = _wrap_mid(6, card_regions[6], "#0F172A", "#334155", body_6, "Dow 50,018 Nasdaq -1.5%")

    # #7 Mid (186x50): Deep-space #1E1B4B + Ariane 6 rocket + stars + dashed orbit arc + top-right 36 SATS
    body_7 = (
        '<circle cx="32" cy="11" r="1.1" fill="#E2E8F0"/>'
        '<circle cx="88" cy="12" r="1.2" fill="#FDE68A"/>'
        '<circle cx="24" cy="36" r="1.0" fill="#93C5FD"/>'
        '<circle cx="96" cy="39" r="1.1" fill="#CBD5E1"/>'
        '<circle cx="130" cy="34" r="1.1" fill="#FFFFFF"/>'
        '<circle cx="170" cy="38" r="1.2" fill="#93C5FD"/>'
        # Dashed orbital trajectory sweeping across full width
        '<path d="M 12,41 Q 78,6 176,34" fill="none" stroke="#38BDF8" stroke-width="1.2" stroke-dasharray="3.5 2.5" opacity="0.75"/>'
        # Small satellite icon on right orbital arc
        '<rect x="142" y="30" width="9" height="6" rx="1" fill="#FACC15"/>'
        '<rect x="131" y="31.5" width="9" height="3" fill="#38BDF8"/>'
        '<rect x="153" y="31.5" width="9" height="3" fill="#38BDF8"/>'
        # Exhaust flame plume
        '<polygon points="55,34 48,47 55,43 62,47" fill="#F97316"/>'
        '<polygon points="55,34 51.5,43 55,41 58.5,43" fill="#FACC15"/>'
        # Ariane 6 rocket body & boosters
        '<rect x="46" y="20" width="4.4" height="14" rx="1.5" fill="#CBD5E1"/>'
        '<rect x="59.6" y="20" width="4.4" height="14" rx="1.5" fill="#CBD5E1"/>'
        '<path d="M 51,15 C 51,7.5 55,5 55,5 C 55,5 59,7.5 59,15 L 59,34 L 51,34 Z" fill="#F8FAFC" stroke="#38BDF8" stroke-width="0.9"/>'
        '<rect x="51" y="15" width="8" height="3" fill="#0284C7"/>'
        '<circle cx="55" cy="23" r="1.8" fill="#0F172A"/>'
        + _pill("p1", 106, 5, 74, 20, "#0F172A", "36 SATS", "#FACC15", 11.0, rx=2.5, stroke="#FACC15", stroke_w=1.1, letter_spacing=0.45, font_weight=800)
    )
    scenes[7] = _wrap_mid(7, card_regions[7], "#1E1B4B", "#4338CA", body_7, "Ariane 6 36 satellites launch")

    # #8 Mid (186x50): Warm apricot desert highway + bus & stalled truck + top-right 13 DEAD
    body_8 = (
        # Desert dune silhouette on far right
        '<path d="M 118,35 Q 146,24 185,33 L 185,36 L 118,36 Z" fill="#FDBA74" opacity="0.65"/>'
        # Full-width highway asphalt & dashed stripe
        '<rect x="1" y="35" width="184" height="14" fill="#334155"/>'
        '<line x1="4" y1="43" x2="182" y2="43" stroke="#FDE68A" stroke-width="1.4" stroke-dasharray="8 6"/>'
        # Worker bus left-center (clear of pin #8)
        '<rect x="20" y="23" width="42" height="14" rx="2.5" fill="#C2410C" stroke="#0F172A" stroke-width="1.1"/>'
        '<rect x="24" y="26" width="7" height="4.5" rx="0.8" fill="#FEF3C7"/>'
        '<rect x="33" y="26" width="7" height="4.5" rx="0.8" fill="#FEF3C7"/>'
        '<rect x="42" y="26" width="7" height="4.5" rx="0.8" fill="#FEF3C7"/>'
        '<rect x="51" y="26" width="7" height="5.5" rx="0.8" fill="#BAE6FD"/>'
        '<circle cx="30" cy="38" r="3.4" fill="#0F172A" stroke="#E2E8F0" stroke-width="1"/>'
        '<circle cx="52" cy="38" r="3.4" fill="#0F172A" stroke="#E2E8F0" stroke-width="1"/>'
        # Stalled truck right-center
        '<rect x="70" y="19" width="32" height="18" rx="1.5" fill="#475569" stroke="#0F172A" stroke-width="1.1"/>'
        '<path d="M 102,25 L 114,25 L 118,31 L 118,37 L 102,37 Z" fill="#64748B" stroke="#0F172A" stroke-width="1.1"/>'
        '<circle cx="79" cy="38" r="3.4" fill="#0F172A" stroke="#E2E8F0" stroke-width="1"/>'
        '<circle cx="110" cy="38" r="3.4" fill="#0F172A" stroke="#E2E8F0" stroke-width="1"/>'
        # Impact flash
        '<polygon points="66,15 68,21 74,20 69,25 73,29 67,28 66,33 64,27 59,27 63,23 60,18 65,20" fill="#DC2626"/>'
        '<circle cx="66" cy="24" r="2.6" fill="#FACC15"/>'
        + _pill("p1", 108, 5, 72, 20, "#9A3412", "13 DEAD", "#FFFFFF", 11.2, rx=2.5, stroke="#431407", stroke_w=0.8)
    )
    scenes[8] = _wrap_mid(8, card_regions[8], "#FFEDD5", "#FB923C", body_8, "UAE bus-truck crash 13 dead")

    # #9 Mid (186x50): Mint-green & coastal wave horizon + bright blue water drop + top-right $55M AID
    body_9 = (
        '<path d="M 1,35 Q 28,28 56,35 T 112,35 T 168,35 L 185,35 L 185,49 L 1,49 Z" fill="#86EFAC"/>'
        '<path d="M 1,41 Q 30,36 60,41 T 120,41 T 180,41 L 185,41 L 185,49 L 1,49 Z" fill="#38BDF8" opacity="0.65"/>'
        # Water drop left-center
        '<path d="M 60,8 C 60,8 75,23 75,32 A 15,15 0 0,1 45,32 C 45,23 60,8 60,8 Z" '
        'fill="#0284C7" stroke="#0C4A6E" stroke-width="1.4"/>'
        '<path d="M 53,29 C 53,24 57,18 59,15 C 58,21 56,26 56,31 A 4,4 0 0,1 53,29 Z" fill="#BAE6FD"/>'
        # Clean water ripple rings right
        '<ellipse cx="136" cy="40" rx="22" ry="4" fill="none" stroke="#0284C7" stroke-width="1.2" opacity="0.55"/>'
        '<ellipse cx="136" cy="40" rx="11" ry="2" fill="none" stroke="#0369A1" stroke-width="1.1" opacity="0.7"/>'
        + _pill("p1", 102, 5, 78, 20, "#15803D", "$55M AID", "#FFFFFF", 11.0, rx=2.5, stroke="#14532D", stroke_w=0.8)
    )
    scenes[9] = _wrap_mid(9, card_regions[9], "#DCFCE7", "#4ADE80", body_9, "Port Sudan $55m water aid")

    # #10 Mid (186x50): Cyan streetfront across width + amber explosion burst + top-right 6 DEAD
    body_10 = (
        '<rect x="1" y="40" width="184" height="9" fill="#A5F3FC"/>'
        # Left & center streetfront buildings
        '<rect x="18" y="21" width="46" height="23" fill="#334155" stroke="#0F172A" stroke-width="1.1"/>'
        '<polygon points="16,21 66,21 62,15 20,15" fill="#0E7490" stroke="#0F172A" stroke-width="1"/>'
        '<rect x="23" y="26" width="14" height="10" fill="#E0F2FE"/>'
        '<rect x="42" y="26" width="14" height="18" fill="#1E293B"/>'
        # Adjacent streetfront on right
        '<rect x="114" y="27" width="58" height="17" fill="#475569" stroke="#0F172A" stroke-width="1"/>'
        '<rect x="120" y="31" width="12" height="8" fill="#E0F2FE"/>'
        '<rect x="137" y="31" width="12" height="8" fill="#E0F2FE"/>'
        '<rect x="154" y="31" width="12" height="8" fill="#FEF3C7"/>'
        # Amber/red explosion burst at center
        '<polygon points="82,9 86,18 97,14 91,23 103,27 92,30 97,39 86,34 81,43 78,33 68,35 74,26 66,19 77,20" fill="#DC2626"/>'
        '<polygon points="82,15 85,21 91,19 88,24 94,27 88,29 90,34 84,31 81,36 79,30 74,31 77,26 73,22 79,23" fill="#F59E0B"/>'
        '<circle cx="82" cy="26" r="4" fill="#FEF08A"/>'
        + _pill("p1", 112, 5, 68, 20, "#B91C1C", "6 DEAD", "#FFFFFF", 11.4, rx=2.5, stroke="#7F1D1D", stroke_w=0.8)
    )
    scenes[10] = _wrap_mid(10, card_regions[10], "#CFFAFE", "#22D3EE", body_10, "Hanoi gas blast 6 dead")

    # #11 Mid (186x50): Full-width seafoam seismograph grid (x=12..174) + sharp waveform + top-right M5.3
    body_11 = (
        '<line x1="12" y1="16" x2="174" y2="16" stroke="#99F6E4" stroke-width="0.9"/>'
        '<line x1="12" y1="28" x2="174" y2="28" stroke="#5EEAD4" stroke-width="1.1"/>'
        '<line x1="12" y1="40" x2="174" y2="40" stroke="#99F6E4" stroke-width="0.9"/>'
        '<polyline points="12,28 28,28 34,24 39,33 45,16 51,43 57,7 63,46 69,12 75,40 81,19 87,35 93,24 100,32 108,26 118,30 130,27 146,28 174,28" '
        'fill="none" stroke="#0F766E" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/>'
        + _pill("p1", 118, 5, 62, 20, "#0F766E", "M5.3", "#FFFFFF", 11.8, rx=2.5, stroke="#134E4A", stroke_w=0.8)
    )
    scenes[11] = _wrap_mid(11, card_regions[11], "#CCFBF1", "#2DD4BF", body_11, "Nepal M5.3 earthquake")

    # #12 Mid (186x50): Light rose sky with dark storm cloud, lightning, rain across width + top-right 20,000 FLEE
    body_12 = (
        # Main dark storm cloud left-center
        '<path d="M 28,24 C 22,24 21,16 27,14 C 28,8 37,6 43,9.5 C 48,5 59,7 61,13 '
        'C 68,13 71,19 67,23.5 C 66,24 64,24 62,24 Z" fill="#334155" stroke="#0F172A" stroke-width="1.2"/>'
        # Secondary cloud bank lower-right
        '<path d="M 102,35 C 97,35 97,29 102,28 C 104,24 113,23 118,26 C 123,23 134,25 136,29 '
        'C 142,29 144,34 140,35 Z" fill="#475569" opacity="0.8"/>'
        # Lightning bolt
        '<polygon points="48,21 42,32 47.5,32 44,44 56,30 50,30 53.5,21" fill="#FACC15" stroke="#B45309" stroke-width="0.9"/>'
        # Rain streaks across width
        '<g stroke="#9D174D" stroke-width="1.8" stroke-linecap="round">'
        '<line x1="30" y1="28" x2="26" y2="39"/>'
        '<line x1="37" y1="28" x2="33" y2="41"/>'
        '<line x1="61" y1="28" x2="57" y2="40"/>'
        '<line x1="69" y1="28" x2="65" y2="39"/>'
        '<line x1="110" y1="37" x2="107" y2="45"/>'
        '<line x1="122" y1="37" x2="119" y2="45"/>'
        '<line x1="134" y1="37" x2="131" y2="45"/>'
        '</g>'
        + _pill("p1", 104, 5, 76, 20, "#831843", "20K FLEE", "#FFFFFF", 11.2, rx=2.5, stroke="#500724", stroke_w=0.8)
    )
    scenes[12] = _wrap_mid(12, card_regions[12], "#FCE7F3", "#F472B6", body_12, "Brazil storm 20,000 displaced")

    # #13 Mid (186x50): Civic ice-blue backdrop + full-width circuit traces + checkmark shield + top-right 5% FINE
    body_13 = (
        # Subtle full-width digital circuit lines
        '<g stroke="#38BDF8" stroke-width="1.3" opacity="0.75">'
        '<line x1="18" y1="26" x2="170" y2="26"/>'
        '<line x1="26" y1="36" x2="158" y2="36"/>'
        '<circle cx="18" cy="26" r="2.2" fill="#0369A1"/>'
        '<circle cx="26" cy="36" r="2.2" fill="#0369A1"/>'
        '<circle cx="170" cy="26" r="2.2" fill="#0369A1"/>'
        '<circle cx="158" cy="36" r="2.2" fill="#0369A1"/>'
        '<circle cx="132" cy="36" r="2.2" fill="#0284C7"/>'
        '</g>'
        # Checkmark shield left-center
        '<path d="M 60,7 L 79,13 L 79,26 C 79,35.5 70.5,42 60,46 C 49.5,42 41,35.5 41,26 L 41,13 Z" '
        'fill="#0284C7" stroke="#0F172A" stroke-width="1.5"/>'
        '<path d="M 60,7 L 79,13 L 79,26 C 79,35.5 70.5,42 60,46 Z" fill="#0369A1"/>'
        '<polyline points="50,26 57,33 70,19" fill="none" stroke="#FFFFFF" stroke-width="3.6" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        + _pill("p1", 108, 5, 72, 20, "#0369A1", "5% FINE", "#FFFFFF", 11.4, rx=2.5, stroke="#0C4A6E", stroke_w=0.8)
    )
    scenes[13] = _wrap_mid(13, card_regions[13], "#E0F2FE", "#38BDF8", body_13, "Australia online safety 5% fine")

    return scenes


def build_world_map_svg(pins: List[MapPin] = MAP_PINS) -> str:
    """Full-world editorial locator map (360x185) with clearly framed continents & Pins 1–13."""
    graticule = (
        '<g stroke="#C6DFEE" stroke-width="0.7" stroke-dasharray="2.5 2.5">'
        '<line x1="0" y1="46" x2="360" y2="46"/>'
        '<line x1="0" y1="92" x2="360" y2="92" stroke-dasharray="none" opacity="0.85"/>'
        '<line x1="0" y1="138" x2="360" y2="138"/>'
        '<line x1="90" y1="0" x2="90" y2="185"/>'
        '<line x1="180" y1="0" x2="180" y2="185"/>'
        '<line x1="270" y1="0" x2="270" y2="185"/>'
        '</g>'
    )

    continents = (
        '<g fill="#94A396" stroke="#3F4D42" stroke-width="1.1" stroke-linejoin="round">'
        '<path d="M 16,24 L 46,16 L 86,15 L 114,24 L 118,38 L 108,52 L 96,62 L 84,74 '
        'L 72,74 L 62,62 L 48,58 L 36,46 L 22,38 Z"/>'
        '<path d="M 76,72 L 90,82 L 98,88 L 93,91 L 80,83 L 71,74 Z"/>'
        '<path d="M 122,9 L 152,8 L 155,21 L 136,28 L 123,21 Z"/>'
        '<path d="M 96,86 L 118,86 L 136,102 L 140,118 L 130,138 L 118,158 L 106,172 '
        'L 98,166 L 96,142 L 88,116 L 90,96 Z"/>'
        '<path d="M 155,25 L 165,24 L 166,36 L 156,37 Z"/>'
        '<path d="M 166,38 L 178,18 L 198,12 L 218,16 L 226,30 L 222,48 L 208,53 '
        'L 192,50 L 178,52 L 165,48 Z"/>'
        '<path d="M 160,60 L 188,56 L 208,62 L 216,78 L 224,96 L 216,120 L 202,148 '
        'L 188,158 L 176,146 L 172,118 L 158,100 L 154,78 Z"/>'
        '<path d="M 222,126 L 228,126 L 227,142 L 221,141 Z"/>'
        '<path d="M 216,52 L 226,22 L 270,14 L 318,18 L 346,28 L 338,46 L 320,56 L 314,72 '
        'L 302,88 L 292,98 L 284,86 L 270,104 L 258,88 L 250,76 L 246,88 L 226,90 L 212,78 L 212,64 Z"/>'
        '<path d="M 328,44 L 336,42 L 338,58 L 330,62 Z"/>'
        '<path d="M 284,106 L 306,110 L 322,112 L 318,118 L 296,116 L 282,111 Z"/>'
        '<path d="M 284,126 L 310,120 L 332,128 L 336,146 L 322,160 L 296,158 L 282,144 Z"/>'
        '<path d="M 343,152 L 351,150 L 353,166 L 345,168 Z"/>'
        '</g>'
    )

    pins_parts: List[str] = []
    for p in pins:
        color = REGION_COLORS[p.region]
        fsize = "8.6" if p.num >= 10 else "9.4"
        pins_parts.append(
            f'<g class="map-pin" data-pin="{p.num}" data-x="{p.x}" data-y="{p.y}">'
            f'<circle cx="{p.x}" cy="{p.y}" r="8.2" fill="{color}" stroke="#FFFFFF" stroke-width="1.4"/>'
            f'<text x="{p.x}" y="{p.y + 3.1}" text-anchor="middle" '
            f'font-family="{FONT_SANS}" font-size="{fsize}" font-weight="900" fill="#FFFFFF">{p.num}</text>'
            f'</g>'
        )

    return (
        '<svg class="world-map-svg" viewBox="0 0 360 185" width="360" height="185" '
        'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Full-world locator map for stories 1 to 13">'
        '<rect x="0.5" y="0.5" width="359" height="184" rx="3" fill="#E6F2FA" stroke="#94A3B8" stroke-width="1"/>'
        f'{graticule}'
        f'{continents}'
        f'{"".join(pins_parts)}'
        '</svg>'
    )
