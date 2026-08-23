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

<!-- Fill these in before generating. The more specific this is, the less generic the output. -->

- **Business:** The Venetian Company
- **Sector:** TBD
- **Location / market:** TBD
- **Audience:** TBD
- **Tone we're pitching:** TBD
- **Existing brand assets:** none known (no website)
- **Reference points / mood:** TBD

## Layout

```
CLAUDE.md            this file
prompts.py           DISTILLED_AESTHETICS_PROMPT — the system prompt for generation
helpers.py           Claude client + streaming generation + save/preview helpers
generate.py          CLI entry point: python generate.py "<brief>"
html_outputs/        timestamped generated pages (gitignored except .gitkeep)
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
- **Every page is self-contained.** One `.html` file — inline CSS, inline JS, no build
  step, no external asset hosts except Google Fonts. It has to open by double-click on a
  prospect's laptop.
- **Never overwrite a previous output.** Outputs are timestamped so we can compare
  directions side by side.
- **Don't invent facts about the client.** No fake testimonials, fake awards, fake
  addresses, fake founding dates, fake client logos. Use obviously-placeholder copy
  (e.g. "Est. —", lorem-adjacent but on-brand) or leave a `<!-- TODO -->`. This is going
  in front of the actual business owner; fabricated credentials are how a pitch dies.
- **Vary the direction between runs.** If the last output was a dark serif thing, the
  next one shouldn't be. Keep genuinely different directions to show as options.

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
