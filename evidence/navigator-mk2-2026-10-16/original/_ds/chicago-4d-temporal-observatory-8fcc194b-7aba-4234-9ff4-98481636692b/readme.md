# Chicago 4D — Temporal Observatory Design System

Chicago 4D is a year-parameterized, walkable, source-cited reconstruction of early Chicago (live at chicago.polecat.live). This system restyles its front door, the **Temporal Observatory**, as a time machine: you pick a coordinate (1835 river settlement, 1904 Prairie Avenue, 1812 Fort Dearborn, which is still being prepared), lock on, engage, and arrive in the walkable scene with its evidence-graded building records.

**The lore.** The Confluence Laboratory, a fictional Cold War nuclear program at the University of Illinois, Chicago Circle (est. 1965), had a criticality excursion that tore a standing *aperture* at Wolf Point, the apex of the Chicago River's forks. The three-armed fork in a ring is a quiet nod to the trefoil. The Apparatus sends passengers through that aperture.

**Four machines (skins).** The same components and token names run on four machine appearances, set via `<html data-skin="…">`:
- `control-room` is the **1960s Control Room**, the standard machine. It needs no attribute. Cold War mission control: console blue, ivory enamel, brushed aluminum, signal-red keys, green phosphor scopes.
- `brass` is **Precision Brass** (steampunk): brass, walnut, ivory, verdigris, amber; engraved serif.
- `worlds-fair` is **World's Fair** (retro-future): ivory, turquoise, orange, graphite; geometric sans; pill controls; light mode.
- `deep-space` is **Deep Space** (advanced future): obsidian, ceramic, cyan, amber; thin precise sans; chamfered corners.

Persist the choice to `localStorage['chicago4d.skin']` (the same key the source's `js/skin.js` uses).

## Sources
- GitHub: **https://github.com/kevinrhaas/chicago** (branch `main`). Key paths: `chicago/4d/renderers/web/portal/` (portal index, css, js, pending), `chicago/4d/renderers/web/css/skins.css`, `card.css`, `goto.css`, `walk.css`, `js/skin.js`, `chicago/reference/images/`. Explore the repo for deeper context: the AGENTS.md provenance rules, more renderer CSS, and the research corpus.
- Concept boards supplied by the user: `assets/concepts/control-room-60s.png` (04 Temporal Observatory), `precision-brass.png` (01 Steampunk), `worlds-fair.png` (02 Retro Future), `deep-space.png` (03 Advanced Future).

## Index
- `styles.css` is the entry point and contains only `@import` lines. It imports `tokens/` (fonts, colors, semantic, typography, spacing, effects, skins, base) and `components/components.css`.
- `components/` holds the React primitives (see list below), each with `.jsx`, `.d.ts`, `.prompt.md` and a card HTML.
- `ui_kits/observatory/` is the click-through: Home → Lock → Transfer → Arrival, plus the 1812 pending screen.
- `guidelines/` holds the foundation specimen cards (Colors, Type, Spacing, Brand).
- `assets/` contains `logo-mark.svg`, `concepts/` (moodboards) and `imagery/` (archival plates from the research corpus, plus three user-supplied Prairie Avenue photographs: street, glass plate and aerial).
- `dev/bundle-fallback.js` is a preview-only shim used when `_ds_bundle.js` isn't compiled yet.
- `SKILL.md`, `github.md`, `thumbnail.html`.
- **`HANDOFF.md`** is the step-by-step guide for applying this system to the chicago 4D repo: skin migration, file-by-file changes and the copy deck.

## Components
- **brand/**: BrandMark, Masthead
- **instruments/**: Chronometer, YearReadout, IndicatorLamp, TransitSequence, AcquisitionStatus, Telemetry, Placard
- **controls/**: EngageButton, MachineSelector (+ `MACHINES`), Pill, SearchField, Toggle, Tabs
- **destinations/**: EraCard, EraArt, SectionLine
- **records/**: BuildingCard, ConfidenceGrade, ResultRow (+ ResultGroup)
- **overlays/**: DepartureOverlay

Source mapping: Masthead/BrandMark/AcquisitionStatus/EraCard/EraArt/SectionLine/Chronometer/DepartureOverlay come from `portal/`. BuildingCard/Tabs/ConfidenceGrade come from `card.css`. Pill/SearchField/Toggle/ResultRow come from `goto.css`. MachineSelector replaces the portal's "Interface" select. YearReadout, IndicatorLamp, TransitSequence and EngageButton come from the 04 concept board.

**Intentional additions:** **Telemetry** (reactor, field and drift readings) and **Placard** (civil-defense hazard label) carry the 1960s nuclear-lab layer that the brief asked for. Neither exists in the repo.

---

## CONTENT FUNDAMENTALS
**Voice: a transit engineer's logbook with the occasional Gilded-Age aside.** The copy is technical and calm, and it is never breathless. The machine reports and the traveller acts. The source home page copy ("The past is within reach", "Find your moment in Chicago") is retired as too corny.

- **Jargon set:** interval, aperture, coordinate, signature, resolve/resolved, lock, engage, drift (±0.4 d), field coherence, return window, recall, breach, survey, calibrating, criticality, clearance (Circle-3), dosimetry.
- **1800s seasoning:** use it sparingly, at most one phrase per screen. Examples: *kindly*, *if you please*, *a dashed poor show*, *strong opinions on hats*, *newfangled electric*, *parasols*, *ask the constable*, *the carriage trade*, *house of entertainment*.
- **Cold War flavour:** Confluence Laboratory, Circle campus, criticality excursion, Event 65, clearance, dosimetry nominal, *stand clear of the aperture*.
- **Person:** address the reader as "you" or "passengers". The system speaks as the Apparatus or the Laboratory in third person ("The Laboratory declines to send anyone to a place it can only guess at"). Don't use "I". Use "we" only in provenance notes.
- **Casing:** eyebrows, labels, status, telemetry and footers are MONO CAPS with wide tracking. Headlines are sentence case, with an accent-coloured (never italic) final word ("Wolf Point aperture: open."). Buttons are imperative caps verbs: ENGAGE 1835, RECALL, ABORT TRANSFER.
- **Numbers:** dates are ISO-ish (`1835.07.01`), coordinates use ′ ″ (`41° 53′ N 87° 38′ W`), and every numeral is tabular.
- **Provenance is sacred.** Never claim certainty you don't have. Copy states the grade: documented, inferred or conjectural. Pending eras say so plainly.
- **No emoji.** The repo's old landing page used emoji (🏙️ 🗺️). This system does not.

Examples: "Sweeping the interval…" · "1835 · signature resolved at the forks" · "Three coordinates resolved. Field nominal." · "Coordinate drift exceeds tolerance (±2.1 d). Recalibrating — a moment, if you please." · "Nothing in the register by that name. Try 'tavern', or ask the constable."

## VISUAL FOUNDATIONS
- **Colour:** each machine has one dark ground (the World's Fair ground is light ivory), a phosphor/readout `--accent`, one hot `--signal` reserved for the primary Engage action, a `--lamp` for indicators, and a `--hazard` yellow for civil-defense placards. Evidence grades `--doc`, `--inf` and `--con` keep the renderer's values. Use one signal-coloured element per view.
- **Type:** see the Type cards. Control Room uses Barlow Semi Condensed (light 300 display) + Barlow + Instrument Serif roman (for the accent word; **no italics anywhere**) + IBM Plex Mono. Brass uses Cormorant Garamond + Cormorant SC + Courier Prime. World's Fair uses League Spartan + Jost + Space Mono. Deep Space uses Saira (200) + Share Tech Mono. Labels run 8–10px mono caps with .12–.24em tracking. Display type has tight negative tracking.
- **Backgrounds:** a flat ground plus a fixed 80px *field grid* (hairlines at about 14% opacity, masked from left), plus one soft radial `--skin-glow` top-right. There are no gradient washes. Imagery is archival engravings shown *through a CRT*: desaturated or sepia, luminosity-blended, with 1px scanlines and a bottom protection gradient. The arrival screen uses a full-bleed plate under a scanline layer and a side darkening gradient.
- **Instruments as illustration:** the chronometer (concentric rings, dashed tick orbits, a river-fork centre, beacons on slow 100–180s orbits, and a sweep hand) is the hero graphic. Hand-drawn SVG beyond this source geometry is not used.
- **Borders:** 1px `--edge` hairlines everywhere. The primary tile gets an accent-tinted border. Brass adds a double inset rule (an engraved plate). World's Fair adds a 5px orange top bar. Deep Space clips corners to 14px chamfers.
- **Corners:** Control Room 6/4px, Brass 3/2px, World's Fair 22px/pill, Deep Space 2px + chamfer.
- **Shadows:** panels use a deep soft drop (`--shadow-panel`). Hovered tiles lift 5px with an accent glow (`--shadow-lift`). Screens and readouts use an inset bezel. Phosphor dots and lamps glow. The Engage key has a solid 2px lower *lip* (`--shadow-button`).
- **Press and hover:** buttons lighten (brightness 1.08) and rise 1px on hover. On press they drop 2px and lose the lip, like a physical key. Tiles lift and their ↗ arrow nudges up and right. List rows tint with `--ink` at 7%. Focus is a 2px accent outline.
- **Motion:** use `--ease-machine` (.4,0,.2,1) for most things and `--ease-detent` (a slight overshoot) for toggles. Timings are .12s hover, .4s lift, and 1.2s for the transfer ring (scales .6→2.8 and fades). Status lines step through messages about every 450ms. Lamps blink with `steps(2)`. There are no bounces or springs elsewhere. `prefers-reduced-motion` disables all of it.
- **Transparency and blur:** only the arrival HUD bar and the floating kit tab bar use `backdrop-filter: blur`. Panels are about 94% opaque.
- **Layout:** content sits in a 1280px max frame with a 98px masthead and a bottom hairline. Destination tiles sit in a 3-column grid with a 14px gap. Content is single-column below 900px.
- **Cards:** a panel fill, a 1px edge, the machine radius and no coloured left-border accents (the only exception is the card flag's 2px accent rule, which comes from the source).

## ICONOGRAPHY
- The source has **no icon font or sprite**. It uses inline SVG geometry (the brand mark, the chronometer, the era skyline line-art) and **unicode glyphs as icons**: ↗ (tile arrow), → (go), ← (back), × (close), › (sequence separator), ↑ (bearing arrow, rotated), · (separator), ☢ U+2622 (hazard placard; this is a system addition).
- The only stroked UI icon is the search lens in SearchField, which uses Lucide "search" geometry (2px stroke, round caps). If more icons are needed, pull **Lucide from CDN** at a 1.5–2px stroke to match. *Substitution flagged:* no icon set exists in the repo.
- Status is shown with **lamps and dots** (a 5–9px glowing circle), not pictograms.
- No emoji, and no PNG icons.
- Logo: `assets/logo-mark.svg` is the ring and river-fork mark, copied verbatim from the portal masthead. Always pair it with the wordmark "CHICAGO" plus a small code ("4D", or the arrival year).

## Fonts: substitution notice
The repo uses system font stacks only. All webfonts here are **Google Fonts substitutes** chosen to match the concept boards (see `tokens/fonts.css`). Replace them with licensed files if you have them.
