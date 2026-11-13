"""Reference catalog for the demo: ships, itineraries, stateroom categories,
shore excursions, adult-exclusive dining, packages and spa.

This is the single source of truth shared by the mock Real-Time CDP export
generator (adobe/generate_mock_export.py imports it), the backend's
personalization engine and the MCP tools. Prices and names are illustrative
demo values, not live Couchbase Cruises pricing.
"""
from __future__ import annotations

import hashlib

# --------------------------------------------------------------------------
# Fleet. Ships use numbered decks; `neighborhoods` is the side of the
# ship a stateroom is assigned to (staterooms are sold port/starboard,
# forward/midship/aft).
# --------------------------------------------------------------------------
_SIDES = ["Port side", "Starboard side"]
SHIPS = {
    "CPL": {"name": "Couchbase Capella", "class": "Capella", "home_port": "PCV", "neighborhoods": _SIDES},
    "HZN": {"name": "Couchbase Horizon", "class": "Capella", "home_port": "PCV", "neighborhoods": _SIDES},
    "MRD": {"name": "Couchbase Meridian", "class": "Capella", "home_port": "FLL", "neighborhoods": _SIDES},
    "ODY": {"name": "Couchbase Odyssey", "class": "Odyssey", "home_port": "PCV", "neighborhoods": _SIDES},
    "AUR": {"name": "Couchbase Aurora", "class": "Odyssey", "home_port": "FLL", "neighborhoods": _SIDES},
    "MGM": {"name": "Couchbase Magma", "class": "Magma", "home_port": "GAL", "neighborhoods": _SIDES},
    "VOY": {"name": "Couchbase Voyager", "class": "Magma", "home_port": "SYD", "neighborhoods": _SIDES},
    "POL": {"name": "Couchbase Polaris", "class": "Polaris", "home_port": "SIN", "neighborhoods": _SIDES},
}
FLEET_SIZE = len(SHIPS)  # the 8-ship Couchbase Cruises fleet

PORTS = {
    "PCV": "Port Canaveral, Florida",
    "FLL": "Fort Lauderdale (Port Everglades), Florida",
    "GAL": "Galveston, Texas",
    "CAS": "Capella Cay, Bahamas",
    "LKC": "Sunrise Cay at Beacon Point, Eleuthera, Bahamas",
    "NAS": "Nassau, Bahamas",
    "CZM": "Cozumel, Mexico",
    "RTB": "Roatán, Honduras",
    "CMY": "Costa Maya, Mexico",
    "STT": "Charlotte Amalie, St. Thomas",
    "SXM": "Philipsburg, St. Maarten",
    "GCM": "George Town, Grand Cayman",
    "FAL": "Falmouth, Jamaica",
    # Australia & Tasmania (Couchbase Voyager's southern season)
    "SYD": "Sydney (Circular Quay), Australia",
    "ABH": "Airlie Beach (Whitsundays), Queensland",
    "CNS": "Cairns (Yorkeys Knob), Queensland",
    "BNE": "Brisbane, Queensland",
    "MEL": "Melbourne, Victoria",
    "HBA": "Hobart, Tasmania",
    "PTA": "Port Arthur, Tasmania",
    # Singapore (Couchbase Polaris)
    "SIN": "Singapore (Marina Bay Cruise Centre)",
    # Panama Canal & Southern Caribbean
    "ARU": "Oranjestad, Aruba",
    "CTG": "Cartagena, Colombia",
    "PCN": "Panama Canal (Gatun Lake), Panama",
    "LIM": "Puerto Limón, Costa Rica",
    "SEA": "At sea",
}

# itinerary_code -> definition. `days` lists one entry per day of the sailing.
ITINERARIES = {
    "7WCCC": {"name": "7 Night Western Caribbean with Capella Cay", "nights": 7,
              "days": ["EMB", "SEA", "CZM", "GCM", "FAL", "SEA", "CAS", "DEB"]},
    "7ECLC": {"name": "7 Night Eastern Caribbean with Sunrise Cay & Capella Cay", "nights": 7,
              "days": ["EMB", "SEA", "STT", "SXM", "SEA", "LKC", "CAS", "DEB"]},
    "5BALC": {"name": "5 Night Bahamas with Sunrise Cay & Capella Cay", "nights": 5,
              "days": ["EMB", "CAS", "LKC", "NAS", "SEA", "DEB"]},
    "4BACC": {"name": "4 Night Bahamas with Capella Cay", "nights": 4,
              "days": ["EMB", "NAS", "CAS", "SEA", "DEB"]},
    "3BACC": {"name": "3 Night Bahamas Getaway with Capella Cay", "nights": 3,
              "days": ["EMB", "NAS", "CAS", "DEB"]},
    "7WCGC": {"name": "7 Night Western Caribbean from Galveston", "nights": 7,
              "days": ["EMB", "SEA", "RTB", "CMY", "CZM", "SEA", "SEA", "DEB"]},
    "7QLDR": {"name": "7 Night Queensland & Great Barrier Reef", "nights": 7,
              "days": ["EMB", "SEA", "BNE", "ABH", "CNS", "SEA", "SEA", "DEB"]},
    "7TASM": {"name": "7 Night Tasmania & Melbourne", "nights": 7,
              "days": ["EMB", "SEA", "MEL", "SEA", "HBA", "PTA", "SEA", "DEB"]},
    "4SGAS": {"name": "4 Night Singapore Getaway at Sea", "nights": 4,
              "days": ["EMB", "SEA", "SEA", "SEA", "DEB"]},
    "3SGAS": {"name": "3 Night Singapore Escape at Sea", "nights": 3,
              "days": ["EMB", "SEA", "SEA", "DEB"]},
    "10PCN": {"name": "10 Night Panama Canal with Costa Rica & Caribbean", "nights": 10,
              "days": ["EMB", "SEA", "SEA", "ARU", "CTG", "PCN", "LIM", "SEA", "GCM", "SEA", "DEB"]},
}

# ship -> itineraries it sails (first is the "anchor" itinerary)
SHIP_ITINERARIES = {
    "CPL": ["3BACC", "4BACC"],
    "HZN": ["7ECLC", "7WCCC"],
    "MRD": ["5BALC", "4BACC"],
    "ODY": ["7WCCC", "7ECLC"],
    "AUR": ["4BACC", "3BACC", "5BALC"],
    "MGM": ["7WCGC", "10PCN"],
    "VOY": ["7QLDR", "7TASM"],
    "POL": ["4SGAS", "3SGAS"],
}

# --------------------------------------------------------------------------
# Staterooms. Rank is the upgrade ladder; prices are per person per night.
# --------------------------------------------------------------------------
CABIN_CATEGORIES = [
    {"code": "IN", "name": "Inside", "rank": 1, "base_ppn": 125, "decks": (2, 10)},
    {"code": "OV", "name": "Oceanview", "rank": 2, "base_ppn": 155, "decks": (2, 10)},
    {"code": "VE", "name": "Verandah", "rank": 3, "base_ppn": 205, "decks": (5, 11)},
    {"code": "CF", "name": "Concierge Family Oceanview with Verandah", "rank": 4, "base_ppn": 330, "decks": (11, 13)},
    {"code": "CS", "name": "Concierge 1-Bedroom Suite", "rank": 5, "base_ppn": 520, "decks": (11, 13)},
    {"code": "RS", "name": "Concierge Royal Suite", "rank": 6, "base_ppn": 780, "decks": (12, 13)},
    {"code": "TS", "name": "Concierge Tower Suite", "rank": 7, "base_ppn": 1350, "decks": (14, 15)},
]
CATEGORY_BY_CODE = {c["code"]: c for c in CABIN_CATEGORIES}
CATEGORY_PERKS = {
    "VE": ["Private verandah", "Split bath"],
    "CF": ["Concierge Lounge & private sun deck", "Pre-arrival planning with the Concierge team", "Priority boarding",
           "Sleeps up to five"],
    "CS": ["Separate living room & master bedroom", "Concierge Lounge & private sun deck", "Priority Shore Excursion and dining booking",
           "Complimentary premium Wi-Fi"],
    "RS": ["Wraparound verandah with whirlpool", "Dining room & walk-in closets", "Dedicated concierge host",
           "Tides Spa Thermal Suite access"],
    "TS": ["Two-story suite at the top of the ship", "Sleeps up to eight", "Private concierge team",
           "Vela, Soleil and Tides Spa included"],
}

# Minimum Stateroom Upgrade bid per person per night for a step of N ranks.
UPGRADE_BID_MIN_PPN = {1: 25, 2: 60, 3: 110, 4: 220, 5: 380}


def upgrade_price_ppn(from_code: str, to_code: str) -> int:
    """Instant-upgrade price (per person per night) between two categories."""
    a, b = CATEGORY_BY_CODE[from_code], CATEGORY_BY_CODE[to_code]
    delta = max(0, b["base_ppn"] - a["base_ppn"])
    # Last-minute upgrade discount, but always comfortably above the bid
    # floor - otherwise bidding would never make sense.
    price = max(delta * 0.82, upgrade_bid_min(from_code, to_code) * 1.6)
    return int(round(price / 5.0) * 5)


def upgrade_bid_min(from_code: str, to_code: str) -> int:
    steps = CATEGORY_BY_CODE[to_code]["rank"] - CATEGORY_BY_CODE[from_code]["rank"]
    return UPGRADE_BID_MIN_PPN.get(steps, 0)


def _h(*parts: str) -> int:
    return int(hashlib.sha1("|".join(parts).encode()).hexdigest()[:8], 16)


def initial_inventory(sailing_id: str) -> dict:
    """Deterministic unsold staterooms per category for a sailing - what the
    revenue team would release to upgrades a week or two before sailing."""
    out = {}
    for c in CABIN_CATEGORIES:
        if c["code"] == "IN":
            continue
        cap = {"OV": 14, "VE": 22, "CF": 9, "CS": 4, "RS": 2, "TS": 1}[c["code"]]
        out[c["code"]] = _h(sailing_id, c["code"]) % (cap + 1)
    # Always leave a little room in the hero categories so demos never dead-end.
    out["VE"] = max(out["VE"], 3)
    out["CF"] = max(out["CF"], 2)
    out["CS"] = max(out["CS"], 1)
    return out


# --------------------------------------------------------------------------
# Shore excursions (tags drive interest matching)
# --------------------------------------------------------------------------
EXCURSIONS = [
    # Capella Cay
    {"id": "CAS-CABANA", "port": "CAS", "name": "Capella Cay Private Family Cabana", "price": 549, "duration_hrs": 7,
     "tags": ["beach", "luxury", "relaxation", "family"], "activity": "low"},
    {"id": "CAS-SERENITY", "port": "CAS", "name": "Stillwater Bay Adults-Only Beach Cabana", "price": 449, "duration_hrs": 7,
     "tags": ["beach", "relaxation", "adults", "luxury"], "activity": "low"},
    {"id": "CAS-SNORKEL", "port": "CAS", "name": "Snorkeling Lagoon & Shipwreck Trail", "price": 39, "duration_hrs": 2,
     "tags": ["snorkeling", "ocean", "nature", "family"], "activity": "medium"},
    {"id": "CAS-STINGRAY", "port": "CAS", "name": "Stingray Lagoon Adventure", "price": 55, "duration_hrs": 1,
     "tags": ["ocean", "nature", "family", "characters"], "activity": "medium"},
    {"id": "CAS-PARASAIL", "port": "CAS", "name": "Capella Cay Parasailing", "price": 119, "duration_hrs": 1,
     "tags": ["thrill", "views", "ocean"], "activity": "high"},
    {"id": "CAS-BIKE", "port": "CAS", "name": "Bike Rental & Capella Cay 5K Nature Trail", "price": 29, "duration_hrs": 2,
     "tags": ["fitness", "nature", "family"], "activity": "high"},
    {"id": "CAS-GLASSBOTTOM", "port": "CAS", "name": "Glass-Bottom Boat Reef Tour", "price": 59, "duration_hrs": 1,
     "tags": ["ocean", "nature", "photography", "family"], "activity": "low"},
    # Sunrise Cay at Beacon Point
    {"id": "LKC-CABANA", "port": "LKC", "name": "Sunrise Cabana at Driftwood Beach", "price": 599, "duration_hrs": 7,
     "tags": ["beach", "luxury", "relaxation", "family"], "activity": "low"},
    {"id": "LKC-JUNKANOO", "port": "LKC", "name": "Island Cultural Center Junkanoo Workshop", "price": 49, "duration_hrs": 2,
     "tags": ["culture", "family", "live shows"], "activity": "low"},
    {"id": "LKC-KAYAK", "port": "LKC", "name": "Beacon Point Glass-Bottom Kayak Eco Tour", "price": 79, "duration_hrs": 2,
     "tags": ["kayaking", "nature", "photography"], "activity": "medium"},
    {"id": "LKC-MABRIKA", "port": "LKC", "name": "Coral Cove Adults-Only Beach Lounger & Umbrella", "price": 69, "duration_hrs": 6,
     "tags": ["beach", "relaxation", "adults"], "activity": "low"},
    {"id": "LKC-SNORKEL", "port": "LKC", "name": "Beacon Point Reef Snorkel", "price": 69, "duration_hrs": 2,
     "tags": ["snorkeling", "ocean", "nature"], "activity": "medium"},
    # Cozumel
    {"id": "CZM-REEF", "port": "CZM", "name": "Palancar Reef Snorkel & Beach Break", "price": 79, "duration_hrs": 4,
     "tags": ["snorkeling", "ocean", "nature"], "activity": "medium"},
    {"id": "CZM-TULUM", "port": "CZM", "name": "Tulum Ruins by Ferry", "price": 139, "duration_hrs": 7,
     "tags": ["history", "culture", "photography"], "activity": "medium"},
    {"id": "CZM-TEQUILA", "port": "CZM", "name": "Tequila & Mexican Cuisine Tasting", "price": 69, "duration_hrs": 3,
     "tags": ["food", "culture", "adults"], "activity": "low"},
    {"id": "CZM-DOLPHIN", "port": "CZM", "name": "Dolphin Encounter at Chankanaab", "price": 149, "duration_hrs": 4,
     "tags": ["ocean", "nature", "family", "photography"], "activity": "medium"},
    # Roatan
    {"id": "RTB-ZIP", "port": "RTB", "name": "Canopy Zipline & Sloth Encounter", "price": 99, "duration_hrs": 4,
     "tags": ["thrill", "nature", "family"], "activity": "high"},
    {"id": "RTB-WESTBAY", "port": "RTB", "name": "West Bay Beach Break", "price": 59, "duration_hrs": 5,
     "tags": ["beach", "relaxation", "snorkeling"], "activity": "low"},
    # Costa Maya
    {"id": "CMY-CHACCHOBEN", "port": "CMY", "name": "Chacchoben Mayan Ruins", "price": 89, "duration_hrs": 5,
     "tags": ["history", "culture", "nature"], "activity": "medium"},
    {"id": "CMY-BACALAR", "port": "CMY", "name": "Bacalar Lagoon of Seven Colors Kayak", "price": 119, "duration_hrs": 6,
     "tags": ["kayaking", "nature", "photography"], "activity": "high"},
    # Nassau
    {"id": "NAS-ATLANTIS", "port": "NAS", "name": "Atlantis Aquaventure Water Park", "price": 199, "duration_hrs": 6,
     "tags": ["waterpark", "family", "thrill"], "activity": "high"},
    {"id": "NAS-PIGS", "port": "NAS", "name": "Swimming Pigs & Sandbar Speedboat", "price": 169, "duration_hrs": 4,
     "tags": ["ocean", "nature", "photography"], "activity": "medium"},
    {"id": "NAS-FOOD", "port": "NAS", "name": "Bahamian Food & Rum Walking Tour", "price": 79, "duration_hrs": 3,
     "tags": ["food", "culture"], "activity": "low"},
    # St. Thomas
    {"id": "STT-MAGENS", "port": "STT", "name": "Magens Bay Beach & Mountain Top", "price": 59, "duration_hrs": 4,
     "tags": ["beach", "views", "relaxation"], "activity": "low"},
    {"id": "STT-STJOHN", "port": "STT", "name": "St. John Snorkel Catamaran", "price": 129, "duration_hrs": 5,
     "tags": ["snorkeling", "ocean", "sailing"], "activity": "medium"},
    # St. Maarten
    {"id": "SXM-REGATTA", "port": "SXM", "name": "America's Cup 12-Metre Regatta", "price": 119, "duration_hrs": 3,
     "tags": ["sailing", "thrill", "adults"], "activity": "high"},
    {"id": "SXM-MAHO", "port": "SXM", "name": "Maho Beach & Marigot Shopping", "price": 49, "duration_hrs": 4,
     "tags": ["beach", "shopping", "photography"], "activity": "low"},
    # Grand Cayman
    {"id": "GCM-STINGRAY", "port": "GCM", "name": "Stingray City Sandbar & Snorkel", "price": 89, "duration_hrs": 4,
     "tags": ["ocean", "nature", "snorkeling", "family"], "activity": "medium"},
    {"id": "GCM-SEVENMILE", "port": "GCM", "name": "Seven Mile Beach Club Day", "price": 79, "duration_hrs": 5,
     "tags": ["beach", "relaxation", "luxury"], "activity": "low"},
    # Falmouth
    {"id": "FAL-DUNNS", "port": "FAL", "name": "Dunn's River Falls Climb", "price": 99, "duration_hrs": 6,
     "tags": ["nature", "thrill", "family"], "activity": "high"},
    {"id": "FAL-BAMBOO", "port": "FAL", "name": "Martha Brae Bamboo Rafting", "price": 89, "duration_hrs": 4,
     "tags": ["nature", "relaxation", "culture"], "activity": "low"},
    # Queensland
    {"id": "BNE-KOALA", "port": "BNE", "name": "Lone Pine Koala Sanctuary & River Cruise", "price": 89, "duration_hrs": 5,
     "tags": ["nature", "family", "photography"], "activity": "low"},
    {"id": "BNE-FOOD", "port": "BNE", "name": "Brisbane Laneways Food & Craft Beer Walk", "price": 79, "duration_hrs": 3,
     "tags": ["food", "culture", "adults"], "activity": "low"},
    {"id": "ABH-WHITEHAVEN", "port": "ABH", "name": "Whitehaven Beach & Hill Inlet Lookout", "price": 149, "duration_hrs": 6,
     "tags": ["beach", "views", "photography", "relaxation"], "activity": "medium"},
    {"id": "ABH-REEF", "port": "ABH", "name": "Great Barrier Reef Pontoon Snorkel", "price": 219, "duration_hrs": 8,
     "tags": ["snorkeling", "ocean", "nature"], "activity": "medium"},
    {"id": "CNS-KURANDA", "port": "CNS", "name": "Kuranda Skyrail & Scenic Railway", "price": 139, "duration_hrs": 7,
     "tags": ["nature", "views", "family", "culture"], "activity": "low"},
    {"id": "CNS-DAINTREE", "port": "CNS", "name": "Daintree Rainforest & Mossman Gorge", "price": 159, "duration_hrs": 8,
     "tags": ["nature", "photography", "culture"], "activity": "medium"},
    # Tasmania & Melbourne
    {"id": "MEL-PENGUIN", "port": "MEL", "name": "Phillip Island Penguin Parade", "price": 129, "duration_hrs": 8,
     "tags": ["nature", "family", "photography"], "activity": "low"},
    {"id": "MEL-YARRA", "port": "MEL", "name": "Yarra Valley Wine & Cheese Trail", "price": 149, "duration_hrs": 7,
     "tags": ["wine", "food", "adults"], "activity": "low"},
    {"id": "HBA-MONA", "port": "HBA", "name": "MONA Museum by Ferry", "price": 89, "duration_hrs": 4,
     "tags": ["culture", "adults", "views"], "activity": "low"},
    {"id": "HBA-WELLINGTON", "port": "HBA", "name": "Mt Wellington Summit & Bonorong Wildlife", "price": 109, "duration_hrs": 5,
     "tags": ["nature", "views", "family"], "activity": "medium"},
    {"id": "PTA-HISTORIC", "port": "PTA", "name": "Port Arthur Historic Site & Harbour Cruise", "price": 79, "duration_hrs": 4,
     "tags": ["history", "culture", "views"], "activity": "low"},
    {"id": "PTA-TASMAN", "port": "PTA", "name": "Tasman Peninsula Sea Cliffs Eco-Cruise", "price": 139, "duration_hrs": 3,
     "tags": ["ocean", "nature", "thrill", "photography"], "activity": "high"},
    # Panama Canal & Southern Caribbean
    {"id": "ARU-SUBMARINE", "port": "ARU", "name": "Atlantis Submarine Reef Dive", "price": 129, "duration_hrs": 2,
     "tags": ["ocean", "nature", "family"], "activity": "low"},
    {"id": "ARU-JEEP", "port": "ARU", "name": "Natural Pool 4x4 Safari", "price": 109, "duration_hrs": 5,
     "tags": ["thrill", "nature", "beach"], "activity": "high"},
    {"id": "CTG-WALLED", "port": "CTG", "name": "Walled City & Castillo San Felipe", "price": 69, "duration_hrs": 4,
     "tags": ["history", "culture", "photography"], "activity": "low"},
    {"id": "CTG-ROSARIO", "port": "CTG", "name": "Rosario Islands Beach Escape", "price": 139, "duration_hrs": 6,
     "tags": ["beach", "snorkeling", "relaxation"], "activity": "low"},
    {"id": "PCN-LOCKS", "port": "PCN", "name": "Agua Clara Locks & Gatun Lake Boat Tour", "price": 119, "duration_hrs": 5,
     "tags": ["history", "views", "family", "photography"], "activity": "low"},
    {"id": "PCN-RAINFOREST", "port": "PCN", "name": "Gatun Rainforest Aerial Tram & Sloth Sanctuary", "price": 139, "duration_hrs": 6,
     "tags": ["nature", "family", "photography"], "activity": "medium"},
    {"id": "LIM-TORTUGUERO", "port": "LIM", "name": "Tortuguero Canals Wildlife Boat", "price": 99, "duration_hrs": 5,
     "tags": ["nature", "photography", "family"], "activity": "low"},
    {"id": "LIM-ZIPLINE", "port": "LIM", "name": "Veragua Rainforest Zipline & Hanging Bridges", "price": 129, "duration_hrs": 6,
     "tags": ["thrill", "nature", "adults"], "activity": "high"},
]
EXCURSION_BY_ID = {e["id"]: e for e in EXCURSIONS}

INTERESTS = sorted({t for e in EXCURSIONS for t in e["tags"]}
                   | {"spa", "fitness", "characters", "live shows", "kids clubs", "fireworks", "fine dining", "wellness"})

# --------------------------------------------------------------------------
# Adult-exclusive & premium dining, packages, spa
# Rotational dining in the three main dining rooms
# is included in the fare; these are the bookable, cover-charge experiences.
# --------------------------------------------------------------------------
DINING = [
    {"id": "VELA", "name": "Vela", "cuisine": "Northern Italian, adults only", "price_pp": 55, "ships": ["MGM", "VOY", "AUR", "ODY", "POL"],
     "tags": ["italian", "celebration", "classic", "adults", "wine"]},
    {"id": "VELASTEAK", "name": "Vela Steakhouse", "cuisine": "Italian steakhouse, adults only", "price_pp": 55, "ships": ["CPL", "HZN", "MRD"],
     "tags": ["steak", "celebration", "classic", "adults"]},
    {"id": "VELABRUNCH", "name": "Vela Brunch", "cuisine": "Sea-day brunch, adults only", "price_pp": 55, "ships": "*",
     "tags": ["brunch", "adults", "wine", "views"]},
    {"id": "LUMEN", "name": "Lumen", "cuisine": "French fine dining, adults only", "price_pp": 135, "ships": ["AUR", "ODY"],
     "tags": ["fine dining", "celebration", "wine", "adults"]},
    {"id": "SOLEIL", "name": "Soleil", "cuisine": "French fine dining, adults only", "price_pp": 135, "ships": ["CPL", "HZN", "MRD"],
     "tags": ["fine dining", "celebration", "wine", "adults"]},
    {"id": "LUMENDESSERT", "name": "Lumen Dessert Experience", "cuisine": "Six-course dessert tasting", "price_pp": 60, "ships": ["AUR", "ODY"],
     "tags": ["creative", "celebration", "adults"]},
    {"id": "CAPTAINSTEA", "name": "Captain's Afternoon Tea", "cuisine": "Afternoon tea hosted by the ship's officers", "price_pp": 220, "ships": ["AUR", "ODY", "CPL", "HZN"],
     "tags": ["family", "characters", "celebration", "show"]},
    {"id": "CHEFSTABLE", "name": "The Chef's Table at Soleil", "cuisine": "Multi-course wine pairing", "price_pp": 195, "ships": ["CPL", "HZN", "MRD"],
     "tags": ["fine dining", "wine", "celebration", "adults"]},
]
DINING_BY_ID = {d["id"]: d for d in DINING}
DINING_TIMES = ["17:45", "18:15", "18:45", "19:15", "19:45", "20:15", "20:45", "21:15"]

PACKAGES = [
    {"code": "PLUS", "name": "Premium Wine Package", "price_per_day": 60, "per": "stateroom/night",
     "blurb": "A bottle from the premium list each night at your rotational restaurant, a Harbor Café coffee card and "
              "prepaid gratuities for the whole stateroom.", "propensity": "beverage_package_propensity"},
    {"code": "ZERO_ALC", "name": "Smoothie & Specialty Coffee Card", "price_per_day": 12, "per": "person/day",
     "blurb": "Specialty coffees, smoothies, fresh juice and mocktails at Harbor Café, Skyline Café and the pool decks.",
     "propensity": "beverage_package_propensity"},
    {"code": "WIFI", "name": "Premium Surf Wi-Fi", "price_per_day": 25, "per": "device/day",
     "blurb": "The fastest Wi-Fi at sea - stream, video call and post from anywhere on board.", "propensity": "wifi_propensity"},
    {"code": "PREMIER", "name": "Snapshots Photo Package", "price_per_day": 45, "per": "stateroom/day",
     "blurb": "Every professional photo from your sailing - deck parties, the Captain's Gala, formal night and the "
              "Grand Theatre - as unlimited digital downloads, plus a keepsake photo book.",
     "propensity": "premier_propensity"},
    {"code": "SPEC_DINING", "name": "Adult-Exclusive Dining Package", "price_per_day": 55, "per": "person/day",
     "blurb": "Dinner at Vela, Lumen or Soleil on every night of your voyage.", "propensity": "specialty_dining_propensity"},
]
PACKAGE_BY_CODE = {p["code"]: p for p in PACKAGES}

SPA = [
    {"id": "SPA-HOTSTONE", "name": "Tides Spa Hot Stone Massage", "price": 199, "minutes": 75, "tags": ["relaxation", "spa"]},
    {"id": "SPA-COUPLES", "name": "Couples Massage in a Spa Villa", "price": 349, "minutes": 50, "tags": ["celebration", "spa", "couples"]},
    {"id": "SPA-FACIAL", "name": "Elemis Pro-Collagen Facial", "price": 179, "minutes": 50, "tags": ["spa", "beauty"]},
    {"id": "SPA-ENCLAVE", "name": "Thermal Suite Pass (voyage)", "price": 249, "minutes": 0, "tags": ["spa", "relaxation", "wellness"]},
    {"id": "SPA-ACUP", "name": "Medical Acupuncture", "price": 165, "minutes": 50, "tags": ["wellness"]},
]
SPA_BY_ID = {s["id"]: s for s in SPA}

ARRIVAL_SLOTS = ["10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00"]

# Crimson Club tiers. Thresholds are in loyalty points (the generator awards
# about 9 per completed cruise): Silver after the first cruise, Gold from 5,
# Platinum from 10, Pearl from 25.
LOYALTY_TIERS = ["First-Time", "Silver", "Gold", "Platinum", "Pearl"]
LOYALTY_THRESHOLDS = {"First-Time": 0, "Silver": 1, "Gold": 45, "Platinum": 90, "Pearl": 225}


def ship_has_dining(ship_code: str, dining_id: str) -> bool:
    ships = DINING_BY_ID[dining_id]["ships"]
    return ships == "*" or ship_code in ships


def a_or_an(name: str) -> str:
    """'a Verandah', 'an Oceanview'."""
    return f"{'an' if name[:1].lower() in 'aeiou' else 'a'} {name}"


def dining_full(sailing_id: str, restaurant_id: str, date: str, time: str) -> bool:
    """Deterministic "fully booked" seatings (about 1 in 5) for a sailing -
    the restaurant reservation system's view of the night."""
    return _h(sailing_id, restaurant_id, date, time) % 5 == 0


def dining_availability(reservation: dict) -> dict:
    """Fully booked times per restaurant per night, for every adult-exclusive
    restaurant on the guest's ship: {restaurant_id: {date: [times]}}. Synced to
    the phone with the offers so the dining screen can grey out full seatings,
    offline too."""
    nights = [p["date"] for p in reservation["ports"]][:-1]
    out: dict = {}
    for d in DINING:
        if not ship_has_dining(reservation["ship_code"], d["id"]):
            continue
        out[d["id"]] = {n: [t for t in DINING_TIMES if dining_full(reservation["sailing_id"], d["id"], n, t)]
                        for n in nights}
    return out


def public_catalog() -> dict:
    """What the mobile app syncs as `catalog` documents."""
    return {
        "ships": SHIPS,
        "ports": PORTS,
        "itineraries": ITINERARIES,
        "cabin_categories": [
            {**{k: v for k, v in c.items() if k != "decks"}, "perks": CATEGORY_PERKS.get(c["code"], [])}
            for c in CABIN_CATEGORIES
        ],
        "excursions": EXCURSIONS,
        "dining": DINING,
        "dining_times": DINING_TIMES,
        "packages": PACKAGES,
        "spa": SPA,
        "arrival_slots": ARRIVAL_SLOTS,
    }
