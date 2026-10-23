# Field Navigator Mk II — experience redesign (design doc Rev 1.0)

Transcribed 2026-10-16 from the owner's Claude Design project "Temporal Observatory UI Redesign",
file `Navigator Design Doc.dc.html` (base: kevinrhaas/chicago `dev` @ cc2e803). The original page,
its design-system tokens (`original/_ds/`), and the ten dev phone screenshots the review cites
(`dev-screenshots/IMG_6942..6951.png`) are kept beside this file. Open `original/Navigator Design Doc.dc.html`
in a browser for the mockups (M1–M10).

**The mockup plates under `original/assets/` came with the design doc and have no source record.
They are layout props, not evidence, and must not be used as assets or cited until a source record
with rights exists (AGENTS.md hard rules 1 and 6).** The Glessner copy in the mockups is illustrative
(see the editorial note in §08).

## Owner rulings on the doc's open questions (2026-10-16, in the thread that filed these tickets)

| Question | Ruling |
|---|---|
| A /research page for the order book and other internal views? | **No separate page: hide them behind a toggle** — Settings › About › Researcher mode, off by default. |
| Sound on by default, or always opt-in? | **On by default** (it starts with the first tap; Settings › Sound turns it off). |
| Who writes and approves summaries and captions? | **The loop writes them from graded, sourced facts; the owner approves the Glessner pilot as the pattern.** After that they ship on the gate (lint, reading level, sources). |
| Anonymous usage events ("Measure fun")? | **Local-only counts** on the device, shown in Settings › About; nothing is sent anywhere. |
| Keepsakes in the Jaunts app or their own app? | Not asked; filed on the doc's suggestion — in the Jaunts app for now. |
| "Mk II" in-world, or each skin's own name? | Not asked; filed as one name, NAVIGATOR MK II, on every skin (a one-string change). |

## 01 · Review of the dev build

A great machine at the front door. A filing cabinet after landing.
I reviewed kevinrhaas/chicago@dev under chicago/4d/renderers/web. That covered the portal, the arrival gate, the HUD, the drawer, the building card, and the destination and jaunt data, plus ten phone screenshots of the 1904 Prairie Avenue scene. The Observatory and the jump already feel like a time machine. Everything after landing feels like a research database.
Keep · it works
The Observatory console, the chronometer lock-on and the 1.2 s transfer ring (portal/).
The split-flap year digits in the arrival device (arrival.js setDigits).
The four machine skins and the Wolf Point story.
Every claim is graded Attested, Inferred or Reconstructed and has sources. This is the project's backbone.
One inventory of places, people and businesses (destinations.js).
Jaunts with stops, sources and keepsakes (data/jaunts/, 28 routes).
The touch controls: the left thumb walks and the right side looks.
What breaks the spell
There are two gates after loading: Tap to enter, then a Welcome card.
Seven HUD buttons in two rows cover about a quarter of a phone screen.
Eight menu tabs scroll sideways, with no sense of where you are.
The building card opens with file paths and parcel IDs.
Internal words show up in the UI: order book, tier 1, tickets, commit gate.
The best material is missing or buried: who lived there, who designed it, and why it matters.
SevFindingWhere
HIGHThe label says Destination year while the digits show the present year (2024 in the screenshot). You can't tell where you're going.index.html #arrival-year · arrival.js yearForProgress
HIGHTap to enter, then the Welcome card (Jaunts · Starting at… · Explore by myself). That is two stops before you can play.#gate-btn · #welcome · IMG_6950–51
HIGHThe building card opens with "(data/street_grid/1904.json)" and "parcel prairie_1800", and gives the address three times.popup.js · IMG_6942
HIGHBug: bay dining [object Object] appears under Attributes.popup.js / compact-attributes.js · IMG_6945
HIGHWrong era: the 1835 fire-limit by-law ("5 August 1835… hay") appears on a 1904 building.card Evidence tab · IMG_6944
MEDThe HUD has year, Start/Jaunts, Confidence (an unlabeled dot on phones), its caret, pace, Fly, theme and menu. That is too many targets..hud-top
MEDThe Travel tab asks Walk/Wagon/Horse twice ("how you get there" and "your own pace") and adds three speed sliders.#s-travel · #s-pace · IMG_6948
MEDThe Evidence hub has ten topics, and some are in internal language: "order book", "the tickets that owe it", "commit gate".evidence.js · #order-book
MED"Evidence", "Citations" and "Sources" name the same thing in different places.drawer tab · card tab · card section
MEDGo to shows empty chips ("Corners 0") and a "reconstructed roofs (0)" checkbox, and cuts off result titles.goto.js · IMG_6947
LOWPayload, Link and ETA readouts are good machine flavor. Keep them. The lamp codes STRUCT and SYNC don't say what is loading.#arrival-readout · #arrival-lamps
LOWThe light/dark toggle sits in the HUD. The DEV pill and build stamp overlap the device on phones.#btn-theme · #gate-build

## 02 · Principles

Five rules every ticket answers to.
1The device is the interface
Every menu, setting and record lives on the handheld Navigator. The world stays clear.
2Land, don't load
Loading is part of the trip. There are no gates and no "tap to enter". When the year locks, you are there.
3Headline first, depth on demand
Every screen opens with the three things worth knowing. Detail is one tap away and never in the way.
4Talk like a great tour guide
Write for a curious 15-year-old: short, specific, a little funny. Machine words go in labels, never in sentences you have to read.
5Honest in color
Every fact shows its grade: Attested, Inferred or Reconstructed. The grade is a small dot, not a lecture.

## 03 · Audience, voice and terms

Keep the machine's flavor. Lose the paperwork.
Voice rules
Target an 8th-grade reading level. CI checks it (Flesch-Kincaid ≤ 9).
Keep sentences to 20 words or fewer. Use concrete nouns and active verbs.
Put one surprising detail on every screen.
Talk to "you". Humor is welcome. Never mock the people of the past.
Use plain units: "about 160 feet long", not "161 ft 3 in".
Never show file names, IDs, snake_case, ticket numbers or tier labels.
Machine lore stays in mono-caps labels: ARRIVED, RECALL, LOCKED.
Fake-but-plausible telemetry is welcome: payload, link, field coherence, drift, signal. It lives in readouts and labels. Sentences you have to read stay plain.
Before → after
"John J. Glessner House was a residence at 1800 S. Prairie Avenue … on parcel prairie_1800 (data/street_grid/1904.json)."→ "A granite fortress on the street, a sunny courtyard inside."
"Consulting the Chicago American, 18…"→ "Un-building the Loop…"
"64 claims stand behind this building, and every one of them is in exactly one row here."→ "64 facts. 22 Attested, 6 Inferred, 36 Reconstructed. Tap any one to see its sources."
Locked terms
These words stay exactly as they are across the product. Each one gets a one-line plain meaning wherever it first appears on a screen (shown on tap and in the Guide glossary).
- **Attested** — A source from the time says so. (replaces "documented")
- **Inferred** — Worked out from clues about this exact place. (keep)
- **Reconstructed** — No record exists. We built it so the street makes sense, and say so. (replaces "conjectural")
Confidence viewRecolor the world by grade, or hide a grade completely.becomes a Navigator app
LibertiesEvery choice we made without a source, listed by name.keep; a section inside Sources
SourcesWhere each fact comes from: maps, photos, letters, newspapers.standard term. Retires "Evidence" and "Citations".
Renamed terms
CoordinateDestination
Start / Jaunts chipJaunts app
Starting at… / Pick a placeGo to
Explore by myselfFree roam
Travel / paceMove
Controls / HelpGuide
FirmsShops & work
Modeled phaseStood here
Present statusToday
STRUCT / SYNC lampsSTREETS · BUILDINGS · TREES · PEOPLE
Not recordedUnknown
Order book · tickets · tierNever shown

## 04 · The journey

One trip. Five beats. No dead ends.
The handheld Navigator is with you from the first frame. In the Observatory it is docked into the console. During the jump it is in your hand. When you land it flips to its home screen. Nothing appears that the device didn't put there.
1904 · LOCKED
A · OBSERVATORY · as today
Pick a destination tile. The chronometer locks on and the year readout rolls. No change except copy.
1904
SCAN › LOCK › JUMP
B · JUMP · 1.2 s
The transfer ring. The page navigates while the ring is still expanding.
DESTINATION 1904
1966
Glessner House saved
C · TIME-STREAM · real load
The handheld screen. The current year rolls backward while the scene loads, with captions for landmark years.
ARRIVED
D · LANDING · 700 ms
The year locks with a clunk, the screen flashes, and the device flips over. The scene comes into focus behind it.
ARRIVED · 1904.07.01Jaunt · Go to · Free roam
E · NAVIGATOR HOME
Three choices. Your first tap unlocks audio and look controls. Free roam docks the device.
Journey states (one machine, used by every screen)
observatory›locking›jumping›time-stream›landing›landed›exploring⇄inspecting · on-jaunt · touring›recall (back to Observatory)

## 05 · Arrival and landing

The big number is when you are. The small one is where you're going.
NAVIGATOR MK IIIN TRANSIT
DESTINATION1904· PRAIRIE AVE
1
9
6
6
NOW PASSING
TIME-STREAM
1966 · Chicagoans save the Glessner House from the wrecking ball.
› Rolling back the skyline · OK› Un-building the Loop…
STREETS
BUILDINGS
TREES
PEOPLE
PAYLOAD8.6/14.4 MBLINK1.8 MB/sETAT-00:04
62 YEARS TO GO60%
← ABORTHOLD STEADY
M1 · TIME-STREAM (LOADING)
ARRIVED · 1904.07.01 · 10:42
You're on Prairie Avenue.
Summer 1904. Chicago's richest street, and the Glessners are home.
Take a JauntA corner of Prairie Avenue · 4 min→
Go to…A house, a person, a shop→
Free roamPocket the Navigator and wander→
First time? Take the 60-second tour
M2 · AFTER THE FLIP (HOME)
Year readout: two lines
Small line, above: DESTINATION 1904 · PRAIRIE AVE. It shows from first paint (inline script, like today's digits) and never changes during the trip.
Big ticker: the year you are passing. It starts at the present year and rolls down to the destination. Keep the existing split-flap digits and pacing.
Delete the "Destination year" label over the ticker. That label is the bug.
On landing the small line changes to ARRIVED and the ticker digits turn from amber to phosphor green.
Time-stream captions
As the ticker passes a landmark year, a one-line caption appears for about 2 s. Each destination has its own deck of 8–12 captions (1904 example: 1966 house saved · 1933 Century of Progress fair · 1919 Black Sox scandal · 1909 Burnham Plan). Captions are graded content, like any other fact. On a fast connection show at most 3 captions, and pick the most important ones.
Telemetry: semi-real, on purpose
Keep the Payload, Link and ETA readouts (real bytes, real rate, the forecast ETA from boot-forecast.js). Add a YEARS TO GO counter next to them. The six lamps become four named groups: STREETS (scene + terrain + ground), BUILDINGS, TREES (flora), PEOPLE (people + interaction). Log lines mix machine and destination: "SYNCING TIME MESH… OK", "UN-BUILDING THE LOOP…", "PLANTING 1904 ELMS…", "LOCATING GLESSNER HOUSEHOLD…".
Landing, not "Tap to enter"
Ready fires and the last digit drops into place with a clunk (sound plus navigator.vibrate(30) where supported).
A phosphor flash and ARRIVED stamp take 180 ms.
The device turns over (rotateY 0→180°, 520 ms, ease-machine). The back face is the Navigator Home.
The scene behind un-blurs from 12px to 0 and the gate scrim fades out.
The Home sheet settles at half height. Tapping a choice is the user gesture that unlocks audio and pointer lock.
FAILURE STATE
"The jump stalled somewhere around 1950." Buttons: TRY AGAIN and BACK TO THE OBSERVATORY. The error detail sits in a collapsed "Details for your teacher" section.

## 06 · The Navigator

A handheld with a rail of apps that knows where you are.
The Navigator replaces the hamburger drawer, the Start/Jaunts chip, the Confidence chip and caret, the pace and theme chips, and the Welcome card. It has three heights on phones and a side panel on desktop. A left rail of icons switches apps. Icons appear and disappear depending on where you are and what you're doing, with a short glint when one arrives.
SCR 01 · HOME1904.07.01
YOU ARE ATPrairie Ave & 18th Stfacing west · 10:42 am · warm
RIGHT IN FRONT OF YOUGlessner HouseInspect →
JAUNT IN PROGRESS1 / 2
A corner of Prairie Avenue
MOVEWalking
CONFIDENCEOff
FIELD 0.998DRIFT ±0.4 DSIG ▮▮▮▯RECALL ●
M3 · PHONE · FULL HEIGHT · HOME
INSPECT · 1800 S PRAIRIE
Glessner House
A granite fortress on the street, a sunny courtyard inside…
1904 · JUL 1
M4 · DESKTOP · LEFT PANEL 400 PX, COLLAPSES TO RAIL (N)
DOCK · 64 pxA pill at the bottom edge showing year, current app icon and a grip. Tap or swipe up to open.
HALF · 48%The default. The world stays visible above, so you can keep walking while it's open.
FULL · 82%For reading: the dossier, Sources, the Guide. Swipe down to drop a level.
Machine chrome: it's an instrument, not an app
SCREEN CODESEvery app header reads like a console screen: "SCR 03 · INSPECT", with the scene date on the right.
TELEMETRY STRIPA thin phosphor footer that ticks every 800 ms: FIELD, DRIFT, SIG and a RECALL lamp. It reuses portal.js telemetry and drift events. It is decorative, so mark it aria-hidden.
SEMI-REAL READOUTSReal numbers dressed as instruments: distance to target, heading, speed in mph, facts loaded, frame rate as "FRAME CLK". Fake ones (coherence, drift) never pretend to be research.
BEZEL & KEYSAn inset bezel, four corner screws, and one signal-red key per screen (RECALL, ENGAGE, GO). Pressed keys drop 2 px and lose their lip.
SCOPE PANELSDark green CRT wells with 1 px scanlines for the log, notable facts and the mini map. Reading text stays on the normal panel.
BOOT ON SWITCHSwitching apps runs a 160 ms "tube warm-up": a scanline sweep and a header flicker. Reduced motion uses a plain crossfade.
The rail: when each app shows
AppWhat's in itShows when
HomeWhere you are, what's in front of you, the Jaunt in progress, quick statusAlways
JauntsJaunts · Go to · Free roam (the Welcome card choices, permanently)Always
InspectThe building dossier (§08)A building is selected, or one is under the reticle within 40 m
PeopleWho lived and worked nearby, plus Shops & work as a filterThe scene has people records (1835 yes, 1904 Glessner household)
MapThe whole field with your arrow, tap-to-travel, Jaunt routeAlways
ConfidenceConfidence view: show, hide, color and opacity per grade (§09)Always. The icon glows while the view is on.
MoveWalk · Run · Wagon · Horse · Fly, speed, getting-there style, comfortAlways
JumpOther destinations, Recall to the Observatory, time of day (when supported)Always. Also opens from the year chip.
GuideTour mode, controls, glossary, "Is this real?" FAQAlways, pinned to the bottom of the rail
SettingsDisplay, Comfort, Performance, Machine skin, Units, Sound, About & What's newAlways, pinned to the bottom of the rail
At most 10 icons; usually 8. Contextual icons slide in under Jaunts, and a lamp-amber dot marks the first appearance. What's new moves into Settings. Its dot shows on the Settings icon, never in the HUD.

## 07 · Navigator apps

Jaunts, Move, Map, Jump, Guide and Settings.
SCR 02 · JAUNTS1904.07.01
JauntsGo toFree roam
CONTINUE · STOP 2 OF 2A corner of Prairie AvenueNext: the house from the street
MORE IN 1904
8 MIN · 5 STOPS
Millionaires' RowWho lived on the richest block in town?
Upstairs, downstairsA day for the staff · 6 min→
Getting there: WalkingChange ›
M5 · JAUNTS APP
SCR 06 · MOVEHALF
Walk
Run
Wagon
Horse
Fly
Wagon speedRattling along · 24 mph
When you pick a placeTeleportRide thereFly over
M6 · MOVE · HALF HEIGHT
Jaunts
Jaunts: a card per route with a photo, minutes and stops, plus a keepsake badge once earned. A Jaunt in progress sits on top with "Continue".
Go to: the current search (destinations.js) with filters Places · People · Shops & work · Viewpoints. Chips with zero results are hidden. Titles wrap to two lines. Each row shows distance and an arrow.
Free roam: docks the Navigator and shows a one-time tip: "Tap any building to inspect it."
Remove "Include reconstructed roofs". Search respects the Confidence view: if Reconstructed is hidden, those results are dimmed and say so.
Move
One mode picker replaces both "How you get there" and "Your own pace": Walk, Run, Wagon, Horse, Fly.
One slider for the selected mode only. Keep the named speeds ("rattling along").
Getting-there style is a single choice: Teleport, Ride there (on the street at your mode) or Fly over.
Comfort lives here: head bob, eye height, snap-turn on touch.
The HUD keeps a single Walk/Fly toggle. Everything else is here.
Map
The current "whole field" map moves inside the device. Tap a building to preview it, then Go. Jaunt routes are drawn as dotted lines. A legend toggle uses the Confidence view colors.
Jump
The three destinations as mini era cards, with your current one marked HERE. Picking another runs a short in-world jump: ring, time-stream, landing. RECALL returns to the Observatory. Its button is the one signal-red key on this screen.
Settings
Display: brightness, field of view, road visibility, labels, light/dark, text size (100–140%).
Machine: the four skins as preview tiles.
Performance: detail, sharpness, frame pacing, with an "Auto" recommendation.
Sound: master, effects, ambience.
Units, then About & What's new (the build stamp lives here in dev).
Each "Why this default" essay becomes a one-line hint plus a "Why?" popover of 40 words or fewer.

## 08 · The building dossier

Read the front page in 20 seconds. Spend 20 minutes if you want.
The Inspect app replaces the floating card. The front page answers the questions a visitor actually has: what is it, who lived here, who designed it, what should I look at, and what makes it remarkable. Every line carries its grade dot. The tabs go deeper.
INSPECT×
1800 S. PRAIRIE AVE · AT 18TH ST
Glessner House
STILL STANDINGBUILT 1887HOME
A granite fortress on the street, a sunny courtyard inside. The architect turned the house's back on busy Prairie Avenue, and the neighbors were not impressed. By 1904 John and Frances Glessner have lived here for 17 years.
ARCHITECTH. H. Richardson
OWNERJohn J. Glessner
STYLERomanesque
TODAYA museum
WHO LIVES HERE · 1904ALL →
JGJohn J. GlessnerFarm-machine executive, helped found International Harvester
FGFrances M. GlessnerSilversmith, beekeeper, kept a journal for decades
+ household staff · grown children George and Frances
LOOK FOR
Rough pink-grey granite wallsSHOW ME
The great arch on 18th StreetSHOW ME
Skinny windows on the north sideSHOW ME
NOTABLE FACTS
Their daughter Frances grew up to build tiny, perfect crime-scene dollhouses. Detectives still train with them.
1 of 3 · swipe
CONFIDENCE · 64 FACTSSOURCES →
22 Attested6 Inferred36 Reconstructed
OverviewPeopleDesignStoryPhotosSources
M7 · INSPECT · OVERVIEW (FULL HEIGHT, SCROLLED)
← GLESSNER HOUSE×
Design
STYLE GUIDE · 1 OF 6
Richardsonian Romanesque
Named after this house's architect. Think castle more than mansion: heavy stone, round arches, very little decoration.
HOW TO SPOT IT
Rough-cut stoneRound archesDeep-set windowsLow, heavy mass
ON THIS HOUSE · TAP TO LOOK
1Wellesley granite street wallsStone on the street sides only. Brick everywhere else.
2Red clay tile roofUnglazed, so it stays matte, not shiny.
3The hidden courtyardThe house faces inward. Vines cover the brick.
4Carriage doorsCopied from an 1888 photograph.
5Exact window sizesNo drawing gives every one. Listed in Liberties.
COMPARE STYLES
ItalianateTall windows, curved hoods, bracketed eaves
Greek RevivalColumns, triangle gables. Big in 1835.
Queen AnneTowers, porches, everything at once
M8 · INSPECT · DESIGN TAB
Front page, top to bottom
Plate: the best period photo, shown through the CRT treatment. If none exists, a render from the "Show me" angle.
Address line, name, three status chips: Still standing or Gone (year), Built year, Use.
Summary: 3 sentences, 60 words or fewer. Authored, not generated from attributes.
Key facts grid: Architect, Owner, Style, Today. Each has a grade dot.
Who lives here (scene year): up to 3 people with a one-line role, then "+ N more".
Look for: 3 features. "Show me" turns the camera to the feature and pulses an outline.
Notable facts: 1–3 surprising facts about the people or the building, swipeable.
Confidence meter: the Attested / Inferred / Reconstructed split. Tap to open Sources.
Tabs
PeopleResidents, staff and visitors in the scene year, then before and after. Each person card links to the People app.
DesignThe style guide card, numbered hotspots ("On this house") and Compare styles. Hotspots replace the old attribute table.
StoryBUILT → YOU ARE HERE → TODAYA timeline from design to today, filtered by era. 1835 civic rules never show on 1904 buildings.
PhotosA grid sorted by date, each with year, a caption and a "from this spot" button. Group the 162 images and show the 12 best first.
SourcesFacts grouped by grade, with Liberties as a section. Human source titles only. Full citations collapse under each fact.
EDITORIAL NOTE
The Glessner copy here is illustrative. Before it ships, every line must map to a graded fact in glessner-dossier.json or a source record. In particular, check the daughter's Nutshell Studies, Richardson's death before construction, and the 1966 rescue. All three are well known but are not yet in the 4D sources.

## 09 · Confidence view

See what's Attested. See what we Reconstructed. Choose how.
SCR 05 · CONFIDENCE VIEWON
NORMALBY GRADEATTESTED ONLYX-RAY
Attested412
TINT · 60%
Inferred138
TINT · 60%
Reconstructed553
TINTGHOSTDITHER
OPACITY35%
Liberties: 553 choices made without a source →
GRADE MASK 3/3MESHES 1,103FRAME CLK 58
M9 · CONFIDENCE VIEW
Today the Confidence view is a chip, a caret and a checkbox menu in the HUD. It becomes a Navigator app. Each grade gets one row with four controls, and presets make the common views one tap.
ShowOn or off per grade. Off removes those meshes, as the #cm-attested / #cm-inferred / #cm-reconstructed checkboxes do today.
Color4 curated swatches per grade. The default is the renderer's grade color, and a color-blind-safe set is available.
LookTint (recolor), Ghost (see-through) or Dither (today's Reconstructed massing).
Opacity0–100%. Sets tint strength for Tint and transparency for Ghost.
NORMALEverything shown, no color. The default.
BY GRADEToday's Confidence chip. Hotkey C still works.
ATTESTED ONLYShows only the parts somebody wrote down.
X-RAYAttested solid, Inferred at 50%, Reconstructed ghosted at 25%.
While the view is on, a small legend chip sits under the year chip in the HUD. Tapping it opens this app.
Overlays sit at the bottom of the app: street names, building labels, people pins and the Jaunt route.
Choices persist in localStorage['chicago4d.confidence'] and carry between destinations.

## 10 · In-world HUD

Give the sky back to 1904.
1904 1 July
Start / Jaunts
● ▾
Walk
↑
◐
≡
≈ 25% OF SCREEN
BEFORE · DEV TODAY
1904 · 07.01
CONF
N274°
GLESSNER HOUSE · 38 FT
NAVIGATOR▲
AFTER · ≤ 10% OF SCREEN
Stays on screenBehavior
Year chipTop left, amber LED digits. Tap opens Jump.
Confidence legendOnly while the Confidence view is on. Tap opens the app.
Compass + mini mapTop right, merged into one round instrument. Tap opens Map.
Target tagWhen the reticle rests on a building for 400 ms: name and distance. Tap it or press E to Inspect.
Quick columnWalk/Fly toggle, plus an Inspect key that appears with a target. Max 2 buttons.
Navigator dockBottom center on phones, left rail on desktop. N or Tab toggles it.
Street readoutKept. A 2 s toast when you cross onto a new street, then it fades.
Moved into the Navigator: Start / Jaunts (to Jaunts app), Confidence chip and caret (to Confidence), pace (to Move), theme (to Settings › Display), menu (to the dock), the control-help popover (to Guide), DEV pill (to Settings › About, dev builds only).

## 11 · Tour mode

Sixty seconds of training, then your Navigator license.
An interactive walkthrough the Navigator runs itself, framed as a Confluence Laboratory field check. It offers itself once after the first landing on a device. It can be replayed from Guide. Every step waits for you to actually do the thing, and Skip is always visible.
FIELD CHECK · 4 / 7SKIP ×
TASK · INSPECT A STRUCTURE
Tap the Glessner House.
Every building has a file. This one is famous.
WAITING FOR INPUT
M10 · TOUR · STEP 4
#Bubble copyCompletes when
01This is your Navigator. Everything you need lives here.Dock highlighted, tap Next
02Look around. Drag the right side of the screen (or move the mouse).Camera yaw changes ≥ 60°
03Walk. Left thumb, or W A S D. Head for the corner.Moved ≥ 5 m
04Tap the Glessner House. Every building has a file.Inspect opens on any structure
05Front page first. Tabs go deeper. Try Design.Any tab other than Overview opened
06How sure are we? Turn on the Confidence view.Preset other than Normal chosen
07Ready. Take a Jaunt, or Jump to another year.Tap Finish. Awards the NAVIGATOR LICENSE keepsake.
Bubbles are 14 words or fewer. A spotlight cut-out marks the target, and the rest of the screen dims to 55%.
Progress persists. Reload mid-tour and it resumes at the same step, or it can be abandoned from Guide.
Teacher mode (Guide › For teachers) shows the same 7 steps as a printable one-page handout.
Contextual hints after the tour are one-time only: first Jaunt, first Jump, first Reconstructed building.

## 12 · Content and culling

Keep the research. Promote the best. Retire the plumbing.
Promote to the front page
People: residents, their jobs, one human detail each
Architect and style
Three things to look for, each with a camera target
Notable facts about the people or the structure
Still standing or gone, and what it is today
Move one level down
Attribute table → Design hotspots
Modeled phase dates → Story timeline
Per-claim sources and "why" → Sources tab
Liberties per building → Sources › Liberties
Fire limit (1835 only) → Story, and the 1835 Jaunt "Inside the fire limit"
City numbers, fauna, plants, exclusions, open questions → Guide › About this destination
Remove from visitor UI
File paths, parcel IDs, source IDs in snake_case
"Tier 1 · period/eyewitness" (keep in data, show as "from the time" or "written later")
Order book, ticket references, commit-gate notes. These move to a separate /research page for adults.
Repeated addresses
"Why this default" essays longer than 40 words
Building summary record
A new authored file per notable structure, read by the Inspect app. Structures without one get a generated fallback built from the sidecar using templates, never raw fields.
data/summaries/glessner_house.json
{
"id": "glessner_house", "scene": "1904",
"name": "Glessner House",
"address": "1800 S. Prairie Ave · at 18th St",
"status": { "text": "Still standing", "today": "A museum", "grade": "attested", "sources": [...] },
"built": { "year": 1887, "grade": "attested" },
"use": "Home",
"summary": "≤ 60 words, ≤ 3 sentences",
"key": [ { "label": "Architect", "value": "H. H. Richardson", "grade": "attested", "sources": [...] }, ... ],
"residents": [ { "person": "john_j_glessner", "role": "≤ 12 words" } ],
"lookFor": [ { "text": "≤ 8 words", "feature": "street_wall_granite", "camera": {"yaw":-82,"pitch":6}, "grade": "attested" } ],
"notable": [ { "text": "≤ 25 words", "about": "person|structure", "grade": "...", "sources": [...] } ],
"style": "richardsonian_romanesque",
"story": [ { "date": "1885-05", "text": "...", "era": "1904" } ]
}
Impact scorePick which facts make the front page by ranking: surprising (×3), about a person (×2), visible from the street (×2), Attested (×1.5).
Style libraryShared modules: Greek Revival, Italianate, Second Empire, Queen Anne, Richardsonian Romanesque, Chicago School. Each has 4 "how to spot it" cues and a reference plate.
LintedCI checks length limits, reading grade ≤ 9, a grade on every fact, sources on every Attested fact, and no ids or paths in strings.

## 13 · Look, motion and sound

Cool on the outside. Easy to read on the inside.
Type roles (Control Room skin)
Glessner HouseDISPLAY 300 · 28–34
A granite fortress on the street, a sunny courtyard inside.BODY 16 / 1.55
SCR 03 · INSPECTLABEL MONO CAPS
Reading text is Barlow, 16 px minimum on phones (raised from today's 14), and never mono.
Mono caps are for labels of 4 words or fewer, numbers and telemetry.
Lines are 65 characters or fewer. Contrast is 4.5:1 or better on every panel.
The Text size setting scales all reading text 100–140% and reflows the layout.
Motion
Year ticker rollexisting · per digit flap
Landing flash + stamp180 ms
Device flip520 ms · rotateY · ease-machine
Sheet detent change280 ms · ease-detent
App switch (tube warm-up)160 ms · scanline sweep
Rail icon arrives240 ms slide + glint
"Show me" camera turn900 ms · ease-in-out
Reduced motion: no flip (crossfade instead), ticker in 5 steps (existing reducedProgress), instant camera cuts.
Sound (new, off by default in class)
Ticker: a soft flap tick per digit change, capped at 12 per second.
Landing: a low clunk and a short reverb tail.
Navigator: relay clicks on rail taps and a hum while open.
Ambience per destination: wagons and birds in 1835, streetcar bells in 1904.
Settings › Sound has master, effects and ambience. The first-run default follows the device mute state.
Readouts from the design system
Use YearReadout, ConfidenceGrade, IndicatorLamp, Telemetry and Tabs from the Temporal Observatory system. All four skins inherit the Navigator automatically.

## 14 · Build notes

Recommendations, not orders.
Journey state machineA tiny js/journey.js emitting state events (§04). The HUD, Navigator, Tour and audio subscribe. arrival.js calls journey.land() from settle() instead of enabling #gate-btn.
Gesture gating without a gateAudio resume and pointer lock need a user gesture. Use the first tap on a Home choice, the canvas, or any Navigator control. On desktop show a "CLICK TO ENGAGE LOOK" tag until lock. iOS has no pointer lock, so only audio applies there.
App registrynavigator.register({ id, icon, label, code, when(ctx), badge(ctx), mount(el), unmount() }). Existing goto.js, people.js, businesses.js, settings and evidence mounts become apps and keep their element ids, so the smoke gate still passes.
Portal continuityportal.js already writes sessionStorage['chicago4d.transfer']. If it is less than 10 s old, the arrival page starts with the ring's tail on screen so the jump reads as one shot.
Deep links/1904/?nav=inspect:glessner_house&tab=design opens after landing. Back closes the current app before leaving the page. Teachers can share any screen.
Confidence view renderingPer-grade uniforms (color, mode, opacity) on the batched materials in confidence.js and batch-material.js. Ghost mode needs depthWrite off, sorted last. Dither reuses the current Reconstructed path.
Lazy and lightOnly Home ships in the boot payload. Other apps load on first open. Inspect prefetches the summary file when a target tag appears.
AccessibilityThe rail is a tablist and apps are tabpanels. The Navigator is a non-modal region that moves focus on open. Landing announces "Arrived: Prairie Avenue, 1 July 1904". Telemetry is aria-hidden.
Measure funAnonymous events: landed, first inspect, tab opened, Show me used, Jaunt started and finished, Tour step reached, Confidence preset. The target is first inspect within 90 s for 70% of visitors.



## 15 · Ticket backlog (from the page data)

Suggested order: E1 → E2 → E3 unblock everything else. E5 and E10 can run in parallel with an editor.

### E1 · Journey and arrival

_The jump, time-stream and landing feel like one continuous trip with no gates._

- **NAV-101 · Two-line year readout** — A small DESTINATION 1904 · PRAIRIE AVE line sits above the ticker from first paint. The ticker shows the year being passed, from the present to the target. The "Destination year" label over the ticker is gone.
- **NAV-102 · Time-stream captions** — Captions show as the ticker passes milestone years: at most 3 on fast loads and 8 on slow ones. Each is 70 characters or fewer, graded, and from the destination deck.
- **NAV-103 · Arrival telemetry pass** — Payload, Link and ETA are kept. A YEARS TO GO counter is added. The six lamps become STREETS, BUILDINGS, TREES, PEOPLE, mapped to boot phases. Log lines come from the destination deck.
- **NAV-104 · Landing replaces Tap to enter** — On ready: clunk, flash and ARRIVED stamp, then the device flips to Home. #gate-btn is removed. The scene is interactive 900 ms or less after ready.
- **NAV-105 · Gesture gating without a gate** — Audio and pointer lock start on the first Home choice or canvas interaction. iOS Safari logs no autoplay errors. Desktop shows CLICK TO ENGAGE LOOK until lock.
- **NAV-106 · Portal continuity** — If the transfer timestamp is less than 10 s old, the arrival page opens with the ring tail animating.
- **NAV-107 · Failure state** — Shows "The jump stalled…" with TRY AGAIN and BACK TO THE OBSERVATORY. Details sit in a collapsed panel.

### E2 · Navigator shell

_One handheld device holds every menu, setting and record._

- **NAV-201 · Device component** — Phone: bottom sheet with DOCK, HALF and FULL detents, driven by drag and tap. Desktop: 400 px left panel that collapses to the rail. Bezel, screen code header and telemetry strip included.
- **NAV-202 · App registry + contextual rail** — Apps declare when(ctx). Inspect appears only with a target or selection, People only when the scene has people. Icons animate in and out within 240 ms.
- **NAV-203 · Dock** — Always visible when closed: status lamp, NAVIGATOR label, current app icon. One tap opens to the last app at HALF.
- **NAV-204 · Deep links + back** — ?nav=app[:id]&tab= opens after landing. The browser back button closes the current app first.
- **NAV-205 · Keyboard + a11y** — N/Tab toggles, 1–9 select rail apps, Esc closes. Rail is a tablist and focus moves into the app on open.
- **NAV-206 · Migrate drawer panels** — goto, people, businesses, evidence and settings mount inside apps. Every id read by the smoke gate still resolves.
- **NAV-207 · Telemetry strip** — Footer ticks every 800 ms with FIELD, DRIFT, SIG and RECALL. Reuses portal drift logic, is aria-hidden, and pauses when hidden.

### E3 · HUD declutter

_The world gets its screen back._

- **NAV-301 · Remove HUD chips** — Start/Jaunts, Confidence + caret, pace, theme and menu are removed from .hud-top. Their functions are reachable in the Navigator.
- **NAV-302 · Year chip and compass-map instrument** — Year chip opens Jump. The merged round compass/mini map opens Map.
- **NAV-303 · Target tag + quick column** — The reticle dwell (400 ms) shows name and distance. The quick column holds Walk/Fly and a contextual Inspect key, never more than 2.
- **NAV-304 · Footprint budget** — HUD covers 10% or less of a 390×844 viewport and respects safe areas.
- **NAV-305 · Dev chrome** — DEV pill and build stamp move to Settings › About on phones.

### E4 · Jaunts app

_Jaunts, Go to and Free roam stay one tap away forever._

- **NAV-401 · Jaunts app shell** — Segments: Jaunts · Go to · Free roam. Opens from Home choices and the rail.
- **NAV-402 · Jaunt cards** — Each card shows plate, title, premise, minutes, stops and keepsake state. A Jaunt in progress is pinned on top with Continue, and this survives reload.
- **NAV-403 · Go to cleanup** — Zero-result chips are hidden. Titles wrap to 2 lines. Rows show distance and bearing.
- **NAV-404 · Remove reconstructed-roofs checkbox** — Search follows the Confidence view. Hidden-grade results show dimmed with a reason.
- **NAV-405 · Free roam** — Docks the Navigator and shows a one-time tip.

### E5 · Building dossier (Inspect)

_Headline facts in 20 seconds, depth on demand._

- **NAV-501 · Overview layout** — Order: plate, address, name, chips, summary, key facts, residents, Look for, Notable facts, Confidence meter. Matches M7.
- **NAV-502 · Summary record + compiler** — data/summaries/<id>.json schema (§12) is validated in CI, with a grade on every fact and sources on every Attested fact.
- **NAV-503 · Fallback summary** — Templated from the sidecar when no summary exists. Never contains ids, paths or snake_case.
- **NAV-504 · Tabs** — Overview · People · Design · Story · Photos · Sources. A new building always opens on Overview.
- **NAV-505 · Show me** — Turns the camera to the feature in 900 ms and pulses an outline for 2 s. In fly mode it moves to a viewpoint first.
- **NAV-506 · Design tab + style library** — Style card, numbered hotspots with grades, Compare styles. Six style modules authored.
- **NAV-507 · Story tab, era filter** — Timeline from design to today. Content tagged with another scene era never renders, which fixes the 1835 fire limit on 1904 cards.
- **NAV-508 · Sources tab** — Facts grouped by Attested, Inferred and Reconstructed, with a Liberties section. Human-readable source titles. Full citations collapse.
- **NAV-509 · Fix [object Object]** — Object-valued attributes render their value or are omitted. A unit test covers bay_dining.
- **NAV-510 · Photos** — Images sorted by date. The 12 best show first and the rest sit behind "All 162".

### E6 · Confidence view app

_Show, hide, color and fade each grade._

- **NAV-601 · Presets** — NORMAL, BY GRADE, ATTESTED ONLY, X-RAY. Hotkey C toggles BY GRADE.
- **NAV-602 · Per-grade controls** — Show toggle, 4 swatches, Look (Tint, Ghost, Dither), opacity 0–100. Live counts per grade.
- **NAV-603 · Renderer uniforms** — Per-grade color, mode and opacity in confidence.js. Ghost sorts last with depthWrite off. 60 fps holds on the mid-tier phone profile.
- **NAV-604 · Persist + HUD legend** — Saved to chicago4d.confidence and carried across destinations. A legend chip shows in the HUD while the view is on.
- **NAV-605 · Overlays** — Street names, building labels, people pins and Jaunt route, each with its own toggle.

### E7 · Move app

_One question: how do you want to move?_

- **NAV-701 · Mode picker** — Walk, Run, Wagon, Horse, Fly replace #s-travel and #s-pace. One slider for the active mode, keeping the named speeds.
- **NAV-702 · Getting-there style** — Teleport, Ride there or Fly over is used by Go to, Map and Jaunts.
- **NAV-703 · Comfort** — Head bob, eye height (keeping the researched default and its "Why?"), snap-turn on touch.

### E8 · Guide and Tour mode

_Anyone can learn the Navigator in a minute._

- **NAV-801 · Tour engine** — 7 steps (§11), each completing on a real action. Skip, resume after reload, replay from Guide.
- **NAV-802 · First-landing offer** — Offered once per device after landing. Declining never re-prompts.
- **NAV-803 · Controls sheet** — Device-aware: touch or keyboard, from controls/intent.js.
- **NAV-804 · Glossary + FAQ** — Locked terms with one-line meanings. "Is this real?" and "What does Reconstructed mean?" answered in 60 words or fewer each.
- **NAV-805 · Navigator License** — Keepsake awarded on finishing the tour, shown in the Jaunts app keepsakes.
- **NAV-806 · Teacher handout** — Printable one-page version of the tour and three suggested Jaunts per destination.

### E9 · Map, Jump and Settings

_Everything else, in its place._

- **NAV-901 · Map app** — Whole field inside the device, tap-to-preview then Go, Jaunt route drawn.
- **NAV-902 · Jump app** — Era mini-cards with HERE marker. In-world jump runs ring, time-stream and landing. RECALL is the only signal-red key.
- **NAV-903 · Settings app** — Display (incl. light/dark, text size), Machine skins, Performance, Sound, Units, About & What's new.
- **NAV-904 · Short "Why?"** — Each "Why this default" becomes a hint plus a popover of 40 words or fewer. Full text moves to /research.

### E10 · Voice and content pass

_Written for a curious 15-year-old._

- **NAV-1001 · String table + glossary** — All UI strings in one table. Locked terms enforced, renamed terms applied (§03).
- **NAV-1002 · Evidence hub → Guide › About this destination** — Ten topics become 4 cards: How we grade, Sources, Liberties, What lived and grew here. The order book moves to /research.
- **NAV-1003 · Visitor-UI lint** — CI fails on file paths, ids, snake_case, "tier", "ticket" or "order book" in visitor strings.
- **NAV-1004 · Reading-level check** — Summaries, facts and bubbles score Flesch-Kincaid ≤ 9.
- **NAV-1005 · Glessner pilot** — The full summary record for Glessner House is authored and fact-checked against the dossier. It becomes the reference for other buildings.
- **NAV-1006 · Student playtest** — 6–8 students, 3 tasks (find a house, learn who lived there, tell Attested from Reconstructed). 80% or more succeed unaided.


## 16 · Test cases (from the page data)

| ID | Area | Steps | Expect |
|---|---|---|---|
| QA-01 | Arrival | Jump to 1904 from the Observatory. | Small line reads DESTINATION 1904 from first paint. Ticker rolls from the present year to 1904. |
| QA-02 | Arrival | Wait for ready. | No Tap to enter. Device flips to Home. Scene interactive within 900 ms. |
| QA-03 | Arrival | Throttle to Slow 3G. | Payload, Link, ETA and YEARS TO GO update. 8 or fewer captions. Year never moves backwards. |
| QA-04 | Gestures | iOS Safari: land, tap Free roam. | Ambience starts. No console errors. |
| QA-05 | Gestures | Desktop: land, click the scene, press Esc, press N. | Pointer lock engages, then releases. Navigator opens. |
| QA-06 | Motion | Enable reduced motion and jump. | Ticker in 5 steps. Crossfade instead of flip. No telemetry ticking. |
| QA-07 | Rail | Look at Glessner House, then away. | Inspect icon appears with the target tag and leaves 300 ms after the target is lost (unless selected). |
| QA-08 | Dossier | Inspect a building with no summary file. | Fallback renders with no ids, paths or snake_case. |
| QA-09 | Dossier | Open every tab on a 1904 building. | No 1835 content. No "[object Object]" anywhere in the DOM. |
| QA-10 | Dossier | Tap Show me on each Look for item. | Camera turns to the feature and the outline pulses. |
| QA-11 | Confidence | Hide Reconstructed, set Attested opacity to 30%, reload. | Reconstructed meshes gone. Tint at 30%. Both persist. |
| QA-12 | Confidence | Choose ATTESTED ONLY. | Same scene as hiding Inferred and Reconstructed by hand. |
| QA-13 | Jaunts | Start a Jaunt, reload mid-way. | Home and Jaunts app both show Continue at the right stop. |
| QA-14 | Go to | Open Go to in 1904. | No zero-count chips. Long titles wrap to two lines. |
| QA-15 | Deep link | Open /1904/?nav=inspect:glessner_house&tab=design. | After landing, Inspect opens on Design. |
| QA-16 | Tour | Run tour; reload at step 4; skip at 6. | Resumes at 4. Skip ends cleanly. Replay is available in Guide. |
| QA-17 | HUD | Measure HUD on 390×844. | 10% or less of the viewport covered. |
| QA-18 | Text size | Set text size to 140%, open the dossier. | Everything reflows with no clipped text. |
| QA-19 | Keyboard | Complete the tour and change the Confidence view using only the keyboard. | All reachable, with visible focus. |
| QA-20 | Screen reader | VoiceOver: land in 1904. | Announces "Arrived: Prairie Avenue, 1 July 1904". |
| QA-21 | Skins | Cycle all four skins with the Navigator open. | Every app is legible at 4.5:1 or better. |

## Open questions and definition of done (as written)

Open questions for the owner
Is a /research page for adults acceptable as the home for the order book and other internal views?
Sound on by default outside school networks, or always opt-in?
Who writes and approves the building summaries and time-stream captions? Is there a teen review panel?
Should the Jaunts app also hold keepsakes, or should keepsakes get their own rail app later?
Should the Navigator label read "Mk II" in-world, or carry the skin's own name per machine?
Definition of done (every NAV ticket)
Works on a 390×844 phone and a 1440×900 laptop.
Works in all four skins and with reduced motion.
No ids, file paths or snake_case visible (string lint passes).
Locked terms used exactly: Attested, Inferred, Reconstructed, Confidence view, Liberties, Sources, Jaunts.
Smoke gate ids preserved, or the gate is updated in the same PR.
CONFLUENCE LABORATORY · FIELD NAVIGATOR MK II · DESIGN REV 1.0The machine is fiction. The town is real research.