---
name: Kumpel & Hütte
description: A shared home for older people in the Ruhrgebiet, set like a kitchen table laid for one more guest.
colors:
  brick: "#a8432f"
  brick-deep: "#8e3524"
  ochre: "#d99a2b"
  ochre-ink: "#74501f"
  moss: "#4f6b3a"
  moss-deep: "#3b5230"
  linen: "#f3eadc"
  oat: "#e7dbc8"
  paper: "#fbf7f0"
  card: "#f7e8d4"
  oak: "#d8be97"
  line: "#d6c7b0"
  ink: "#2b221c"
  ink-soft: "#5a4a3e"
  coal: "#231c17"
  gold: "#b48c47"
typography:
  display:
    fontFamily: "Vollkorn, Vollkorn Fallback, Georgia, serif"
    fontSize: "clamp(1.95rem, 1.45rem + 2vw, 2.9rem)"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.005em"
  headline:
    fontFamily: "Vollkorn, Vollkorn Fallback, Georgia, serif"
    fontSize: "clamp(1.6rem, 1.3rem + 1.2vw, 2.1rem)"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.005em"
  title:
    fontFamily: "Vollkorn, Vollkorn Fallback, Georgia, serif"
    fontSize: "clamp(1.35rem, 1.2rem + 0.6vw, 1.6rem)"
    fontWeight: 700
    lineHeight: 1.25
  subtitle:
    fontFamily: "Vollkorn, Vollkorn Fallback, Georgia, serif"
    fontSize: "clamp(1.125rem, 1.05rem + 0.3vw, 1.25rem)"
    fontWeight: 700
    lineHeight: 1.3
  wordmark:
    fontFamily: "Vollkorn, Vollkorn Fallback, Georgia, serif"
    fontSize: "clamp(1.45rem, 1.1rem + 1.2vw, 1.8rem)"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Atkinson Next, Atkinson Fallback, Arial, sans-serif"
    fontSize: "clamp(1.125rem, 0.95rem + 0.4vw, 1.3125rem)"
    fontWeight: 400
    lineHeight: 1.6
    fontFeature: "lnum"
  lede:
    fontFamily: "Atkinson Next, Atkinson Fallback, Arial, sans-serif"
    fontSize: "clamp(1.125rem, 1.05rem + 0.3vw, 1.25rem)"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Atkinson Next, Atkinson Fallback, Arial, sans-serif"
    fontSize: "0.9rem"
    fontWeight: 700
    lineHeight: 1.45
  figures:
    fontFamily: "Atkinson Next, Atkinson Fallback, Arial, sans-serif"
    fontSize: "clamp(1.125rem, 1.05rem + 0.3vw, 1.25rem)"
    fontWeight: 400
    fontFeature: "tnum, lnum"
rounded:
  note: "3px"
  sm: "4px"
  md: "6px"
  frame-inner: "12px"
  lg: "18px"
  pill: "999px"
  arch: "12rem"
spacing:
  gutter: "max(1.25rem, 2.4vw)"
  measure: "36rem"
  header: "4.25rem"
  flow: "1em"
  section: "clamp(3rem, 7vw, 6.5rem)"
  section-joined: "clamp(1rem, 3vw, 2.5rem)"
  container: "76rem"
  container-medium: "56rem"
  tap-min: "2.75rem"
  control: "3rem"
components:
  button-primary:
    backgroundColor: "{colors.brick}"
    textColor: "{colors.paper}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "0.6em 1.25em"
    height: "3rem"
  button-primary-hover:
    backgroundColor: "{colors.brick-deep}"
    textColor: "{colors.paper}"
  button-quiet:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "0.6em 1.25em"
    height: "3rem"
  button-quiet-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  link-arrow:
    textColor: "{colors.ochre-ink}"
    height: "2.75rem"
  hero-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "1.05em 1.45em 1.2em"
  hero-caption:
    backgroundColor: "rgb(35 28 23 / 0.72)"
    textColor: "{colors.paper}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "0.2em 0.6em"
  price-note:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.figures}"
    rounded: "{rounded.note}"
    width: "min(100%, 30rem)"
  price-band:
    backgroundColor: "{colors.moss-deep}"
    textColor: "{colors.paper}"
  faq-item:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "0.85rem 1.25rem"
    height: "3.25rem"
  door-way:
    backgroundColor: "{colors.linen}"
    textColor: "{colors.ink}"
    rounded: "{rounded.arch}"
  door-band:
    backgroundColor: "{colors.brick}"
    textColor: "{colors.paper}"
  photo-frame:
    backgroundColor: "{colors.oak}"
    rounded: "{rounded.lg}"
    padding: "clamp(0.4rem, 0.8vw, 0.65rem)"
  jumplist-chip:
    backgroundColor: "{colors.oat}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0.4rem 1rem"
    height: "2.75rem"
  jumplist-chip-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  field:
    backgroundColor: "#ffffff"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "0.7rem 0.9rem"
    height: "3rem"
  callbar-call:
    backgroundColor: "{colors.brick}"
    textColor: "{colors.paper}"
    rounded: "{rounded.md}"
    height: "3rem"
  callbar-write:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    height: "3rem"
  consent:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "1.5rem"
  footer:
    backgroundColor: "{colors.coal}"
    textColor: "#e8dfd2"
---

# Design System: Kumpel & Hütte

## Overview

**Creative North Star: "Der gedeckte Küchentisch"**

Every page is a table set for one more guest. The ground is linen and oat, the surfaces are pale oak and paper, and the only strong colours are the ones a Ruhrgebiet kitchen already owns: a brick-red front door, the ochre of a miner's lamp, the moss of the garden outside. Photography of the real house leads; type and colour hold still around it. On the home page the photo is the room: the kitchen fills the first viewport edge to edge, the header sits over it, and the headline rests on a warm place-card set low on the table.

Density is low and deliberate. Body text starts at 18px and scales to 21px, lines stay near 36rem, and every control is at least 44px tall. The system is built for older eyes and for relatives reading on a phone, so legibility outranks ornament: the two faces are Vollkorn, a hearty book serif, and Atkinson Hyperlegible Next, a sans designed for low vision. Warmth comes from material metaphors carried in real CSS (an oak frame around photos, a ruled note for the price, an arched doorway for each way in), not from decoration layered on top.

The system refuses the category standard: no stock-smile hero, no trust badges, no three-icon card grid. Features are written as a ruled ledger. Proof is only shown when it is real: stock photos are captioned "Symbolbild", and unverified reviews never render.

**Key Characteristics:**
- Warm Scandinavian restraint on linen, grounded in Ruhrgebiet brick, ochre and moss.
- The real kitchen photo is the first viewport; the headline sits on a place-card.
- Every material metaphor is literal CSS: oak frames, a ruled price note, arched doors.
- Large type and targets (18px+ body, 44px+ controls), with states always drawn.
- Honest content: captions say what a photo shows, and only verified voices appear.

## Colors

A small household palette on warm paper: one colour to act, one to warm, one to reassure, and coal for text and ground.

### Primary
- **Door Brick** (brick): The colour of acting. Primary buttons, the call button in the header and the callbar, the closing "door" band at the foot of every page, FAQ chevrons, step numbers, list markers, the map pin, and the double rule under the price total. Also the browser `accent-color`.
- **Fired Brick** (brick-deep): Hover state for every brick control, and the default link colour on linen (6.6:1).

### Secondary
- **Lamp Ochre** (ochre): Warmth and emphasis, never text. Current-page underlines in the navigation, hover underlines on titles, round bullet markers, the quote attribution rule, text selection, and translucent tints behind totals (`rgb(217 154 43 / 0.14–0.35)`).
- **Lamp Ochre Ink** (ochre-ink): The text-safe ochre (6:1 on card and linen). Arrow links ("Besuch vereinbaren"), person roles, and the German opening quote mark.

### Tertiary
- **Garden Moss Deep** (moss-deep): The trust band. Full-bleed background for the quote section and the price section, with paper text (8:1).
- **Garden Moss** (moss): Used only as the faint ruling on the price note (`rgb(79 107 58 / 0.18)`).

### Neutral
- **Linen** (linen): The page ground, the header at rest, the mobile menu panel, and the face of each door arch. Also the `theme-color`.
- **Oat** (oat): The alternate section band, table heads, job headers, jumplist chips, and the "sill" under each door arch.
- **Paper** (paper): Raised surfaces: FAQ items, cards, the price note, forms, the callbar, desktop dropdowns. Text colour on every dark or brick ground.
- **Place-card** (card): Reserved for the home hero card that holds the headline over the photo.
- **Pale Oak** (oak): The frame around photos and the map, and the breadcrumb slash.
- **Pencil Line** (line): Hairlines and 1px ring borders around paper surfaces, ledger row rules, table rules.
- **Hearth Ink** (ink): All body text and headings (13:1 on linen); the focus ring; the ledger's top rule.
- **Soft Ink** (ink-soft): Secondary text: ledes, captions, answers, meta, field hints (7:1 on linen and card).
- **Coal** (coal): The footer ground and the tint of the hero-caption tab; behind the photo on wide screens.

### Brand
- **Hearth Gold** (gold): The logo colour and nothing else. The house-and-heart mark in the header and footer, and the favicon on a coal tile. Over the home photo the mark turns paper, like the wordmark beside it.

### Named Rules
**The One Job Rule.** Each strong colour has one job: brick means act, ochre means warmth and emphasis, moss means trust. Don't use brick for decoration or moss for a button.

**The Ink-Variant Rule.** Ochre never carries text. When ochre-family text is needed, use ochre-ink on light grounds, or the pale lamp tint `#f2c46d` on moss and coal (5.3:1 on moss-deep).

## Typography

**Display Font:** Vollkorn (with a metric-matched Georgia fallback)
**Body Font:** Atkinson Hyperlegible Next (with a metric-matched Arial fallback)

**Character:** A sturdy, warm book serif for anything spoken aloud (headings, the wordmark, the navigation on small screens, quotes, totals), paired with a sans built for low-vision readers for everything read closely. Both are self-hosted latin-subset variable fonts with `font-display: swap` and fallbacks tuned with `size-adjust` so the swap does not shift the layout.

### Hierarchy
- **Display** (700, `--step-4`, 1.15): Page `h1` titles, the contact-page heading and the door heading at the foot of each page.
- **Headline** (700, `--step-3`, 1.15): Section `h2`, home-card titles, the moss-band quote (600, 1.3), the price total figure.
- **Title** (700, `--step-2`, 1.25): `h3`, news titles, person names, door verbs ("Anrufen", "Schreiben", "Besuchen"), and navigation links in the mobile panel (600).
- **Subtitle** (700, `--step-1`, 1.3): `h4`, ledger row titles, FAQ group titles, facts titles.
- **Wordmark** (600, 500 at 80em and up): "Kumpel & Hütte" in Vollkorn, led by the house-and-heart mark (`partials/logo.html`, stroked in `currentColor`). In the header the tagline sits directly under the name, same face, about 0.58em, sentence case ("Gemeinsam statt einsam"; English: "Together instead of alone"). The mark centres on that two-line lockup. The footer keeps the tagline as its own line under the single-line wordmark.
- **Hero place-card headline** (700): Deliberately modest, `clamp(1.6rem, …, 1.75rem)` on phones and `1.32em` of the card's own fluid size on desktop, set on one line from 80em. The photo carries the scale, not the type.
- **Body** (400, 18–21px root, 1.6): All running text, with lining figures. Keep text columns at `--measure` (36rem).
- **Lede** (400, `--step-1`, Soft Ink): The paragraph under a page title or section head.
- **Relief line** (Vollkorn 500, `--step-2`, 1.5): The single serif paragraph right after the home photo.
- **Label** (700, `--step--1` = 0.9rem): Breadcrumbs, meta, table data labels, footer headings, captions (400). Always sentence case.
- **Figures** (tabular lining figures): Prices, sums, phone numbers, table cells.

### Named Rules
**The Sentence Case Rule.** No uppercase labels, no tracked-out small caps, no kickers above headings. The only positive tracking in the system is 0.04em on the two-letter language switch ("EN").

**The Honest Sum Rule.** Anywhere money appears, set tabular lining figures so the lines add up like a sum on paper (570 + 200 + 200 = 970).

## Layout

The page is a vertical stack of full-width "bricks" (sections) inside a 76rem container with a fluid gutter (`max(1.25rem, 2.4vw)`); medium content narrows to 56rem and prose to one 36rem column. Long-form prose uses a named grid (full / wide / content) so tables, galleries and photos can step 8rem wider than the text column without breaking the measure.

Rhythm: sections pad `clamp(3rem, 7vw, 6.5rem)` top and bottom. Two plain sections in a row collapse the gap between them to `clamp(1rem, 3vw, 2.5rem)`, so a run of related content reads as one room. Coloured bands (oat, moss quote, moss prices) always keep full padding. Inside flows, siblings sit 1em apart; headings in prose get 2em above and 0.6em below.

Every page ends the same way: the brick door band with three arched ways in (call, write, visit), then the coal footer.

Breakpoints: 40em shows the mail icon in the header; 48em moves the hero card onto the photo, shows the door ways in three columns, and hides the mobile callbar; 56em opens two-column splits, the ledger and the price layout; 64em adds the house page's sticky aside; 80em swaps the menu button for the one-row navigation. On short landscape screens (`max-height: 30em`) the callbar hides and the header stops being sticky.

Responsive specifics:
- **Home hero, phones:** the photo is `min(68svh, 34rem)` tall and the place-card overlaps its bottom edge by 3.5rem, inset by the gutter.
- **Home hero, 48em and up:** the photo fills `max(min(100svh, 56.25vw), 34rem)` on a coal ground; the card sits absolutely at lower left, 44–46% wide.
- **Mobile callbar:** a fixed paper bar at the bottom of every page with "Anrufen" (brick, 1.4fr) and "Schreiben" (outlined, 1fr); the body reserves 4rem plus the safe-area inset for it.
- **Tables under 48em** become stacked cards with each cell labelled from its column head.
- Text scales with the root size, so layouts reflow cleanly at 200% zoom (the 80em navigation falls back to the menu panel).

## Elevation & Depth

Depth is physical and sparing: things that are set down on the table cast a soft, low shadow; everything else is flat paper edged with a 1px Pencil Line ring (`box-shadow: 0 0 0 1px var(--line)`). Shadows are always warm (tinted from ink or coal), long and diffuse with a negative spread, never hard-edged. Two objects are also tilted slightly to feel placed by hand: the price note (-1.2deg) and photos in split layouts (±0.8deg from 56em).

### Shadow Vocabulary
- **Place-card** (`0 24px 50px -24px rgb(24 14 8 / 0.55), 0 2px 6px rgb(24 14 8 / 0.12)`): The home hero card on the photo.
- **Pinned note** (`0 30px 50px -28px rgb(0 0 0 / 0.6), 0 2px 4px rgb(0 0 0 / 0.15)`): The price note on the moss band.
- **Hung frame** (`0 22px 40px -26px rgb(43 34 28 / 0.55)`): Oak photo frames.
- **Paper ring** (`0 0 0 1px var(--line)`): FAQ items, cards, tables, facts, job posts, map card.
- **Header lifted** (`0 1px 0 var(--line), 0 8px 24px -16px rgb(43 34 28 / 0.35)`): The sticky header once the page scrolls.
- **Dropdown** (`0 18px 40px -18px rgb(43 34 28 / 0.45), 0 0 0 1px var(--line)`): Desktop sub-navigation.
- **Callbar** (`0 -1px 0 var(--line), 0 -10px 24px -18px rgb(43 34 28 / 0.5)`): The mobile call bar.
- **Door sill** (`inset 0 -6px 0 var(--oat)`, ochre on hover): The step at the foot of each door arch.

### Named Rules
**The Set-Down Rule.** Only objects placed on a surface (the place-card, the price note, framed photos, the open dropdown) get a cast shadow. Everything else is flat paper with a hairline ring.

**The Scrim Rule.** Text over photography always sits under a scrim tuned to 4.5:1 or better: the hero photo carries a top gradient from `rgb(24 14 8 / 0.7)` under the header, fading to clear by 34%, and the header text adds a soft shadow while it floats over the photo.

## Shapes

Corners are gently softened, like worn furniture: 6px on buttons, fields and paper surfaces; 4px on small tabs (hero caption, desktop dropdown items, the price share box); 3px on the paper price note. Photos sit in a Pale Oak frame with 18px outer corners and the image radius reduced to follow the inner edge (12px in the gallery and map). The two round forms are the pill (jumplist chips) and the circle (icon buttons, step numbers, bullet dots). The signature silhouette is the arch: each "way in" at the foot of the page is a doorway with a 12rem rounded top and 6px bottom corners.

Icons are an authored line set on a 24px grid with a 2px round stroke (phone, mail, house, arrow, chevron, menu, close, pin, clock, globe, calendar), drawn in `currentColor` at 1.25em.

## Components

### Buttons
Warm and solid, like a painted door: one strong colour, a firm edge, no gloss.
- **Shape:** Gently rounded (6px), 2px border in the fill colour, at least 48px tall.
- **Primary:** Door Brick fill with paper text, 700 weight, `0.6em 1.25em` padding, icon then label with a 0.55em gap. The call button spells out the phone number ("Anrufen: 0160 90889269").
- **Hover / Focus:** Fill and border darken to Fired Brick over 0.2s. Focus is the global ring (see Navigation).
- **Quiet:** Transparent with a `currentColor` border and ink text; on hover it fills with ink and turns paper. In the hero card the quiet button drops its border and becomes an ochre-ink arrow link.
- **Arrow link:** Ochre-ink, 700, min 44px tall, with a trailing arrow that slides 0.2em right on hover while an underline appears.

### Cards / Containers
- **Corner Style:** 6px.
- **Background:** Paper on linen or oat grounds; the hero card alone uses the place-card colour.
- **Shadow Strategy:** Paper ring by default; cast shadows only per the Set-Down Rule.
- **Border:** None; the 1px ring is a box-shadow so it never shifts layout.
- **Internal Padding:** `clamp(1.25rem, 3vw, 2.25rem)` for sections and facts, `clamp(1.5rem, 3vw, 2.5rem)` for forms and job posts.

### Inputs / Fields
- **Style:** White fill, 2px warm-grey border (`#8f7d6b`, 3.9:1 against white), 6px corners, min 48px tall, `0.7rem 0.9rem` padding. Labels sit above in 700; the "required" hint is Soft Ink at label size. Textareas start at 9rem and resize vertically. Checkboxes are 1.4rem.
- **Focus:** The border turns ink, plus the global focus ring.

### Navigation
- **Wide screens (80em and up):** One calm row of Vollkorn links (500, min 18px) separated by centred middle dots (`·`, 70% opacity, hidden from screen readers). The current section gets a 3px ochre underline offset 0.35em; hover draws a 2px underline. Items with children open a paper dropdown with sans sublinks (600), where hover fills with linen. The language switch is a two-letter "EN"/"DE". A mail icon button and the brick "Anrufen" button close the row.
- **Small screens:** The mark and wordmark, a mail icon from 40em, and an outlined "Menü" button (2px `currentColor` border, 48px tall). Below 30em the wordmark scales down so it clears the menu button, and the tagline stays directly under the name at about 0.6em, sized to the width of "Kumpel & Hütte". The menu opens a full linen panel under the header with large Vollkorn links (`--step-2`), group names as quiet sans labels, and the phone, email and office hours at the bottom. Escape closes it and returns focus.
- **Over the home photo:** The header is transparent with paper text until the page scrolls, then becomes linen with the lifted shadow.
- **Focus (global):** A 3px ink outline offset 3px with a 6px linen halo; on photo, brick and coal grounds the outline turns paper and the halo takes the ground colour. Current page, open answers and focus are always drawn, never implied by colour alone.

### Home Hero ("the photo is the room")
The real kitchen photo fills the first viewport with the header over it. The headline "Nicht Heim. Nicht allein. Einfach Zuhause!" sits on the place-card at lower left with a short lede, the brick call button and the "Besuch vereinbaren" arrow link. The card settles into place once (0.9s, rising 14px, `cubic-bezier(0.16, 1, 0.3, 1)`) only when motion is allowed. A caption saying what the photo shows sits on a translucent coal tab at lower right.

### Photo Frame
Photos hang in a Pale Oak frame (18px corners, `clamp(0.4rem, 0.8vw, 0.65rem)` padding, hung-frame shadow) with an oat placeholder behind the image. Captions sit below in Soft Ink at label size, and every stock photo is captioned "Symbolbild".

### Ledger
Features as a ruled list, never icon cards: a 2px ink rule on top, 1px Pencil Line rules between rows, a Vollkorn subtitle and Soft Ink text in each row, two columns from 56em.

### Price Note
The published price, pinned like a note on the fridge. A paper card (3px corners, pinned-note shadow, -1.2deg tilt) with faint moss ruling every 2.2rem sits on the moss-deep band. It holds a table of line items with tabular figures, a 2px ink rule above the total, the total in Vollkorn at `--step-3` underlined with a 5px double brick rule, and a translucent ochre box for the personal share.

### FAQ
Paper items with the ring, built on native `details`/`summary`. The summary is 700, at least 52px tall, with a brick chevron drawn by `clip-path` that turns 180° when open; hover turns the question Fired Brick. Answers are Soft Ink.

### Door (closing band)
Every page ends on a brick band with a display-size paper heading and three linen "ways" shaped as arches (12rem top radius): a brick line icon, a Vollkorn verb, the detail (number, email, address) in tabular 700, and a Soft Ink note. On hover a way lifts 4px and its oat sill turns ochre; the lift is dropped under reduced motion.

### Mobile Callbar
A fixed paper bar on screens under 48em: the brick "Anrufen" button and an ink-outlined "Schreiben" button, both 48px tall, so phone and email are always one tap away. Hidden while the menu or the consent banner is open.

### Consent Banner
One plain question about statistics, asked once and never as a modal. Under 64em it is a paper sheet fixed to the foot of the screen with the callbar shadow; from 64em it becomes a paper card at the lower right with the dropdown shadow, clear of the home place-card. A Vollkorn title, the notice at caption size with a link to the privacy policy, and two quiet buttons of identical size and style ("Zustimmen", "Ablehnen"), because rejecting must be as easy as accepting. While it is open the footer grows by the banner's height so nothing ends up underneath it. "Cookie-Einstellungen" in the footer and in the privacy policy reopens it with the current choice stated.

### Jumplist Chips and Numbered Steps
In-page jump links are oat pills (min 44px) that fill with ink on hover. Move-in steps are an ordered list with 2.3rem brick circles carrying the number in Vollkorn.

## Do's and Don'ts

### Do:
- **Do** let the real photo lead: full-bleed on the home page, oak-framed everywhere else, with a caption that says what it shows ("Symbolbild" for stock).
- **Do** keep body text at the 18px-plus root size, text columns near 36rem, and every tap target at least 44px (48px for primary controls).
- **Do** use brick only for actions and the closing door, ochre for underlines and emphasis, moss-deep for the trust bands.
- **Do** put text over photography under a scrim that reaches 4.5:1 or better.
- **Do** set prices and phone numbers in tabular lining figures, and keep the price note as the one place the sum is shown.
- **Do** draw every state: ochre underline for the current page, rotated chevron for an open answer, the ink-and-linen ring for focus.
- **Do** wrap motion in `prefers-reduced-motion`; motion is one settle on arrival and small hover nudges, nothing else.
- **Do** end every page with the door band and keep the mobile callbar on small screens.

### Don't:
- **Don't** build the category standard: no stock-smile hero, no trust badges, no three-icon feature cards. Use the ledger.
- **Don't** show testimonials, reviews or quotes that are not verified; the reviews section renders nothing without verified entries.
- **Don't** add uppercase labels, tracked small caps or kickers above headings.
- **Don't** set text in plain ochre; use ochre-ink or the pale lamp tint on dark grounds.
- **Don't** cast shadows on flat content, or use hard offset drop shadows; paper surfaces get the 1px ring. The only zero-blur shadow is the inset door sill.
- **Don't** use icon fonts or glyph icons; use the authored 2px line icons.
- **Don't** load third-party scripts or fonts; both faces are self-hosted and the site ships one fingerprinted stylesheet. The one exception is Google Tag Manager, and only after a visitor agrees in the consent banner.
