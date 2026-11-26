#!/usr/bin/env python3
"""Draw the project web (docs/web-light.svg, docs/web-dark.svg) and the README links table.

The project list below is the only source: edit it, then run `python3 scripts/web.py`.
A project with a URL is public and gets a link in the table; None means private (name only).
A group with no projects is shown as "coming soon".
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
    "AI research": [("notebooks", None)],
    "Mathematics": [],
}
HEMISPHERES = [("Development", DEVELOPMENT, -1), ("Research", RESEARCH, 1)]

THEMES = {
    "light": dict(ink="#1f2328", mute="#59636e", line="#d1d9e0", core="#000", ring="#000"),
    "dark": dict(ink="#f0f6fc", mute="#9198a1", line="#3d444d", core="#000", ring="#656c76"),
}
W, H = 1100, 960
CX, CY = W / 2, H / 2
RX, RY = 230, 440  # projects sit on an ellipse around their hemisphere's label
PITCH = 2 * RY * 0.86 / 42  # row spacing; the fullest hemisphere fills the height
HUB = 120  # distance from AI to each hemisphere's label
SOON = "coming soon"


def f(v):
    return f"{v:.1f}"


def width(text, size):
    return len(text) * size * 0.56


def exit_point(gx, gy, hw, px, py, hh=12):
    """Where the line from a label's centre towards (px, py) leaves the label's box."""
    dx, dy = px - gx, py - gy
    t = min(hw / abs(dx) if dx else 1e9, hh / abs(dy) if dy else 1e9)
    return f"{f(gx + dx * t)} {f(gy + dy * t)}"


def draw(t):
    lines, texts = [], []
    for name, groups, side in HEMISPHERES:
        hx, hw = CX + side * HUB, width(name, 18) / 2 + 8
        lines.append(f'<path d="M{f(CX + side * 34)} {f(CY)}L{exit_point(hx, CY, hw, CX, CY)}"/>')
        texts.append(f'<text class="h" x="{f(hx)}" y="{f(CY)}">{name}</text>')
        leaves = {g: [n for n, _ in p] or [SOON] for g, p in groups.items()}
        rows = sum(map(len, leaves.values())) + len(leaves) - 1
        y = CY - (rows - 1) * PITCH / 2
        for group, names in leaves.items():
            ys = [y + i * PITCH for i in range(len(names))]
            y += (len(names) + 1) * PITCH
            pts = [(hx + side * RX * math.sqrt(max(0, 1 - ((v - CY) / RY) ** 2)), v) for v in ys]
            my = sum(ys) / len(ys)
            mx = sum(x for x, _ in pts) / len(pts)
            gy = CY + (my - CY) * 0.82
            gx = hx + side * RX * 0.5 * math.sqrt(max(0, 1 - ((gy - CY) / (RY * 0.8)) ** 2)) + side * 30
            gw = width(group, 15) / 2 + 8
            lines.append(f'<path d="M{exit_point(hx, CY, hw, gx, gy)}L{exit_point(gx, gy, gw, hx, CY)}"/>')
            texts.append(f'<text class="g" x="{f(gx)}" y="{f(gy)}">{group}</text>')
            anchor = "start" if side > 0 else "end"
            for (x, py), n in zip(pts, names):
                lines.append(f'<path d="M{exit_point(gx, gy, gw, x, py)}L{f(x)} {f(py)}"/>')
                cls = ' class="s"' if n == SOON else ""
                texts.append(f'<circle cx="{f(x)}" cy="{f(py)}" r="2.5"/>'
                             f'<text{cls} x="{f(x + side * 10)}" y="{f(py)}" text-anchor="{anchor}">{n}</text>')
    x0 = CX - HUB - RX - 10 - max(width(n, 14) for g in DEVELOPMENT.values() for n, _ in g) - 12
    x1 = CX + HUB + RX * 0.9 + 10 + max([width(n, 14) for g in RESEARCH.values() for n, _ in g] + [width(SOON, 14)]) + 12
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f(x0)} 50 {f(x1 - x0)} {H - 100}" role="img" aria-label="Projects in two hemispheres around AI: development and research" font-family="system-ui,-apple-system,'Segoe UI',sans-serif" font-size="14">
<style>text{{fill:{t['mute']};dominant-baseline:central}}.h,.g{{fill:{t['ink']};text-anchor:middle;font-weight:600}}.h{{font-size:18px}}.g{{font-size:15px}}.s{{font-style:italic}}circle{{fill:{t['mute']}}}path{{stroke:{t['line']};fill:none}}</style>
{chr(10).join(lines + texts)}
<circle cx="{f(CX)}" cy="{f(CY)}" r="26" style="fill:{t['core']};stroke:{t['ring']}"/><text x="{f(CX)}" y="{f(CY)}" text-anchor="middle" style="fill:#fff;font-weight:700;font-size:16px">AI</text>
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
