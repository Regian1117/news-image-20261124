"""Custom geometric vector SVG scenes for Hero (314x78) and Mid (236x52) cards."""

from __future__ import annotations

from html import escape
from typing import Dict


FONT_SANS = "'Segoe UI', Arial, Helvetica, sans-serif"


def _hero_svg(bg: str, band: str, art: str, primary: str, sub: str, dark_bg: bool = False) -> str:
    pill_stroke = ' stroke="#94A3B8" stroke-width="1.2"' if dark_bg else ' stroke="#020617" stroke-width="0.6"'
    frame_stroke = "#334155" if dark_bg else "#CBD5E1"
    return (
        f'<svg class="scene-svg hero-svg" viewBox="0 0 314 78" width="314" height="78" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(primary)} — {escape(sub)}">'
        f'<rect x="0.5" y="0.5" width="313" height="77" rx="3" fill="{bg}" stroke="{frame_stroke}" stroke-width="1"/>'
        f'<rect x="1" y="54" width="312" height="23" fill="{band}" opacity="0.42"/>'
        f'<line x1="111" y1="7" x2="111" y2="71" stroke="#94A3B8" stroke-width="1" stroke-dasharray="2 2" opacity="0.7"/>'
        f'<g class="scene-art">{art}</g>'
        f'<g class="callout-group">'
        f'<rect class="callout-pill" data-pill="primary" x="118" y="10.5" width="186" height="27.5" rx="4" fill="#0F172A"{pill_stroke}/>'
        f'<text class="callout-text" data-pill-for="primary" x="211" y="29.1" text-anchor="middle" '
        f'font-family="{FONT_SANS}" font-size="13.5" font-weight="900" letter-spacing="0.35" fill="#FFFFFF">'
        f'{escape(primary)}</text>'
        f'<rect class="callout-pill" data-pill="sub" x="118" y="42.5" width="186" height="24" rx="3" '
        f'fill="#FACC15" stroke="#B45309" stroke-width="1"/>'
        f'<text class="callout-text" data-pill-for="sub" x="211" y="58.6" text-anchor="middle" '
        f'font-family="{FONT_SANS}" font-size="11.0" font-weight="900" letter-spacing="0.5" fill="#0F172A">'
        f'{escape(sub)}</text>'
        f'</g></svg>'
    )


def _mid_svg(bg: str, band: str, art: str, primary: str, sub: str, dark_bg: bool = False) -> str:
    pill_stroke = ' stroke="#94A3B8" stroke-width="1.2"' if dark_bg else ' stroke="#020617" stroke-width="0.6"'
    sep_stroke = "#475569" if dark_bg else "#94A3B8"
    frame_stroke = "#334155" if dark_bg else "#CBD5E1"
    return (
        f'<svg class="scene-svg mid-svg" viewBox="0 0 236 52" width="236" height="52" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(primary)} — {escape(sub)}">'
        f'<rect x="0.5" y="0.5" width="235" height="51" rx="2.5" fill="{bg}" stroke="{frame_stroke}" stroke-width="1"/>'
        f'<rect x="1" y="36" width="234" height="15" fill="{band}" opacity="0.42"/>'
        f'<line x1="71" y1="5" x2="71" y2="47" stroke="{sep_stroke}" stroke-width="1" stroke-dasharray="2 2" opacity="0.7"/>'
        f'<g class="scene-art">{art}</g>'
        f'<g class="callout-group">'
        f'<rect class="callout-pill" data-pill="primary" x="76" y="4" width="152" height="22.5" rx="3" fill="#0F172A"{pill_stroke}/>'
        f'<text class="callout-text" data-pill-for="primary" x="152" y="19.3" text-anchor="middle" '
        f'font-family="{FONT_SANS}" font-size="10.9" font-weight="900" letter-spacing="0.2" fill="#FFFFFF">'
        f'{escape(primary)}</text>'
        f'<rect class="callout-pill" data-pill="sub" x="76" y="29" width="152" height="19.5" rx="2.5" '
        f'fill="#FACC15" stroke="#B45309" stroke-width="1"/>'
        f'<text class="callout-text" data-pill-for="sub" x="152" y="42.4" text-anchor="middle" '
        f'font-family="{FONT_SANS}" font-size="9.3" font-weight="900" letter-spacing="0.3" fill="#0F172A">'
        f'{escape(sub)}</text>'
        f'</g></svg>'
    )


def build_scenes() -> Dict[int, str]:
    scenes: Dict[int, str] = {}

    # #1 Hero: Riyadh KAFD skyline towers, incoming missile, burst (x strictly 0..108)
    art_1 = (
        # Ground horizon
        '<rect x="6" y="68" width="98" height="4" rx="1" fill="#92400E" opacity="0.45"/>'
        # Left towers
        '<rect x="12" y="42" width="14" height="26" fill="#475569"/>'
        '<rect x="15" y="46" width="3" height="4" fill="#FDE68A"/>'
        '<rect x="20" y="46" width="3" height="4" fill="#FDE68A"/>'
        '<rect x="15" y="54" width="3" height="4" fill="#CBD5E1"/>'
        '<rect x="20" y="54" width="3" height="4" fill="#CBD5E1"/>'
        '<polygon points="30,68 30,28 42,20 48,28 48,68" fill="#334155"/>'
        '<rect x="34" y="32" width="3" height="4" fill="#E2E8F0"/>'
        '<rect x="40" y="32" width="3" height="4" fill="#E2E8F0"/>'
        '<rect x="34" y="40" width="3" height="4" fill="#FDE68A"/>'
        '<rect x="40" y="40" width="3" height="4" fill="#E2E8F0"/>'
        '<rect x="34" y="48" width="3" height="4" fill="#E2E8F0"/>'
        '<rect x="40" y="48" width="3" height="4" fill="#FDE68A"/>'
        # Main KAFD faceted tower
        '<polygon points="54,68 54,14 68,8 78,16 78,68" fill="#1E293B"/>'
        '<polygon points="68,8 78,16 78,68 68,68" fill="#0F172A"/>'
        '<rect x="58" y="20" width="4" height="5" fill="#93C5FD"/>'
        '<rect x="58" y="29" width="4" height="5" fill="#93C5FD"/>'
        '<rect x="58" y="38" width="4" height="5" fill="#FDE68A"/>'
        '<rect x="58" y="47" width="4" height="5" fill="#93C5FD"/>'
        '<rect x="58" y="56" width="4" height="5" fill="#93C5FD"/>'
        # Right secondary tower
        '<rect x="83" y="38" width="16" height="30" fill="#475569"/>'
        '<rect x="86" y="43" width="3.5" height="4" fill="#CBD5E1"/>'
        '<rect x="92" y="43" width="3.5" height="4" fill="#FDE68A"/>'
        '<rect x="86" y="52" width="3.5" height="4" fill="#CBD5E1"/>'
        '<rect x="92" y="52" width="3.5" height="4" fill="#CBD5E1"/>'
        # Incoming missile trail & body
        '<path d="M 10,12 Q 36,12 58,24" fill="none" stroke="#DC2626" stroke-width="2" stroke-dasharray="4 2.5"/>'
        '<polygon points="44,16 56,22 47,24" fill="#991B1B"/>'
        # Impact starburst on main tower
        '<polygon points="72,14 75,21 83,18 78,25 86,29 77,31 79,39 72,33 65,38 67,30 59,28 67,24 65,16 70,21" fill="#DC2626"/>'
        '<polygon points="72,19 74,24 79,23 76,27 80,30 75,30 75,34 72,31 68,33 69,29 65,28 69,25 68,21 71,24" fill="#FACC15"/>'
        '<circle cx="94" cy="20" r="6" fill="#94A3B8" opacity="0.45"/>'
        '<circle cx="100" cy="14" r="4.5" fill="#64748B" opacity="0.35"/>'
    )
    scenes[1] = _hero_svg("#FEF3C7", "#FDE68A", art_1, "11 HURT · PORT HIT", "RIYADH & YEMEN")

    # #2 Hero: China probe — crimson emblem + dark official seal (x strictly 0..108)
    art_2 = (
        # Crimson emblem circle
        '<circle cx="44" cy="39" r="28" fill="#991B1B"/>'
        '<circle cx="44" cy="39" r="23.5" fill="#B91C1C" stroke="#FACC15" stroke-width="1.6"/>'
        # Gold five-point star
        '<polygon points="44,21 48,33 60,33 50,40 54,52 44,45 34,52 38,40 28,33 40,33" fill="#FACC15"/>'
        # Official dark CCDI inspection seal overlapping right
        '<circle cx="80" cy="46" r="21" fill="#0F172A" stroke="#F8FAFC" stroke-width="2"/>'
        '<circle cx="80" cy="46" r="16" fill="none" stroke="#FACC15" stroke-width="1.2" stroke-dasharray="3 2"/>'
        # Magnifying glass inside seal
        '<circle cx="78" cy="43" r="6.5" fill="none" stroke="#F8FAFC" stroke-width="2.4"/>'
        '<line x1="83" y1="48" x2="90" y2="55" stroke="#FACC15" stroke-width="3" stroke-linecap="round"/>'
    )
    scenes[2] = _hero_svg("#ECFDF5", "#D1FAE5", art_2, "POLITBURO PROBE", "SHANGHAI CHIEF")

    # #3 Hero: Poland NATO airspace — Polish flag + radar rings + drone silhouette (x strictly 0..108)
    art_3 = (
        # Radar concentric rings centered at (69, 41)
        '<circle cx="69" cy="41" r="30" fill="#DBEAFE" stroke="#1E3A8A" stroke-width="1.2" stroke-dasharray="3 2.5"/>'
        '<circle cx="69" cy="41" r="20" fill="none" stroke="#1E3A8A" stroke-width="1.2" opacity="0.8"/>'
        '<circle cx="69" cy="41" r="10" fill="none" stroke="#1E3A8A" stroke-width="1.2" opacity="0.8"/>'
        '<line x1="39" y1="41" x2="99" y2="41" stroke="#1E3A8A" stroke-width="0.9" opacity="0.55"/>'
        '<line x1="69" y1="11" x2="69" y2="71" stroke="#1E3A8A" stroke-width="0.9" opacity="0.55"/>'
        '<path d="M 69,41 L 91,20 A 30,30 0 0,1 99,41 Z" fill="#1D4ED8" opacity="0.22"/>'
        '<circle cx="69" cy="41" r="2.8" fill="#1E3A8A"/>'
        # Polish flag top-left
        '<rect x="10" y="13" width="34" height="11" fill="#FFFFFF" stroke="#64748B" stroke-width="0.8"/>'
        '<rect x="10" y="24" width="34" height="11" fill="#DC143C" stroke="#64748B" stroke-width="0.8"/>'
        '<line x1="10" y1="12" x2="10" y2="62" stroke="#334155" stroke-width="2" stroke-linecap="round"/>'
        # Jet delta-wing drone silhouette entering from east
        '<polygon points="62,25 89,19 84,26 94,32 76,29 72,35 71,28" fill="#0F172A"/>'
        '<circle cx="94" cy="24" r="3" fill="#DC2626"/>'
        '<line x1="97" y1="24" x2="104" y2="24" stroke="#DC2626" stroke-width="1.8" stroke-dasharray="2 1.5"/>'
    )
    scenes[3] = _hero_svg("#EFF6FF", "#BFDBFE", art_3, "NATO AIRSPACE", "EASTERN FLANK")

    # #4 Mid: Gaza City — target reticle (x strictly 0..68)
    art_4 = (
        '<circle cx="36" cy="26" r="18" fill="#FEF3C7" stroke="#B45309" stroke-width="2"/>'
        '<circle cx="36" cy="26" r="10.5" fill="none" stroke="#DC2626" stroke-width="1.6" stroke-dasharray="3 2"/>'
        '<line x1="12" y1="26" x2="60" y2="26" stroke="#991B1B" stroke-width="1.6"/>'
        '<line x1="36" y1="4" x2="36" y2="48" stroke="#991B1B" stroke-width="1.6"/>'
        '<circle cx="36" cy="26" r="3.6" fill="#DC2626"/>'
        # Corner viewfinder ticks
        '<path d="M 14,12 L 14,8 L 18,8 M 54,8 L 58,8 L 58,12 M 14,40 L 14,44 L 18,44 M 54,44 L 58,44 L 58,40" '
        'fill="none" stroke="#0F172A" stroke-width="1.5"/>'
    )
    scenes[4] = _mid_svg("#FFFBEB", "#FDE68A", art_4, "SECURITY CHIEF", "GAZA CITY")

    # #5 Mid: Zaporizhzhia flats — apartment silhouettes + strike mark (x strictly 0..68)
    art_5 = (
        '<rect x="8" y="21" width="16" height="26" fill="#475569"/>'
        '<rect x="11" y="25" width="3.5" height="3.5" fill="#E2E8F0"/>'
        '<rect x="17" y="25" width="3.5" height="3.5" fill="#FDE047"/>'
        '<rect x="11" y="32" width="3.5" height="3.5" fill="#E2E8F0"/>'
        '<rect x="17" y="32" width="3.5" height="3.5" fill="#E2E8F0"/>'
        '<rect x="11" y="39" width="3.5" height="3.5" fill="#FDE047"/>'
        '<rect x="27" y="13" width="19" height="34" fill="#1E293B"/>'
        '<rect x="30" y="19" width="4" height="4" fill="#93C5FD"/>'
        '<rect x="38" y="19" width="4" height="4" fill="#FDE047"/>'
        '<rect x="30" y="27" width="4" height="4" fill="#E2E8F0"/>'
        '<rect x="38" y="27" width="4" height="4" fill="#93C5FD"/>'
        '<rect x="30" y="35" width="4" height="4" fill="#E2E8F0"/>'
        '<rect x="38" y="35" width="4" height="4" fill="#E2E8F0"/>'
        '<rect x="49" y="24" width="15" height="23" fill="#334155"/>'
        '<rect x="52" y="28" width="3.5" height="3.5" fill="#E2E8F0"/>'
        '<rect x="58" y="28" width="3.5" height="3.5" fill="#E2E8F0"/>'
        '<rect x="52" y="35" width="3.5" height="3.5" fill="#FDE047"/>'
        # Strike flash & burst on center flats
        '<polygon points="40,5 44,12 52,10 47,16 53,21 44,20 42,26 39,19 32,20 37,15 33,9 39,11" fill="#DC2626"/>'
        '<polygon points="41,9 43,13 48,13 44,16 47,19 42,18 41,21 40,17 36,17 39,15 37,12 40,13" fill="#FACC15"/>'
    )
    scenes[5] = _mid_svg("#EFF6FF", "#BFDBFE", art_5, "2 DEAD · 40+ HURT", "UKRAINE WAR")

    # #6 Mid: England heat deaths — sun + red thermometer (x strictly 0..68)
    art_6 = (
        # Sun
        '<circle cx="24" cy="25" r="9.5" fill="#F59E0B" stroke="#D97706" stroke-width="1.2"/>'
        '<g stroke="#D97706" stroke-width="2" stroke-linecap="round">'
        '<line x1="24" y1="8" x2="24" y2="12"/>'
        '<line x1="24" y1="38" x2="24" y2="42"/>'
        '<line x1="7" y1="25" x2="11" y2="25"/>'
        '<line x1="37" y1="25" x2="41" y2="25"/>'
        '<line x1="12" y1="13" x2="15" y2="16"/>'
        '<line x1="33" y1="34" x2="36" y2="37"/>'
        '<line x1="12" y1="37" x2="15" y2="34"/>'
        '<line x1="33" y1="16" x2="36" y2="13"/>'
        '</g>'
        # Thermometer
        '<rect x="49" y="6" width="9" height="29" rx="4.5" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.6"/>'
        '<circle cx="53.5" cy="39" r="7.2" fill="#DC2626" stroke="#0F172A" stroke-width="1.6"/>'
        '<rect x="51.4" y="11" width="4.2" height="27" rx="2" fill="#DC2626"/>'
        '<line x1="60" y1="12" x2="64" y2="12" stroke="#0F172A" stroke-width="1.2"/>'
        '<line x1="60" y1="18" x2="63" y2="18" stroke="#0F172A" stroke-width="1.2"/>'
        '<line x1="60" y1="24" x2="64" y2="24" stroke="#0F172A" stroke-width="1.2"/>'
    )
    scenes[6] = _mid_svg("#FEF2F2", "#FECACA", art_6, "5,258 DEATHS", "ENGLAND HEAT")

    # #7 Mid: Australia tech bill — blue shield + checkmark (x strictly 0..68)
    art_7 = (
        '<path d="M 36,6 L 56,12 L 56,26 C 56,36 47,43 36,47 C 25,43 16,36 16,26 L 16,12 Z" '
        'fill="#0284C7" stroke="#0F172A" stroke-width="1.8"/>'
        '<path d="M 36,6 L 56,12 L 56,26 C 56,36 47,43 36,47 Z" fill="#0369A1"/>'
        '<polyline points="26,26 33,33 47,18" fill="none" stroke="#FFFFFF" stroke-width="4" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        # Digital node accents left
        '<circle cx="10" cy="18" r="2.2" fill="#0284C7"/>'
        '<circle cx="10" cy="30" r="2.2" fill="#0284C7"/>'
        '<line x1="12" y1="18" x2="16" y2="18" stroke="#0284C7" stroke-width="1.4"/>'
        '<line x1="12" y1="30" x2="16" y2="30" stroke="#0284C7" stroke-width="1.4"/>'
    )
    scenes[7] = _mid_svg("#F0F9FF", "#BAE6FD", art_7, "5% GLOBAL FINE", "TECH SAFETY")

    # #8 Mid: 14 nations Myanmar ICJ — justice scales (x strictly 0..68)
    art_8 = (
        # Pillar & base
        '<rect x="34.2" y="10" width="3.6" height="33" fill="#0F172A"/>'
        '<rect x="23" y="42" width="26" height="4.5" rx="1.5" fill="#0F766E"/>'
        '<circle cx="36" cy="10" r="3" fill="#0D9488" stroke="#0F172A" stroke-width="1.2"/>'
        # Crossbar
        '<line x1="14" y1="15" x2="58" y2="15" stroke="#0F172A" stroke-width="2.4" stroke-linecap="round"/>'
        # Left pan
        '<line x1="17" y1="15" x2="11" y2="30" stroke="#334155" stroke-width="1.2"/>'
        '<line x1="17" y1="15" x2="23" y2="30" stroke="#334155" stroke-width="1.2"/>'
        '<path d="M 9,30 Q 17,38 25,30 Z" fill="#0D9488" stroke="#0F172A" stroke-width="1.2"/>'
        # Right pan
        '<line x1="55" y1="15" x2="49" y2="30" stroke="#334155" stroke-width="1.2"/>'
        '<line x1="55" y1="15" x2="61" y2="30" stroke="#334155" stroke-width="1.2"/>'
        '<path d="M 47,30 Q 55,38 63,30 Z" fill="#0D9488" stroke="#0F172A" stroke-width="1.2"/>'
    )
    scenes[8] = _mid_svg("#F0FDFA", "#99F6E4", art_8, "14 NATIONS", "ICJ RULINGS")

    # #9 Mid: Southern Brazil storm — storm cloud + lightning + rain (x strictly 0..68)
    art_9 = (
        # Dark storm cloud
        '<path d="M 15,27 C 9,27 8,18 14,16 C 15,9 24,7 30,11 C 35,6 46,8 48,14 '
        'C 55,14 59,20 55,26 C 54,27 52,27 50,27 Z" fill="#334155" stroke="#0F172A" stroke-width="1.4"/>'
        # Lightning bolt
        '<polygon points="36,24 29,36 35,36 31,47 44,33 37,33 41,24" fill="#FACC15" stroke="#B45309" stroke-width="1"/>'
        # Rain streaks
        '<g stroke="#A21CAF" stroke-width="2" stroke-linecap="round">'
        '<line x1="16" y1="31" x2="12" y2="41"/>'
        '<line x1="24" y1="31" x2="20" y2="43"/>'
        '<line x1="48" y1="31" x2="44" y2="42"/>'
        '<line x1="56" y1="31" x2="52" y2="41"/>'
        '</g>'
    )
    scenes[9] = _mid_svg("#FDF4FF", "#F5D0FE", art_9, "20,000 DISPLACED", "93% HOMES HIT")

    # #10 Mid: Euclid farthest quasar — dark starfield + glowing quasar (x strictly 0..68)
    art_10 = (
        # Starfield dots
        '<circle cx="11" cy="11" r="1.1" fill="#E2E8F0"/>'
        '<circle cx="22" cy="8" r="1.4" fill="#93C5FD"/>'
        '<circle cx="58" cy="10" r="1.2" fill="#FDE68A"/>'
        '<circle cx="14" cy="40" r="1.3" fill="#CBD5E1"/>'
        '<circle cx="56" cy="42" r="1.1" fill="#93C5FD"/>'
        '<circle cx="62" cy="24" r="1.0" fill="#FFFFFF"/>'
        '<circle cx="18" cy="28" r="0.9" fill="#FFFFFF"/>'
        # Accretion halo & rings
        '<ellipse cx="36" cy="26" rx="22" ry="8" transform="rotate(-18 36 26)" '
        'fill="none" stroke="#38BDF8" stroke-width="1.6" opacity="0.85"/>'
        '<circle cx="36" cy="26" r="10.5" fill="#F59E0B" opacity="0.35"/>'
        # 4-point quasar diffraction spikes
        '<polygon points="36,7 38.5,23.5 55,26 38.5,28.5 36,45 33.5,28.5 17,26 33.5,23.5" fill="#FACC15"/>'
        '<circle cx="36" cy="26" r="5" fill="#FFFFFF"/>'
    )
    scenes[10] = _mid_svg("#1E293B", "#0F172A", art_10, "630M YRS", "DEEP SPACE", dark_bg=True)

    # #11 Mid: BYD French car plant — blue electric vehicle + lightning bolt (x strictly 0..68)
    art_11 = (
        # Road line
        '<line x1="8" y1="42" x2="64" y2="42" stroke="#64748B" stroke-width="1.8" stroke-linecap="round"/>'
        # EV body
        '<path d="M 11,35 L 13,25 L 22,16 L 45,16 L 55,25 L 61,27 L 62,35 Z" '
        'fill="#1D4ED8" stroke="#0F172A" stroke-width="1.4"/>'
        # Cabin windows
        '<polygon points="23,19 35,19 35,25 17,25" fill="#BFDBFE"/>'
        '<polygon points="37,19 44,19 51,25 37,25" fill="#BFDBFE"/>'
        # Wheels
        '<circle cx="22" cy="36" r="5.8" fill="#0F172A"/>'
        '<circle cx="22" cy="36" r="2.4" fill="#E2E8F0"/>'
        '<circle cx="50" cy="36" r="5.8" fill="#0F172A"/>'
        '<circle cx="50" cy="36" r="2.4" fill="#E2E8F0"/>'
        # EV lightning bolt badge on door
        '<polygon points="36,24 31,31 35,31 33,37 41,29 37,29 39,24" fill="#FACC15" stroke="#0F172A" stroke-width="0.6"/>'
    )
    scenes[11] = _mid_svg("#EFF6FF", "#BFDBFE", art_11, "2ND EU EV PLANT", "FRANCE EV DEAL")

    return scenes
