"""Custom geometric vector SVG scenes (Hero 314x68, Mid 236x46) and world locator map."""

from __future__ import annotations

from html import escape
from typing import Dict, List

from data import MAP_PINS, REGION_COLORS, MapPin

FONT_SANS = "'Segoe UI', Arial, Helvetica, sans-serif"


def _hero_svg(bg: str, band: str, art: str, primary: str, sub: str, dark_bg: bool = False) -> str:
    pill_stroke = ' stroke="#94A3B8" stroke-width="1.2"' if dark_bg else ' stroke="#020617" stroke-width="0.6"'
    frame_stroke = "#334155" if dark_bg else "#CBD5E1"
    return (
        f'<svg class="scene-svg hero-svg" viewBox="0 0 314 68" width="314" height="68" '
        f'preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{escape(primary)} — {escape(sub)}">'
        f'<rect x="0.5" y="0.5" width="313" height="67" rx="3" fill="{bg}" stroke="{frame_stroke}" stroke-width="1"/>'
        f'<rect x="1" y="47" width="312" height="20" fill="{band}" opacity="0.42"/>'
        f'<line x1="109" y1="6" x2="109" y2="62" stroke="#94A3B8" stroke-width="1" stroke-dasharray="2 2" opacity="0.72"/>'
        f'<g class="scene-art">{art}</g>'
        f'<g class="callout-group">'
        f'<rect class="callout-pill" data-pill="primary" x="116" y="7" width="188" height="26" rx="4" fill="#0F172A"{pill_stroke}/>'
        f'<text class="callout-text" data-pill-for="primary" x="210" y="24.6" text-anchor="middle" '
        f'font-family="{FONT_SANS}" font-size="13.0" font-weight="900" letter-spacing="0.3" fill="#FFFFFF">'
        f'{escape(primary)}</text>'
        f'<rect class="callout-pill" data-pill="sub" x="116" y="37" width="188" height="23.5" rx="3" '
        f'fill="#FACC15" stroke="#B45309" stroke-width="1"/>'
        f'<text class="callout-text" data-pill-for="sub" x="210" y="52.7" text-anchor="middle" '
        f'font-family="{FONT_SANS}" font-size="10.6" font-weight="900" letter-spacing="0.45" fill="#0F172A">'
        f'{escape(sub)}</text>'
        f'</g></svg>'
    )


def _mid_svg(bg: str, band: str, art: str, primary: str, sub: str, dark_bg: bool = False) -> str:
    pill_stroke = ' stroke="#94A3B8" stroke-width="1.2"' if dark_bg else ' stroke="#020617" stroke-width="0.6"'
    sep_stroke = "#475569" if dark_bg else "#94A3B8"
    frame_stroke = "#334155" if dark_bg else "#CBD5E1"
    return (
        f'<svg class="scene-svg mid-svg" viewBox="0 0 236 46" width="236" height="46" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(primary)} — {escape(sub)}">'
        f'<rect x="0.5" y="0.5" width="235" height="45" rx="2.5" fill="{bg}" stroke="{frame_stroke}" stroke-width="1"/>'
        f'<rect x="1" y="32" width="234" height="13" fill="{band}" opacity="0.42"/>'
        f'<line x1="68" y1="4.5" x2="68" y2="41.5" stroke="{sep_stroke}" stroke-width="1" stroke-dasharray="2 2" opacity="0.72"/>'
        f'<g class="scene-art">{art}</g>'
        f'<g class="callout-group">'
        f'<rect class="callout-pill" data-pill="primary" x="73" y="2.5" width="156" height="20.5" rx="3" fill="#0F172A"{pill_stroke}/>'
        f'<text class="callout-text" data-pill-for="primary" x="151" y="16.8" text-anchor="middle" '
        f'font-family="{FONT_SANS}" font-size="10.0" font-weight="900" letter-spacing="0.2" fill="#FFFFFF">'
        f'{escape(primary)}</text>'
        f'<rect class="callout-pill" data-pill="sub" x="73" y="25.5" width="156" height="18" rx="2.5" '
        f'fill="#FACC15" stroke="#B45309" stroke-width="0.9"/>'
        f'<text class="callout-text" data-pill-for="sub" x="151" y="37.7" text-anchor="middle" '
        f'font-family="{FONT_SANS}" font-size="8.6" font-weight="900" letter-spacing="0.28" fill="#0F172A">'
        f'{escape(sub)}</text>'
        f'</g></svg>'
    )


def build_scenes() -> Dict[int, str]:
    scenes: Dict[int, str] = {}

    # #1 Hero (314x68, art x <= 104): Riyadh KAFD skyline towers, incoming missile, burst
    art_1 = (
        '<rect x="6" y="59" width="95" height="3.5" rx="1" fill="#92400E" opacity="0.45"/>'
        '<rect x="11" y="37" width="13" height="22" fill="#475569"/>'
        '<rect x="14" y="41" width="3" height="3.5" fill="#FDE68A"/>'
        '<rect x="19" y="41" width="3" height="3.5" fill="#FDE68A"/>'
        '<rect x="14" y="48" width="3" height="3.5" fill="#CBD5E1"/>'
        '<rect x="19" y="48" width="3" height="3.5" fill="#CBD5E1"/>'
        '<polygon points="28,59 28,25 39,18 45,25 45,59" fill="#334155"/>'
        '<rect x="32" y="29" width="3" height="3.5" fill="#E2E8F0"/>'
        '<rect x="38" y="29" width="3" height="3.5" fill="#E2E8F0"/>'
        '<rect x="32" y="36" width="3" height="3.5" fill="#FDE68A"/>'
        '<rect x="38" y="36" width="3" height="3.5" fill="#E2E8F0"/>'
        '<rect x="32" y="44" width="3" height="3.5" fill="#E2E8F0"/>'
        '<rect x="38" y="44" width="3" height="3.5" fill="#FDE68A"/>'
        '<polygon points="51,59 51,12 65,7 75,14 75,59" fill="#1E293B"/>'
        '<polygon points="65,7 75,14 75,59 65,59" fill="#0F172A"/>'
        '<rect x="55" y="18" width="4" height="4.5" fill="#93C5FD"/>'
        '<rect x="55" y="26" width="4" height="4.5" fill="#93C5FD"/>'
        '<rect x="55" y="34" width="4" height="4.5" fill="#FDE68A"/>'
        '<rect x="55" y="42" width="4" height="4.5" fill="#93C5FD"/>'
        '<rect x="55" y="50" width="4" height="4.5" fill="#93C5FD"/>'
        '<rect x="80" y="33" width="16" height="26" fill="#475569"/>'
        '<rect x="83" y="38" width="3.5" height="3.5" fill="#CBD5E1"/>'
        '<rect x="89" y="38" width="3.5" height="3.5" fill="#FDE68A"/>'
        '<rect x="83" y="46" width="3.5" height="3.5" fill="#CBD5E1"/>'
        '<rect x="89" y="46" width="3.5" height="3.5" fill="#CBD5E1"/>'
        '<path d="M 9,10 Q 34,10 56,21" fill="none" stroke="#DC2626" stroke-width="2" stroke-dasharray="4 2.5"/>'
        '<polygon points="42,14 54,19.5 45,21.5" fill="#991B1B"/>'
        '<polygon points="69,12 72,18 79,16 75,22 82,25 74,27 76,34 69,29 63,33 65,26 57,24 64,21 63,14 67,18" fill="#DC2626"/>'
        '<polygon points="69,16 71,21 75,20 73,23 76,26 72,26 72,30 69,27 66,29 67,25 63,24 66,22 66,18 68,21" fill="#FACC15"/>'
        '<circle cx="91" cy="17" r="5" fill="#94A3B8" opacity="0.45"/>'
        '<circle cx="97" cy="12" r="4" fill="#64748B" opacity="0.35"/>'
    )
    scenes[1] = _hero_svg("#FEF3C7", "#FDE68A", art_1, "11 HURT · PORT HIT", "RIYADH & YEMEN")

    # #2 Hero (314x68, art x <= 104): China probe — crimson emblem + dark official seal
    art_2 = (
        '<circle cx="42" cy="34" r="25" fill="#991B1B"/>'
        '<circle cx="42" cy="34" r="20.5" fill="#B91C1C" stroke="#FACC15" stroke-width="1.5"/>'
        '<polygon points="42,18 45.6,29 57,29 47.8,35.5 51.3,46.5 42,40 32.7,46.5 36.2,35.5 27,29 38.4,29" fill="#FACC15"/>'
        '<circle cx="77" cy="40" r="19" fill="#0F172A" stroke="#F8FAFC" stroke-width="1.8"/>'
        '<circle cx="77" cy="40" r="14.5" fill="none" stroke="#FACC15" stroke-width="1.2" stroke-dasharray="3 2"/>'
        '<circle cx="75" cy="37.5" r="5.8" fill="none" stroke="#F8FAFC" stroke-width="2.2"/>'
        '<line x1="79.5" y1="42" x2="86" y2="48.5" stroke="#FACC15" stroke-width="2.8" stroke-linecap="round"/>'
    )
    scenes[2] = _hero_svg("#ECFDF5", "#D1FAE5", art_2, "POLITBURO PROBE", "SHANGHAI CHIEF")

    # #3 Hero (314x68, art x <= 104): Brooklyn US Courts — courthouse + gavel illustration
    art_3 = (
        # Courthouse facade left-center (x=10..66)
        '<polygon points="38,8 10,22 66,22" fill="#4C1D95" stroke="#0F172A" stroke-width="1.2"/>'
        '<circle cx="38" cy="16.5" r="2.5" fill="#FACC15"/>'
        '<rect x="12" y="22" width="52" height="3.5" fill="#334155"/>'
        '<rect x="16" y="25.5" width="6" height="26" fill="#FFFFFF" stroke="#475569" stroke-width="1"/>'
        '<rect x="28" y="25.5" width="6" height="26" fill="#FFFFFF" stroke="#475569" stroke-width="1"/>'
        '<rect x="42" y="25.5" width="6" height="26" fill="#FFFFFF" stroke="#475569" stroke-width="1"/>'
        '<rect x="54" y="25.5" width="6" height="26" fill="#FFFFFF" stroke="#475569" stroke-width="1"/>'
        '<rect x="11" y="51.5" width="54" height="4" fill="#475569"/>'
        '<rect x="8" y="55.5" width="60" height="4.5" rx="1" fill="#1E293B"/>'
        # Judge gavel & sound block on right (x=66..102)
        '<rect x="70" y="53" width="28" height="6.5" rx="2" fill="#7C3AED" stroke="#0F172A" stroke-width="1.2"/>'
        '<g transform="rotate(-32 82 32)">'
        '<rect x="72" y="21" width="22" height="12" rx="2.5" fill="#92400E" stroke="#0F172A" stroke-width="1.3"/>'
        '<rect x="74" y="20" width="3.5" height="14" rx="1" fill="#FACC15"/>'
        '<rect x="88.5" y="20" width="3.5" height="14" rx="1" fill="#FACC15"/>'
        '<rect x="81" y="33" width="4.5" height="21" rx="1.5" fill="#B45309" stroke="#0F172A" stroke-width="1"/>'
        '</g>'
    )
    scenes[3] = _hero_svg("#F5F3FF", "#DDD6FE", art_3, "10 OF 12 GUILTY", "CLEARED OF RICO")

    # #4 Mid (236x46, art x <= 64): Poland NATO airspace — flag + radar rings + drone
    art_4 = (
        '<circle cx="43" cy="24" r="18" fill="#DBEAFE" stroke="#1E3A8A" stroke-width="1" stroke-dasharray="2.5 2"/>'
        '<circle cx="43" cy="24" r="11.5" fill="none" stroke="#1E3A8A" stroke-width="1" opacity="0.8"/>'
        '<circle cx="43" cy="24" r="5.5" fill="none" stroke="#1E3A8A" stroke-width="1" opacity="0.8"/>'
        '<line x1="25" y1="24" x2="61" y2="24" stroke="#1E3A8A" stroke-width="0.8" opacity="0.5"/>'
        '<line x1="43" y1="6" x2="43" y2="42" stroke="#1E3A8A" stroke-width="0.8" opacity="0.5"/>'
        '<path d="M 43,24 L 56,11 A 18,18 0 0,1 61,24 Z" fill="#1D4ED8" opacity="0.22"/>'
        '<rect x="7" y="8" width="22" height="7.5" fill="#FFFFFF" stroke="#64748B" stroke-width="0.7"/>'
        '<rect x="7" y="15.5" width="22" height="7.5" fill="#DC143C" stroke="#64748B" stroke-width="0.7"/>'
        '<line x1="7" y1="7" x2="7" y2="40" stroke="#334155" stroke-width="1.8" stroke-linecap="round"/>'
        '<polygon points="36,15 55,11 51,16 58,20 46,18 43,22 42,17" fill="#0F172A"/>'
        '<circle cx="59" cy="14" r="2.2" fill="#DC2626"/>'
    )
    scenes[4] = _mid_svg("#EFF6FF", "#BFDBFE", art_4, "NATO AIRSPACE", "EASTERN FLANK")

    # #5 Mid (236x46, art x <= 64): Sanofi–Insmed $41bn pharma deal — medical pill + cross
    art_5 = (
        # Medical cross badge left
        '<rect x="8" y="10" width="24" height="26" rx="4" fill="#1E3A8A" stroke="#0F172A" stroke-width="1.2"/>'
        '<rect x="17" y="14.5" width="6" height="17" rx="1" fill="#FFFFFF"/>'
        '<rect x="11.5" y="20" width="17" height="6" rx="1" fill="#FFFFFF"/>'
        # Two-tone tilted pharmaceutical capsule right
        '<g transform="rotate(-34 48 24)">'
        '<rect x="34" y="17" width="28" height="13" rx="6.5" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.4"/>'
        '<path d="M 48,17 L 55.5,17 A 6.5,6.5 0 0,1 55.5,30 L 48,30 Z" fill="#0D9488"/>'
        '<line x1="48" y1="17" x2="48" y2="30" stroke="#0F172A" stroke-width="1.2"/>'
        '<rect x="38" y="19.5" width="7" height="2.2" rx="1" fill="#BFDBFE"/>'
        '</g>'
    )
    scenes[5] = _mid_svg("#EFF6FF", "#DBEAFE", art_5, "$41BN DEAL", "PHARMA BUYOUT")

    # #6 Mid (236x46, art x <= 64): Dow 50,018 — dark slate rising green chart
    art_6 = (
        # Subtle gridlines
        '<line x1="8" y1="14" x2="62" y2="14" stroke="#334155" stroke-width="0.8"/>'
        '<line x1="8" y1="24" x2="62" y2="24" stroke="#334155" stroke-width="0.8"/>'
        '<line x1="8" y1="34" x2="62" y2="34" stroke="#334155" stroke-width="0.8"/>'
        # Area fill under rising line
        '<polygon points="8,38 18,33 27,35 37,24 46,26 57,10 57,40 8,40" fill="#22C55E" opacity="0.22"/>'
        # Rising green line + points + arrow
        '<polyline points="8,38 18,33 27,35 37,24 46,26 57,10" fill="none" stroke="#4ADE80" stroke-width="2.6" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        '<polygon points="59,7 51,10 58,15" fill="#4ADE80"/>'
        '<circle cx="18" cy="33" r="2" fill="#86EFAC"/>'
        '<circle cx="37" cy="24" r="2" fill="#86EFAC"/>'
        '<line x1="8" y1="40" x2="62" y2="40" stroke="#64748B" stroke-width="1.2"/>'
    )
    scenes[6] = _mid_svg("#0F172A", "#1E293B", art_6, "DOW 50,018", "NASDAQ -1.5%", dark_bg=True)

    # #7 Mid (236x46, art x <= 64): Ariane 6 launch — dark space rocket liftoff
    art_7 = (
        # Starfield
        '<circle cx="11" cy="9" r="1.1" fill="#E2E8F0"/>'
        '<circle cx="21" cy="14" r="1.2" fill="#93C5FD"/>'
        '<circle cx="56" cy="11" r="1.2" fill="#FDE68A"/>'
        '<circle cx="14" cy="31" r="1.0" fill="#CBD5E1"/>'
        '<circle cx="58" cy="28" r="1.1" fill="#93C5FD"/>'
        # Exhaust flame plume
        '<polygon points="35,31 28,43 35,39 42,43" fill="#F97316"/>'
        '<polygon points="35,31 31.5,39 35,37 38.5,39" fill="#FACC15"/>'
        # Rocket boosters & core
        '<rect x="26.5" y="19" width="4.2" height="13" rx="1.5" fill="#CBD5E1"/>'
        '<rect x="39.3" y="19" width="4.2" height="13" rx="1.5" fill="#CBD5E1"/>'
        '<path d="M 31.5,14 C 31.5,7 35,4.5 35,4.5 C 35,4.5 38.5,7 38.5,14 L 38.5,31 L 31.5,31 Z" '
        'fill="#F8FAFC" stroke="#38BDF8" stroke-width="0.9"/>'
        '<rect x="31.5" y="14" width="7" height="3" fill="#0284C7"/>'
        '<circle cx="35" cy="21" r="1.7" fill="#0F172A"/>'
        # Orbit arc hint
        '<path d="M 10,20 Q 35,2 61,18" fill="none" stroke="#38BDF8" stroke-width="1" stroke-dasharray="2.5 2" opacity="0.65"/>'
    )
    scenes[7] = _mid_svg("#0F172A", "#1E293B", art_7, "36 SATELLITES", "ARIANE 6 VA271", dark_bg=True)

    # #8 Mid (236x46, art x <= 64): England heat deaths — sun + red thermometer
    art_8 = (
        '<circle cx="22" cy="22" r="8.5" fill="#F59E0B" stroke="#D97706" stroke-width="1.1"/>'
        '<g stroke="#D97706" stroke-width="1.8" stroke-linecap="round">'
        '<line x1="22" y1="7" x2="22" y2="10.5"/>'
        '<line x1="22" y1="33.5" x2="22" y2="37"/>'
        '<line x1="7" y1="22" x2="10.5" y2="22"/>'
        '<line x1="33.5" y1="22" x2="37" y2="22"/>'
        '<line x1="11.5" y1="11.5" x2="14" y2="14"/>'
        '<line x1="30" y1="30" x2="32.5" y2="32.5"/>'
        '<line x1="11.5" y1="32.5" x2="14" y2="30"/>'
        '<line x1="30" y1="14" x2="32.5" y2="11.5"/>'
        '</g>'
        '<rect x="46" y="5" width="8.5" height="25.5" rx="4.2" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.5"/>'
        '<circle cx="50.25" cy="34.5" r="6.4" fill="#DC2626" stroke="#0F172A" stroke-width="1.5"/>'
        '<rect x="48.2" y="9.5" width="4.1" height="24" rx="2" fill="#DC2626"/>'
        '<line x1="56.5" y1="10.5" x2="60.5" y2="10.5" stroke="#0F172A" stroke-width="1.1"/>'
        '<line x1="56.5" y1="16" x2="59.5" y2="16" stroke="#0F172A" stroke-width="1.1"/>'
        '<line x1="56.5" y1="21.5" x2="60.5" y2="21.5" stroke="#0F172A" stroke-width="1.1"/>'
    )
    scenes[8] = _mid_svg("#FEF2F2", "#FECACA", art_8, "5,258 DEATHS", "ENGLAND HEAT")

    # #9 Mid (236x46, art x <= 64): Gaza City — precision target reticle
    art_9 = (
        '<circle cx="34" cy="23" r="16" fill="#FEF3C7" stroke="#B45309" stroke-width="1.8"/>'
        '<circle cx="34" cy="23" r="9.2" fill="none" stroke="#DC2626" stroke-width="1.5" stroke-dasharray="3 2"/>'
        '<line x1="12" y1="23" x2="56" y2="23" stroke="#991B1B" stroke-width="1.5"/>'
        '<line x1="34" y1="4" x2="34" y2="42" stroke="#991B1B" stroke-width="1.5"/>'
        '<circle cx="34" cy="23" r="3.2" fill="#DC2626"/>'
        '<path d="M 14,10 L 14,6.5 L 18,6.5 M 50,6.5 L 54,6.5 L 54,10 M 14,36 L 14,39.5 L 18,39.5 M 50,39.5 L 54,39.5 L 54,36" '
        'fill="none" stroke="#0F172A" stroke-width="1.4"/>'
    )
    scenes[9] = _mid_svg("#FFFBEB", "#FDE68A", art_9, "SECURITY CHIEF", "GAZA CITY")

    # #10 Mid (236x46, art x <= 64): Australia tech bill — blue shield + checkmark
    art_10 = (
        '<path d="M 35,5 L 53,10.5 L 53,23 C 53,32 45,38 35,41.5 C 25,38 17,32 17,23 L 17,10.5 Z" '
        'fill="#0284C7" stroke="#0F172A" stroke-width="1.6"/>'
        '<path d="M 35,5 L 53,10.5 L 53,23 C 53,32 45,38 35,41.5 Z" fill="#0369A1"/>'
        '<polyline points="26,23 32.5,29.5 45,16" fill="none" stroke="#FFFFFF" stroke-width="3.6" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="10.5" cy="16" r="2" fill="#0284C7"/>'
        '<circle cx="10.5" cy="27" r="2" fill="#0284C7"/>'
        '<line x1="12.5" y1="16" x2="17" y2="16" stroke="#0284C7" stroke-width="1.3"/>'
        '<line x1="12.5" y1="27" x2="17" y2="27" stroke="#0284C7" stroke-width="1.3"/>'
    )
    scenes[10] = _mid_svg("#F0F9FF", "#BAE6FD", art_10, "5% GLOBAL FINE", "ONLINE SAFETY")

    # #11 Mid (236x46, art x <= 64): Southern Brazil storm — storm cloud + lightning + rain
    art_11 = (
        '<path d="M 15,24 C 9.5,24 8.5,16 14,14 C 15,8 23.5,6 29,9.5 C 33.5,5 43.5,7 45.5,12.5 '
        'C 52,12.5 55.5,18 52,23 C 51,24 49,24 47,24 Z" fill="#334155" stroke="#0F172A" stroke-width="1.3"/>'
        '<polygon points="34,21 28,31.5 33.5,31.5 30,41.5 41.5,29 35.5,29 39,21" fill="#FACC15" stroke="#B45309" stroke-width="0.9"/>'
        '<g stroke="#A21CAF" stroke-width="1.8" stroke-linecap="round">'
        '<line x1="16" y1="27.5" x2="12.5" y2="36.5"/>'
        '<line x1="23.5" y1="27.5" x2="20" y2="38"/>'
        '<line x1="45.5" y1="27.5" x2="42" y2="37.5"/>'
        '<line x1="53" y1="27.5" x2="49.5" y2="36.5"/>'
        '</g>'
    )
    scenes[11] = _mid_svg("#FDF4FF", "#F5D0FE", art_11, "20,000 DISPLACED", "BRAZIL STORM")

    return scenes


def build_world_map_svg(pins: List[MapPin] = MAP_PINS) -> str:
    """Clean editorial world locator map (360x172) with 11 region-colored numbered pins."""
    # Simplified accurate continents aligned to pin coordinates (1..11)
    continents = (
        # North America
        '<path d="M 16,22 L 42,14 L 78,12 L 106,18 L 112,30 L 98,42 L 96,52 L 84,58 L 76,68 '
        'L 66,68 L 58,56 L 44,54 L 34,42 L 22,34 Z" fill="#C7C0B0" stroke="#78716C" stroke-width="0.9"/>'
        # Central America & Caribbean
        '<path d="M 74,66 L 86,74 L 94,80 L 90,82 L 78,75 L 70,68 Z" fill="#C7C0B0" stroke="#78716C" stroke-width="0.8"/>'
        # Greenland
        '<path d="M 116,8 L 146,7 L 150,19 L 132,26 L 118,20 Z" fill="#C7C0B0" stroke="#78716C" stroke-width="0.85"/>'
        # South America
        '<path d="M 94,78 L 112,80 L 128,94 L 134,108 L 124,126 L 114,144 L 104,158 L 96,154 '
        'L 94,132 L 86,108 L 86,88 Z" fill="#C7C0B0" stroke="#78716C" stroke-width="0.9"/>'
        # UK & Ireland
        '<path d="M 154,19 L 164,18 L 166,28 L 156,29 Z" fill="#C7C0B0" stroke="#78716C" stroke-width="0.8"/>'
        # Europe
        '<path d="M 164,34 L 176,16 L 196,10 L 214,14 L 222,26 L 218,44 L 204,49 L 190,46 '
        'L 178,49 L 164,46 L 162,38 Z" fill="#C7C0B0" stroke="#78716C" stroke-width="0.9"/>'
        # Africa
        '<path d="M 158,56 L 184,52 L 206,56 L 214,68 L 224,84 L 218,104 L 204,128 L 190,140 '
        'L 178,132 L 172,108 L 160,92 L 152,74 Z" fill="#C7C0B0" stroke="#78716C" stroke-width="0.9"/>'
        # Madagascar
        '<path d="M 222,114 L 227,114 L 226,128 L 220,127 Z" fill="#C7C0B0" stroke="#78716C" stroke-width="0.75"/>'
        # Middle East & Asia
        '<path d="M 214,48 L 222,22 L 264,12 L 312,16 L 342,26 L 334,42 L 318,52 L 312,68 '
        'L 298,82 L 288,92 L 282,82 L 270,96 L 258,84 L 252,72 L 246,84 L 230,84 L 218,68 '
        'L 214,58 Z" fill="#C7C0B0" stroke="#78716C" stroke-width="0.9"/>'
        # Japan
        '<path d="M 326,42 L 334,40 L 336,54 L 328,58 Z" fill="#C7C0B0" stroke="#78716C" stroke-width="0.8"/>'
        # Indonesia / Maritime SE Asia
        '<path d="M 284,98 L 302,102 L 318,104 L 314,110 L 294,108 L 282,103 Z" '
        'fill="#C7C0B0" stroke="#78716C" stroke-width="0.8"/>'
        # Australia
        '<path d="M 284,118 L 306,112 L 326,118 L 332,134 L 320,146 L 296,144 L 282,134 Z" '
        'fill="#C7C0B0" stroke="#78716C" stroke-width="0.9"/>'
        # New Zealand
        '<path d="M 340,142 L 348,140 L 350,154 L 342,156 Z" fill="#C7C0B0" stroke="#78716C" stroke-width="0.8"/>'
    )

    graticule = (
        '<g stroke="#B8D6EC" stroke-width="0.6" stroke-dasharray="2 2">'
        '<line x1="0" y1="43" x2="360" y2="43"/>'
        '<line x1="0" y1="86" x2="360" y2="86" stroke-dasharray="none" opacity="0.8"/>'
        '<line x1="0" y1="129" x2="360" y2="129"/>'
        '<line x1="90" y1="0" x2="90" y2="172"/>'
        '<line x1="180" y1="0" x2="180" y2="172"/>'
        '<line x1="270" y1="0" x2="270" y2="172"/>'
        '</g>'
    )

    pins_svg_parts: List[str] = []
    for p in pins:
        color = REGION_COLORS[p.region]
        fsize = "8.8" if p.num >= 10 else "9.6"
        pins_svg_parts.append(
            f'<g class="map-pin" data-pin="{p.num}" data-x="{p.x}" data-y="{p.y}">'
            f'<circle cx="{p.x}" cy="{p.y + 1.2}" r="9.2" fill="#0F172A" opacity="0.28"/>'
            f'<circle cx="{p.x}" cy="{p.y}" r="8.6" fill="{color}" stroke="#FFFFFF" stroke-width="1.6"/>'
            f'<text x="{p.x}" y="{p.y + 3.2}" text-anchor="middle" '
            f'font-family="{FONT_SANS}" font-size="{fsize}" font-weight="900" fill="#FFFFFF">{p.num}</text>'
            f'</g>'
        )

    return (
        '<svg class="world-map-svg" viewBox="0 0 360 172" width="360" height="172" '
        'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="World locator map for stories 1 to 11">'
        '<rect x="0.5" y="0.5" width="359" height="171" rx="3" fill="#D8EBF8" stroke="#94A3B8" stroke-width="1"/>'
        f'{graticule}'
        f'{continents}'
        f'{"".join(pins_svg_parts)}'
        '</svg>'
    )
