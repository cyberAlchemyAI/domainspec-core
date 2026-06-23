# Visual Definitions

Status: `draft-pass`
Source: `docs/research/source-notes/troqar-visual-identity.md`
Studio profile: `projects/ui-prototyping-studio/development/prototype-gate/troqar-product-architecture/troqar-ui-guidelines.json`

## Brand Grounding

| Element | Definition |
| --- | --- |
| Product name | TROQAR |
| Tagline | Corra. Conecte. Conquiste. |
| Visual thesis | Running performance meets territory, people, and challenges. |
| Core tension | Fire/action energy balanced with green/territory ownership. |

## Image-Derived Identity Direction

The reference image defines TROQAR as a dark, athletic, mobile-first app brand:
near-black asphalt surfaces, compressed display type, vivid orange action,
green territory ownership, route/topographic texture, and a badge-like runner
logo. The app should feel like an active running game and territory companion,
not a pale admin dashboard or generic OAuth demo.

| Signal | Rule |
| --- | --- |
| Product feel | Competitive running, territorial discovery, community challenge, compact mobile app shell. |
| Primary surface | Full dark shell (`#050808` / `#0B0F10`) with raised green-black panels. |
| Accent balance | Orange carries action and motion; green carries connection, territory, ownership, and success. |
| Visual motifs | Hex badge, runner silhouette, route line, topographic texture, compact metric cards, bottom navigation. |
| First page | Login-ready and app-like; Strava is the only visible MVP login method. |

## Logo System

| Asset | Definition |
| --- | --- |
| Mark | Hexagonal badge with orange upper/right stroke, green lower/left stroke, and a stylized runner whose orange torso transitions into green stride/route motion. |
| Wordmark | `TROQAR` in all-caps condensed athletic type; `TROQ` is fire-orange and `AR` is territory-green. |
| Tagline | `CORRA. CONECTE. CONQUISTE.` split across orange, off-white, and green. |
| Compact use | Use the hex mark alone for mobile header, bottom nav, favicon/app icon, or small badges. |
| Full use | Use the horizontal lockup on login and roomy header surfaces. |
| Doc assets | [Logo mark](assets/troqar-logo-mark.svg) and [logo lockup](assets/troqar-logo-lockup.svg). |

## Palette Roles

| Token | Role | Usage |
| --- | --- | --- |
| `fire-orange` (`#FF5C1A`) | Primary action, invasion, challenge urgency. | Connect, submit, active challenge, contested state. |
| `territory-green` (`#1ED97A`) | Control, success, owned territory, verification. | Verified ownership, connected provider, completed mission. |
| `asphalt-black` (`#050808`) | Full app background and logo negative space. | Page shell, login background, deep app chrome. |
| `asphalt-ink` (`#0B0F10`) | App shell and high-contrast dark surface. | Header, nav, primary text inversion. |
| `card-green-black` (`#101918`) | Raised app card surface. | Dashboard cards, profile panels, activity panels. |
| `panel-raised` (`#121C1A`) | Secondary raised surface. | Metric cards, active challenge cards, route preview panels. |
| `off-white` (`#F4F1E8`) | Primary readable text on dark surfaces. | Headings, important labels, CTAs on dark. |
| `cool-gray` (`#8A9693`) | Muted supporting copy. | Privacy notes, caveats, secondary metadata. |
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

- Default to a dark app shell; light cards should be exceptional export or doc
  surfaces, not the product's first impression.
- Pages should be data-first and action-forward, not marketing-page layouts.
- The first viewport after login should show a next action, current territory/control, and active challenge.
- The anonymous first viewport should show the TROQAR logo/lockup, a Strava-only
  connect action, and a privacy/evidence promise.
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

- White admin-dashboard visual language for the app's main authenticated or
  login-first surfaces.
- Single-hue orange-only or green-only UI.
- Purple or blue-purple SaaS gradients.
- Beige, cream, sand, or tan as a dominant product palette.
- Dark, vague atmospheric backgrounds when users need to inspect routes or data.
- Hidden caveats for preview, geometry, or verification state.
- Marketing hero pages as the app's first authenticated screen.
- Multiple visible login providers in the MVP first screen; Strava is the only
  visible login method until product scope changes.

## Studio Consumption

UI Prototyping Studio consumes the image-derived direction through
[`troqar-ui-guidelines.json`](../../../../ui-prototyping-studio/development/prototype-gate/troqar-product-architecture/troqar-ui-guidelines.json),
which is listed in the TROQAR export profile. Future prototype variants must
respect that profile before producing a BodyWar handoff.

## Production UI Anchors

The first production UI pass must keep these visual selectors aligned with the
image-derived direction:

| `data-od-id` | Visual Obligation |
| --- | --- |
| `auth.login-first` | Dark login-first surface, not a light dashboard. |
| `login.hero` | TROQAR identity is first-viewport signal. |
| `login.preview-card` | Mobile app-style preview uses dark panels, orange action, and green territory. |
| `auth.connect.cta` | Fire-orange Strava action. |
| `profile.safe-athlete-card` | Connected card keeps token custody and public profile copy visible. |
| `profile.privacy-card` | Privacy copy stays legible on dark surface. |
| `activity.recent-summary` | Activity summary preserves redaction and no-geometry-proof language. |
| `track.geometry-status` | Placeholder/preview geometry is visually distinct from verified state. |
| `evidence.status-chip` | Evidence status is preview/submitted, never verified by implication. |
