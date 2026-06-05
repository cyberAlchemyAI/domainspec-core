# Source Note: TROQAR Gamification JSX

## Source

- File: `/mnt/c/Users/vlad_/Downloads/troqar-gamificacao-1.jsx.txt`
- Type: React JSX concept document
- Status: seed evidence

## Observed Claims

- The JSX defines an interactive TROQAR gamification concept with tabs for score, XP, territory conquest, recovery, teams, and seasons.
- Zone Score is composite:
  - Pace Score: 40%
  - Distance Score: 35%
  - Frequency Score: 25%
  - Maximum displayed score: 550 points.
- Distance score uses kilometers inside the hex, with a cap.
- Frequency score uses unique visit days in a 14-day cycle, with same-day duplicate runs collapsed.
- A valid visit is tied to a valid run covering at least 60% of the perimeter.
- XP sources include neutral conquest, invasion, reconquest, strategic/legendary/sponsored zones, defense, streaks, personal records, distance, missions, referrals, battle pass completion, and clan activity.
- XP multipliers include active kingdoms, large kingdoms, strategic zones, XP boosts, weekly events, and long streaks.
- Zone conquest types include neutral zones, common invasion, strategic invasion, and legendary zones.
- Common invasion uses a contested state and a 48h window; strategic invasion uses a harder margin and 72h window.
- Recovery rules define who can respond, expiration, bonuses, and cooldowns for common, strategic, legendary, and neutral zones.
- Clan model says each run generates individual XP and 30% of that XP contributes to the clan without reducing the runner's XP.
- Clan mechanics include coordinated attacks, mutual defense, kingdom chains, clan wars, and clan ranking rewards.
- Season model uses daily, 14-day, monthly, and quarterly cycles. Profile XP, badges, titles, and clan coffer do not reset.

## Design Tensions

- The JSX score formula may be more inclusive than fastest-time-only conquest, but it needs balancing and explanation.
- JSX clan contribution uses XP contribution; the GDD also has RunCoin coffer mechanics. These should remain separate unless unified by a later decision.
- Some numeric values differ from the GDD; DomainSpec should record these as unresolved until selected.

