#!/usr/bin/env python3
"""Sum up 18 November 2026's world news in one image.

Run:
    python3 main.py

Writes:
    news-2026-11-18.svg  (1600 x 2000 px newspaper front page)

Only the Python standard library is used. The SVG uses generic serif
and sans-serif font families, so it renders anywhere.
"""

import textwrap
from xml.sax.saxutils import escape

W, H = 1600, 2000
OUT = "news-2026-11-18.svg"

LEAD = {
    "kicker": "CHINA  ·  RUSSIA  ·  UNITED STATES",
    "headline": "Xi greets 'old friend' Putin as Trump heads for China",
    "summary": (
        "China's Xi Jinping welcomed Vladimir Putin in Beijing while "
        "Donald Trump flew in via Manila for a high-stakes visit — and "
        "said he would be keen to meet Kim Jong Un."
    ),
}

STORIES = [
    ("ARTIFICIAL INTELLIGENCE", "#7c3aed",
     "Nvidia spy scandal shadows China's AI dreams",
     "The chip giant says it will not reinstate Jensen Huang even as it "
     "reports soaring sales after his dramatic exit."),
    ("UNITED STATES", "#1d4ed8",
     "Democrats take Alaska as midterm count ends",
     "Mary Peltola's Senate win, two weeks after voting, caps the "
     "party's rout of the Republicans in the midterms."),
    ("TECHNOLOGY", "#b45309",
     "Rubio: US is not 'under systemic attack'",
     "After a run of tech outages — and a reported failure on the NSA's "
     "classified network — Washington sees zero evidence of coordination."),
    ("GAMES", "#be123c",
     "GTA 6 hype peaks a day before launch",
     "Grand Theft Auto 6 arrives tomorrow, and gamers everywhere are "
     "counting down to the most talked-about release of the year."),
    ("ENERGY", "#15803d",
     "Pakistan's solar boom outruns its grid",
     "Rooftop solar is spreading so fast that the national grid is "
     "struggling to keep up with the revolution."),
    ("TRANSPORT", "#0e7490",
     "Waymo pulls robotaxis off US freeways",
     "The driverless fleet leaves every American freeway after "
     "California banned the cars from its roads."),
]


def wrap(text, size, width_px):
    per_line = max(8, int(width_px / (size * 0.52)))
    return textwrap.wrap(text, per_line)


def text(x, y, s, size, fill="#111111", weight="normal",
         family="Georgia, serif", anchor="start", spacing=None):
    sp = ' letter-spacing="%s"' % spacing if spacing else ""
    return (
        '<text x="%s" y="%s" font-family="%s" font-size="%s" '
        'font-weight="%s" fill="%s" text-anchor="%s"%s>%s</text>'
        % (x, y, family, size, weight, fill, anchor, sp, escape(s))
    )


def block(x, y, parts, size, leading, fill="#222222", weight="normal",
          family="Georgia, serif"):
    return "\n".join(
        text(x, y + i * leading, s, size, fill, weight, family)
        for i, s in enumerate(parts)
    )


def flag_china(x, y, w, h):
    return "\n".join([
        '<rect x="%s" y="%s" width="%s" height="%s" fill="#de2910"/>' % (x, y, w, h),
        text(x + 16, y + 52, "★", 44, "#ffde00", "bold", "Arial, sans-serif"),
        text(x + 66, y + 34, "★", 22, "#ffde00", "bold", "Arial, sans-serif"),
        text(x + 92, y + 56, "★", 22, "#ffde00", "bold", "Arial, sans-serif"),
        text(x + 82, y + 88, "★", 22, "#ffde00", "bold", "Arial, sans-serif"),
        text(x + 52, y + 102, "★", 22, "#ffde00", "bold", "Arial, sans-serif"),
    ])


def flag_russia(x, y, w, h):
    third = h // 3
    return "\n".join([
        '<rect x="%s" y="%s" width="%s" height="%s" fill="#ffffff" stroke="#cbd5e1"/>' % (x, y, w, h),
        '<rect x="%s" y="%s" width="%s" height="%s" fill="#0039a6"/>' % (x, y + third, w, third),
        '<rect x="%s" y="%s" width="%s" height="%s" fill="#d52b1e"/>' % (x, y + 2 * third, w, h - 2 * third),
    ])


def flag_usa(x, y, w, h):
    stripe = h // 13
    parts = ['<rect x="%s" y="%s" width="%s" height="%s" fill="#ffffff"/>' % (x, y, w, h)]
    for i in range(0, 13, 2):
        parts.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#b22234"/>' % (x, y + i * stripe, w, stripe))
    parts.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#3c3b6e"/>' % (x, y, int(w * 0.4), 7 * stripe))
    for r in range(3):
        for c in range(4):
            cx = x + 10 + c * 12
            cy = y + 10 + r * 16
            parts.append('<circle cx="%s" cy="%s" r="3" fill="#ffffff"/>' % (cx, cy))
    return "\n".join(parts)


def lead_art():
    p = ['<rect x="940" y="245" width="600" height="525" fill="#101828"/>']
    p.append('<circle cx="1240" cy="420" r="105" fill="#9fc5e8"/>')
    p.append('<ellipse cx="1240" cy="420" rx="105" ry="42" fill="none" stroke="#5b7a99" stroke-width="3"/>')
    p.append('<ellipse cx="1240" cy="420" rx="42" ry="105" fill="none" stroke="#5b7a99" stroke-width="3"/>')
    p.append('<ellipse cx="1240" cy="420" rx="78" ry="105" fill="none" stroke="#5b7a99" stroke-width="3"/>')
    p.append(text(1240, 300, "THE WORLD TODAY", 26, "#ffffff", "bold", "Arial, sans-serif", "middle", "4"))
    p.append(flag_china(970, 560, 160, 110))
    p.append(flag_russia(1150, 560, 160, 110))
    p.append(flag_usa(1330, 560, 160, 110))
    p.append(text(1050, 700, "BEIJING", 20, "#ffffff", "bold", "Arial, sans-serif", "middle"))
    p.append(text(1230, 700, "MOSCOW", 20, "#ffffff", "bold", "Arial, sans-serif", "middle"))
    p.append(text(1410, 700, "WASHINGTON", 20, "#ffffff", "bold", "Arial, sans-serif", "middle"))
    p.append(text(1240, 748, "Three capitals, one day of news.", 22, "#cbd5e1", "normal", "Georgia, serif", "middle"))
    return "\n".join(p)


def card(x, y, w, h, tag, color, headline, summary):
    p = ['<rect x="%s" y="%s" width="%s" height="%s" fill="#ffffff" stroke="#d8d2c4"/>' % (x, y, w, h),
         '<rect x="%s" y="%s" width="%s" height="10" fill="%s"/>' % (x, y, w, color),
         text(x + 28, y + 58, tag, 24, color, "bold", "Arial, sans-serif", spacing="2")]
    hl = wrap(headline, 40, w - 56)
    p.append(block(x + 28, y + 118, hl, 40, 48, "#111111", "bold"))
    sm = wrap(summary, 27, w - 56)
    p.append(block(x + 28, y + 118 + len(hl) * 48 + 18, sm, 27, 36, "#333333"))
    return "\n".join(p)


def main():
    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="2000" viewBox="0 0 1600 2000">',
         '<rect width="1600" height="2000" fill="#f8f4ea"/>',
         '<rect x="60" y="70" width="1480" height="3" fill="#111111"/>',
         text(800, 168, "THE WORLD IN ONE PAGE", 92, "#111111", "bold", "Georgia, serif", "middle", "2"),
         text(800, 208, "WEDNESDAY, 18 NOVEMBER 2026  ·  ONE DAY, ONE IMAGE", 26, "#444444", "normal", "Arial, sans-serif", "middle", "3"),
         '<rect x="60" y="228" width="1480" height="2" fill="#111111"/>',
         '<rect x="60" y="234" width="1480" height="1" fill="#111111"/>']
    p.append(text(60, 300, LEAD["kicker"], 26, "#be123c", "bold", "Arial, sans-serif", spacing="3"))
    hl = wrap(LEAD["headline"], 60, 840)
    p.append(block(60, 380, hl, 60, 72, "#111111", "bold"))
    sm = wrap(LEAD["summary"], 28, 840)
    p.append(block(60, 380 + len(hl) * 72 + 34, sm, 28, 40, "#333333"))
    p.append(lead_art())
    xs = [60, 820]
    ys = [800, 1160, 1520]
    for i, (tag, color, headline, summary) in enumerate(STORIES):
        p.append(card(xs[i % 2], ys[i // 2], 720, 340, tag, color, headline, summary))
    p.append('<rect x="60" y="1895" width="1480" height="2" fill="#111111"/>')
    p.append(text(800, 1938, "Sources: BBC News, 18 November 2026  ·  Headlines summarised by main.py  ·  One program, one image.", 22, "#666666", "normal", "Arial, sans-serif", "middle"))
    p.append('</svg>')
    svg = "\n".join(p)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print("Wrote %s (%d bytes, %dx%d)" % (OUT, len(svg), W, H))


if __name__ == "__main__":
    main()
