# Venetian Company — pitch sample

Speculative sample website generator for The Venetian Company, a prospect with no
current web presence. Generates self-contained, deliberately non-generic HTML pages we
can show them before reaching out.

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Generate

```bash
python generate.py "A single-page site for The Venetian Company. Hero, what we do, selected work, contact."
```

Pages land in `html_outputs/<timestamp>.html` — timestamped, never overwritten, so
different design directions can be compared side by side.

From a notebook:

```python
from helpers import generate_html_with_claude
from prompts import SYSTEM_PROMPT

generate_html_with_claude(SYSTEM_PROMPT, "A single-page site for ...")
```

See [CLAUDE.md](CLAUDE.md) for the brief, the working rules, and the aesthetics system
prompt.
