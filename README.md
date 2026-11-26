[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/stwbz/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/stwbz/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# Sum up 25 November's world news in one image

A newspaper front page for **Wednesday 25 November 2026**, drawn with Python +
PIL — every word is drawn as text, so nothing is garbled.
Built for the [make.fun bounty "Sum up 25 November's world news in one image"](https://make.fun/bounty/news-image-20261125).

## The layout

The same winner template the 24 November entry validated: a giant serif date,
a UTC timeline strip, a numbers strip, three big data-carrying hero scenes,
ten numbered small cards, a numbered world map, a numbered "Also On" list, a
DATE CHECK box, and a sources footer.

It carries **35 stories, every one of them first reported on Wednesday 25
November 2026** by a named outlet (AP, Reuters, AFP, BBC, CNN, FT, Xinhua,
UEFA, BEA, DOL, Yonhap, SPA, ISW, OHCHR, Finnhub and others). The full story
list with one named source and one specific figure or name per story is in
`~/workspace/makefun/news-image-20261125-research-v2.md` (§1, build notes, not
part of the submitted bundle), as corrected by the v2 audit
(`~/workspace/makefun/news-image-20261125-audit-v2.md`).

- **Hero 1 — Dow erases a 1,100-point plunge to close green:** the dark
  stock chart, Dow −1,104 to 48,913.74 in the morning, then +164.25 to close
  +0.33% at 50,182.95 — the biggest intraday comeback since February 2022.
  S&P −0.25%, Nasdaq −0.62%, Brent $94.61 +3.51% (Jan settle).
- **Hero 2 — Tankers hit mines in Hormuz, then an LNG carrier burns:** a
  strait map with three burning tankers. Tagged CLAIMED — it is an IRGC
  claim, not a confirmed fact: 3–4 ships claimed in total, no vessel named,
  no independent verification. JMIC counted 7 tankers struck 16–22 Nov;
  the tally reached 10 before the 25 Nov claims.
- **Hero 3 — Lille stun Bayern as Roma end PSG's perfect record:** the full
  Matchday 5 scoreboard, all nine results (Lille 2-1 Bayern, PSG 2-2 Roma,
  Liverpool 3-0 Club Brugge, Barcelona 4-1 Sabah, and five more).
- **Cards 4–13:** Shenzhou-24 carries the first Pakistani to Tiangong,
  Trump's new tariffs on 14 partners (China 20%, Malaysia 18%), US GDP
  4.3% with core PCE 3.3%, the KOSPI −6.16% AI rout, the Saudi coalition
  bombing Hodeidah, Ukrainian drones torching two Samara refineries, the
  Israeli strikes that killed 5 in Gaza including North Gaza security chief
  Mohammad Abu al-Ouf, Nvidia −3.91% as Anthropic touches a record low,
  at least 30 killed in Niger State, and the Australia–Solomons security
  pact signed in Canberra (PM Matthew Wale, A$740m).
- **Also On Wednesday 25 November (14–35):** Iraq's top court backing
  Baghdad on the Kurdistan borders, the 2.3m Captagon seizure, judges
  recommending dropping Netanyahu's bribery case, Russian missiles hitting
  Kyiv, the 76 hostages freed in Cartagena, 31 killed in the Egypt fuel
  crash, three bodies found in the flooded Bogor mine, Italy edging South
  Korea in the Davis Cup, Mulder's 7/31 Test sweep, Tatum's 41 in the NBA
  Cup, Australia's Digital Duty of Care, the Phala Phala report quashed,
  the UN rights chief's warning, the Ebola evacuation in Congo, India's
  $1.2bn incentive package, the Mackenzie conviction, Senegal's 128–9
  resolution, the Iowa lead-azide detonation, the LUMA contract voided,
  Europe's markets down (DAX 24,702.13), and HP jumping 11.4% to $31.12.
- **DATE CHECK** lists the stories deliberately left out because they
  happened on another day (the Ghalibaf 7 conditions and the Nvidia −5.86%
  / KOSPI +6.32% / Nikkei +3.91% moves of 24 Nov, the RSF defector presser
  of 23 Nov, and more) and the items not yet happened (Thanksgiving, the
  F1 Qatar GP, the Fed decision, the Davis Cup semi).

## v2 (26 Nov 2026, ~10:45 WIB) — font + layout revision

The owner compared v1 with the feed's top 10 and found our typography and
layout well below theirs — including the descender of the "y" in
"Wednesday" touching the line below it. v2 fixes that and the other
defects found in visual QA, with no change to the facts or figures
(same 35 stories, same heroes, same strips, same DATE CHECK claims,
except the DATE CHECK box itself: four minor left-out items — Huawei
guilty, Senegal AFCON via CAS, UCL Tue games, Miss Universe final —
were dropped so the box fits at a readable size).

- **Fonts (the big change).** DejaVu Serif is gone as the display face.
  Masthead and headlines are now Playfair Display (high-contrast Didone
  display serif): masthead 900, hero headlines 800, card headlines 800.
  The subhead is Playfair Display Italic 700 in navy. All labels,
  kickers, timestamps, sources and index lines are Inter (clean
  grotesque sans), bold for kickers with letter-spacing. Body copy is
  Inter regular. Fonts are bundled in `fonts/` (PlayfairDisplay.ttf,
  PlayfairDisplay-Italic.ttf, Inter.ttf), subsetted to Latin +
  punctuation (— · − etc.), 240 KB total, so `draw.py` runs offline and
  deterministically; it loads them from `fonts/` next to the script.
- **The "y" overlap — root cause found.** v1 drew the date at y=34 in
  54pt DejaVu (ascender 59 + descender 14 = line box to y=107) and the
  subhead at y=90 — the descenders crossed the subhead by 17px. v2
  draws the date at y=32 in 52pt Playfair (line box to y=103) and the
  subhead at y=109, with 6px of clear air. Every headline was checked
  for descender clearance the same way.
- **Grid discipline, zero collisions (audit of v1's defects):**
  card 11's source line is now drawn after its dek instead of at a
  fixed y+130 (the old fixed offset is what made it collide); card 6's
  source ("CONFIRMED · BEA, DEPT. OF LABOR, WSJ") now fits on one line
  in narrower Inter, and its mini-chart labels sit above their own bars
  instead of crowding them; the DATE CHECK text now fits inside its
  red-bordered box at 8pt; map pin 13 (Canberra) is nudged off the
  right edge and pins 1/11 (New York) and 5/6 (Washington) are spread
  in different directions; the tariff mini's "15% EU/JP/KR/TW" line no
  longer spills out of its white stamp; the Nvidia mini text is 9pt
  bold instead of faint 8pt.
- **Two defects found in v2's own first render and fixed:** the Dow
  chart's plunge point ran through the score lines (the red line struck
  through the text) — the chart is now scaled to the top 70% of its
  box with a single score line below it; and the UCL scoreboard's third
  row fell below its green box, so its white text vanished on the
  paper — rows now start at y+16 with a 9px step and all nine results
  are visible.
- **Hierarchy (per the feed research):** giant Playfair date masthead →
  italic serif subhead → region/UTC strip (region counts ride on the
  UTC header line, right-aligned) → huge Playfair numerals in the
  IN NUMBERS strip → bold serif hero headlines → numbered scene
  headlines with red circled numbers → small Inter body + source →
  footer legend + DATE CHECK. At ~300px thumbnail size the masthead,
  the hero numerals and the red chips stay readable; body copy becomes
  texture, as in the top entries.
- **Size:** still 1024×1024 as in v1 (kit rule: at most 1 MiB and at
  most 1024×1024 px — a portrait canvas such as 819×1024 is permitted
  by that rule and is what the top feed uses, but v2 keeps the square
  format; portrait is recorded here as an option for a later revision).
  v2 entry.png is 231,848 bytes, deterministic (same sha256 twice),
  under the 1 MiB cap.
- **Kit check (local, `check --worktree`):** 4 passed
  (competition_open, snapshot, license_osi, entrypoint), 1 failed
  (transcripts_present — expected at build-only stage; the bundle is a
  submit-time step), 14 skipped, 5 checked at submission.
- **Files:** `entry-v1.png` is the v1 image, kept as a backup;
  `entry.png` is v2. `main.ts` is unchanged and was re-tested
  (copies entry.png byte-identical to `$MAKEFUN_OUTPUT_DIR`).
- **Remaining visual nits (honest):** the UTC header's region counts
  end very close to the right border ("S. AMERICA 1" hugs it); the
  economy mini's "Q2 3.4% / Q3 4.3%" labels are separated but tight;
  the UCL board's third-column result "SLAVIA 0-1 VILLARREAL" ends
  close to its panel edge; the Hormuz "3-4 CLAIMED" tag sits close to
  the centred "STRAIT OF HORMUZ" label; the footer has ~2px of slack
  to the border.

## v3 (26 Nov 2026, ~11:00 WIB) — portrait rebuild on the #1 reference

The owner sent a screenshot of the feed's #1 entry (@hwang-steven,
99.2%, "50 STORIES · 10 REGIONS · 21 FIELDS") and said v2 was "still
less neat than this". v3 rebuilds the layout on that reference, with
our own content (35 stories, 7 regions, 12 fields — never the
reference's 50/10/21).

- **Dimensions.** Portrait **819×1024**, verified against the kit's
  RULES.txt ("at most 1 MiB and at most 1024 by 1024 pixels") — both
  sides are within the cap, so portrait is allowed. Square was what
  forced everything cramped in v2: small heroes/scenes, minimal
  whitespace, a squeezed UTC strip and DATE CHECK.
- **Structure (reference order, our numbers):** navy top bar
  ("THE WORLD IN ONE DAY" + "35 STORIES · 7 REGIONS · 12 FIELDS ·
  ALL FIRST REPORTED ON WEDNESDAY 25 NOVEMBER 2026") → giant
  Playfair masthead → red italic subhead naming the three heroes →
  7 coloured region tabs with our counts (N. America 8, Africa 7,
  Middle East 7, Europe 6, Asia 4, Oceania 2, S. America 1) → IN
  NUMBERS strip of 5 (20% tariff, −6.16% Kospi, 1,100-pt Dow, 30
  Nigeria, 31 Egypt) → 3 large heroes → 10 scenes in 2 rows of 5 →
  map + ALSO ON list → red-bordered DATE CHECK → sources footer.
  No UTC strip in v3 (the reference has none; the Shenzhou/Hormuz
  times live in the deks instead). No fields line (no per-field
  counts exist in the v2 research — none invented).
- **Heroes rotated.** Hero 1 = tariffs (#5), hero 2 = Kospi (#7),
  hero 3 = Shenzhou (#4): they carry the strongest flat
  illustrations (container ship with an "UP TO 20%" badge, dark
  falling chip chart, Tiangong station over Earth) and the subhead
  can name all three. Dow (#1), Hormuz (#2) and UCL (#3) move to
  scenes 4–6 with strong illustrations of their own. Every hero has
  a verification pill (CONFIRMED) and a "WHY IT MATTERS" line.
  Nothing is dropped: heroes 1–3 + scenes 4–13 + ALSO 14–35 = all
  35 stories. Map pins are renumbered to match (1 tariffs, 2 Kospi,
  3 Shenzhou, 4 Dow, 5 Hormuz, 6 UCL, 7 GDP, 8 Hodeidah, 9 Samara,
  10 Gaza, 11 Nvidia, 12 Nigeria, 13 Solomon; Washington and New
  York pins are nudged apart where two stories share a city).
- **Two defects found in v3's own first renders and fixed:** the
  station's Earth ellipse was drawn wider than its column and spilled
  into the Kospi hero and over the headline (its box now ends exactly
  at the column edge, and the panels are brighter blue so the station
  reads against the dark space); and 10 of the 22 ALSO items measured
  wider than their 244px column (worst #33 at 278px, off the page) —
  their headlines were shortened to fit one 7pt line each, with a
  programmatic guard that shrinks any over-wide item to 6pt instead
  of letting it spill.
- **Fonts** stay Playfair Display + Inter from `fonts/`.
- **Size:** 819×1024 PNG, 213,111 bytes, deterministic (same sha256
  twice), under the 1 MiB cap. `main.ts` re-tested (byte-identical
  copy). Kit check (local, `check --worktree`): 4 passed
  (competition_open, snapshot, license_osi, entrypoint), 1 failed
  (transcripts_present — expected at build-only stage; the bundle is
  a submit-time step), 14 skipped, 5 checked at submission.
- **Files:** `entry-v2.png` is the v2 image, kept as a backup;
  `entry.png` is v3.

## v4 (26 Nov 2026, ~11:15 WIB) — font-overlap fix

The owner said "design oke tapi liat tuh font pada numpuk". A zoomed
QA pass over v3 (`/tmp/qa_v3/`, crops at 2x) showed the overlaps were
systemic, not one spot — and measuring the fonts found the root cause
in the code, not in the text.

- **Root cause (measured with PIL `getmetrics`).** v3 stepped
  multi-line text by `font.size + 1..3`, but a glyph's real line box
  is ascent+descent, which for Playfair is ~1.4x the size: Playfair
  20pt needs 28px and got 23px (5px overlap per line), Playfair 13pt
  needs 19px and got 14px, Inter 7pt needs 9px and got 8.5px (ALSO
  ON) / 9px (DATE CHECK). The 54pt masthead's box ends ~y113 while
  the subhead sat at a fixed y=106, so the 'y' in Wednesday touched
  it. New helper `line_step(fnt, extra)` = ascent+descent+extra is
  now used by every multi-line draw (`draw_wrapped`, `draw_lines`,
  WHY, source, ALSO, DATE CHECK, footer).
- **Layout is now measured, not assumed.** Heroes: the rule below
  them sits under the TALLEST hero card. Scenes: row 2 starts 10px
  (now 8px) below the TALLEST row-1 card. That kills the worst v3
  defect by construction — row-1 source lines ("CONFIRMED · UEFA"
  over the "11 · MARKETS · NEW YORK" kicker, "CONFIRMED · SPA, ARAB
  NEWS, ISW" over "13 · AUSTRALIA · CANBERRA", "CONFIRMED · BEA,
  DEPT. OF LABOR, WSJ" crowding "12 · NIGERIA · NIGER STATE") can
  no longer spill into the next row. The masthead/subhead, NUMBERS
  strip, map/ALSO, DATE CHECK and footer are likewise placed from
  measured heights, with a final-page assert (final y 1008 of 1024).
- **Headlines shortened to max 2 lines** (was 3): Dow "Dow erases
  1,100-point plunge", Hormuz "Tankers hit mines in Hormuz", UCL
  "Lille stun Bayern, Roma end PSG's record", GDP "US economy booms
  4.3% as inflation runs hot", Hodeidah "Saudi coalition bombs
  Hodeidah", Gaza "Israeli strikes kill 5 in Gaza", Nvidia "Nvidia
  -3.9% as Anthropic touches record low", Solomon "Australia and
  Solomons sign security pact", hero 3 "Pakistan's first astronaut
  docks at China's station". The dropped words all survive in the
  deks. Scene deks are capped at 2 lines. Headline leading is now
  1.15–1.25x (e.g. 12pt Playfair steps 19px) — descenders (g, y, p)
  clear the line below on every headline, verified visually per
  headline in the new crops.
- **Kospi hero chart:** the falling red line used to strike through
  "SAMSUNG -9.9%". The label block now paints its dark background
  over the chart line before the labels are drawn, so the line can
  never cross them.
- **NUMBERS strip:** captions shortened to one line each ("top
  proposed US tariff", "Kospi close, worst in AI rout", "Dow erases
  1,100-pt plunge") — v3's two-line captions touched the rule below.
- **ALSO ON / DATE CHECK:** step 8.5px → 10px (ALSO) and 9px → 11px
  (DATE CHECK) for 7pt Inter (9px line box); the DATE CHECK box
  height is computed from its line count.
- **Kicker guard (found in the v4 QA pass).** "12 · NIGERIA · NIGER
  STATE" measured 159px in a 153px column at 10pt/track-1, so it ran
  into the next column's kicker with only a 2px gap. Kickers now
  shrink tracking, then size, until they fit their column.
- **Ship badge (regression from the v4b illustration shrink).**
  Shrinking the hero illustrations 80 → 64px to reclaim page height
  left the r=28 badge (spans y+4..y+60) sitting on top of the
  "CHINA" hull label (y+42) — only the 'C' peeked out. Badge is now
  r=20 at cy=y+22 (bottom y+42) and EU/CHINA sit at y+44..y+57.
  Stocks mini ticker went 7pt → 6pt so its last '%' clears the box
  edge.
- **Page-height budget.** The honest leading added ~40px, reclaimed
  by: hero illustrations 80 → 64px, hero headlines 19 → 18pt, hero
  deks 11 → 10pt, masthead 52 → 50pt, subhead 14 → 13pt, map
  92 → 88px, tighter section gaps. Final y 1008 of 1024 (border
  at 1015).
- **Content unchanged.** Same 35 stories, heroes, strips, map and
  DATE CHECK as v3 — only wording lengths (headlines/deks shortened
  to fit) and layout changed. No facts or figures were altered.
- **Size:** 819×1024 PNG, 199,969 bytes (v4d), deterministic (same
  sha256 on two consecutive runs), under the 1 MiB cap. `main.ts`
  re-tested (byte-identical copy). Kit check (local,
  `check --worktree`): 4 passed (competition_open, snapshot,
  license_osi, entrypoint), 1 failed (transcripts_present — expected
  at build-only stage; the bundle is a submit-time step), 14 skipped,
  5 checked at submission.
- **Files:** `entry-v3.png` is the v3 image, kept as a backup;
  `entry.png` is v4. QA crops for v4 are in `/tmp/qa_v4/`
  (crop_top/heroes/scenes1/scenes2/bottom at 2x).
- **Remaining nits (honest).** (a) 8pt bold all-caps source/kicker
  lines show slightly uneven gaps inside some words ("REPOR TED",
  "UKRA NIAN") — that is the Inter bearings at tiny size: RAQM
  kerning was tried and measured byte-identical to the basic engine
  in this Pillow build, so there is no kerning to turn on; the words
  stay legible, and it is not an overlap. (b) Hero 3's station
  illustration is still the weakest of the three heroes. (c) The
  Hodeidah mini scene is sparse. (d) Small score text in the Dow
  mini (7pt) and UCL board (6pt) is only fully legible at full size;
  at ~300px thumbnail the masthead, IN NUMBERS figures and red chips
  carry the page, as in the reference.

## The files

- `entry.png` — the image itself (819×1024 PNG, 199,969 bytes in v4,
  under the 1 MiB cap; verified legible at full size and at ~300 px
  across — the date, the three heroes and the numbers strip stay
  readable).
- `entry-v3.png` — the v3 image, kept as a backup.
- `entry-v2.png` — the v2 image, kept as a backup.
- `entry-v1.png` — the v1 image, kept as a backup.
- `fonts/` — Playfair Display (roman + italic) and Inter, subsetted
  to Latin + punctuation, loaded by `draw.py` from this folder.
- `draw.py` — the script that draws `entry.png` (run it to regenerate
  it). Written from scratch for this day: no generic pictogram icons —
  every hero and card is a data scene or chart (a Dow comeback line with
  real closes, a strait map with three burning tankers, a nine-result
  scoreboard, a rocket, a tariff stamp, GDP bars, a falling KOSPI line)
  plus a rough equirectangular world map with numbered pins.
- `main.ts` — the entrypoint: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Build

```sh
python3 draw.py        # writes entry.png, deterministic (same sha256 twice)
```

`draw.py` uses only the Python standard library and Pillow, with the
bundled Playfair Display and Inter fonts in `fonts/` (subsetted Latin).
No network access, no randomness, no timestamps — re-running it
produces a byte-identical file.

## Why this entry differs from the 24 November entry

Same template, new day, new facts — and the v2 re-research applied. The
25 November stories were re-verified from primary sources in a second
pass (22 kept, 10 corrected, 3 dropped, 3 added), then audited a third
time for dates and numbers. Ambiguous claims were dropped rather than
guessed: the S&P CreditWatch claim on Nvidia is out, the Hormuz total is
written as "3–4 ships claimed" instead of a false precise 3, the 09:46
strip time became the verified 09:08, Brent is the verified $94.61 Jan
settle, and the Solomon Islands card was rewritten (Canberra, PM Matthew
Wale, A$740m, China pact lapsing April 2027 — not "cancelled").
