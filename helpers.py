"""Generation helpers: stream a page out of Claude, save it, preview it.

Usage from a notebook or REPL:

    from helpers import generate_html_with_claude
    from prompts import SYSTEM_PROMPT

    generate_html_with_claude(SYSTEM_PROMPT, "A single-page site for ...")

Requires ANTHROPIC_API_KEY in the environment.
"""

import html
import os
import re
import time
import webbrowser
from datetime import datetime
from pathlib import Path

from anthropic import Anthropic

from prompts import SYSTEM_PROMPT

# claude-opus-5 is the stronger option if pages aren't landing; override with
# ANTHROPIC_MODEL rather than editing this file.
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
MAX_TOKENS = 64000
OUTPUT_DIR = Path("html_outputs")

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


# --- notebook display, optional -------------------------------------------------

def _notebook_display():
    """Return (display, HTML) inside a Jupyter kernel, (None, None) anywhere else."""
    try:
        from IPython import get_ipython
        from IPython.display import HTML as DisplayHTML
        from IPython.display import display
    except ImportError:  # plain python, CLI
        return None, None
    shell = get_ipython()
    if shell is None or shell.__class__.__name__ != "ZMQInteractiveShell":
        return None, None  # terminal IPython or a script: stream to stdout instead
    return display, DisplayHTML


def _stream_panel(text, border="#c8102e"):
    escaped = html.escape(text)
    return f"""
    <div id="stream-container" style="border: 2px solid {border}; border-radius: 8px; padding: 16px; background: #f8f9fa; max-height: 500px; overflow-y: auto;">
        <pre style="margin: 0; font-family: monospace; font-size: 12px; color: #2d2d2d; white-space: pre-wrap; word-wrap: break-word;">{escaped}</pre>
    </div>
    <script>
        requestAnimationFrame(() => {{
            const container = document.getElementById('stream-container');
            if (container) {{ container.scrollTop = container.scrollHeight; }}
        }});
    </script>
    """


# --- core helpers ---------------------------------------------------------------


def save_html(html_content):
    """Write a page to html_outputs/<timestamp>.html and return the path."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = OUTPUT_DIR / f"{timestamp}.html"
    filepath.write_text(html_content, encoding="utf-8")
    return str(filepath)


def extract_html(text):
    """Pull the HTML document out of Claude's response.

    Prefers a fenced ```html block; falls back to any fenced block, then to a bare
    document if the model skipped the fence entirely. Returns None if nothing
    HTML-shaped is present.
    """
    fenced = re.findall(r"```(?:html)?\s*\n(.*?)```", text, re.DOTALL)
    if fenced:
        return max(fenced, key=len).strip()

    bare = re.search(r"(<!DOCTYPE html.*?</html>)", text, re.DOTALL | re.IGNORECASE)
    if bare:
        return bare.group(1).strip()

    return None


def open_in_browser(filepath):
    """Open a saved page in the default browser. No-op on headless machines."""
    abs_path = Path(filepath).resolve()
    try:
        opened = webbrowser.open(f"file://{abs_path}")
    except webbrowser.Error:
        opened = False
    if opened:
        print(f"🌐 Opened in browser: {filepath}")
    else:
        print(f"🌐 No browser available — open it manually: {abs_path}")


def generate_html_with_claude(system_prompt=SYSTEM_PROMPT, user_prompt=""):
    """Stream a page from Claude, save it, and preview it. Returns the file path."""
    if not user_prompt:
        raise ValueError("user_prompt is required — describe the page you want.")
    if not client.api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set.")

    print("🚀 Generating HTML…\n")

    full_response = ""
    start_time = time.time()
    display, DisplayHTML = _notebook_display()
    display_id = display(DisplayHTML(""), display_id=True) if display else None

    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "adaptive"},
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    ) as stream:
        for text in stream.text_stream:
            full_response += text
            if display_id:
                display_id.update(DisplayHTML(_stream_panel(full_response)))
            else:
                print(text, end="", flush=True)

    elapsed = time.time() - start_time
    if display_id:
        display_id.update(DisplayHTML(_stream_panel(full_response, border="#28a745")))
    print(f"\n✅ Complete in {elapsed:.1f}s\n")

    html_content = extract_html(full_response)
    if html_content is None:
        raw = save_html(full_response)
        print(f"❌ Could not extract HTML. Raw response saved to: {raw}")
        raise ValueError("Failed to extract HTML from Claude's response.")

    filepath = save_html(html_content)
    print(f"💾 HTML saved to: {filepath}")
    open_in_browser(filepath)

    return filepath
