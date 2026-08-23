# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repo is

A portfolio/pitch workspace. The goal is to generate a **speculative sample website for
The Venetian Company** — a prospect that currently has no web presence — so we have
something concrete to show them before reaching out.

Nothing here is a live client deliverable yet. Treat every generated page as a pitch
asset: it has to look like it was designed on purpose, by a person, for this specific
business.

## Client brief

Everything below is taken from the client's own public Instagram
(@thevenetiancompany_ profile and their About Us / Pricing story highlights).
**Nothing here is inferred — do not add to this list without a source.**

- **Business:** The Venetian Company — "The Venetian Company - Venetian Plastering"
- **Sector:** Venetian plaster & microcement. Listed on IG as "Product/service",
  bio "VENETIAN PLASTER/MICROCEMENT — A team of finishing specialists covering all
  aspects"
- **Contact:** Adam Knowles — 07527180499
- **Instagram:** [@thevenetiancompany_](https://instagram.com/thevenetiancompany_)
  (228 posts, ~2.9k followers)
- **Partner:** tiling via [@sktiling](https://instagram.com/sktiling)
- **Services (verbatim from their About Us highlight):** full house applications,
  media walls, bathrooms, swimming pool areas, feature walls, microcement,
  staircases, wet rooms, floors — "and more"
- **About (verbatim):** "The Venetian Company are a team of experienced professionals
  skilled in luxury Venetian plastering. We have experience creating unique and
  sophisticated designs to suit a variety of homes or commercial spaces." … "We are a
  friendly, customer-focused business with a passion for bringing your dream home to
  reality."
- **Pricing process (verbatim from their Pricing highlight):** pricing depends on the
  size of the area and desired finish/style; quoted after initial discussions and
  agreed before commencing; alternative finishes offered to suit a budget; up to 2
  samples included, additional samples £80; 50% deposit before commencing, balance due
  on completion.
- **Enquiry channel:** direct message or **WhatsApp** — "please direct message or
  contact us via the WhatsApp below". WhatsApp is the primary route, not email.
- **What they ask an enquirer to send (verbatim from their Enquiries highlight):**
  address of project · photographs of the area · measurements (if available) · your
  desired finish or style. Plus: "Please feel free to send your inspiration photos to
  our team to support in understanding your vision. We are experienced specialists who
  will help in providing guidance for a finish that best suits your requirements."
  And: "Photographs of the area will also support our team to provide a price based on
  size."
- **Site visits (verbatim):** "Once we have agreed your finish, colour and other
  requirements, samples can be provided as part of your package. We are also able to
  visit the area to discuss before going ahead." Note *colour* is agreed alongside
  finish, and a booking date is "mutually agreed" before the deposit is taken.
- **Deposit T&Cs (verbatim from their Deposits highlight):** "a 50% deposit is required
  to secure all project bookings before going ahead. This allows our team to purchase
  the required materials and products for your individual project. This deposit is
  non-refundable. The remaining balance will be due upon completion of the project."
- **Audience:** homeowners doing high-end renovations and new builds, plus commercial
  spaces. Their feed is contemporary architectural — flat-roofed new builds, pool
  areas, curved plaster staircases, wet rooms.
- **Tone we're pitching:** material-led and quiet. Luxury trade, not luxury brochure.
  The finish is the product, so the page should feel like the surface.
- **Service area:** nationwide (confirmed).
- **Studio credit:** pages carry "Designed by YSBDesigns" in the footer.
- **Existing brand assets:** the TVC monogram — a thin black ring with the T, V and
  C **interlocked down a shared axis**, the T's stem running into the V and the V's
  point into the C. They are not three stacked letters with gaps; the first pass got
  that wrong and set them as separate `<text>` baselines. Adam supplied the artwork,
  and `site/src/components/Monogram.astro` is a **trace of it** (upscaled 4x,
  thresholded, potrace; 98.7% IoU against the original, 9007 ink pixels to 9008).
  The outlines are drawn, so there is no font dependency and the mark inherits
  `currentColor`. Do not tidy the curves — the small asymmetries are in his mark.
  All-caps tracked typography across their story graphics. No website.

### Written from general knowledge, not from them — needs Adam's sign-off

The "Plaster or cement?" band describes how the two materials behave (lime + marble
dust burnished in coats; cement + polymer laid a few mm thick over existing surfaces,
seamless, hard-wearing). That is general material fact, **not** taken from anything the
client has published. It is the one section on the page not sourced from their own
words, so Adam should read it before the page goes anywhere near a customer — if he
works differently, it is wrong in his voice.

### Reference the client's competitor sets

[micro-cementuk.co.uk](https://micro-cementuk.co.uk/) — Manchester microcement firm,
used as a structural reference. Runs Home / About / **What is Microcement** / Our Work /
**Commercial Projects** / Contact / Order / Pay in 3, and describes work "from
residential and commercial projects, to retail spaces such as bars, restaurants, and
more recently gyms". Two ideas taken from it: a materials explainer, and splitting
residential from commercial. Nothing else — we are not copying their copy or layout.

### Network: what this environment cannot reach

The egress proxy returns 403 for both `instagram.com` and `micro-cementuk.co.uk`. So:

- **Instagram cannot be scraped from here.** Client media has to be sent into the chat
  as attachments. That has worked well — keep doing it. Don't promise a scrape.
- Competitor sites may need `WebSearch` (which works) rather than `WebFetch`.

### Unknowns — do NOT invent these

Trading address, service area/radius, years established, company registration, team
size, accreditations, testimonials, review scores, past client names, project
locations, prices beyond the £80 sample fee. **Which commercial sectors they have
worked in** — the competitor names bars, restaurants and gyms; we have no evidence
The Venetian Company has done any of those, so the commercial band stays text-only
until Adam supplies commercial jobs. Leave a `<!-- TODO -->` and ask.

## Current design direction

The first pass was warm cream + a Didone display + terracotta — which is on Anthropic's
own list of clustered AI looks. It was replaced, and the replacement was **sampled from
the client's own photography** rather than picked: quantising their walls returns
near-neutral greys (h0–60, s7–8, l41–63), and the only chroma anywhere on their feed is
the **teal in the marbled staircase (h180)**. So:

- Ground `#E8E9E7` cool screed · `#DBDDDB` · `#C7CAC8`, stone `#A8ACAA`
- Ink `#14181A` blue-black · soft `#333A3D` · muted `#4B5457`
- Accent `#12504F` petrol on light, `#35948F` on dark — from their own marbled wall
- Display/UI: **Archivo** variable at `wdth 125` (expanded architectural caps).
  Prose: **Newsreader**. No Didone, no Jost.

Every muted-on-ground pair was solved for ≥4.5:1 before the palette was applied, not
after. If you change a token, re-run the contrast check — `--ink-mute` on `--paper-3`
is the tight one (4.7:1).

### Two directions, one source

Both are drawn from the same photographs, read two different ways — which is the
argument to make in the room, not "here are two palettes".

| | A — Daylight | B — After hours |
|---|---|---|
| Sampled from | the walls, in daylight | the room, under tungsten |
| Ground | `#E8E9E7` cool screed | `#14120F` warm near-black |
| Accent | `#12504F` petrol, from the marbled wall | `#C79A63` brass, from their fittings (`#D8A878` sampled) |
| Display | Archivo `wdth 125`, uppercase | Newsreader 200, lowercase |
| Labels | Archivo tracked caps | Courier Prime, spec-sheet annotation |
| Thesis | the surface is the product | you judge a finish by taking a light to it |
| Signature | the daylight plate — the wordmark set *inside* a full-bleed photograph, washed toward the ground colour rather than dimmed | the raking light pass |

#### The hero plate (replaces the arch)

The arch is gone. The hero is now one full-bleed photograph
(`hero-courtyard.jpg`) with the wordmark sitting in it, and the thing that
keeps it from being the same hero every agency ships is that **the scrim is
paper, not black**. Everyone else dims the building and sets white type on it;
this washes toward `#E8E9E7` and keeps the ink palette, so the hero still
belongs to Direction A rather than to Direction B.

**The scrim stops are solved, not eyeballed.** Compositing alpha *a* of paper
(sRGB .910) over an image pixel *v* gives `a*.910 + (1-a)*v`. The image has
near-black glazing in it, so the worst case is *v* ≈ 0:

| text | colour | needs | over black needs |
|---|---|---|---|
| `.label` eyebrow, scroll cue | `--color-ink-mute` | 4.5:1 | a ≥ .81 |
| lede | `--color-ink-soft` | 4.5:1 | a ≥ .69 |
| wordmark (large text) | `--color-ink` | 3:1 | a ≥ .44 |

So the small copy lives in the dense end of the ramp and the display type runs
out into the clear end. Verified by rendering the hero, hiding the copy layer,
and sampling the actual composited pixels under every glyph run: **16 viewport
sizes from 320×568 to 1920×1080, worst pixel of every string, minimum ratio
5.07**. Re-run `site/scripts/check-contrast.py` if you touch the stops or the image.

**Mobile stops are in pixels, not percentages.** The copy block is a fixed
height — it ends between 514px and 558px from the top at every phone width —
while the hero is `100svh`. A percentage ramp tuned on a 812px screen left the
scroll cue sitting in open photograph on a 640px one. Pixels track the copy;
percentages track the window. From `md` the copy becomes a centred left column
and the wash becomes a radial anchored on it, which opens the right of the
frame back up.

**The source is only 712×612.** It is upscaled ~2× at 1440 and more on a
retina screen. The wash hides much of that, and the `.grain` layer hides more,
but a higher-resolution original is needed before this goes in front of Adam.

### Type scale

Strict modular scale, defined in `site/src/styles/global.css` under `@theme`.
Ratio **1.25** (major third) from an 18px base at the 1440 anchor, compressed to
**1.14** from 16px at 360 so display steps still fit a phone. Every clamp is the
straight line between those two anchors.

| step | name | 360px | 1440px | line-height | tracking |
|---|---|---|---|---|---|
| −2 | label | 11.5px | 11.5px | 1.45 | +.22em |
| −1 | caption | 14.4px | 14.4px | 1.55 | +.005em |
| 0 | body | 16.0px | 18.0px | 1.70 | 0 |
| 1 | lede | 18.2px | 22.5px | 1.45 | −.005em |
| 2 | h4 | 20.8px | 28.1px | 1.25 | −.012em |
| 3 | h3 | 23.7px | 35.2px | 1.15 | −.016em |
| 6 | h2 | 35.1px | 68.7px | 1.02 | −.022em |
| 9 | h1 | 52.0px | 134.1px | 0.94 | −.028em |

**Steps 4, 5, 7 and 8 are deliberately unused.** That hole between h3 and h1 is
what makes the display read as large rather than merely big. Do not fill it —
if something seems to need step 4, it wants h3 or h2.

Line-height falls as size rises; tracking runs monotonically from +.22em on the
label to −.028em on h1. Each token carries **all three** values
(`--text-h2`, `--text-h2--line-height`, `--text-h2--letter-spacing`), so a
utility cannot pick up a size without its leading and tracking. Add sizes by
adding a step, never with an arbitrary `text-[…]`.

**label and caption are fixed, not fluid.** Interpolating them produced a clamp
whose min exceeded its max — small text wants to be relatively *larger* on a
phone — and CSS silently resolves that to the min, discarding the max. UI text
at that size is a constant.

Two justified off-scale values, both documented in place: `.endmark` (a mark
measured against the viewport, `15.6vw`) and the hero's "The" (`.26em` of h1 —
a lockup keeps its ratio at every size).

**One cap, which is not a third exception.** `.wordmark` sets
`font-size: min(var(--text-h1), calc((100vw - 2 * var(--spacing-gutter)) / 6.44))`.
h1 is still the scale step; the `min()` only stops it exceeding what the column
can carry. The floor at the 360 anchor (52.03px) stops the type shrinking while
the column keeps shrinking, so on a phone "COMPANY" ran past the gutter and the
`overflow:hidden` mask each hero word sits in shaved the last glyph — 5px over
at 375, 13px at 360, 53px at 320. The divisor is measured: in Archivo `wdth 125`
at h1 tracking, "COMPANY" sets 6.40× its own font-size, and 6.44 leaves margin.
Above ~388px the scale is already the smaller of the two, so nothing changes
there or on desktop (h1 is still exactly 134.1px at 1440). The rule is
**unlayered on purpose** — `text-h1` is a utility, and Tailwind's utilities
layer beats `@layer components` regardless of specificity.

### Rhythm and motion

`--spacing-section: clamp(6rem, 13.5vw, 12.5rem)` (~194px at 1440) and
`--spacing-head: clamp(3.25rem, 7.5vw, 6rem)`, taken from the BAMO and Olivia
Harper references.

The outer rhythm is settled — section seams run 258–389px at 1440 and nothing
there is cramped. What was cramped was **inside** sections: closing notes and
credits sitting 24–36px under the blocks they belong to. Those were audited by
measuring the rendered page and doubled. Don't tighten them back:

| where | was | now |
|---|---|---|
| index → "and more" note | 36px | 72px |
| feature figure → plates grid | 56px | 112px |
| plates grid → photo credit | 24px | 48px |
| quotes → placeholder flag | 28px | 56px |
| contact h2 → phone number | 24px | 48px |
| phone number → CTA | 40px | 80px |
| CallBand row gap (stacked) | 24px | 48px |

The 20px between an eyebrow and its heading is a **lockup**, not a gap — it
matches `SectionHead`'s `mb-5` and should stay tight. **Motion was re-specced** to subtle / 200–300ms / nothing bounces, which
supersedes the earlier "unhurried, don't speed these up" note taken from the
references. That older rule is gone — do not reinstate it from the reference
screenshots.

- One curve for all interaction motion: `--ease-motion: cubic-bezier(.33,1,.68,1)`
  (easeOutCubic). Both control-point y values are ≤ 1, so it decelerates into
  place and **cannot overshoot**. Anything with y > 1 — `back.out`, spring
  curves — bounces and is banned.
- `--duration-reveal: 280ms`, `--duration-hover: 240ms`. Every transition and
  entrance sits in the 200–300ms band; verified against the live document.
- Scroll reveals travel **14px**, not 34px. A long throw at 280ms reads as a
  jerk — short travel is what makes a fast reveal feel subtle.
- Stagger step is 40ms, so a nine-child group finishes in ~600ms.

One ambient loop is deliberately outside the band because it is neither a
reveal nor a hover: the hero scroll `cue` (3.4s). It is a slow drift, not an
interaction. The arch light `sweep` (22s) was the other one; it went with the
arch, and its keyframe was deleted rather than left orphaned.


## Stack and brief

| | |
|---|---|
| Audience | a trader charging upwards of £1,500 a project — the page has to carry that price |
| The one action | book a call. One CTA, repeated, never a menu of asks |
| Quality bar | the BAMO and Olivia Harper references: scale, rhythm, motion |
| Stack | Astro + Tailwind v4, static output, no CMS, Cloudflare Pages |
| Banned | purple gradients · emoji as icons · Inter as display · stock-photo placeholders · centred-everything |

The ban list was already satisfied when it arrived — fonts are Archivo/Newsreader, every
image is the client's own, there is no `text-align:center` anywhere, and the only "Inter"
matches in the source are `IntersectionObserver`. Keep it that way.

**One conflict, reconciled rather than ignored.** Adam's own published intake is
"direct message or WhatsApp" with address, photographs, measurements and desired finish.
A call-first CTA cuts across that. So the CTA books a call and opens WhatsApp with the
request pre-written, and his four items became "worth having ready for the call" —
step 01 of the process is now the call. Both things stay true.

## Layout

```
site/                the site — Astro + Tailwind, deploys to Cloudflare Pages
  src/data/site.ts     every client-supplied fact, one file, no CMS
  src/components/      BookCall.astro is the one CTA, used six times
  scripts/             check-contrast.py — samples the real composited pixels
                       under the hero copy; run it if you touch the plate
  public/assets/       canonical home for the client's photography and film
  public/_headers      Cloudflare cache policy
CLAUDE.md            this file
prompts.py           DISTILLED_AESTHETICS_PROMPT — the system prompt for generation
helpers.py           Claude client + streaming generation + save/preview helpers
generate.py          CLI entry point: python generate.py "<brief>"
html_outputs/        timestamped generated pages (gitignored except .gitkeep)
samples/             pages we've kept and are willing to show
  venetian-company/index.html    Direction A — "Daylight": cool screed, Archivo
                                 expanded caps, petrol accent. This is the one
                                 deployed to gh-pages.
  venetian-company-b/index.html  Direction B — "After hours": warm near-black,
                                 lowercase Newsreader, brass accent, raking-light
                                 signature. Comparison option, not deployed.
                                 Its assets/ is a symlink to Direction A's.
  venetian-company/assets/       the client's own photography and film (see CREDITS.md)
  venetian-company/build-artifact.py  strips the wrapper, inlines media, for Artifacts
  venetian-company/build-site.py      builds dist/ — a clean standalone site for hosting
dist/                built site, gitignored
```

## How to generate a page

```bash
export ANTHROPIC_API_KEY=sk-ant-...
pip install -r requirements.txt
python generate.py "A single-page site for The Venetian Company — ..."
```

Or from a notebook / REPL:

```python
from helpers import generate_html_with_claude
from prompts import DISTILLED_AESTHETICS_PROMPT

generate_html_with_claude(DISTILLED_AESTHETICS_PROMPT, "A single-page site for ...")
```

`generate_html_with_claude` streams the response, extracts the HTML from the fenced code
block, writes it to `html_outputs/<timestamp>.html`, and opens it in a browser when one
is available.

## Working rules

- **Always pass `DISTILLED_AESTHETICS_PROMPT` as the system prompt** when generating a
  page. It exists to keep output off the "AI slop" attractor; skipping it defeats the
  point of the whole repo.
- **The site is an Astro app** (`site/`), not a single file. The old one-file rule was
  superseded by an explicit stack directive — Astro + Tailwind, static, no CMS, deployed
  to Cloudflare Pages. `samples/` keeps the two single-file directions as archives; they
  still open by double-click and symlink into `site/public/assets` for media.
- **One action, repeated.** Every call-to-action on the site is
  `src/components/BookCall.astro` — same words, same destination. Six instances, one
  href. Do not add a second competing ask.
  **Never hide it with a passed class.** `BookCall`'s own `base` sets
  `inline-flex`, and Tailwind v4 emits `.inline-flex` *after* `.hidden` in the
  same layer, so `class="hidden md:…"` silently loses — that is how the nav CTA
  ended up rendering at 375px, wrapping to two lines and pushing the header to
  104px. Wrap the component in an element that carries the display utility
  (`<span class="hidden md:contents">`) instead.
- **Never overwrite a previous output.** Outputs are timestamped so we can compare
  directions side by side.
- **Deploying to Pages.** `python samples/venetian-company/build-site.py` rebuilds
  `dist/`, then push it to the orphan `gh-pages` branch — that branch holds the built
  site only, one plain commit, no repo furniture. Never merge `gh-pages` into anything
  or merge anything into it.
- **Two ways to publish, and they leak different things.** `build-artifact.py` makes
  a private Artifact — no repo, no history, but a claude.ai URL. `build-site.py` makes
  `dist/` for GitHub Pages — a neutral URL, but Pages exposes the repo behind it, and
  **this repo is public and contains CLAUDE.md plus Claude co-author trailers on every
  commit.** Serving Pages from here hands anyone who reads the URL a route straight to
  that. For a Pages URL with nothing to trace, push `dist/` to a separate repo with its
  own clean history. `index.html` stays the source of truth for both.
- **Reviews must be real.** The page has a review section built and visibly marked
  `PLACEHOLDER`. Do not fill it in. Three quotes with first name + area have to come
  from Adam's actual customers.
- **Client media is the client's.** Anything under `assets/` came off their Instagram
  and is theirs. Credit it, keep `CREDITS.md` current, and pull it if the pitch dies.
- **Don't invent facts about the client.** No fake testimonials, fake awards, fake
  addresses, fake founding dates, fake client logos. Use obviously-placeholder copy
  (e.g. "Est. —", lorem-adjacent but on-brand) or leave a `<!-- TODO -->`. This is going
  in front of the actual business owner; fabricated credentials are how a pitch dies.
- **Vary the direction between runs.** If the last output was a dark serif thing, the
  next one shouldn't be. Keep genuinely different directions to show as options.

## Installed skills

Two design skills are vendored into `.claude/skills/` so they travel with the repo —
this environment is ephemeral, so a user-level install at `~/.claude/skills/` would not
survive the container.

| Skill | Source | Licence |
|---|---|---|
| `frontend-design` | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | see its `LICENSE.txt` |
| `ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) v2.13.0 | MIT |

`ui-ux-pro-max` ships a searchable local dataset and a CLI:

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<brief>" --domain typography
# domains: style color chart landing product ux typography icons gsap react web google-fonts
python3 .claude/skills/ui-ux-pro-max/scripts/design_system.py --help
```

Its `scripts/tests/` were dropped on install (the skill's own CI, not ours). Scanned
before installing: no network calls, no `subprocess`/`eval`/`exec`, no writes outside
its own directory.

**These do not replace `DISTILLED_AESTHETICS_PROMPT`** — that is still the system prompt
for generation. Treat the skills as reference material during hand-editing.

## The aesthetics system prompt

The canonical copy lives in `prompts.py` as `DISTILLED_AESTHETICS_PROMPT`. Reproduced
here so it's readable without opening the code:

```text
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight. Focus on:

Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.

Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.

Motion: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.

Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:
	- Overused font families (Inter, Roboto, Arial, system fonts)
	- Clichéd color schemes (particularly purple gradients on white backgrounds)
	- Predictable layouts and component patterns
	- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!
</frontend_aesthetics>
```

## Model

`helpers.py` reads the model from the `ANTHROPIC_MODEL` env var, defaulting to
`claude-sonnet-4-6`. `claude-opus-5` is the stronger option if the sample pages aren't
landing.
