"""Structured V4 38-story, 10-region, 25-field dataset for Tuesday 24 November 2026."""

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
    source: str
    epistemic: str
    highlight: str = ""


@dataclass(frozen=True)
class MapPin:
    num: int
    region: str
    x: int
    y: int


REGIONS: List[RegionMeta] = [
    RegionMeta("Europe", "EUROPE", "#1E3A8A", 6),
    RegionMeta("Middle East", "MIDDLE EAST", "#C2410C", 5),
    RegionMeta("East Asia", "EAST ASIA", "#B91C1C", 4),
    RegionMeta("N. America", "NORTH AMERICA", "#6D28D9", 4),
    RegionMeta("Africa", "AFRICA", "#15803D", 4),
    RegionMeta("LatAm", "LATIN AMERICA", "#9D174D", 3),
    RegionMeta("South Asia", "SOUTH ASIA", "#0F766E", 3),
    RegionMeta("Oceania", "OCEANIA", "#0369A1", 3),
    RegionMeta("SE Asia", "SE ASIA", "#0E7490", 3),
    RegionMeta("World", "WORLD", "#334155", 3),
]

REGION_COLORS: Dict[str, str] = {r.key: r.color for r in REGIONS}

EPISTEMIC_COLORS: Dict[str, str] = {
    "CONFIRMED": "#047857",
    "OFFICIAL": "#0F766E",
    "REPORTED": "#1D4ED8",
    "CLAIM": "#B45309",
    "ONGOING": "#6D28D9",
}

EPISTEMIC_SHORT: Dict[str, str] = {
    "CONFIRMED": "C",
    "OFFICIAL": "O",
    "REPORTED": "R",
    "CLAIM": "CL",
    "ONGOING": "ON",
}

EDITION_DATE = "Tuesday 24 November 2026"
EDITION_DATE_SHORT = "TUE 24 NOV 2026 (UTC)"
FIELD_COUNT = 25

SUBHEAD = (
    "Yemen's Houthis hit Riyadh tower; 11 hurt · "
    "US jury convicts Huawei on 10 of 12 counts · "
    "China probes Chen Jining."
)

TIMELINE_ANCHORS: List[Tuple[str, str]] = [
    ("01:00", "Hanoi blast"),
    ("01:32", "Nepal quake"),
    ("05:30", "Sanofi deal"),
    ("11:14", "Ariane 6 launch"),
    ("12:00", "Shanghai probe"),
    ("15:00", "US confidence"),
    ("21:00", "Dow 50,018"),
]

KEY_NUMBERS: List[Tuple[str, str]] = [
    ("9 dead", "Ukraine strikes toll"),
    ("$41bn", "Sanofi buys Insmed"),
    ("50,018", "Dow record close"),
    ("36", "Amazon Leo satellites"),
    ("13 dead", "UAE bus-truck crash"),
    ("20,000", "Brazil storm displaced"),
]

HERO_CARDS: List[CardItem] = [
    CardItem(
        num=1,
        region="Middle East",
        kicker="RIYADH · WAR",
        epistemic="REPORTED",
        sources="Al Arabiya",
        headline="Yemen's Houthis hit Riyadh tower; 11 hurt",
        deck="Saudi coalition blames Houthis for financial tower strike and bombs Hodeidah port.",
        scene_id=1,
    ),
    CardItem(
        num=2,
        region="N. America",
        kicker="NEW YORK · COURTS",
        epistemic="CONFIRMED",
        sources="Reuters · AP",
        headline="US jury convicts Huawei on 10 of 12 counts",
        deck="New York federal jury finds guilt on bank fraud, sanctions and trade secrets; cleared of racketeering.",
        scene_id=2,
    ),
    CardItem(
        num=3,
        region="East Asia",
        kicker="SHANGHAI · POLITICS",
        epistemic="OFFICIAL",
        sources="Reuters · CNN",
        headline="China probes Shanghai party chief Chen Jining",
        deck="Politburo member, 62, investigated for serious violations — fourth senior leader probed this term.",
        scene_id=3,
    ),
]

MID_CARDS: List[CardItem] = [
    CardItem(
        num=4,
        region="Europe",
        kicker="UKRAINE · WAR",
        epistemic="CONFIRMED",
        sources="Reuters · Kyiv Ind.",
        headline="Russian strikes kill 9 across Ukraine",
        deck="Dawn raids hit Zaporizhzhia homes; 40+ hurt nationwide.",
        scene_id=4,
    ),
    CardItem(
        num=5,
        region="Europe",
        kicker="PARIS · PHARMA",
        epistemic="OFFICIAL",
        sources="Sanofi · Reuters",
        headline="Sanofi agrees $41bn deal for Insmed",
        deck="Cash buyout expands French firm's lung-drug pipeline.",
        scene_id=5,
    ),
    CardItem(
        num=6,
        region="N. America",
        kicker="WALL ST · MARKETS",
        epistemic="CONFIRMED",
        sources="Reuters · ABC",
        headline="Dow closes past 50,000; Nasdaq dips 1.5%",
        deck="Blue-chip index ends at 50,018 as chip stocks pull back.",
        scene_id=6,
    ),
    CardItem(
        num=7,
        region="World",
        kicker="KOUROU · SPACE",
        epistemic="CONFIRMED",
        sources="Arianespace · Xinhua",
        headline="Ariane 6 lofts 36 Amazon satellites",
        deck="Tenth flight lifts off from French Guiana with broadband craft.",
        scene_id=7,
    ),
    CardItem(
        num=8,
        region="Middle East",
        kicker="UAE · DISASTER",
        epistemic="OFFICIAL",
        sources="The National · AP",
        headline="Ras Al Khaimah bus crash kills 13",
        deck="Worker bus carrying 41 hits stalled truck; 14 injured.",
        scene_id=8,
    ),
    CardItem(
        num=9,
        region="Africa",
        kicker="SUDAN · AID",
        epistemic="OFFICIAL",
        sources="AfDB · Reuters",
        headline="$55m water aid launched in Port Sudan",
        deck="AfDB and UNICEF back emergency clean water for displaced.",
        scene_id=9,
    ),
    CardItem(
        num=10,
        region="SE Asia",
        kicker="VIETNAM · DISASTER",
        epistemic="CONFIRMED",
        sources="VnExpress · AP",
        headline="Gas blast at Hanoi eatery kills 6",
        deck="Gas explosion injures 12+ and collapses restaurant front.",
        scene_id=10,
    ),
    CardItem(
        num=11,
        region="South Asia",
        kicker="NEPAL · QUAKE",
        epistemic="CONFIRMED",
        sources="USGS · AP",
        headline="M5.3 quake shakes eastern Nepal",
        deck="Shallow tremor felt near Tibet border; no casualties reported.",
        scene_id=11,
    ),
    CardItem(
        num=12,
        region="LatAm",
        kicker="BRAZIL · WEATHER",
        epistemic="OFFICIAL",
        sources="IOM · AP",
        headline="Brazil storm displaces nearly 20,000",
        deck="Five dead as severe storm wrecks homes in the south.",
        scene_id=12,
    ),
    CardItem(
        num=13,
        region="Oceania",
        kicker="AUSTRALIA · TECH LAW",
        epistemic="OFFICIAL",
        sources="Guardian · AP",
        headline="Australia clinches online safety bill",
        deck="Digital Duty of Care sets fines up to 5% of global revenue.",
        scene_id=13,
    ),
]

BRIEF_COLUMNS: List[List[BriefItem]] = [
    # Col A (#14-#26 = 13 rows)
    [
        BriefItem(14, "Europe", "England:", "5,258 heat deaths in summer 2026.", "UKHSA", "OFFICIAL", highlight="5,258"),
        BriefItem(15, "Europe", "BYD France:", "Exclusive talks for Ineos EV plant.", "Reuters", "OFFICIAL"),
        BriefItem(16, "Europe", "UK defence:", "Agencies warn arms firms of sabotage.", "MoD", "OFFICIAL"),
        BriefItem(17, "Europe", "Football:", "Real Madrid beat PSV 5–1; Arsenal 1–1.", "UEFA", "CONFIRMED"),
        BriefItem(18, "Middle East", "Gaza City:", "Strike kills Hamas chief Abu Nahel.", "Reuters", "CONFIRMED"),
        BriefItem(19, "Middle East", "Iraq oil:", "Baghdad orders Kurdish oil takeover.", "National", "OFFICIAL"),
        BriefItem(20, "Middle East", "Iran rial:", "Falls to record 2.85m per dollar.", "Anadolu", "CONFIRMED"),
        BriefItem(21, "East Asia", "South Korea:", "Russian jets trigger 07:52 air alert.", "Herald", "CONFIRMED"),
        BriefItem(22, "East Asia", "Autos:", "Chinese EVs pass Japan in 6 markets.", "SCMP", "REPORTED"),
        BriefItem(23, "East Asia", "US–China:", "Bilateral farm talks open in Beijing.", "Reuters", "OFFICIAL"),
        BriefItem(24, "N. America", "US economy:", "Confidence climbs to 103.3.", "Conf. Board", "CONFIRMED", highlight="103.3"),
        BriefItem(25, "N. America", "Canada:", "Ottawa rejects Pentagon spending critique.", "Guardian", "OFFICIAL"),
        BriefItem(26, "Africa", "Nigeria:", "Central bank holds key rate at 23%.", "Reuters", "OFFICIAL"),
    ],
    # Col B (#27-#38 = 12 rows)
    [
        BriefItem(27, "Africa", "Ethiopia:", "Amnesty urges Alamata shelling probe.", "Amnesty", "CONFIRMED"),
        BriefItem(28, "Africa", "South Africa:", "Unveils $372m satellite plan.", "SAnews", "OFFICIAL"),
        BriefItem(29, "South Asia", "India:", "00:30 UTC bus crash kills 4 children.", "PTI", "CONFIRMED"),
        BriefItem(30, "South Asia", "Bangladesh:", "Ex-PM Hasina plans 16 Dec return.", "Reuters", "CLAIM"),
        BriefItem(31, "SE Asia", "Myanmar:", "14 nations urge junta to obey court.", "Reuters", "OFFICIAL"),
        BriefItem(32, "SE Asia", "Indonesia:", "139 returned after Manila scam raid.", "The Star", "OFFICIAL"),
        BriefItem(33, "LatAm", "Colombia:", "Gunmen hold ~25 in Cartagena store.", "Reuters", "ONGOING"),
        BriefItem(34, "LatAm", "Brazil trade:", "Seeks WTO panel on US 301 tariffs.", "WTO", "OFFICIAL"),
        BriefItem(35, "Oceania", "Solomons:", "To let 2022 China security pact lapse.", "SMH", "REPORTED"),
        BriefItem(36, "Oceania", "Vanuatu:", "Lawmakers back A$500m Australia pact.", "AAP", "OFFICIAL"),
        BriefItem(37, "World", "UNODC:", "47,000 women killed by kin (5 an hour).", "UNODC", "OFFICIAL", highlight="47,000"),
        BriefItem(38, "World", "UN AI arms:", "Guterres urges binding AI rules.", "UN", "OFFICIAL"),
    ],
]

MAP_PINS: List[MapPin] = [
    MapPin(1, "Middle East", 215, 71),
    MapPin(2, "N. America", 101, 41),
    MapPin(3, "East Asia", 305, 53),
    MapPin(4, "Europe", 209, 35),
    MapPin(5, "Europe", 175, 43),
    MapPin(6, "N. America", 73, 56),
    MapPin(7, "World", 115, 92),
    MapPin(8, "Middle East", 242, 77),
    MapPin(9, "Africa", 193, 98),
    MapPin(10, "SE Asia", 290, 83),
    MapPin(11, "South Asia", 266, 70),
    MapPin(12, "LatAm", 118, 136),
    MapPin(13, "Oceania", 316, 146),
]

DATE_CHECK_TEXT = (
    "Every story happened or was first reported on Tue 24 Nov 2026 (UTC). "
    "Left out: Iran Hormuz mines claim, Nvidia CEO return & "
    "EU 22nd Russia sanctions (Mon 23 Nov) · COP31 no deal (Sun 22 Nov) · "
    "Shenzhou-24 launch (Wed 25 Nov)."
)

FOOTER_RIGHT = "Original vector illustrations · every story names its sources"


def compute_region_counts() -> Dict[str, int]:
    counts: Dict[str, int] = {r.key: 0 for r in REGIONS}
    for card in HERO_CARDS + MID_CARDS:
        counts[card.region] += 1
    for col in BRIEF_COLUMNS:
        for brief in col:
            counts[brief.region] += 1
    return counts


def validate_dataset() -> Tuple[int, Dict[str, int]]:
    assert len(HERO_CARDS) == 3, f"Expected 3 hero cards, got {len(HERO_CARDS)}"
    assert len(MID_CARDS) == 10, f"Expected 10 mid cards, got {len(MID_CARDS)}"
    brief_total = sum(len(col) for col in BRIEF_COLUMNS)
    assert brief_total == 25, f"Expected 25 briefs, got {brief_total}"

    counts = compute_region_counts()
    total = sum(counts.values())
    assert total == 38, f"Expected 38 stories, got {total}"
    assert len(REGIONS) == 10, f"Expected 10 regions, got {len(REGIONS)}"

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

    illustrated = HERO_CARDS + MID_CARDS
    assert [p.num for p in MAP_PINS] == list(range(1, 14)), "Map pins must be 1..13"
    for pin, card in zip(MAP_PINS, illustrated):
        assert pin.num == card.num and pin.region == card.region, (
            f"Pin #{pin.num} ({pin.region}) does not match card #{card.num} ({card.region})"
        )

    for i, a in enumerate(MAP_PINS):
        for b in MAP_PINS[i + 1 :]:
            dist = math.hypot(a.x - b.x, a.y - b.y)
            assert dist >= 17.0, f"Map pins #{a.num} and #{b.num} too close: {dist:.1f}"

    return total, counts
