# Source Note: RunWar GDD

## Source

- File: `/mnt/c/Users/vlad_/Downloads/RunWar_GDD_Completo.pdf`
- Type: PDF game design document
- Status: seed evidence
- Extraction: temporary local PDF text extraction with `pypdf`; no generated extraction cache committed.

## Observed Claims

- RunWar is a GPS-based territorial running game: "Conquiste o mapa. Domine sua cidade. Corra ou perca."
- The core loop is running to conquer a hex zone, receiving invasion notifications, defending territory, expanding adjacent territory, climbing leagues, and winning event/season rewards.
- Hex zones are roughly 400m point-to-point. A valid conquest requires covering about 60% of a hex perimeter.
- Large cities can contain thousands of playable hexes; the GDD example cites around 2,400 hexes for Sao Paulo.
- Zones can become neutral after 14 days without defense or activity.
- Zone types include common, strategic, event, legendary, and sponsored zones.
- Common invasions use a 48h defense window and a 6h same-zone attack cooldown.
- The GDD uses a fastest/reference-time model for invasion: an attacker must beat the owner's reference by at least 3s/km.
- Clan members can help defend; the lower/better clan time can become the reference for defense.
- Power-ups include shields, fortress effects, alarms, traps, spy, turbo, raid, mine, XP boost, imã de zona, marco, and replay.
- Clans have roles, membership limits, coffer mechanics, mutual defense, coordinated attacks, declared rivals, and monthly clan wars.
- Leagues are Recruta, Guerreiro, Comandante, and General, based on active zones.
- Profile XP is permanent; league and seasonal rankings change over time.
- Anti-cheat is central and includes fake GPS detection, sensor fusion, vehicle detection, presence proof, social reporting, and backend validation.
- Monetization concepts include premium, battle pass, RunCoins, brand sponsorship, paid events, B2B data/API, dashboards, white-label events, and wearable integrations.
- Roadmap starts with a pre-MVP manual pilot: WhatsApp group, Strava screenshots, admin registration, first 50 hexes mapped manually, and retention validation before code.

## Design Tensions

- The GDD emphasizes reference time and pace supremacy, while the JSX source emphasizes a composite Zone Score.
- Monetization is extensive, but early validation should avoid pay-to-win distortion.
- Anti-cheat is described as existential, but the first pilot may need cheap manual validation before full sensor fusion.
