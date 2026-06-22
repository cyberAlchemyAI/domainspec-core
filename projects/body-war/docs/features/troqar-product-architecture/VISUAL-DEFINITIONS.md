# Visual Definitions

Status: `draft-pass`
Source: `docs/research/source-notes/troqar-visual-identity.md`

## Brand Grounding

| Element | Definition |
| --- | --- |
| Product name | TROQAR |
| Tagline | Corra. Conecte. Conquiste. |
| Visual thesis | Running performance meets territory, people, and challenges. |
| Core tension | Fire/action energy balanced with green/territory ownership. |

## Palette Roles

| Token | Role | Usage |
| --- | --- | --- |
| `fire-orange` | Primary action, invasion, challenge urgency. | Connect, submit, active challenge, contested state. |
| `territory-green` | Control, success, owned territory, verification. | Verified ownership, connected provider, completed mission. |
| `asphalt-ink` | App shell and high-contrast text. | Header, nav, primary text. |
| `route-blue` | Map/route utility and neutral route state. | Route outlines, informational chips. |
| `sand-light` | Calm surface background. | Page background and empty states. |
| `warning-amber` | Preview or caveat state. | Geometry caveats, preview accepted. |

## Typography Roles

| Role | Source Direction | Usage |
| --- | --- | --- |
| Display | Bebas Neue reference | Page titles, route names, challenge titles. |
| Body | DM Sans reference | Body copy, forms, tables, data labels. |
| Numeric/Data | DM Sans tabular or system fallback | Pace, distance, XP, rankings. |

## Composition Rules

- Pages should be data-first and action-forward, not marketing-page layouts.
- The first viewport after login should show a next action, current territory/control, and active challenge.
- Route and map surfaces should reveal actual route/territory state, not decorative abstract graphics.
- Cards are for repeated route/activity/challenge items and operator queue entries; page sections stay unframed layouts or full-width bands.
- Buttons should use clear action labels and familiar icons once an icon set is selected.

## Visual Component Definitions

| Component | Visual Rule |
| --- | --- |
| `RouteHero` | Display title, route status, controller metric, and geometry caveat. |
| `ControllerPanel` | Strong state indicator; preview basis is visually distinct from verified. |
| `ActiveChallengeCard` | Fire-orange accent, progress, reward, deadline. |
| `GeometryStatusBadge` | Neutral/amber/green status by geometry maturity. |
| `XPProgressBar` | Green progress, numeric label, no fake precision. |
| `BottomNavigation` | Five stable destinations: Home, Routes, Challenges, Community, Profile. |
| `ActivityCard` | Distance, moving time, pace, sport type, eligibility. |
| `ReviewQueueItem` | Evidence status, source, actor, decision controls. |

## Page Visual Hierarchy

1. Primary status and action.
2. Current territory or route context.
3. Challenge/progression incentive.
4. Supporting feed/history.
5. Secondary navigation.

## Do Not Use

- Single-hue orange-only or green-only UI.
- Dark, vague atmospheric backgrounds when users need to inspect routes or data.
- Hidden caveats for preview, geometry, or verification state.
- Marketing hero pages as the app's first authenticated screen.
