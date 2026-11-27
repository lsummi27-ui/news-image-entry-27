#!/usr/bin/env python3
"""Draw a 1024x1024 newspaper front page: THE WORLD TODAY, Friday 27 November 2026."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
BAND = (22, 28, 44)
RED = (158, 28, 28)
GREY = (90, 86, 78)
RULE = (150, 144, 132)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def story(draw, x, y, w, label, headline, standfirst, hl_size=25):
    """One sub-story block. Returns y after the block."""
    f_lab = font(SANS_B, 14)
    f_hl = font(SERIF_B, hl_size)
    f_st = font(SANS, 16)
    draw.text((x, y), label.upper(), font=f_lab, fill=RED)
    y += 20
    y = draw_lines(draw, wrap(draw, headline, f_hl, w), x, y, f_hl, INK, hl_size + 5)
    y += 3
    y = draw_lines(draw, wrap(draw, standfirst, f_st, w), x, y, f_st, (58, 56, 50), 20)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    inner = W - 2 * M

    # --- Masthead band ---
    d.rectangle([0, 0, W, 158], fill=BAND)
    f_title = font(SERIF_B, 84)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 22), title, font=f_title, fill=(247, 243, 234))
    f_sub = font(SANS_B, 20)
    sub = "FRIDAY 27 NOVEMBER 2026  \u2022  WORLD NEWS IN ONE PAGE  \u2022  No. 331"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 116), sub, font=f_sub, fill=(196, 190, 175))

    # --- Thin rules under masthead ---
    d.line([(M, 172), (W - M, 172)], fill=RULE, width=2)
    d.line([(M, 178), (W - M, 178)], fill=RULE, width=1)

    # --- Lead story ---
    y = 196
    f_kick = font(SANS_B, 17)
    d.text((M, y), "LEAD STORY  \u2022  UNITED STATES", font=f_kick, fill=RED)
    y += 28
    f_lead = font(SERIF_B, 62)
    lead = "Thanksgiving storm halts Macy's parade"
    lead_lines = wrap(d, lead, f_lead, inner)
    y = draw_lines(d, lead_lines, M, y, f_lead, INK, 66)
    y += 6
    f_dek = font(SERIF, 26)
    dek = ("First postponement in 100 years as heavy rain, wind and flooding "
           "sweep the United States on Thanksgiving Day.")
    y = draw_lines(d, wrap(d, dek, f_dek, inner), M, y, f_dek, (48, 46, 42), 32)
    y += 10
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 14

    # --- Three-column grid of sub-stories ---
    gap = 24
    col_w = (inner - 2 * gap) // 3
    xs = [M, M + col_w + gap, M + 2 * (col_w + gap)]
    for cx in (M + col_w + gap // 2, M + 2 * col_w + gap + gap // 2):
        d.line([(cx, y), (cx, 940)], fill=RULE, width=1)

    cols = [
        [
            ("Trade", "Trump proposes 25% tariff on Indian goods",
             "Move follows trade investigations; New Delhi weighs its response."),
            ("Egypt", "Fuel tanker crash near Cairo kills at least 31",
             "Huge highway fire after collision; dozens more hurt, officials say."),
            ("Thailand", "Major fire at Bangkok oil refinery",
             "Bangchak shuts all units as residents nearby are told to evacuate."),
            ("South Africa", "Ramaphosa wins court bid over impeachment report",
             "President overturns the report that had threatened his office."),
        ],
        [
            ("Korea", "Kim vows to expand nuclear arsenal",
             "North Korean leader defiant despite Trump's latest overture."),
            ("Space", "Musk: every US child to get two SpaceX shares",
             "Giveaway said to be worth about $18 billion in total."),
            ("Europe", "EU leaders weigh \u20ac1.6 trillion budget",
             "Plus a $49-billion loan to Ukraine as summit talks continue."),
            ("Space", "Pakistani astronaut joins Chinese mission",
             "First foreigner aboard a Chinese crewed flight, Shenzhou-24 to Tiangong."),
        ],
        [
            ("Health", "Ebola outbreak in DR Congo passes 12,000 cases",
             "Confirmed infections keep climbing; aid teams race to contain it."),
            ("Bangladesh", "Garment workers win 36% minimum-wage rise",
             "Pay deal follows days of street protests across the industry."),
            ("Chess", "Gukesh and Sindarov draw game two",
             "World Championship stays level after a hard-fought second game."),
            ("Space", "SpaceX cleared for one million satellites",
             "Approval paves the way for orbital data centres above Earth."),
        ],
    ]

    for x, stories in zip(xs, cols):
        cy = y
        for label, hl, st in stories:
            cy = story(d, x, cy, col_w, label, hl, st, hl_size=22) + 10

    # --- Footer ---
    d.line([(M, 956), (W - M, 956)], fill=RULE, width=2)
    f_foot = font(SANS, 16)
    foot = "THE WORLD TODAY  \u2022  Friday 27 November 2026  \u2022  All the day's world news on one page"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 968), foot, font=f_foot, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
