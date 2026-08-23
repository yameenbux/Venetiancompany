> **Read `docs/project-brief.md` first.** It holds the client's own words — the
> verbatim services, pricing, deposit and enquiry copy taken off their Instagram,
> plus the do-not-invent list. The proxy blocks Instagram, so none of it can be
> re-fetched. This file used to contain it; it was moved out, not deleted.
>
> **One version only.** The "After hours" alternative has been removed. We propose
> a single design; the customer is not being asked to choose.

# BAMO — "Our Projects" Page Teardown

**URL:** https://bamo.com/our-projects/
**Studio:** BAMO, Inc. — interior design collective (hospitality, F&B, private residential)
**Site credit:** SDCO Partners
**Captured:** 23 August 2026 — three screenshots plus a 28-second screen recording (iPad Safari, 2732×2048 landscape)

> Source note: the live page blocks automated fetching, so everything below is read off the supplied media. Static structure comes from the screenshots; all motion and interaction notes come from frame-by-frame extraction of the recording. Anything still not observable is flagged as **[unknown]**.

---

## 1. Page structure (top to bottom)

| # | Section | Background | Purpose |
|---|---------|-----------|---------|
| 1 | Sticky header | Transparent over hero | Menu toggle / wordmark / "Work" link |
| 2 | Hero | Full-bleed photograph | Page title + scroll cue |
| 3 | Intro statement | Cream (#FAF6EF-ish) | Positioning headline + supporting paragraph |
| 4 | Project grid | Cream | 3-column card grid, paginated |
| 5 | Our Clients | Terracotta (#D9503C-ish) | Accordion lists of client names |
| 6 | CTA band | Full-bleed photo, dark overlay | "Start Your Project" → Contact |
| 7 | Footer | Cream | Tagline, five office addresses, newsletter, legal |
| 8 | Oversized wordmark | Cream | Giant "BAMO" as a closing graphic device |
| — | Filter drawer | Terracotta | Right-anchored overlay panel, five taxonomies (see §5b) |

---

## 2. Header

- **Left:** hamburger icon (three short stacked rules, unequal widths — not a generic burger). Becomes an **X** when the overlay is open.
- **Centre:** `BAMO` wordmark, high-contrast serif, wide letterspacing. Renders dark over the light hero — implies either mix-blend-mode or a per-page colour token.
- **Right:** `WORK` — single uppercase, letterspaced text link. This is the only persistent nav item outside the overlay.
- Header sits *over* the hero image, no background fill.

### Nav overlay (screenshot 1)

- Full-viewport terracotta panel.
- Background carries large, soft, abstract organic shapes in a slightly darker tint of the same red — very low contrast, almost a watermark. Reads as flowing fabric or a torso/limb abstraction.
- Nav items laid out **horizontally in a single row**, vertically centred, evenly distributed:
  `Our Projects` · `Our Process` · `Our Studio` · `News & Press` · `Connect`
- Type: large display serif (~48–56px equivalent), near-black on terracotta.
- `WORK` persists top-right; close X top-left in the same position as the burger.
- **Animation (observed):** the entire panel — background, shapes and nav items together — **cross-fades in at full-viewport scale over roughly 0.5s**. It does not slide, wipe, or expand from the burger. Mid-transition frames show the red at partial opacity with the hero photograph still legible underneath and the nav labels already ghosted in at the same opacity.
- **No stagger.** All five items resolve simultaneously. A staggered reveal is the obvious thing to reach for here and they deliberately didn't — it keeps the moment quiet rather than showy.
- In motion the red reads noticeably **hotter and more saturated** than in the static screenshot — closer to a vivid red-orange than the muted terracotta the still suggests. Treat the still as colour-shifted.
- **[unknown]** hover states on the nav items, phone-width stacking behaviour.

---

## 3. Hero

**The hero is a slideshow, not a single image** — the screenshots hide this entirely.

- **Behaviour:** full-bleed photographs **cross-fade** into one another. Each image holds roughly 5 seconds, with a dissolve of roughly 0.8–1 second. Mid-transition frames show both images superimposed at ~50% — a straight opacity dissolve, no Ken Burns zoom, no slide, no pan.
- **Images observed in 28 seconds (2 — the loop may be longer):**
  1. Rooftop terrace at golden hour — timber slatted screen, pergola, parasol, clipped hedging, infinity-edge water, high-rise towers and river beyond. Almost certainly Capella Bangkok.
  2. Estate at dusk — low timber cabins with lit windows, long reflecting pool, decked terrace with black Adirondack chairs, ornamental grasses, redwoods behind. Reads as one of the Napa projects.
- **The title does not move or re-render between slides.** "Our Projects" and the arrow sit in a fixed layer above the image stack. Only the photography changes.
- **Title:** large display serif, white, bottom-left, generous left margin.
- **Scroll cue:** thin downward arrow to the right of the title, roughly optically centred on the viewport.
- No overlay scrim; the images' own sky gradients do the contrast work, and both selected images place their darkest area (planting/foreground) exactly where the title sits. That is a photo-selection constraint, not a CSS one — worth noting if you copy this pattern with images you don't control.
- On scroll the hero moves up out of frame conventionally; no pinning or parallax detected at 1fps sampling. **[unknown]** whether a subtle parallax exists below that threshold.

---

## 4. Intro statement

- **Headline (2 lines, display serif, dark brown/near-black):** a statement about immersive spaces that stir the senses, invite exploration and spark emotion.
- **Body paragraph (small sans, ~3 lines, constrained to ~half viewport width):** positions the work as global — spanning time zones, markets and mediums — and lists the range as everything from small pied-à-terres and superyachts through to workplaces and award-winning resorts.
- Left-aligned, sits in the left ~60% of the column. Large whitespace to the right — deliberate asymmetry, no right-hand column.

---

## 5. Project grid

**Layout:** 3 columns × 3 rows visible = 9 cards. Equal-width columns, consistent gutters, landscape (~4:3) image crops.

**Card anatomy (top to bottom):**
1. Image
2. Thin hairline rule
3. Category eyebrow — uppercase, small, letterspaced, muted grey. Can list multiple categories comma-separated.
4. Project title — serif, sentence case, dark.

**The nine visible projects:**

| Category | Project |
|----------|---------|
| Food & Beverage | Beaulieu Vineyard |
| Hotels | The Bellevue Hotel |
| Food & Beverage | Robert Mondavi Winery |
| Branded Residences, Hotels | Napa First Street Hotel & Residences |
| Private Residential | Kips Bay Show House \| Palm Beach 2026 |
| Food & Beverage, Hotels | Capella Bangkok |
| Hotels | Passalacqua |
| Private Residential | Atherton Residence |
| Private Residential | Providence Residence |

**Pagination:** centred `LOAD MORE` link in terracotta, with `9 of 52` beneath it in small grey type. So the full archive is 52 projects, loaded 9 at a time.

**Category taxonomy observed on cards:** Hotels · Private Residential · Food & Beverage · Branded Residences.

---

## 5b. Filter drawer

Confirmed by the recording — invisible in all three screenshots.

- A **terracotta panel anchored to the right edge** of the viewport, sitting below the header (the `WORK` link stays visible above it).
- **Vertical `FILTER` label** rotated 90° on the panel's left edge, small uppercase letterspaced type.
- **Five filter taxonomies**, stacked vertically, display serif, sentence case, left-aligned within the panel:
  1. Market Sector
  2. Region
  3. Environment
  4. Style
  5. Project Type
- Beneath them, a small **outlined `CLEAR ALL FILTERS` button** — thin 1px border, uppercase letterspaced micro-type. Its presence implies each taxonomy expands into a multi-select.
- The panel occupies roughly the right quarter of the viewport width and runs full height below the header.

**Why this matters:** the card categories are only a *display* of one taxonomy (Market Sector). The real filtering model is five-dimensional — sector, geography, indoor/outdoor environment, aesthetic style, and project type. That's a far more considered content model than the grid lets on, and it's what makes 52 projects navigable rather than a wall.

**[unknown]** the trigger. The drawer was caught mid-animation during a page transition rather than opened deliberately, so I can't tell whether it's a fixed tab on the right edge, a control that appears on scroll, or an item inside the header. The individual values under each taxonomy are also unseen.

---

## 6. Our Clients

- Full-width terracotta band — the strongest colour moment on the page, and the same red as the nav overlay. Ties the two together.
- **Heading:** "Our Clients", centred, display serif, dark.
- **Accordion, two rows**, each with a hairline rule and a +/− indicator on the right:
  - `Brands` — **expanded** (− icon)
  - `Owners & Developers` — **collapsed** (+ icon) — **[unknown]** contents

**Brands list** — 3 columns, alphabetised *across* rows (col1 → col2 → col3, then next row), small type, dark on terracotta:

| | | |
|---|---|---|
| Auberge Collection | Autograph Collection Hotels | Capella Hotels & Resorts |
| Conrad Hotels Resorts | Curio Collection by Hilton | Exclusive Resorts |
| Fairmont Hotels & Resorts | Four Seasons Hotels & Resorts | Halekulani Hotel |
| JW Marriott Hotels & Resorts | Mandarin Oriental Hotel Group | Park Hyatt Hotels |
| Ritz-Carlton Hotel Company | Rosewood Hotels & Resorts | Solis Hotels |
| St. Regis Hotels & Resorts | Taj Hotels | The Peninsula Hotels |
| The Ritz-Carlton Reserve | Waldorf-Astoria Hotels & Resorts | Westin Hotels & Resorts |

21 brands. Plain text, no logos — a deliberate choice: it reads as a credential list rather than a logo wall, and sidesteps the visual mess of mismatched brand marks.

---

## 7. CTA band

- Full-bleed photograph of a studio/office interior: floor-to-ceiling windows, desk with lamp and books, materials, a vase of dark red flowers, a large "B" graphic on the far wall.
- Dark scrim over the image for legibility.
- **Heading:** "Start Your Project" — display serif, white, centred.
- **Sub:** two lines about creating something extraordinary together.
- **Button:** `CONTACT US` — uppercase, letterspaced, small, likely a text link or ghost button.

---

## 8. Footer

- **Left:** "A collective of interior designers." — two lines, display serif, dark. This is the brand's positioning line, given the most typographic weight in the footer.
- Beneath it: `© 2026 BAMO, Inc. | Privacy Policy` and `Site by SDCO Partners`.
- **Office columns** (uppercase city label + address, small sans):

| San Francisco | Providence | Miami | New York City | Barcelona |
|---|---|---|---|---|
| 1000 Brannan Street, Suite 300, San Francisco, CA 94103 | 1 Park Row, Suite 401, Providence, RI 02903 | 3350 Virginia Street, 2nd Floor, Miami, FL 33133 | 195 Chrystie Street, 303D, New York, NY 10002 | Premià de Mar, Barcelona, Spain |

- **Connect column:** `info@bamo.com`, `Careers`, plus a row of social icons — Instagram, LinkedIn, YouTube, Facebook, and one more (Vimeo or Behance).
- **Newsletter:** `NEWSLETTER` label, full-width underline input with placeholder "Email Address", right-aligned arrow submit. Minimal — no box, just a rule.
- **Closing graphic:** enormous `BAMO` wordmark spanning the full viewport width, cropped at the bottom edge. Faint ghost shapes behind it echo the nav overlay's organic forms.

---

## 9. Design system notes

**Colour**
- Cream / warm off-white — primary background
- Terracotta / burnt coral — single accent, used for the clients band, the nav overlay, and the `LOAD MORE` link. Used sparingly and at full strength rather than diluted everywhere.
- Near-black warm brown — body and display text
- White — text over imagery only

**Type**
- One high-contrast display serif for all headings, project titles, nav, and the wordmark. Large sizes, tight-ish leading.
- One small sans for body copy, eyebrows, addresses, and UI labels — always uppercase and letterspaced when used as a label.
- Two typefaces total. That restraint is doing most of the work.

**Layout**
- Wide margins, heavy whitespace, left-aligned asymmetric text blocks.
- Hairline rules as the only separator device — no cards, no shadows, no borders around images.
- Full-bleed photography alternating with quiet cream sections; the rhythm is image → quiet → image → colour → image → quiet.

**Motion (observed in the recording)**

| Moment | Behaviour | Approx. duration |
|---|---|---|
| Hero slideshow | Opacity cross-fade between full-bleed photos, fixed title layer | ~5s hold, ~1s dissolve |
| Nav overlay open | Full-viewport opacity fade of panel + items together, no stagger | ~0.5s |
| Nav overlay close | Same fade in reverse | ~0.5s |
| Page navigation | Solid-colour curtain covers the viewport, then lifts to reveal the new page | ~1.5–2s total |
| Filter drawer | Right-anchored panel translates in/out horizontally | <0.5s |

**The page transition is the most distinctive move on the site.** Clicking a nav item does *not* fade the overlay back to the old page and then load the new one. Instead the terracotta overlay cross-fades directly into a **solid warm sand/taupe curtain** — a third colour, roughly `#D9CBB8`, noticeably duller and browner than the cream page background — which fills the entire viewport for around 1.5–2 seconds while the next page assembles behind it. The curtain then clears and the new hero is already in place.

Three deliberate choices in that:
- The curtain colour is *not* the page background. Using a distinct tone makes the transition read as an intentional interstitial rather than a page that failed to paint.
- It runs long enough to fully mask load and layout shift. Nothing ever janks into place on this site because you're never allowed to watch it happen.
- Red → sand → photograph gives the navigation a three-beat rhythm. It is slow by web standards and that slowness is the point: it borrows the pacing of a printed monograph.

**Other interaction**
- Overlay nav rather than an inline menu — keeps the header to three elements.
- Progressive loading with an explicit count (`9 of 52`) instead of infinite scroll.
- Accordion for long client lists; five-taxonomy filter drawer for the archive.
- **[unknown]** hover treatments on project cards, scroll-reveal animation on the grid.

---

## 10. What's worth stealing

1. **One accent colour, used loudly.** The terracotta appears in exactly three places and carries the entire brand personality. Most portfolios dilute an accent across a dozen small elements and it stops meaning anything.
2. **The `9 of 52` counter.** It signals depth of work without forcing the visitor to scroll through all of it. A portfolio with three case studies obviously can't use this — but the underlying move (make your volume of work legible) is worth thinking about.
3. **Client list as plain text, not logos.** Cheaper to build, easier to maintain, and it avoids the "logo wall of two clients" problem.
4. **The oversized wordmark footer.** Costs nothing, ends the page with confidence.
5. **Category eyebrow above project title.** Two lines of metadata do the work of a filter UI you may not need yet.
6. **The coloured page-transition curtain.** Cheap to implement, and it buys you cover for every load delay and layout shift on the site. This is the single most portable idea here — it works at three projects exactly as well as at fifty-two.
7. **Restraint in the overlay animation.** No stagger, no slide, no easing theatrics. One opacity fade. Most portfolio sites over-animate their nav because it's the easiest place to show off.

---

## 11. Gaps in this document

- Remaining 43 projects (only the first 9 load without interaction)
- Contents of the "Owners & Developers" accordion
- The values inside each of the five filter taxonomies, and how the drawer is triggered
- Hover treatments on project cards; any scroll-reveal on the grid
- Individual project detail page structure
- Whether the hero slideshow runs to more than two images
- Exact hex values, typeface names, and breakpoint behaviour — none of which can be read off a screenshot or a recording

> Everything in this last list except the project archive itself is answerable in about ten minutes with DevTools open on the live site. The recording was worth extracting; it is still no substitute for inspecting the thing.
