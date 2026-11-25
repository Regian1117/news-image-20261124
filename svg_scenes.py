"""Full-bleed editorial SVG scenes (3 Hero 314x80, 10 Mid 186x54) and full-world locator map."""

from __future__ import annotations

from html import escape
from typing import Dict, List

from data import HERO_CARDS, MAP_PINS, MID_CARDS, REGION_COLORS, MapPin

FONT_SANS = "'Segoe UI', Arial, Helvetica, sans-serif"


def _corner_pin(num: int, region: str) -> str:
    color = REGION_COLORS[region]
    fsize = "10.0" if num >= 10 else "11.0"
    return (
        f'<g class="card-pin">'
        f'<circle cx="14" cy="14" r="10.5" fill="{color}" stroke="#FFFFFF" stroke-width="1.8"/>'
        f'<text x="14" y="17.8" text-anchor="middle" font-family="{FONT_SANS}" '
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
    letter_spacing: float = 0.25,
) -> str:
    stroke_attr = f' stroke="{stroke}" stroke-width="{stroke_w}"' if stroke else ""
    cx = x + w / 2.0
    # Visual center baseline tuned for Segoe UI / Arial bold uppercase
    ty = y + h * 0.5 + font_size * 0.355
    return (
        f'<rect class="callout-pill" data-pill="{pid}" x="{x}" y="{y}" width="{w}" height="{h}" '
        f'rx="{rx}" fill="{fill}"{stroke_attr}/>'
        f'<text class="callout-text" data-pill-for="{pid}" x="{cx:.1f}" y="{ty:.1f}" '
        f'text-anchor="middle" font-family="{FONT_SANS}" font-size="{font_size}" '
        f'font-weight="900" letter-spacing="{letter_spacing}" fill="{text_fill}">{escape(text)}</text>'
    )


def _wrap_hero(num: int, region: str, bg: str, frame: str, body: str, label: str) -> str:
    return (
        f'<svg class="scene-svg hero-svg" viewBox="0 0 314 80" width="314" height="80" '
        f'preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{escape(label)}">'
        f'<rect x="0.5" y="0.5" width="313" height="79" rx="3" fill="{bg}" stroke="{frame}" stroke-width="1"/>'
        f'{body}'
        f'{_corner_pin(num, region)}'
        f'</svg>'
    )


def _wrap_mid(num: int, region: str, bg: str, frame: str, body: str, label: str) -> str:
    return (
        f'<svg class="scene-svg mid-svg" viewBox="0 0 186 54" width="186" height="54" '
        f'preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{escape(label)}">'
        f'<rect x="0.5" y="0.5" width="185" height="53" rx="2.5" fill="{bg}" stroke="{frame}" stroke-width="1"/>'
        f'{body}'
        f'{_corner_pin(num, region)}'
        f'</svg>'
    )


def build_scenes() -> Dict[int, str]:
    card_regions: Dict[int, str] = {c.num: c.region for c in HERO_CARDS + MID_CARDS}
    scenes: Dict[int, str] = {}

    # #1 Hero (314x80): Full-bleed warm sand Arabian Peninsula mini-map + trajectory hitting Riyadh tower
    body_1 = (
        # Subtle coastal water corners
        '<path d="M 1,1 L 313,1 L 313,79 L 1,79 Z" fill="#E6F2FA"/>'
        # Warm sand Arabian Peninsula landmass spanning left & center
        '<path d="M 14,1 L 122,1 L 146,12 L 176,36 L 186,52 L 166,68 L 128,79 L 60,79 L 36,56 L 18,28 Z" '
        'fill="#FDE68A" stroke="#D97706" stroke-width="1"/>'
        # Inner desert contour shading
        '<path d="M 38,14 L 116,14 L 154,42 L 136,68 L 72,68 Z" fill="#FEF3C7" opacity="0.65"/>'
        # Yemen southern zone tint
        '<path d="M 60,79 L 128,79 L 142,66 L 78,60 Z" fill="#FDBA74" opacity="0.55"/>'
        # Map region labels well clear of pin #1 (cx=14,cy=14,r=10.5)
        f'<text x="72" y="38" text-anchor="middle" font-family="{FONT_SANS}" font-size="8.0" '
        'font-weight="800" letter-spacing="0.5" fill="#92400E">SAUDI ARABIA</text>'
        f'<text x="74" y="75" text-anchor="middle" font-family="{FONT_SANS}" font-size="8.0" '
        'font-weight="900" letter-spacing="0.5" fill="#9A3412">YEMEN</text>'
        # Riyadh skyline cluster at center-right of map
        '<rect x="122" y="36" width="11" height="24" fill="#475569"/>'
        '<polygon points="136,60 136,15 147,9 156,17 156,60" fill="#1E293B"/>'
        '<rect x="140" y="21" width="3.5" height="4" fill="#93C5FD"/>'
        '<rect x="147" y="21" width="3.5" height="4" fill="#FDE68A"/>'
        '<rect x="140" y="30" width="3.5" height="4" fill="#93C5FD"/>'
        '<rect x="147" y="30" width="3.5" height="4" fill="#93C5FD"/>'
        '<rect x="140" y="39" width="3.5" height="4" fill="#FDE68A"/>'
        '<rect x="159" y="34" width="12" height="26" fill="#334155"/>'
        # Red missile trajectory arc from Yemen to Riyadh tower
        '<path d="M 103,68 Q 114,32 143,22" fill="none" stroke="#DC2626" stroke-width="2.2" stroke-dasharray="4 2.2"/>'
        '<circle cx="103" cy="68" r="3" fill="#B91C1C"/>'
        # Starburst impact
        '<polygon points="146,12 149,18 156,16 152,22 159,26 151,28 153,35 146,29 140,34 142,27 134,24 141,21 140,14 144,18" fill="#DC2626"/>'
        '<polygon points="146,17 148,21 152,20 150,23 153,26 149,26 149,29 146,27 143,28 144,25 141,24 144,22 143,18 145,21" fill="#FACC15"/>'
        # Corner pills
        + _pill("p1", 194, 11, 110, 26, "#B91C1C", "11 HURT", "#FFFFFF", 13.0, rx=3.5, stroke="#7F1D1D", stroke_w=0.9)
        + _pill("p2", 194, 43, 110, 25, "#FFFFFF", "HODEIDAH HIT", "#991B1B", 10.6, rx=3.0, stroke="#B91C1C", stroke_w=1.2)
    )
    scenes[1] = _wrap_hero(1, card_regions[1], "#FEF3C7", "#D97706", body_1, "Riyadh strike 11 hurt, Hodeidah hit")

    # #2 Hero (314x80): Full-bleed soft lavender courthouse columns + gavel + GUILTY / 10 OF 12
    body_2 = (
        '<rect x="1" y="58" width="312" height="21" fill="#DDD6FE" opacity="0.7"/>'
        # Neoclassical courthouse facade (x=28..134)
        '<polygon points="81,10 30,27 132,27" fill="#5B21B6" stroke="#1E1B4B" stroke-width="1.3"/>'
        '<circle cx="81" cy="20" r="3" fill="#FACC15"/>'
        '<rect x="32" y="27" width="98" height="4" fill="#312E81"/>'
        '<rect x="38" y="31" width="9" height="31" fill="#FFFFFF" stroke="#6D28D9" stroke-width="1.1"/>'
        '<rect x="57" y="31" width="9" height="31" fill="#FFFFFF" stroke="#6D28D9" stroke-width="1.1"/>'
        '<rect x="76" y="31" width="9" height="31" fill="#FFFFFF" stroke="#6D28D9" stroke-width="1.1"/>'
        '<rect x="95" y="31" width="9" height="31" fill="#FFFFFF" stroke="#6D28D9" stroke-width="1.1"/>'
        '<rect x="114" y="31" width="9" height="31" fill="#FFFFFF" stroke="#6D28D9" stroke-width="1.1"/>'
        '<rect x="28" y="62" width="106" height="4.5" fill="#4C1D95"/>'
        '<rect x="22" y="66.5" width="118" height="5.5" rx="1" fill="#1E1B4B"/>'
        # Judge gavel + strike block (x=138..184)
        '<rect x="142" y="62" width="38" height="8" rx="2" fill="#4C1D95" stroke="#1E1B4B" stroke-width="1.2"/>'
        '<g transform="rotate(-34 158 37)">'
        '<rect x="144" y="24" width="26" height="14" rx="2.5" fill="#78350F" stroke="#0F172A" stroke-width="1.3"/>'
        '<rect x="146.5" y="23" width="4" height="16" rx="1" fill="#FACC15"/>'
        '<rect x="163.5" y="23" width="4" height="16" rx="1" fill="#FACC15"/>'
        '<rect x="155" y="38" width="5" height="25" rx="1.5" fill="#92400E" stroke="#0F172A" stroke-width="1"/>'
        '</g>'
        + _pill("p1", 194, 11, 110, 26, "#881337", "GUILTY", "#FFFFFF", 13.4, rx=3.5, stroke="#4C0519", stroke_w=0.9)
        + _pill("p2", 194, 43, 110, 25, "#1E1B4B", "10 OF 12", "#FACC15", 12.2, rx=3.0, stroke="#6D28D9", stroke_w=1.0)
    )
    scenes[2] = _wrap_hero(2, card_regions[2], "#F3E8FF", "#8B5CF6", body_2, "Huawei guilty 10 of 12 counts")

    # #3 Hero (314x80): Full-bleed rose Shanghai Pudong skyline + magnifying glass portrait
    body_3 = (
        '<rect x="1" y="57" width="312" height="22" fill="#FECDD3" opacity="0.72"/>'
        # Pudong skyline (x=22..112)
        '<rect x="24" y="42" width="12" height="28" fill="#64748B"/>'
        # Oriental Pearl Tower silhouette
        '<line x1="48" y1="11" x2="48" y2="70" stroke="#334155" stroke-width="2.2"/>'
        '<polygon points="48,48 39,70 43,70 48,56 53,70 57,70" fill="#334155"/>'
        '<circle cx="48" cy="28" r="5.2" fill="#BE123C" stroke="#1E293B" stroke-width="1"/>'
        '<circle cx="48" cy="45" r="7.2" fill="#BE123C" stroke="#1E293B" stroke-width="1"/>'
        # Shanghai Tower & World Financial Center
        '<polygon points="64,70 68,14 77,10 81,70" fill="#1E293B"/>'
        '<rect x="85" y="24" width="15" height="46" fill="#334155"/>'
        '<rect x="88.5" y="29" width="8" height="4" fill="#FFE4E6"/>'
        '<rect x="103" y="40" width="11" height="30" fill="#475569"/>'
        # Bold magnifying glass over official portrait silhouette
        '<circle cx="144" cy="37" r="22" fill="#FFFFFF" stroke="#0F172A" stroke-width="3.2"/>'
        '<circle cx="144" cy="37" r="18.5" fill="#FEF2F2" stroke="#DC2626" stroke-width="1" stroke-dasharray="3 2"/>'
        # Official bust silhouette inside lens
        '<circle cx="144" cy="31" r="6.5" fill="#1E293B"/>'
        '<path d="M 131,51 C 131,42 136,39 144,39 C 152,39 157,42 157,51 Z" fill="#1E293B"/>'
        '<polygon points="142,40 146,40 145,48 144,50 143,48" fill="#DC2626"/>'
        # Magnifying handle
        '<line x1="160" y1="53" x2="174" y2="69" stroke="#0F172A" stroke-width="5.5" stroke-linecap="round"/>'
        '<line x1="160" y1="53" x2="174" y2="69" stroke="#B91C1C" stroke-width="2.2" stroke-linecap="round"/>'
        + _pill("p1", 186, 11, 118, 26, "#991B1B", "UNDER PROBE", "#FFFFFF", 12.2, rx=3.5, stroke="#450A0A", stroke_w=0.9)
        + _pill("p2", 186, 43, 118, 25, "#FFFFFF", "CHEN JINING", "#0F172A", 11.2, rx=3.0, stroke="#991B1B", stroke_w=1.2)
    )
    scenes[3] = _wrap_hero(3, card_regions[3], "#FFE4E6", "#E11D48", body_3, "Shanghai party chief Chen Jining under probe")

    # #4 Mid (186x54): Ukraine war — cool slate skyline/smoke + crimson 9 KILLED + dark slate ZAPORIZHZHIA
    body_4 = (
        '<rect x="1" y="38" width="184" height="15" fill="#CBD5E1" opacity="0.6"/>'
        # Smoke plumes
        '<circle cx="48" cy="18" r="8" fill="#64748B" opacity="0.45"/>'
        '<circle cx="57" cy="12" r="6.5" fill="#475569" opacity="0.38"/>'
        '<circle cx="66" cy="9" r="5" fill="#94A3B8" opacity="0.35"/>'
        # Damaged apartment blocks
        '<rect x="18" y="29" width="16" height="22" fill="#475569"/>'
        '<rect x="21" y="33" width="3" height="3" fill="#E2E8F0"/>'
        '<rect x="27" y="33" width="3" height="3" fill="#FDE047"/>'
        '<rect x="21" y="40" width="3" height="3" fill="#E2E8F0"/>'
        '<rect x="37" y="21" width="19" height="30" fill="#1E293B"/>'
        '<rect x="40" y="26" width="3.5" height="3.5" fill="#93C5FD"/>'
        '<rect x="47" y="26" width="3.5" height="3.5" fill="#FDE047"/>'
        '<rect x="40" y="34" width="3.5" height="3.5" fill="#E2E8F0"/>'
        '<rect x="47" y="34" width="3.5" height="3.5" fill="#E2E8F0"/>'
        '<rect x="59" y="27" width="17" height="24" fill="#334155"/>'
        '<rect x="63" y="32" width="3" height="3" fill="#E2E8F0"/>'
        '<rect x="69" y="32" width="3" height="3" fill="#FDE047"/>'
        # Strike spark
        '<polygon points="48,14 51,20 58,19 53,24 57,28 50,27 48,32 46,26 40,26 44,22 42,17 46,19" fill="#DC2626"/>'
        '<polygon points="48,18 50,21 53,21 51,23 53,26 49,25 48,27 47,24 44,24 46,22 45,20 47,21" fill="#FACC15"/>'
        + _pill("p1", 86, 5, 94, 20.5, "#B91C1C", "9 KILLED", "#FFFFFF", 10.6, rx=2.5)
        + _pill("p2", 86, 28.5, 94, 20, "#1E293B", "ZAPORIZHZHIA", "#FFFFFF", 9.0, rx=2.5, letter_spacing=0.15)
    )
    scenes[4] = _wrap_mid(4, card_regions[4], "#E2E8F0", "#94A3B8", body_4, "Ukraine strikes 9 killed Zaporizhzhia")

    # #5 Mid (186x54): Paris Pharma — soft sky-blue + tilted purple/white capsule + deep navy $41BN DEAL
    body_5 = (
        '<circle cx="44" cy="40" r="3" fill="#93C5FD"/>'
        '<circle cx="76" cy="14" r="2.6" fill="#A78BFA" opacity="0.7"/>'
        '<circle cx="84" cy="42" r="2.2" fill="#60A5FA"/>'
        '<g transform="rotate(-32 54 28)">'
        '<rect x="29" y="18" width="50" height="20" rx="10" fill="#FFFFFF" stroke="#1E1B4B" stroke-width="1.6"/>'
        '<path d="M 54,18 L 69,18 A 10,10 0 0,1 69,38 L 54,38 Z" fill="#6D28D9"/>'
        '<line x1="54" y1="18" x2="54" y2="38" stroke="#1E1B4B" stroke-width="1.4"/>'
        '<rect x="35" y="21.5" width="13" height="3.2" rx="1.6" fill="#DBEAFE"/>'
        '</g>'
        + _pill("p1", 92, 14.5, 88, 25, "#0F172A", "$41BN DEAL", "#FFFFFF", 11.2, rx=3.0)
    )
    scenes[5] = _wrap_mid(5, card_regions[5], "#DBEAFE", "#60A5FA", body_5, "Sanofi $41bn pharma deal")

    # #6 Mid (186x54): Wall St — dark navy chart with green rising arrow, red dashed dip, 50,018 + TECH -1.5%
    body_6 = (
        '<line x1="12" y1="18" x2="90" y2="18" stroke="#1E293B" stroke-width="0.9"/>'
        '<line x1="12" y1="30" x2="90" y2="30" stroke="#1E293B" stroke-width="0.9"/>'
        '<line x1="12" y1="42" x2="90" y2="42" stroke="#334155" stroke-width="1"/>'
        # Area under rising Dow line
        '<polygon points="14,42 30,36 46,38 62,25 82,12 82,42" fill="#22C55E" opacity="0.22"/>'
        # Rising green Dow curve + arrow
        '<polyline points="14,42 30,36 46,38 62,25 82,12" fill="none" stroke="#4ADE80" stroke-width="2.8" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        '<polygon points="86,9 77,11 83,17" fill="#4ADE80"/>'
        # Dashed red Nasdaq dip
        '<polyline points="22,26 42,29 62,33 84,41" fill="none" stroke="#F87171" stroke-width="1.8" stroke-dasharray="3.5 2"/>'
        + _pill("p1", 94, 4.5, 86, 21, "#15803D", "50,018", "#FFFFFF", 10.6, rx=2.5)
        + _pill("p2", 94, 28.5, 86, 20.5, "#B91C1C", "TECH -1.5%", "#FFFFFF", 9.6, rx=2.5, letter_spacing=0.15)
    )
    scenes[6] = _wrap_mid(6, card_regions[6], "#0F172A", "#334155", body_6, "Dow 50,018 Nasdaq -1.5%")

    # #7 Mid (186x54): Kourou Space — deep indigo space + rocket liftoff + stars + bordered gold 36 SATS
    body_7 = (
        '<circle cx="32" cy="11" r="1.2" fill="#E2E8F0"/>'
        '<circle cx="78" cy="12" r="1.3" fill="#FDE68A"/>'
        '<circle cx="24" cy="36" r="1.1" fill="#93C5FD"/>'
        '<circle cx="84" cy="39" r="1.2" fill="#CBD5E1"/>'
        '<circle cx="68" cy="24" r="1.0" fill="#FFFFFF"/>'
        '<path d="M 18,32 Q 52,5 90,22" fill="none" stroke="#38BDF8" stroke-width="1.1" stroke-dasharray="3 2" opacity="0.6"/>'
        # Exhaust flame
        '<polygon points="52,36 44,50 52,45 60,50" fill="#F97316"/>'
        '<polygon points="52,36 48,45 52,43 56,45" fill="#FACC15"/>'
        # Ariane 6 boosters & fuselage
        '<rect x="42.5" y="21" width="4.8" height="15" rx="1.6" fill="#CBD5E1"/>'
        '<rect x="56.7" y="21" width="4.8" height="15" rx="1.6" fill="#CBD5E1"/>'
        '<path d="M 48,16 C 48,8 52,5 52,5 C 52,5 56,8 56,16 L 56,36 L 48,36 Z" fill="#F8FAFC" stroke="#38BDF8" stroke-width="0.9"/>'
        '<rect x="48" y="16" width="8" height="3.5" fill="#0284C7"/>'
        '<circle cx="52" cy="24" r="1.9" fill="#0F172A"/>'
        + _pill("p1", 96, 14.5, 84, 25, "#0F172A", "36 SATS", "#FACC15", 11.8, rx=3.0, stroke="#FACC15", stroke_w=1.2)
    )
    scenes[7] = _wrap_mid(7, card_regions[7], "#1E1B4B", "#4338CA", body_7, "Ariane 6 36 satellites launch")

    # #8 Mid (186x54): UAE disaster — warm apricot highway + bus/truck silhouettes + dark terracotta 13 DEAD
    body_8 = (
        # Highway asphalt & dashed lane
        '<rect x="1" y="38" width="184" height="15" fill="#334155"/>'
        '<line x1="4" y1="46" x2="182" y2="46" stroke="#FDE68A" stroke-width="1.5" stroke-dasharray="8 6"/>'
        # Worker bus left (clear of pin #8 at cx=14,cy=14,r=10.5)
        '<rect x="16" y="25" width="35" height="14" rx="2.5" fill="#C2410C" stroke="#0F172A" stroke-width="1.1"/>'
        '<rect x="19" y="28" width="6.5" height="4.5" rx="0.8" fill="#FEF3C7"/>'
        '<rect x="27.5" y="28" width="6.5" height="4.5" rx="0.8" fill="#FEF3C7"/>'
        '<rect x="36" y="28" width="6.5" height="4.5" rx="0.8" fill="#FEF3C7"/>'
        '<rect x="44.5" y="28" width="4.5" height="5.5" rx="0.8" fill="#BAE6FD"/>'
        '<circle cx="24" cy="40" r="3.4" fill="#0F172A" stroke="#E2E8F0" stroke-width="1"/>'
        '<circle cx="43" cy="40" r="3.4" fill="#0F172A" stroke="#E2E8F0" stroke-width="1"/>'
        # Stalled truck right
        '<rect x="58" y="20" width="23" height="19" rx="1.5" fill="#475569" stroke="#0F172A" stroke-width="1.1"/>'
        '<path d="M 81,26 L 91,26 L 94,32 L 94,39 L 81,39 Z" fill="#64748B" stroke="#0F172A" stroke-width="1.1"/>'
        '<circle cx="65" cy="40" r="3.4" fill="#0F172A" stroke="#E2E8F0" stroke-width="1"/>'
        '<circle cx="87" cy="40" r="3.4" fill="#0F172A" stroke="#E2E8F0" stroke-width="1"/>'
        # Impact flash between bus & truck
        '<polygon points="54,17 56,23 62,22 57,27 61,31 55,30 54,35 52,29 47,29 51,25 48,20 53,22" fill="#DC2626"/>'
        '<circle cx="54" cy="26" r="2.7" fill="#FACC15"/>'
        + _pill("p1", 100, 11, 80, 24, "#9A3412", "13 DEAD", "#FFFFFF", 11.4, rx=3.0, stroke="#431407", stroke_w=0.9)
    )
    scenes[8] = _wrap_mid(8, card_regions[8], "#FFEDD5", "#FB923C", body_8, "UAE bus-truck crash 13 dead")

    # #9 Mid (186x54): Port Sudan aid — mint-green coastal wave + bright blue water drop + forest-green $55M AID
    body_9 = (
        '<path d="M 1,40 Q 26,33 52,40 T 104,40 T 156,40 T 185,40 L 185,53 L 1,53 Z" fill="#86EFAC"/>'
        '<path d="M 1,45 Q 28,40 56,45 T 112,45 T 168,45 L 185,45 L 185,53 L 1,53 Z" fill="#38BDF8" opacity="0.6"/>'
        # Bright blue water drop
        '<path d="M 55,9 C 55,9 70,25 70,34 A 15,15 0 0,1 40,34 C 40,25 55,9 55,9 Z" '
        'fill="#0284C7" stroke="#0C4A6E" stroke-width="1.4"/>'
        '<path d="M 48,31 C 48,26 52,20 54,17 C 53,23 51,28 51,33 A 4,4 0 0,1 48,31 Z" fill="#BAE6FD"/>'
        + _pill("p1", 92, 14.5, 88, 25, "#15803D", "$55M AID", "#FFFFFF", 11.4, rx=3.0, stroke="#14532D", stroke_w=0.9)
    )
    scenes[9] = _wrap_mid(9, card_regions[9], "#DCFCE7", "#4ADE80", body_9, "Port Sudan $55m water aid")

    # #10 Mid (186x54): Hanoi blast — cyan storefront + starburst explosion + crimson 6 DEAD
    body_10 = (
        '<rect x="1" y="42" width="184" height="11" fill="#A5F3FC"/>'
        # Storefront facade
        '<rect x="20" y="21" width="44" height="26" fill="#334155" stroke="#0F172A" stroke-width="1.2"/>'
        '<polygon points="18,21 66,21 62,14 22,14" fill="#0E7490" stroke="#0F172A" stroke-width="1"/>'
        '<rect x="25" y="27" width="14" height="11" fill="#E0F2FE"/>'
        '<rect x="44" y="27" width="14" height="20" fill="#1E293B"/>'
        # Starburst explosion
        '<polygon points="66,9 70,18 81,14 75,23 87,27 76,30 81,40 70,34 65,44 62,33 52,35 58,26 50,19 61,20" fill="#DC2626"/>'
        '<polygon points="66,15 69,21 75,19 72,24 78,27 72,29 74,34 68,31 65,36 63,30 58,31 61,26 57,22 63,23" fill="#FACC15"/>'
        + _pill("p1", 100, 14.5, 80, 25, "#B91C1C", "6 DEAD", "#FFFFFF", 11.8, rx=3.0, stroke="#7F1D1D", stroke_w=0.9)
    )
    scenes[10] = _wrap_mid(10, card_regions[10], "#CFFAFE", "#22D3EE", body_10, "Hanoi gas blast 6 dead")

    # #11 Mid (186x54): Nepal quake — seafoam seismograph baseline + bold waveform + dark teal M5.3
    body_11 = (
        '<line x1="8" y1="15" x2="106" y2="15" stroke="#99F6E4" stroke-width="0.9"/>'
        '<line x1="8" y1="27" x2="106" y2="27" stroke="#5EEAD4" stroke-width="1.1"/>'
        '<line x1="8" y1="39" x2="106" y2="39" stroke="#99F6E4" stroke-width="0.9"/>'
        '<polyline points="8,27 26,27 32,23 37,32 42,16 48,43 54,7 60,46 66,13 72,38 78,20 84,32 90,26 106,27" '
        'fill="none" stroke="#0F766E" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
        + _pill("p1", 110, 14.5, 70, 25, "#0F766E", "M5.3", "#FFFFFF", 12.6, rx=3.0, stroke="#134E4A", stroke_w=0.9)
    )
    scenes[11] = _wrap_mid(11, card_regions[11], "#CCFBF1", "#2DD4BF", body_11, "Nepal M5.3 earthquake")

    # #12 Mid (186x54): Brazil weather — light rose storm cloud + lightning + rain + plum 20,000 FLEE
    body_12 = (
        '<path d="M 27,26 C 21,26 20,18 26,16 C 27,10 36,8 42,11.5 C 47,7 58,9 60,15 '
        'C 67,15 70,21 66,25.5 C 65,26 63,26 61,26 Z" fill="#334155" stroke="#0F172A" stroke-width="1.3"/>'
        '<polygon points="46,23 40,34 45.5,34 42,46 54,32 48,32 51.5,23" fill="#FACC15" stroke="#B45309" stroke-width="0.9"/>'
        '<g stroke="#9D174D" stroke-width="1.9" stroke-linecap="round">'
        '<line x1="29" y1="30" x2="25" y2="41"/>'
        '<line x1="36" y1="30" x2="32" y2="43"/>'
        '<line x1="59" y1="30" x2="55" y2="42"/>'
        '<line x1="66" y1="30" x2="62" y2="41"/>'
        '</g>'
        + _pill("p1", 84, 14.5, 96, 25, "#831843", "20,000 FLEE", "#FFFFFF", 10.6, rx=3.0, stroke="#500724", stroke_w=0.9)
    )
    scenes[12] = _wrap_mid(12, card_regions[12], "#FCE7F3", "#F472B6", body_12, "Brazil storm 20,000 displaced")

    # #13 Mid (186x54): Australia tech law — ice-blue shield with checkmark + ocean-blue 5% FINE
    body_13 = (
        '<path d="M 54,8 L 74,14 L 74,28 C 74,38 65,45 54,49 C 43,45 34,38 34,28 L 34,14 Z" '
        'fill="#0284C7" stroke="#0F172A" stroke-width="1.6"/>'
        '<path d="M 54,8 L 74,14 L 74,28 C 74,38 65,45 54,49 Z" fill="#0369A1"/>'
        '<polyline points="44,28 51,35 65,20" fill="none" stroke="#FFFFFF" stroke-width="3.8" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="24" cy="23" r="2.2" fill="#0369A1"/>'
        '<circle cx="24" cy="34" r="2.2" fill="#0369A1"/>'
        '<line x1="26.2" y1="23" x2="34" y2="23" stroke="#0369A1" stroke-width="1.4"/>'
        '<line x1="26.2" y1="34" x2="34" y2="34" stroke="#0369A1" stroke-width="1.4"/>'
        + _pill("p1", 94, 14.5, 86, 25, "#0369A1", "5% FINE", "#FFFFFF", 11.8, rx=3.0, stroke="#0C4A6E", stroke_w=0.9)
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
        # North America (clearly inset from left edge, enclosing #6 (73,56) & #2 (101,46))
        '<path d="M 16,24 L 46,16 L 86,15 L 114,24 L 118,38 L 108,52 L 96,62 L 84,74 '
        'L 72,74 L 62,62 L 48,58 L 36,46 L 22,38 Z"/>'
        # Central America land bridge
        '<path d="M 76,72 L 90,82 L 98,88 L 93,91 L 80,83 L 71,74 Z"/>'
        # Greenland
        '<path d="M 122,9 L 152,8 L 155,21 L 136,28 L 123,21 Z"/>'
        # South America (clearly framed, enclosing #7 (115,92) & #12 (118,136))
        '<path d="M 96,86 L 118,86 L 136,102 L 140,118 L 130,138 L 118,158 L 106,172 '
        'L 98,166 L 96,142 L 88,116 L 90,96 Z"/>'
        # UK & Ireland
        '<path d="M 155,25 L 165,24 L 166,36 L 156,37 Z"/>'
        # Europe (enclosing #5 (175,43) & #4 (209,39))
        '<path d="M 166,38 L 178,18 L 198,12 L 218,16 L 226,30 L 222,48 L 208,53 '
        'L 192,50 L 178,52 L 165,48 Z"/>'
        # Africa (enclosing #9 (193,98))
        '<path d="M 160,60 L 188,56 L 208,62 L 216,78 L 224,96 L 216,120 L 202,148 '
        'L 188,158 L 176,146 L 172,118 L 158,100 L 154,78 Z"/>'
        # Madagascar
        '<path d="M 222,126 L 228,126 L 227,142 L 221,141 Z"/>'
        # Middle East & Asia (enclosing #1 (215,79), #8 (242,77), #11 (266,70), #10 (290,83), #3 (305,59))
        '<path d="M 216,52 L 226,22 L 270,14 L 318,18 L 346,28 L 338,46 L 320,56 L 314,72 '
        'L 302,88 L 292,98 L 284,86 L 270,104 L 258,88 L 250,76 L 246,88 L 226,90 L 212,78 L 212,64 Z"/>'
        # Japan
        '<path d="M 328,44 L 336,42 L 338,58 L 330,62 Z"/>'
        # Maritime SE Asia / Indonesia
        '<path d="M 284,106 L 306,110 L 322,112 L 318,118 L 296,116 L 282,111 Z"/>'
        # Australia (enclosing #13 (316,146))
        '<path d="M 284,126 L 310,120 L 332,128 L 336,146 L 322,160 L 296,158 L 282,144 Z"/>'
        # New Zealand
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
