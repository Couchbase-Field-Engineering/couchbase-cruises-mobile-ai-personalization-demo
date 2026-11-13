"""Knowledge Base documents published to AOM by the daily loader.

Two kinds:

* **Guest profile** - one per passenger sailing soon, rendered from that
  morning's Adobe Real-Time CDP profile export as plain prose. The concierge retrieves it with a
  `document_id`-scoped search, so a guest's question can only ever be
  grounded in *their own* profile, never a neighbour's that happens to be
  semantically close.
* **Guest Services Playbook** - fleet, policy and product knowledge (Stateroom Upgrade
  rules, packages, check-in, dining, ports). Its FAQ entries are AEM content
  fragments (adobe/aem/README.md; `FAQ` below is the bundled copy served when
  no AEM endpoint is configured). Contains no personal data, so answers
  grounded only in it are safe to share across guests through AOM's LLM cache.

FAQ entries are also synced to the phone inside the catalog document, so the
app can answer the common questions offline from Couchbase Lite.
"""
from __future__ import annotations

from . import catalog as C

FAQ = [
    {"q": "What time should I arrive at the terminal?",
     "a": "Arrive at the Port Arrival Time you selected during Online Check-In - it's on your boarding pass in the "
          "Couchbase Cruises app. Boarding typically opens around 11:00am and all guests must be on board 90 minutes before "
          "departure. Your Cruise Card, which opens your stateroom and charges to your onboard account, is "
          "waiting at the terminal.",
     "keywords": ["arrive", "arrival", "terminal", "boarding", "board", "what time", "port arrival"]},
    {"q": "How does Stateroom Upgrade work?",
     "a": "Stateroom Upgrade lets you bid per person, per night for a higher stateroom category, up to Concierge level. "
          "You're only charged if your bid is accepted, and you can change or cancel it until bidding closes about 48 "
          "hours before sailing. If you'd rather not wait, an instant upgrade confirms right away at the listed price.",
     "keywords": ["stateroom upgrade", "upgrade bid", "bid", "upgrade", "how does", "concierge"]},
    {"q": "Who can buy a wine package?",
     "a": "Wine packages are for guests 21 and over and are added per stateroom - the bottle is delivered to your table "
          "at rotational dining each night, and anything you don't finish follows you to the next restaurant. Guests "
          "under 21 can add the Smoothie & Specialty Coffee Card instead. Soft drinks at meals and on the pool deck are "
          "always included.",
     "keywords": ["beverage", "drink", "wine", "alcohol", "package", "cocktail", "soda"]},
    {"q": "What's included in the Snapshots Photo Package?",
     "a": "The Snapshots Photo Package bundles every professional photo taken of your party during the sailing - "
          "deck parties, the Captain's Gala, formal night, embarkation and the Grand Theatre - as unlimited digital "
          "downloads, plus a keepsake photo book. Buy it before you sail for the best price; individual prints are "
          "sold separately at the Snapshots studio on board.",
     "keywords": ["snapshots", "photo", "photos", "photo package", "pictures", "bundle"]},
    {"q": "Is Wi-Fi available on board?",
     "a": "Yes - Premium Surf Wi-Fi is the fastest Wi-Fi at sea, good for streaming and video calls. The Couchbase "
          "Cruises app, onboard chat and the daily schedule are always free; internet plans are sold per device "
          "for the whole voyage and are cheaper before you board.",
     "keywords": ["wifi", "wi-fi", "internet", "surf", "online", "connect", "app"]},
    {"q": "Can I change my dining time?",
     "a": "Rotational dining seats you at a different themed restaurant each night with the same servers. Main seating "
          "is around 5:45pm and second seating around 8:15pm; you can request a switch in the app before sailing or at "
          "Guest Services on board, subject to availability. Vela, Lumen and Soleil are adult-exclusive and booked "
          "separately with a cover charge.",
     "keywords": ["dining time", "main dining", "rotational", "dinner time", "seating", "second seating"]},
    {"q": "What do I need for check-in?",
     "a": "Complete Online Check-In in the app: confirm your travel documents, add a security photo, select a Port "
          "Arrival Time and set up your onboard account. Your Cruise Cards are waiting at the terminal; bring "
          "the same travel documents with you.",
     "keywords": ["check-in", "check in", "checkin", "documents", "passport", "online check-in", "cruise card"]},
    {"q": "Are kids' activities included?",
     "a": "Youth clubs are included in your fare: Explorer Club and Explorer Lab for ages 3-10, Compass for "
          "tweens 11-14 and Current for teens 14-17. Little Sailors Nursery for ages 6 months to 3 years is "
          "available for an hourly fee.",
     "keywords": ["kids", "children", "explorer", "teens", "youth", "compass", "current", "nursery"]},
    {"q": "What is Capella Cay?",
     "a": "Couchbase Cruises' private island in the Bahamas, where the ship docks right at the island - no tenders. "
          "The family beach, Stillwater Bay adults-only beach, the Splash Platform, the barbecue lunch and the Capella Cay "
          "5K are included; private cabanas, the stingray adventure, snorkel gear and bike rentals are Port "
          "Adventures worth booking early. Sunrise Cay at Beacon Point on Eleuthera is the second private "
          "island on many Bahamas itineraries.",
     "keywords": ["capella cay", "sunrise cay", "beacon point", "eleuthera", "private island", "bahamas"]},
    {"q": "Are spa treatments cheaper on port days?",
     "a": "Yes. Tides Spa & Salon treatments booked for a port day are typically discounted - this app applies a 20% "
          "port-day price automatically.",
     "keywords": ["spa", "massage", "port day", "discount", "facial", "tides", "thermal suite"]},
]


def playbook_markdown(export_date: str, entries: list[dict] | None = None) -> str:
    lines = [f"# Couchbase Cruises Guest Services Playbook (published {export_date})", "",
             "Fleet, policy and product knowledge for the Couchbase Cruises Guest Concierge agent, from the AEM "
             "guest-services-playbook content fragments and the fleet catalog. Contains no guest data.", ""]
    lines += ["## Frequently asked questions", ""]
    for f in entries or FAQ:
        lines += [f"**{f['q']}** {f['a']}", ""]
    lines += ["## Stateroom categories and upgrade policy", ""]
    for c in C.CABIN_CATEGORIES:
        perks = ", ".join(C.CATEGORY_PERKS.get(c["code"], [])) or "standard amenities"
        lines.append(f"- {c['name']} ({c['code']}): fares from about ${c['base_ppn']} per person per night; {perks}.")
    lines += ["", "Stateroom Upgrade minimum bids per person per night by number of category steps: "
              + ", ".join(f"{k} step{'s' if k > 1 else ''} ${v}" for k, v in C.UPGRADE_BID_MIN_PPN.items()) + ".",
              "Instant upgrades are priced at roughly 82% of the fare difference and confirm immediately, subject to "
              "inventory. Upgrades apply to the whole stateroom party. Complimentary (goodwill) upgrades are a service "
              "recovery gesture that always requires supervisor approval.", ""]
    lines += ["## Packages and add-ons", ""]
    for p in C.PACKAGES:
        lines.append(f"- {p['name']} ({p['code']}): ${p['price_per_day']} per {p['per']}. {p['blurb']}")
    lines += ["", "## Adult-exclusive and premium dining", ""]
    for d in C.DINING:
        ships = "fleetwide" if d["ships"] == "*" else "on " + ", ".join(C.SHIPS[s]["name"] for s in d["ships"])
        lines.append(f"- {d['name']}: {d['cuisine']}, ${d['price_pp']} per guest, {ships}.")
    lines += ["", "## Ships", ""]
    for code, s in C.SHIPS.items():
        lines.append(f"- {s['name']} ({s['class']} class), sails from {C.PORTS[s['home_port']]}. Staterooms sold on the "
                     + " and ".join(s["neighborhoods"]).lower() + ".")
    lines += ["", "## Ports and Shore Excursions", ""]
    for port, name in C.PORTS.items():
        exs = [e for e in C.EXCURSIONS if e["port"] == port]
        if not exs:
            continue
        lines.append(f"### {name}")
        for e in exs:
            lines.append(f"- {e['name']} ({e['id']}): ${e['price']} per guest, {e['duration_hrs']} hours, "
                         f"{e['activity']} activity; good for {', '.join(e['tags'])}.")
        lines.append("")
    lines += ["## Tides Spa & Salon", ""]
    for s in C.SPA:
        lines.append(f"- {s['name']}: ${s['price']}" + (f", {s['minutes']} minutes." if s["minutes"] else "."))
    return "\n".join(lines)


def guest_profile_markdown(p: dict) -> str:
    r = p["reservation"]
    s = p["ml_scores"]
    prefs = p["preferences"]
    party = "; ".join(f"{m['name']} ({m['relationship']}, age {m['age_band']})" for m in r["party"])
    ports = ", ".join(f"day {d['day']} {d['date']} {d['port']}" for d in r["ports"])
    past = p["history"]["past_sailings"][:5]
    past_txt = "; ".join(f"{h['ship_name']} {h['sail_date'][:7]} {h['nights']} nights in {h['cabin_class']}, spent "
                         f"${h['onboard_spend_usd']:,.0f}" for h in past) or "first cruise with us"
    mix = p.get("onboard_spend_mix", {})
    top_mix = ", ".join(f"{k} {v:.0%}" for k, v in sorted(mix.items(), key=lambda kv: -kv[1])[:3])
    owned = p.get("purchased_for_sailing", {})
    return "\n".join([
        f"# Guest profile {p['guest_id']}: {p['first_name']} {p['last_name']}",
        f"Source: Adobe Real-Time CDP profile export {p['export_date']}, scores by {s.get('model_version')}"
        + (f"; audiences: {', '.join(a['name'] for a in p['audiences'])}" if p.get("audiences") else "") + ".",
        "",
        "## Upcoming sailing",
        f"{p['first_name']} sails on {r['ship_name']} - {r['itinerary_name']} - from {r['embark_port']} on "
        f"{r['embark_date']} returning {r['debark_date']} ({r['nights']} nights), booking {r['booking_id']}. "
        f"Stateroom {r['stateroom']['stateroom_number']}, {r['stateroom']['category_name']} on deck "
        f"{r['stateroom']['deck']} ({r['stateroom']['neighborhood']}, {r['stateroom']['location']}). "
        f"Check-in status: {r['checkin_status']}. Dining: {r['dining_assignment']}.",
        f"Traveling party ({r['party_size']}): {party}.",
        f"Itinerary: {ports}.",
        "",
        "## Loyalty and history",
        f"Crimson Club {p['loyalty']['tier']} with {p['loyalty']['points']} points and "
        f"{p['loyalty']['cruises_completed']} completed cruises. Past sailings: {past_txt}. "
        f"Average onboard spend ${p['history']['avg_onboard_spend_usd']:,.0f}; accepted "
        f"{p['history']['upgrades_accepted']} upgrades and placed {p['history']['upgrade_bids_placed']} Stateroom Upgrade bids before.",
        f"Onboard spend mix (top): {top_mix}.",
        "",
        "## Preferences",
        f"Interests: {', '.join(prefs['interests'])}. Dietary: {', '.join(prefs['dietary']) or 'none noted'}. "
        f"Celebrating: {prefs.get('celebration') or 'nothing noted'}. Bed: {prefs['bed_configuration']}, "
        f"pillow {prefs['pillow']}. Stateroom location preference: {prefs.get('stateroom_location_pref') or 'none'}. "
        f"Travels with kids: {'yes' if prefs.get('travels_with_kids') else 'no'}. "
        f"Prefers {prefs['communication_channel']} messages.",
        "",
        "## Personalization signals",
        f"Segment: {s.get('segment')}. Next best action: {s.get('next_best_action')}. "
        f"Upgrade propensity {s.get('upgrade_propensity')}, recommended upgrade category "
        f"{s.get('recommended_upgrade_category')} with a suggested Stateroom Upgrade bid of ${s.get('recommended_bid_per_night_usd')} "
        f"per person per night. Price sensitivity {s.get('price_sensitivity')}. Propensities - beverage package "
        f"{s.get('beverage_package_propensity')}, specialty dining {s.get('specialty_dining_propensity')}, excursions "
        f"{s.get('excursion_propensity')}, spa {s.get('spa_propensity')}, internet {s.get('wifi_propensity')}, "
        f"Snapshots Photo Package {s.get('premier_propensity')}.",
        f"Already purchased for this sailing: packages {owned.get('packages') or 'none'}, excursions "
        f"{owned.get('excursions') or 'none'}.",
    ])
