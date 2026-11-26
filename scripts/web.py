#!/usr/bin/env python3
"""Draw the project web: Artificial Intelligence in the middle, a hemisphere each side, its groups around it, with how many projects each holds (docs/web-light.svg, docs/web-dark.svg), and the README
links table, which names every project.

The project list below is the only source: edit it, then run `python3 scripts/web.py`.
Each project is (label, url). The label is what the web shows, not necessarily the repo name:
several notebook repos (say mathematics-notebooks, machine-learning-notebooks) are each just
"notebooks", and their group says which kind. A url means public: the table links it; None
means private (label only). A group with no projects is shown as "coming soon".
"""
import math
import re
from pathlib import Path

GH = "https://github.com/"
DEVELOPMENT = {
    "Entrepreneurship": [("fiona", None), ("portico", None)],
    "Bureaucracy": [("diplomatic-vat-refund", None), ("relationship-evidence-toolkit", None),
                    ("university-hunt", None)],
    "Tools": [("claude-toolkit", None), ("deep-uninstall-engine", None), ("format-to-format", None),
              ("local-engine-for-notes-and-search", None),
              ("networked-encrypted-storage-terminal", None), ("open-safe", None),
              ("personal-linux-setup", None), ("project-backlog", GH + "ntfifwyb/project-backlog"),
              ("screen-lighting-control", GH + "verticillum/screen-lighting-control"),
              ("torrent-getter", None), ("voice-home-control", None)],
    "Anki": [(n, GH + "prsnlanki/" + n) for n in
             ("anki-setup", "deutsch", "english", "espanol", "esperanto", "mathematics", "ink",
              "psittacus")],
    "Games": [("ituzaingostudio", GH + "ituzaingostudio"), ("karai-pyhare", None),
              ("godot-game-template", None), ("ps2-kit", None),
              ("van-buren-van-buren-and-van-buren", None)],
    "Pedagogy": [("adaptive-instructional-method", None),
                 ("freeCodeCamp", GH + "ntfifwyb/freeCodeCamp"),
                 ("higher-dimensions", GH + "instructional-pages/higher-dimensions"),
                 ("quantum-zeno-effect", GH + "instructional-pages/quantum-zeno-effect")],
    "Optimization": [("nfsh", GH + "cmprssd/nfsh"), ("swjkja", GH + "cmprssd/swjkja")],
    "Cybersecurity": [],
}
RESEARCH = {
    "Machine Learning": [("notebooks", None)],
    "Mathematics": [],
}
HEMISPHERES = [("Development", DEVELOPMENT, -1), ("Research", RESEARCH, 1)]

THEMES = {
    "light": dict(ink="#1f2328", mute="#59636e", line="#d1d9e0"),
    "dark": dict(ink="#f0f6fc", mute="#9198a1", line="#3d444d"),
}
def f(v):
    return f"{v:.1f}"


def width(text, size):
    """Rough rendered width of text: good enough to crop the canvas and leave room."""
    return len(text) * size * 0.56


CX, CY = 0, 0  # the centre; the canvas is cropped to the drawing afterwards
CORE = ("Artificial", "Intelligence")  # the centre, one word per line
CORE_HW = width(max(CORE, key=len), 18) / 2  # half its width, where the lines start
HUB = CORE_HW + 110  # from the centre to each hemisphere's label
R = 210  # groups sit on an arc of this radius, so each hemisphere is round
PITCH = 46  # vertical distance between groups
SOON = "coming soon"
PAD = 20


def count(projects):
    return f"{len(projects)} project{'s' * (len(projects) != 1)}" if projects else SOON


def draw(t):
    lines, texts, xs, ys = [], [], [], []
    anchor = {-1: "end", 1: "start"}
    for name, groups, side in HEMISPHERES:
        hx, hw = CX + side * HUB, width(name, 18) / 2 + 6
        lines.append(f'<path d="M{f(CX + side * CORE_HW)} {f(CY)}H{f(hx - side * hw)}"/>')
        texts.append(f'<text class="h" x="{f(hx)}" y="{f(CY)}">{name}</text>')
        n = len(groups)
        for i, (group, projects) in enumerate(groups.items()):
            y = CY + (i - (n - 1) / 2) * PITCH
            x = hx + side * (hw + 40 + 0.75 * R * math.sqrt(max(0, 1 - ((y - CY) / (R * 1.05)) ** 2)))
            lines.append(f'<path d="M{f(hx + side * hw)} {f(CY)}L{f(x)} {f(y)}"/>')
            tx = x + side * 12
            texts.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="3"/>'
                         f'<text class="g" x="{f(tx)}" y="{f(y - 8)}" text-anchor="{anchor[side]}">{group}</text>'
                         f'<text class="c" x="{f(tx)}" y="{f(y + 10)}" text-anchor="{anchor[side]}">{count(projects)}</text>')
            xs.append(tx + side * width(group, 15))
            ys += [y - 18, y + 20]
    x0, x1 = min(xs) - PAD, max(xs) + PAD
    # centre the middle on the canvas, so the empty half reads as room to grow
    half = max(CX - x0, x1 - CX)
    y0, y1 = min(ys) - PAD, max(ys) + PAD
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f(CX - half)} {f(y0)} {f(2 * half)} {f(y1 - y0)}" role="img" aria-label="Project groups in two hemispheres around artificial intelligence: development and research" font-family="system-ui,-apple-system,'Segoe UI',sans-serif" font-size="14">
<style>text{{fill:{t['mute']};dominant-baseline:central}}.h,.g{{fill:{t['ink']};font-weight:600}}.h{{font-size:18px;text-anchor:middle}}.g{{font-size:15px}}.c{{font-size:12px}}.a{{fill:{t['ink']};font-weight:700;font-size:18px;text-anchor:middle}}circle{{fill:{t['mute']}}}path{{stroke:{t['line']};fill:none}}</style>
{chr(10).join(lines + texts)}
<text class="a" x="{f(CX)}" y="{f(CY - 11)}">{CORE[0]}</text><text class="a" x="{f(CX)}" y="{f(CY + 11)}">{CORE[1]}</text>
</svg>
"""


def table():
    rows = ["| Group | Projects |", "|---|---|"]
    for _, groups, _ in HEMISPHERES:
        for g, projects in groups.items():
            if projects:
                rows.append(f"| **{g}** | " + " · ".join(f"[{n}]({u})" if u else n for n, u in projects) + " |")
    return "\n".join(rows)


def main():
    root = Path(__file__).resolve().parent.parent
    for theme, colours in THEMES.items():
        (root / f"docs/web-{theme}.svg").write_text(draw(colours))
    readme = root / "README.md"
    text, n = re.subn(r"(<!-- links -->\n)(?:.*?\n)?(<!-- /links -->)",
                      lambda m: m[1] + table() + "\n" + m[2], readme.read_text(), flags=re.S)
    assert n == 1, "README needs <!-- links --> and <!-- /links --> markers"
    readme.write_text(text)


if __name__ == "__main__":
    main()
