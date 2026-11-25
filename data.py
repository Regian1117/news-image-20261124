"""Structured news dataset for Tuesday 24 November 2026 broadsheet frontpage."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class RegionMeta:
    key: str
    label: str
    color: str
    expected_count: int


@dataclass(frozen=True)
class CardItem:
    num: int
    region: str
    kicker: str
    epistemic: str
    sources: str
    headline: str
    deck: str
    scene_id: int


@dataclass(frozen=True)
class BriefItem:
    num: int
    region: str
    lead: str
    body: str
    epistemic: str
    show_badge: bool = False


REGIONS: List[RegionMeta] = [
    RegionMeta("Europe", "EUROPE", "#1E3A8A", 9),
    RegionMeta("Middle East", "MIDDLE EAST", "#D97706", 5),
    RegionMeta("South & SE Asia", "SOUTH & SE ASIA", "#0D9488", 5),
    RegionMeta("S. America", "S. AMERICA", "#A21CAF", 4),
    RegionMeta("Africa", "AFRICA", "#991B1B", 3),
    RegionMeta("East Asia", "EAST ASIA", "#15803D", 3),
    RegionMeta("N. America", "N. AMERICA", "#7C3AED", 3),
    RegionMeta("Oceania", "OCEANIA", "#0284C7", 3),
    RegionMeta("World & Space", "WORLD & SPACE", "#334155", 3),
]

REGION_COLORS: Dict[str, str] = {r.key: r.color for r in REGIONS}

EPISTEMIC_COLORS: Dict[str, str] = {
    "CONFIRMED": "#047857",
    "OFFICIAL": "#0F766E",
    "REPORTED": "#1D4ED8",
    "CLAIM": "#B45309",
}

EDITION_DATE = "Tuesday 24 November 2026"
EDITION_DATE_SHORT = "TUE 24 NOV 2026 (UTC)"
FIELD_COUNT = 14

SUBHEAD = (
    "Houthi strike hits Riyadh tower & Saudis bomb Hodeidah · "
    "China probes Shanghai chief Chen Jining · "
    "Russian drone enters Poland; Warsaw summons envoy."
)

TIMELINE_ANCHORS: List[Tuple[str, str]] = [
    ("01:30", "Poland drone alert"),
    ("05:00", "Canberra AI bill"),
    ("09:00", "Germany Ifo 90.6"),
    ("12:00", "Shanghai CCDI probe"),
    ("16:00", "Riyadh tower & Hodeidah"),
    ("21:00", "Wall Street close"),
]

HERO_CARDS: List[CardItem] = [
    CardItem(
        num=1,
        region="Middle East",
        kicker="RIYADH & YEMEN · GULF CONFLICT",
        epistemic="REPORTED",
        sources="Reuters · Al Arabiya",
        headline="Houthi strike hits Riyadh tower; Saudi jets bomb Hodeidah",
        deck=(
            "Projectile hits KAFD office tower injuring 11; coalition hits "
            "Yemen port & intercepts Ras Tanura drones."
        ),
        scene_id=1,
    ),
    CardItem(
        num=2,
        region="East Asia",
        kicker="BEIJING & SHANGHAI · POLITICS",
        epistemic="OFFICIAL",
        sources="Xinhua · Guardian",
        headline="China probes Shanghai party chief Chen Jining",
        deck=(
            "Sitting Politburo member placed under CCDI corruption probe, "
            "the 4th top official targeted since 2025."
        ),
        scene_id=2,
    ),
    CardItem(
        num=3,
        region="Europe",
        kicker="POLAND · NATO AIRSPACE",
        epistemic="OFFICIAL",
        sources="Reuters · Polish MoD",
        headline="Russian drone enters Poland; Warsaw summons envoy",
        deck=(
            "Jet-powered drone crosses near Dorohusk overnight; NATO deploys "
            "AWACS surveillance on eastern flank."
        ),
        scene_id=3,
    ),
]

MID_CARDS: List[CardItem] = [
    CardItem(
        num=4,
        region="Middle East",
        kicker="GAZA CITY · CONFLICT",
        epistemic="CONFIRMED",
        sources="Al Arabiya · SCMP",
        headline="Israeli strike kills Hamas security chief in Gaza",
        deck="Airstrike in western Gaza City kills internal security director Naeem Abu Nahel.",
        scene_id=4,
    ),
    CardItem(
        num=5,
        region="Europe",
        kicker="ZAPORIZHZHIA · UKRAINE WAR",
        epistemic="REPORTED",
        sources="WashPost · NV",
        headline="Russian strikes hit Zaporizhzhia flats, killing 2",
        deck="Aerial strikes damage residential blocks and injure dozens across the southern city.",
        scene_id=5,
    ),
    CardItem(
        num=6,
        region="Europe",
        kicker="ENGLAND · CLIMATE HEALTH",
        epistemic="OFFICIAL",
        sources="UKHSA · Guardian",
        headline="England logs record 5,258 summer heat deaths",
        deck="UK Health Security Agency interim tally marks highest summer heat toll on record.",
        scene_id=6,
    ),
    CardItem(
        num=7,
        region="Oceania",
        kicker="CANBERRA · TECH LAW",
        epistemic="OFFICIAL",
        sources="Guardian · AP",
        headline="Australia clinches Digital Duty of Care bill",
        deck="Parliament deal sets fines up to 5% of global revenue on platforms & AI chatbots.",
        scene_id=7,
    ),
    CardItem(
        num=8,
        region="South & SE Asia",
        kicker="GENEVA · HUMAN RIGHTS",
        epistemic="OFFICIAL",
        sources="Reuters · UK Gov",
        headline="14 nations urge Myanmar to obey ICJ rulings",
        deck="UK, Canada, Australia and allies demand compliance on Rohingya accountability.",
        scene_id=8,
    ),
    CardItem(
        num=9,
        region="S. America",
        kicker="BRAZIL · EXTREME WEATHER",
        epistemic="OFFICIAL",
        sources="IOM · AP",
        headline="Southern Brazil storm displaces nearly 20,000",
        deck="Five dead after severe storm damages 93% of homes in Tupancireta municipality.",
        scene_id=9,
    ),
    CardItem(
        num=10,
        region="World & Space",
        kicker="ESA · ASTRONOMY",
        epistemic="OFFICIAL",
        sources="ESA · CBS",
        headline="Euclid telescope finds farthest known quasar",
        deck="Record galactic core shines from just 630 million years after the Big Bang.",
        scene_id=10,
    ),
    CardItem(
        num=11,
        region="Europe",
        kicker="FRANCE · AUTO & EV",
        epistemic="OFFICIAL",
        sources="Euronext · Reuters",
        headline="BYD in exclusive talks to buy French car plant",
        deck="Chinese EV maker negotiates for Ineos Hambach site as second EU factory.",
        scene_id=11,
    ),
]

BRIEF_COLUMNS: List[List[BriefItem]] = [
    # Column 1 (#12-#20)
    [
        BriefItem(12, "Europe", "UK Defence:", "MI5 warns Ukraine arms firms of sabotage.", "OFFICIAL"),
        BriefItem(13, "Europe", "UK Cyber:", "NCSC flags rise in AI autonomous attacks.", "OFFICIAL"),
        BriefItem(14, "Europe", "France Crypto:", "Senate rejects €100k wallet reporting rule.", "OFFICIAL"),
        BriefItem(15, "Europe", "Germany Ifo:", "Business index rises 7th month to 90.6.", "CONFIRMED"),
        BriefItem(16, "Europe", "Champions League:", "Arsenal draw 1–1 with Dortmund.", "OFFICIAL"),
        BriefItem(17, "Middle East", "Hormuz Mines:", "IRGC says mines hit oil tankers.", "CLAIM", show_badge=True),
        BriefItem(18, "Middle East", "OPCW Funds:", "Iran blasts US for withholding dues.", "OFFICIAL"),
        BriefItem(19, "Middle East", "IDF Probes:", "Israel confirms human-shield inquiries.", "REPORTED"),
        BriefItem(20, "Africa", "Port Sudan:", "AfDB & UNICEF launch $55m water aid.", "OFFICIAL"),
    ],
    # Column 2 (#21-#29)
    [
        BriefItem(21, "Africa", "South Africa:", "Memorial honors ex-Deputy PM Ngcuka.", "OFFICIAL"),
        BriefItem(22, "Africa", "Africa Space:", "Pretoria unveils $372m satellite plan.", "OFFICIAL"),
        BriefItem(23, "East Asia", "Global Autos:", "Chinese EVs overtake Japan in 6 markets.", "REPORTED"),
        BriefItem(24, "East Asia", "US–China:", "Bilateral farm talks open in Beijing.", "OFFICIAL"),
        BriefItem(25, "South & SE Asia", "Indonesia:", "139 returned after $2.9m Manila scam raid.", "OFFICIAL"),
        BriefItem(26, "South & SE Asia", "Vietnam:", "Hanoi eatery explosion kills 6, hurts 12+.", "REPORTED"),
        BriefItem(27, "South & SE Asia", "India Deals:", "PE/VC hits 5-year high of $8.7bn.", "REPORTED"),
        BriefItem(28, "South & SE Asia", "Thailand:", "Passes OECD review; tests Mekong.", "OFFICIAL"),
        BriefItem(29, "N. America", "Wall Street:", "Nasdaq -1.48% (23,734), S&P -0.50%.", "CONFIRMED"),
    ],
    # Column 3 (#30-#38)
    [
        BriefItem(30, "N. America", "US–Canada:", "Ottawa rejects Pentagon spending critique.", "OFFICIAL"),
        BriefItem(31, "N. America", "Mexico–China:", "Panel tackles $120bn+ trade gap.", "OFFICIAL"),
        BriefItem(32, "S. America", "Colombia:", "Gunmen hold ~30 in Cartagena store.", "REPORTED"),
        BriefItem(33, "S. America", "WTO Case:", "Brazil challenges US Sec. 301 tariffs.", "OFFICIAL"),
        BriefItem(34, "S. America", "PAHO Alert:", "Latin America warned on H5N1 bird flu.", "OFFICIAL"),
        BriefItem(35, "Oceania", "Vanuatu:", "Files ICJ case vs France over islands.", "OFFICIAL"),
        BriefItem(36, "Oceania", "Sydney Trial:", "Ex-officer guilty of double murder.", "OFFICIAL"),
        BriefItem(37, "World & Space", "UN AI Arms:", "Guterres urges rules on killer drones.", "OFFICIAL"),
        BriefItem(38, "World & Space", "Arctic Study:", "1960s warming halted natural ice age.", "REPORTED"),
    ],
]

DATE_CHECK_TEXT = (
    "Every story above happened or was first reported on Tue 24 Nov 2026 (UTC). "
    "Left out: EU 22nd Russia sanctions & US $14.7bn Iran OFAC (Mon 23 Nov) · "
    "Vanuatu M6.5 quake (Mon 23 Nov) · BepiColombo Mercury orbit (21 Nov) · "
    "Voyager 1 light-day (18 Nov) · Cartagena rescue storming (early Wed 25 Nov)."
)

FOOTER_SOURCES = "Sources: Reuters, AP, Guardian, Xinhua, UKHSA, ESA, IOM, AfDB, WTO · Drawn in code"


def compute_region_counts() -> Dict[str, int]:
    counts: Dict[str, int] = {r.key: 0 for r in REGIONS}
    for card in HERO_CARDS + MID_CARDS:
        counts[card.region] += 1
    for col in BRIEF_COLUMNS:
        for brief in col:
            counts[brief.region] += 1
    return counts


def validate_dataset() -> Tuple[int, Dict[str, int]]:
    counts = compute_region_counts()
    total = sum(counts.values())
    assert total == 38, f"Expected 38 stories, got {total}"
    for region in REGIONS:
        actual = counts[region.key]
        assert actual == region.expected_count, (
            f"Region {region.key}: expected {region.expected_count}, got {actual}"
        )
    all_nums = (
        [c.num for c in HERO_CARDS]
        + [c.num for c in MID_CARDS]
        + [b.num for col in BRIEF_COLUMNS for b in col]
    )
    assert all_nums == list(range(1, 39)), "Story numbering must be contiguous 1..38"
    return total, counts
