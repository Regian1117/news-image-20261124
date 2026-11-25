"""Structured 39-story world-news dataset for Tuesday 24 November 2026."""

from __future__ import annotations

import math
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


@dataclass(frozen=True)
class MapPin:
    num: int
    region: str
    x: int
    y: int
    place: str


REGIONS: List[RegionMeta] = [
    RegionMeta("Europe", "EUROPE", "#1E3A8A", 9),
    RegionMeta("Middle East", "MIDDLE EAST", "#D97706", 5),
    RegionMeta("South & SE Asia", "SOUTH & SE ASIA", "#0D9488", 5),
    RegionMeta("N. America", "N. AMERICA", "#7C3AED", 4),
    RegionMeta("World & Space", "WORLD & SPACE", "#334155", 4),
    RegionMeta("Africa", "AFRICA", "#991B1B", 3),
    RegionMeta("East Asia", "EAST ASIA", "#15803D", 3),
    RegionMeta("S. America", "S. AMERICA", "#A21CAF", 3),
    RegionMeta("Oceania", "OCEANIA", "#0284C7", 3),
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
FIELD_COUNT = 21

SUBHEAD = (
    "Houthi strike hits Riyadh tower · "
    "China probes Shanghai chief Chen Jining · "
    "US jury convicts Huawei on 10 of 12 counts."
)

TIMELINE_ANCHORS: List[Tuple[str, str]] = [
    ("01:30", "Poland drone"),
    ("05:00", "Canberra AI bill"),
    ("09:00", "Germany Ifo 90.6"),
    ("11:14", "Ariane 6 launch"),
    ("12:00", "Shanghai probe"),
    ("15:00", "US conf. 103.3"),
    ("21:00", "Dow 50,018"),
]

KEY_NUMBERS: List[Tuple[str, str]] = [
    ("10 of 12", "Huawei guilty counts"),
    ("50,018", "Dow closes past 50k"),
    ("$41bn", "Sanofi–Insmed deal"),
    ("5,258", "England heat deaths"),
    ("36 sats", "Ariane 6 Amazon Leo"),
    ("13 dead", "UAE bus-truck crash"),
]

HERO_CARDS: List[CardItem] = [
    CardItem(
        num=1,
        region="Middle East",
        kicker="RIYADH & YEMEN · GULF CONFLICT",
        epistemic="REPORTED",
        sources="Reuters · Al Arabiya",
        headline="Houthi strike hits Riyadh tower; Saudi jets bomb Hodeidah",
        deck="Projectile hits KAFD tower injuring 11; coalition strikes Yemen port & downs Ras Tanura drones.",
        scene_id=1,
    ),
    CardItem(
        num=2,
        region="East Asia",
        kicker="SHANGHAI · CHINA POLITICS",
        epistemic="OFFICIAL",
        sources="Xinhua · Guardian",
        headline="China probes Shanghai party chief Chen Jining",
        deck="Sitting Politburo member placed under CCDI corruption probe, the 4th top official targeted since 2025.",
        scene_id=2,
    ),
    CardItem(
        num=3,
        region="N. America",
        kicker="BROOKLYN · US COURTS & TECH",
        epistemic="CONFIRMED",
        sources="Reuters · Guardian",
        headline="US jury convicts Huawei on 10 of 12 criminal counts",
        deck="Federal verdict cites bank fraud, Iran sanctions and trade secrets; cleared of racketeering.",
        scene_id=3,
    ),
]

MID_CARDS: List[CardItem] = [
    CardItem(
        num=4,
        region="Europe",
        kicker="POLAND · NATO AIRSPACE",
        epistemic="OFFICIAL",
        sources="Reuters · Polish MoD",
        headline="Russian drone enters Poland; Warsaw summons envoy",
        deck="Drone crosses near Dorohusk overnight; NATO deploys AWACS jets.",
        scene_id=4,
    ),
    CardItem(
        num=5,
        region="Europe",
        kicker="FRANCE–US · PHARMA M&A",
        epistemic="OFFICIAL",
        sources="Sanofi · Reuters",
        headline="Sanofi agrees $41bn cash deal to buy Insmed",
        deck="French drugmaker expands respiratory & rare-disease pipeline.",
        scene_id=5,
    ),
    CardItem(
        num=6,
        region="N. America",
        kicker="WALL STREET · MARKETS",
        epistemic="CONFIRMED",
        sources="Reuters · ABC",
        headline="Dow closes above 50,000 as Nasdaq dips 1.5%",
        deck="Blue-chip index ends at 50,018 while chip pullback hits tech.",
        scene_id=6,
    ),
    CardItem(
        num=7,
        region="World & Space",
        kicker="KOUROU · SPACE LAUNCH",
        epistemic="CONFIRMED",
        sources="Arianespace · Xinhua",
        headline="Ariane 6 lofts 36 Amazon Leo satellites",
        deck="Tenth Ariane 6 flight lifts off at 11:14 UTC from French Guiana.",
        scene_id=7,
    ),
    CardItem(
        num=8,
        region="Europe",
        kicker="ENGLAND · CLIMATE HEALTH",
        epistemic="OFFICIAL",
        sources="UKHSA · Guardian",
        headline="England logs record 5,258 summer heat deaths",
        deck="UK Health Security Agency reports highest summer heat toll.",
        scene_id=8,
    ),
    CardItem(
        num=9,
        region="Middle East",
        kicker="GAZA CITY · CONFLICT",
        epistemic="CONFIRMED",
        sources="Al Arabiya · SCMP",
        headline="Israeli strike kills Hamas security chief in Gaza",
        deck="Airstrike in western Gaza City kills chief Naeem Abu Nahel.",
        scene_id=9,
    ),
    CardItem(
        num=10,
        region="Oceania",
        kicker="CANBERRA · TECH LAW",
        epistemic="OFFICIAL",
        sources="Guardian · AP",
        headline="Australia clinches Digital Duty of Care bill",
        deck="Parliament deal sets fines up to 5% of global revenue for harms.",
        scene_id=10,
    ),
    CardItem(
        num=11,
        region="S. America",
        kicker="BRAZIL · EXTREME WEATHER",
        epistemic="OFFICIAL",
        sources="IOM · AP",
        headline="Southern Brazil storm displaces nearly 20,000",
        deck="Five dead after severe storm destroys homes in Rio Grande do Sul.",
        scene_id=11,
    ),
]

BRIEF_COLUMNS: List[List[BriefItem]] = [
    # Col A (#12-#25)
    [
        BriefItem(12, "Europe", "Zaporizhzhia:", "Russian strikes hit homes, killing 2, hurting 40+.", "REPORTED"),
        BriefItem(13, "Europe", "BYD France:", "Exclusive talks to buy Ineos Hambach EV plant.", "OFFICIAL"),
        BriefItem(14, "Europe", "UK Defence:", "UK intelligence warns arms firms of sabotage.", "OFFICIAL"),
        BriefItem(15, "Europe", "Germany Ifo:", "Business climate index rises 7th month to 90.6.", "CONFIRMED"),
        BriefItem(16, "Europe", "France Crypto:", "Senate rejects €100k wallet reporting rule.", "OFFICIAL"),
        BriefItem(17, "Europe", "Champions League:", "Real Madrid beat PSV 5–1; Arsenal draw 1–1.", "OFFICIAL"),
        BriefItem(18, "Middle East", "UAE Crash:", "Bus hits stalled truck in Ras Al Khaimah; 13 dead.", "OFFICIAL"),
        BriefItem(19, "Middle East", "OPCW Funds:", "Iran FM criticizes US for withholding dues.", "OFFICIAL"),
        BriefItem(20, "Middle East", "IDF Probes:", "Israel confirms probes into human-shield claims.", "REPORTED"),
        BriefItem(21, "Africa", "Port Sudan:", "AfDB & UNICEF launch $55m emergency water aid.", "OFFICIAL"),
        BriefItem(22, "Africa", "Africa Space:", "South Africa unveils $372m satellite plan.", "OFFICIAL"),
        BriefItem(23, "Africa", "South Africa:", "State memorial honors ex-Deputy PM Ngcuka.", "OFFICIAL"),
        BriefItem(24, "East Asia", "Global Autos:", "Chinese EVs overtake Japan in 6 markets, lead 26.", "REPORTED"),
        BriefItem(25, "East Asia", "US–China:", "Inaugural bilateral farm talks open in Beijing.", "OFFICIAL"),
    ],
    # Col B (#26-#39)
    [
        BriefItem(26, "South & SE Asia", "Myanmar ICJ:", "14 nations urge junta to obey ICJ rulings.", "OFFICIAL"),
        BriefItem(27, "South & SE Asia", "Vietnam Blast:", "Hanoi hot-pot gas blast kills 6, hurts 12+.", "REPORTED"),
        BriefItem(28, "South & SE Asia", "Indonesia:", "139 returned after $2.9m Manila scam raid.", "OFFICIAL"),
        BriefItem(29, "South & SE Asia", "India Deals:", "PE/VC hits 5-year monthly high of $8.7bn.", "REPORTED"),
        BriefItem(30, "South & SE Asia", "Thailand:", "Passes OECD review; expands river water tests.", "OFFICIAL"),
        BriefItem(31, "N. America", "US Economy:", "Consumer confidence index climbs to 103.3 in Nov.", "CONFIRMED"),
        BriefItem(32, "N. America", "US–Canada:", "Ottawa rejects Pentagon spending critique.", "OFFICIAL"),
        BriefItem(33, "S. America", "Colombia:", "Gunmen hold ~30 hostages in Cartagena store.", "REPORTED"),
        BriefItem(34, "S. America", "WTO Case:", "Brazil seeks panel on US Section 301 tariffs.", "OFFICIAL"),
        BriefItem(35, "Oceania", "Solomons:", "Reports say Honiara will let China pact lapse.", "REPORTED"),
        BriefItem(36, "Oceania", "Vanuatu:", "Files ICJ & UNCLOS case vs France over islands.", "OFFICIAL"),
        BriefItem(37, "World & Space", "Euclid Space:", "ESA telescope finds farthest quasar (630m yrs).", "OFFICIAL"),
        BriefItem(38, "World & Space", "UNODC Brief:", "47,000 women killed by kin in 2025 (5 an hour).", "OFFICIAL"),
        BriefItem(39, "World & Space", "UN AI Arms:", "Guterres urges Security Council AI weapons rules.", "OFFICIAL"),
    ],
]

MAP_PINS: List[MapPin] = [
    MapPin(1, "Middle East", 238, 72, "Riyadh"),
    MapPin(2, "East Asia", 304, 56, "Shanghai"),
    MapPin(3, "N. America", 92, 46, "Brooklyn"),
    MapPin(4, "Europe", 202, 31, "Poland"),
    MapPin(5, "Europe", 175, 42, "France"),
    MapPin(6, "N. America", 68, 48, "Wall St"),
    MapPin(7, "World & Space", 108, 86, "Kourou"),
    MapPin(8, "Europe", 160, 22, "England"),
    MapPin(9, "Middle East", 216, 61, "Gaza"),
    MapPin(10, "Oceania", 316, 136, "Canberra"),
    MapPin(11, "S. America", 114, 126, "Brazil"),
]

DATE_CHECK_TEXT = (
    "Every story above happened or was first reported on Tue 24 Nov 2026 (UTC). "
    "Left out: Iran Hormuz mines claim, EU 22nd Russia sanctions, US $14.7bn Iran OFAC "
    "& Vanuatu M6.5 quake (Mon 23 Nov) · BepiColombo Mercury orbit (21 Nov) · "
    "Cartagena rescue storming (early Wed 25 Nov)."
)

FOOTER_SOURCES = (
    "Sources: Reuters, AP, Guardian, Xinhua, UKHSA, Arianespace, ESA, UNODC, IOM · Drawn in code"
)


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
    assert total == 39, f"Expected 39 stories, got {total}"
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
    assert all_nums == list(range(1, 40)), "Story numbering must be contiguous 1..39"
    assert [p.num for p in MAP_PINS] == list(range(1, 12)), "Map pins must be 1..11"
    for i, a in enumerate(MAP_PINS):
        for b in MAP_PINS[i + 1 :]:
            dist = math.hypot(a.x - b.x, a.y - b.y)
            assert dist >= 20.0, f"Map pins #{a.num} and #{b.num} too close: {dist:.1f}px"
    return total, counts
