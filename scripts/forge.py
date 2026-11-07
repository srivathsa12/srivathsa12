#!/usr/bin/env python3
"""
TVA CASE FILE // VARIANT S-12 — forges every animated panel for the srivathsa12 profile.

Standard library only, so the daily GitHub Action can run it with no installs.
Live panels (doomsday-memo, footer) change daily: Doomsday countdown, days since the Nexus event.
Edit the CONTENT block, then run:  python scripts/forge.py
"""
import base64
import math
import os
import random
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "scripts")
OUT = os.path.join(ROOT, "assets")
IST = timezone(timedelta(hours=5, minutes=30))

# ═════════════════════════════ CONTENT ═════════════════════════════
VARIANT = dict(name="SRIVATHSA", no="S-12", alias="srivathsa12", sector="GITHUB", height="5'2\"",
               cls="HUMAN · CS UNDERGRAD", field="AI & MACHINE LEARNING",
               base="NEWTON SCHOOL OF TECHNOLOGY",
               associates="TONY STARK · LOKI LAUFEYSON · VICTOR VON DOOM")
CHARGES = ["01  UNAUTHORIZED CURIOSITY",
           "02  BUILDING BOTS THAT REPLY AT 3 A.M.",
           "03  DEVIATING FROM THE SACRED TIMELINE"]
NEXUS_EVENT = datetime(2026, 11, 2, tzinfo=IST)
DOOMSDAY = datetime(2026, 12, 18, tzinfo=IST)

EXHIBITS = [
    dict(file="exhibit-a", ex="A", code="PARTICLE MAN", repo="my-portfolio", stamp="APPROVED", ink="#2f6b3a",
         lines=["Interactive portfolio: a Three.js", "particle portrait + a terminal-style", "learning log. One HTML file. No build."],
         tape=["THREE.JS", "HTML", "CSS"], note="Built in a cave, with a box of scraps. And Claude."),
    dict(file="exhibit-b", ex="B", code="MISS MINUTES CRON", repo="scheduled-tasks", stamp="ON SCHEDULE", ink="#9c4a1f",
         lines=["Runs a Python script on a schedule", "with GitHub Actions. Forked to study", "how the Sacred Timeline keeps time."],
         tape=["PYTHON", "GITHUB ACTIONS"], note="For all time. Always. (Every 24 hrs.)"),
    dict(file="exhibit-c", ex="C", code="E.D.I.T.H.", repo="even dead, i'm texting here", stamp="IN PROGRESS", ink="#b3261e",
         lines=["WhatsApp auto-reply bot: greets", "with an intro, serves the services", "menu, hands over contact buttons."],
         tape=["WHATSAPP", "AUTOMATION"], note="Answers at 3 A.M. Never complains."),
    dict(file="exhibit-d", ex="D", code="VICTOR VON REPLY", repo="doombot business suite", stamp="PENDING DOOM", ink="#2f6b3a",
         lines=["WhatsApp automation for a business", "owner: replies, follow-ups and", "reminders on autopilot."],
         tape=["WHATSAPP", "BUSINESS"], note="Doom does not leave customers on read."),
]
TIMELINE = [  # event, date, location, status, state
    ("NEXUS-001", "02.11.2026", "GITHUB", "FIRST REPO", "past"),
    ("MARK-I", "NOV 2026", "my-portfolio", "DEPLOYED", "past"),
    ("STUDY", "NOW", "AGENTIC AI/GENAI", "IN PROGRESS", "now"),
    ("EDITH", "NEXT", "WHATSAPP", "FORGING", "next"),
    ("VON-REPLY", "NEXT", "WHATSAPP", "FORGING", "next"),
    ("??????", "????", "[REDACTED]", "PENDING", "secret"),
]
LEARNING = [("AGENTIC AI", "Building Ultrons that actually follow instructions."),
            ("GENERATIVE AI", "Teaching machines to dream. Responsibly.")]
ARSENAL = ["PYTHON", "HTML/CSS/JS", "THREE.JS", "GITHUB ACTIONS", "AI PAIR-PROGRAMMING"]

# ═════════════════════════════ PALETTE ═════════════════════════════
INK, PAPER, MANILA, MANILA2 = "#1c120b", "#eadcbf", "#d8b878", "#c9a35f"
ORANGE, RUST, BROWN, RED, GREEN = "#c8622a", "#9c4a1f", "#2a1a10", "#b3261e", "#2f6b3a"
AMBER, AMBER2 = "#ffb347", "#ff8c1a"
DOOMG = "#96cda0"

# ═════════════════════════════ PLUMBING ═════════════════════════════
B64 = {n: open(os.path.join(HERE, "fonts", n + ".b64")).read().strip() for n in ("type", "serif", "black", "label")}
FAM = {"type": "TVAType", "serif": "TVASerif", "black": "TVABlack", "label": "TVALabel"}



def photo(name):
    with open(os.path.join(HERE, "photos", name), "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def font_css(*names):
    css = "".join(f"@font-face{{font-family:'{FAM[n]}';src:url(data:font/woff;base64,{B64[n]}) format('woff')}}" for n in names)
    return css + (".ty{font-family:'TVAType','Courier New',monospace;font-weight:700}"
                  ".se{font-family:'TVASerif',Baskerville,Georgia,serif}"
                  ".bk{font-family:'TVABlack','Arial Black',Impact,sans-serif;font-weight:900}"
                  ".lb{font-family:'TVALabel','Helvetica Neue',Arial,sans-serif;font-weight:600}")


BASE_CSS = """
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes draw{to{stroke-dashoffset:0}}
@keyframes blink{0%,55%{opacity:1}56%,100%{opacity:.12}}
@keyframes slam{0%{opacity:0;transform:scale(2.2) rotate(var(--r0,-4deg))}62%{opacity:.95;transform:scale(.96) rotate(var(--r,-10deg))}80%{transform:scale(1.02) rotate(var(--r,-10deg))}100%{opacity:.9;transform:scale(1) rotate(var(--r,-10deg))}}
@keyframes shake{0%,100%{transform:none}20%{transform:translate(2px,3px)}40%{transform:translate(-3px,-1px)}60%{transform:translate(2px,-2px)}80%{transform:translate(-1px,1px)}}
@keyframes swing{0%,100%{transform:rotate(-5deg)}50%{transform:rotate(4deg)}}
.fu{animation:fadeUp .6s cubic-bezier(.2,.8,.2,1) both}
.fi{animation:fadeIn .7s ease both}
.lamp{animation:blink 1.6s steps(1) infinite}
.stamp{transform-box:fill-box;transform-origin:center;animation:slam .42s cubic-bezier(.5,0,.75,0) both}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.dr{stroke-dashoffset:0!important}}
"""

COMMON_DEFS = (
    '<filter id="paperTex" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="7" result="n"/>'
    '<feColorMatrix in="n" values="0 0 0 0 .45  0 0 0 0 .33  0 0 0 0 .2  0 0 0 .22 0" result="t"/><feComposite in="t" in2="SourceGraphic" operator="in"/></filter>'
    '<filter id="blotch" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".012" numOctaves="3" seed="3" result="n"/>'
    '<feColorMatrix in="n" values="0 0 0 0 .55  0 0 0 0 .38  0 0 0 0 .18  0 0 0 -1.6 1.05" result="t"/><feComposite in="t" in2="SourceGraphic" operator="in"/></filter>'
    '<filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feGaussianBlur stdDeviation="8"/></filter>'
    '<filter id="roughInk" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="2" seed="4" result="n"/>'
    '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -3.2 2.3" result="holes"/>'
    '<feComposite in="SourceGraphic" in2="holes" operator="in" result="speck"/>'
    '<feTurbulence type="turbulence" baseFrequency=".04" numOctaves="2" seed="9" result="w"/>'
    '<feDisplacementMap in="speck" in2="w" scale="3.2"/></filter>'
    '<filter id="inkLight" x="-5%" y="-20%" width="110%" height="140%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="6" result="n"/>'
    '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.2 2.4" result="holes"/>'
    '<feComposite in="SourceGraphic" in2="holes" operator="in"/></filter>'
    '<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.4" result="b"/>'
    '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    '<pattern id="deco" width="14" height="14" patternUnits="userSpaceOnUse"><path d="M0 14L7 0L14 14" fill="none" stroke="#c8622a" stroke-opacity=".55" stroke-width="1.2"/></pattern>'
    '<linearGradient id="clipMetal" x1="0" x2="1"><stop offset="0" stop-color="#8b8e93"/><stop offset=".5" stop-color="#e9ecef"/><stop offset="1" stop-color="#7c7f84"/></linearGradient>'
)


def svg(w, h, label, body, css="", defs="", fonts=("type", "serif", "black", "label")):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
            f'<title>{esc(label)}</title><defs>{COMMON_DEFS}{defs}</defs>'
            f'<style>{font_css(*fonts)}{BASE_CSS}{css}</style>{body}</svg>')


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name + ".svg")
    with open(p, "w") as f:
        f.write(content)
    return p


def d(s):
    return f'style="animation-delay:{s:.2f}s"'


def paper(x, y, w, h, fill=PAPER, stroke="#b9a37c"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" filter="url(#blotch)" opacity=".5"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" filter="url(#paperTex)"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{stroke}"/>')


def stamp(x, y, w, h, text, ink, delay, rot=-10, size=None, sub=None):
    size = size or h * .55
    inner = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="none" stroke="{ink}" stroke-width="4"/>'
             f'<rect x="{x+6}" y="{y+6}" width="{w-12}" height="{h-12}" rx="2" fill="none" stroke="{ink}" stroke-width="1.4"/>')
    ty = y + h / 2 + size * .36 + (-6 if sub else 0)
    inner += (f'<text x="{x+w/2}" y="{ty:.1f}" text-anchor="middle" class="bk" font-size="{size:.1f}" fill="{ink}" '
              f'letter-spacing="2" textLength="{w-28}" lengthAdjust="spacingAndGlyphs">{esc(text)}</text>')
    if sub:
        inner += f'<text x="{x+w/2}" y="{y+h-12}" text-anchor="middle" class="lb" font-size="8" fill="{ink}" letter-spacing="2">{esc(sub)}</text>'
    return (f'<g class="stamp" style="animation-delay:{delay:.2f}s;--r:{rot}deg;--r0:{rot+6}deg" filter="url(#roughInk)">{inner}</g>')


class Typist:
    """Sequential typewriter: each string starts after the previous one finishes."""
    def __init__(self, start, cps=80, prefix="tp"):
        self.t, self.cps, self.defs, self.n, self.prefix = start, cps, [], 0, prefix

    def __call__(self, text, x, y, size=15, fill=INK, gap=.04, cls="ty", anchor="start", extra=""):
        self.n += 1
        cw = .6 * size
        n = len(text)
        dur = max(n / self.cps, .05)
        x0 = x - n * cw if anchor == "end" else x
        vals = ";".join(f"{i*cw:.1f}" for i in range(n + 1))
        cid = f"{self.prefix}{self.n}"
        self.defs.append(f'<clipPath id="{cid}"><rect x="{x0-1}" y="{y-size-2}" height="{size*1.7}" width="0">'
                         f'<animate attributeName="width" values="{vals}" calcMode="discrete" begin="{self.t:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>')
        out = (f'<text x="{x0}" y="{y}" class="{cls}" font-size="{size}" fill="{fill}" clip-path="url(#{cid})" xml:space="preserve" {extra}>{esc(text)}</text>')
        self.t += dur + gap
        return out


# ═════════════════════════════ LIVE DATA (GitHub API → data.json cache) ═════════════════════════════
USER = "srivathsa12"
DATA_FILE = os.path.join(HERE, "data.json")
SEED = {  # what the profile looked like when this file was forged; the daily Action replaces it with live data
    "repos": [
        {"name": "my-portfolio", "language": "HTML", "stars": 0, "fork": False, "pushed": "2026-11-02",
         "description": "Interactive portfolio with a Three.js particle portrait and a terminal-style learning log."},
        {"name": "scheduled-tasks", "language": "Python", "stars": 0, "fork": True, "pushed": "",
         "description": "Run your python script on a regular basis using Github actions"},
    ],
    "events": [
        {"type": "PUSH", "repo": "my-portfolio", "detail": "1 COMMIT", "date": "2026-11-02"},
        {"type": "CREATE", "repo": "my-portfolio", "detail": "NEW REPO", "date": "2026-11-02"},
    ],
    "commits_90d": 1,
    "synced": "seed",
}


def _api(path):
    import json, urllib.request
    req = urllib.request.Request("https://api.github.com" + path, headers={
        "Accept": "application/vnd.github+json", "User-Agent": f"{USER}-profile-forge"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", "Bearer " + tok)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def load_data(now):
    import json
    data = SEED
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            data = json.load(f)
    if os.environ.get("FORGE_OFFLINE"):
        return data
    try:
        repos = _api(f"/users/{USER}/repos?per_page=100&sort=pushed")
        events = _api(f"/users/{USER}/events/public?per_page=60")
        out_ev, commits = [], 0
        for e in events:
            t, repo, date = e["type"], e["repo"]["name"].split("/")[-1], e["created_at"][:10]
            p = e.get("payload", {})
            if t == "PushEvent":
                n = p.get("size") or len(p.get("commits", [])) or 1
                commits += n
                out_ev.append({"type": "PUSH", "repo": repo, "detail": f"{n} COMMIT{'S' if n > 1 else ''}", "date": date})
            elif t == "CreateEvent":
                out_ev.append({"type": "CREATE", "repo": repo, "detail": "NEW " + (p.get("ref_type") or "REPO").upper(), "date": date})
            elif t == "PullRequestEvent":
                out_ev.append({"type": "PR", "repo": repo, "detail": (p.get("action") or "").upper(), "date": date})
            elif t == "ForkEvent":
                out_ev.append({"type": "FORK", "repo": repo, "detail": "FORKED", "date": date})
            elif t == "WatchEvent":
                out_ev.append({"type": "STAR", "repo": repo, "detail": "STARRED", "date": date})
            elif t == "IssuesEvent":
                out_ev.append({"type": "ISSUE", "repo": repo, "detail": (p.get("action") or "").upper(), "date": date})
        data = {
            "repos": [{"name": r["name"], "language": r.get("language"), "stars": r.get("stargazers_count", 0),
                       "fork": r.get("fork", False), "pushed": (r.get("pushed_at") or "")[:10],
                       "description": r.get("description") or ""} for r in repos if r["name"] != USER],
            "events": out_ev[:12], "commits_90d": commits, "synced": now.strftime("%Y-%m-%d"),
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=1)
        print("live data synced:", len(data["repos"]), "repos,", len(out_ev), "events")
    except Exception as ex:  # offline / rate-limited: keep the last good snapshot
        print("using cached data:", ex)
    return data


def fmt_date(iso):
    try:
        y, m, dd = iso.split("-")
        return f"{dd}.{m}.{y[2:]}"
    except Exception:
        return iso or "—"


def stats(data):
    repos = data["repos"]
    langs = {}
    for r in repos:
        if r.get("language"):
            langs[r["language"]] = langs.get(r["language"], 0) + 1
    top = max(langs, key=langs.get) if langs else "—"
    last = max((r["pushed"] for r in repos if r.get("pushed")), default="")
    return dict(repos=len(repos), stars=sum(r.get("stars", 0) for r in repos), langs=langs, top=top,
                last=fmt_date(last), commits=data.get("commits_90d", 0))


def header_band(right1, right2, lamp="LIVE CASE", band=BROWN, accent=ORANGE, title="TIME VARIANCE AUTHORITY", tagline="FOR ALL TIME · ALWAYS"):
    return (f'<rect x="20" y="20" width="860" height="62" fill="{band}"/>'
            f'<rect x="20" y="82" width="860" height="10" fill="url(#deco)"/>'
            f'<path d="M20 82.5H880M20 92.5H880" stroke="{accent}" stroke-width="1.2"/>'
            f'<g transform="translate(58 51)"><circle r="19" fill="none" stroke="{accent}" stroke-width="1.6"/><circle r="14.5" fill="none" stroke="{accent}" stroke-opacity=".5"/>'
            f'<path d="M-7 -9H7L0 0L7 9H-7L0 0Z" fill="{accent}"/></g>'
            f'<text x="90" y="49" class="se" font-size="21" fill="#f1dcb6" letter-spacing="5.5">{esc(title)}</text>'
            f'<text x="91" y="67" class="lb" font-size="8.5" fill="{accent}" letter-spacing="3.2">{esc(tagline)}</text>'
            f'<text x="860" y="46" text-anchor="end" class="lb" font-size="10" fill="#f1dcb6" letter-spacing="3">{esc(right1)}</text>'
            f'<text x="860" y="64" text-anchor="end" class="ty" font-size="10" fill="{accent}" letter-spacing="1">{esc(right2)}</text>'
            + (f'<circle cx="306" cy="64" r="3.5" fill="#ff5a2a" class="lamp"/><text x="314" y="67" class="lb" font-size="8" fill="#ff8a5a" letter-spacing="2">{lamp}</text>' if lamp else ""))


DROP_CSS = """
@keyframes drop{0%{opacity:0;transform:translate(0,-40px) rotate(-3.5deg)}60%{opacity:1}100%{opacity:1;transform:rotate(-.5deg)}}
.drop{transform-box:view-box;transform-origin:450px 200px;animation:drop .9s cubic-bezier(.2,.85,.25,1) both}
.sg{stroke-dasharray:420;stroke-dashoffset:420;animation:draw 1.1s ease-in-out forwards}
.dr2{animation:draw 1s cubic-bezier(.6,0,.2,1) forwards}
"""


# ═════════════════════════════ 5. QUARTERMASTER (tech stack) ═════════════════════════════
EQUIPMENT = [  # item, class, status (ISSUED = in use · TRAINING = learning now)
    ("PYTHON", "LANGUAGE", "ISSUED"),
    ("HTML · CSS · JAVASCRIPT", "LANGUAGE", "ISSUED"),
    ("THREE.JS", "3D / WEBGL", "ISSUED"),
    ("GITHUB ACTIONS", "AUTOMATION", "ISSUED"),
    ("GIT · GITHUB", "VERSION CONTROL", "ISSUED"),
    ("LLM APIs · PROMPTING", "GENERATIVE AI", "TRAINING"),
    ("AI AGENTS · TOOL USE", "AGENTIC AI", "TRAINING"),
    ("WHATSAPP AUTOMATION", "INTEGRATION", "TRAINING"),
]


def quartermaster(data):
    W, H = 900, 470
    st = stats(data)
    b = ['<g class="drop"><rect x="34" y="36" width="846" height="420" rx="3" fill="#000" opacity=".5" filter="url(#shadow)"/>',
         paper(20, 20, 860, 430, "#ece2c8"),
         header_band("QUARTERMASTER · EQUIPMENT ISSUE", "FORM TVA-12/Q  ·  ISSUED TO S-12", lamp=None)]
    tx, ty = 44, 122
    for hx, ht in ((tx, "Nº"), (tx + 38, "ITEM"), (tx + 262, "CLASS"), (tx + 418, "STATUS")):
        b.append(f'<text x="{hx}" y="{ty}" class="lb" font-size="8.5" fill="#7b5b3d" letter-spacing="1.8">{ht}</text>')
    b.append(f'<path d="M{tx} {ty+8}H560" stroke="{INK}" stroke-opacity=".6"/>')
    for i, (item, cls_, status) in enumerate(EQUIPMENT):
        y = ty + 34 + i * 36
        dl = .7 + i * .16
        issued = status == "ISSUED"
        b.append(f'<g class="row" style="animation-delay:{dl:.2f}s">'
                 f'<text x="{tx}" y="{y}" class="ty" font-size="12" fill="#7b5b3d">{i+1:02d}</text>'
                 f'<text x="{tx+38}" y="{y}" class="ty" font-size="13.5" fill="{INK}">{esc(item)}</text>'
                 f'<text x="{tx+262}" y="{y}" class="ty" font-size="10.5" fill="#7b5b3d">{esc(cls_)}</text>'
                 f'<rect x="{tx+418}" y="{y-12}" width="14" height="14" fill="none" stroke="{INK}" stroke-width="1.3"/>'
                 f'<text x="{tx+440}" y="{y}" class="bk" font-size="11" fill="{GREEN if issued else RUST}" letter-spacing="1">{"ISSUED" if issued else "IN TRAINING"}</text>'
                 f'<path d="M{tx} {y+12}H560" stroke="#7b5b3d" stroke-opacity=".3" stroke-dasharray="1.5 2.5"/></g>')
        if issued:
            b.append(f'<path d="M{tx+420} {y-5}l4 5 9-12" fill="none" stroke="{GREEN}" stroke-width="2.4" stroke-linecap="round" '
                     f'class="dr2" style="stroke-dasharray:24;stroke-dashoffset:24;animation-delay:{dl+.35:.2f}s"/>')
        else:
            b.append(f'<path d="M{tx+421} {y-2}h8" stroke="{RUST}" stroke-width="2.4" class="dr2" style="stroke-dasharray:10;stroke-dashoffset:10;animation-delay:{dl+.35:.2f}s"/>')
    # right column: live language composition
    rx = 596
    b.append(f'<rect x="{rx}" y="106" width="262" height="320" fill="none" stroke="{INK}" stroke-opacity=".5"/>'
             f'<rect x="{rx}" y="106" width="262" height="18" fill="{INK}"/>'
             f'<text x="{rx+10}" y="119" class="lb" font-size="8" fill="{PAPER}" letter-spacing="1.8">LANGUAGE COMPOSITION · LIVE</text>')
    langs = sorted(st["langs"].items(), key=lambda kv: -kv[1]) or [("—", 1)]
    total = sum(v for _, v in langs)
    inks = [RUST, GREEN, "#1d2a6b", "#7b5b3d", ORANGE, INK]
    x = rx + 16
    bar_w = 230
    for i, (lang, n) in enumerate(langs):
        w = bar_w * n / total
        b.append(f'<rect x="{x:.1f}" y="150" width="{w:.1f}" height="22" fill="{inks[i % len(inks)]}" class="grow" style="animation-delay:{1+i*.2:.2f}s"/>')
        x += w
    for i, (lang, n) in enumerate(langs[:6]):
        y = 204 + i * 24
        pct = round(100 * n / total)
        b.append(f'<g class="row" style="animation-delay:{1.3+i*.15:.2f}s"><rect x="{rx+16}" y="{y-10}" width="11" height="11" fill="{inks[i % len(inks)]}"/>'
                 f'<text x="{rx+36}" y="{y}" class="ty" font-size="12" fill="{INK}">{esc(lang.upper())}</text>'
                 f'<text x="{rx+246}" y="{y}" text-anchor="end" class="ty" font-size="12" fill="#7b5b3d">{pct}%</text></g>')
    ly = 204 + min(len(langs), 6) * 24 + 12
    b.append(f'<path d="M{rx+16} {ly-8}H{rx+246}" stroke="{INK}" stroke-opacity=".35"/>'
             f'<text x="{rx+16}" y="{ly+8}" class="lb" font-size="8" fill="#7b5b3d" letter-spacing="1.8">REPOS ON FILE · LIVE</text>')
    for i, r in enumerate(sorted(data["repos"], key=lambda r: r.get("pushed", ""), reverse=True)[:5]):
        y = ly + 30 + i * 21
        b.append(f'<g class="row" style="animation-delay:{1.8+i*.12:.2f}s"><text x="{rx+16}" y="{y}" class="ty" font-size="11" fill="{INK}">{esc(r["name"][:18])}{" (fork)" if r.get("fork") else ""}</text>'
                 f'<text x="{rx+246}" y="{y}" text-anchor="end" class="ty" font-size="10" fill="#7b5b3d">{fmt_date(r.get("pushed"))}</text></g>')
    b.append(f'<text x="{rx+16}" y="416" class="lb" font-size="7" fill="#7b5b3d" letter-spacing="1.3">RECOUNTED DAILY BY THE TVA · GITHUB ACTIONS</text>')
    b.append(stamp(626, 330, 210, 44, "INVENTORY VERIFIED", GREEN, 2.9, -6, 17))
    b.append(f'<text x="44" y="436" class="lb" font-size="7.5" fill="#7b5b3d" letter-spacing="1.6">EQUIPMENT MUST BE RETURNED BEFORE THE END OF TIME · ISSUED BY QUARTERMASTER O.</text>')
    b.append('</g>')
    css = DROP_CSS + """
@keyframes rowIn{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.row{animation:rowIn .4s ease-out both}
.grow{transform-box:fill-box;transform-origin:left;animation:grow .6s cubic-bezier(.6,0,.2,1) both}
"""
    return write("05-quartermaster", svg(W, H, "Quartermaster equipment sheet — tech stack: " + "; ".join(f"{a} ({s})" for a, _, s in EQUIPMENT)
                                         + ". Languages: " + ", ".join(f"{k} {v}" for k, v in langs), "".join(b), css))


# ═════════════════════════════ 0. TVA WIRE (live ticker) ═════════════════════════════
def ticker(now, data):
    W, H = 900, 46
    st = stats(data)
    days = (DOOMSDAY.date() - now.date()).days
    items = ["INCOMING TRANSMISSION FROM SECTOR 12",
             f"VARIANT S-12 LAST ACTIVE {st['last']}",
             f"{st['repos']} REPOS ON FILE · TOP LANGUAGE {st['top'].upper()}",
             "NOW STUDYING: AGENTIC AI · GENERATIVE AI",
             "IN THE FORGE: E.D.I.T.H. — WHATSAPP AUTO-REPLY BOT",
             "STATUS: OPEN TO WORK — SEE REQUISITION DESK"]
    ev = data.get("events") or []
    if ev:
        e = ev[0]
        items.insert(2, f"LATEST: {e['type']} / {e['repo']} ({e['detail']})")
    if days > 0:
        items.append(f"DOOMSDAY IN {days} DAYS")
    line = "    •    ".join(items) + "    •    "
    cw = 0.6 * 12
    tw = len(line) * cw
    dur = max(tw / 55, 20)
    run = (f'<text x="0" y="28" class="ty" font-size="12" fill="{AMBER}" xml:space="preserve">{esc(line)}</text>'
           f'<text x="{tw:.0f}" y="28" class="ty" font-size="12" fill="{AMBER}" xml:space="preserve">{esc(line)}</text>')
    b = [f'<rect x="0" y="4" width="{W}" height="38" rx="5" fill="#140a03"/>',
         f'<rect x="0" y="4" width="{W}" height="38" rx="5" fill="url(#scan)"/>',
         f'<g clip-path="url(#wire)"><g class="run" transform="translate(150 0)"><g class="mv">{run}</g></g></g>',
         f'<rect x="150" y="4" width="40" height="38" fill="url(#fadeL)"/><rect x="{W-40}" y="4" width="40" height="38" rx="5" fill="url(#fadeR)"/>',
         f'<rect x="0" y="4" width="150" height="38" rx="5" fill="{ORANGE}"/><rect x="140" y="4" width="10" height="38" fill="{ORANGE}"/>',
         f'<circle cx="20" cy="23" r="4.5" fill="#fff4dc" class="lamp"/>',
         f'<text x="32" y="28" class="bk" font-size="12.5" fill="#fff4dc" letter-spacing="2.4">TVA WIRE</text>',
         f'<text x="118" y="27.5" class="ty" font-size="9" fill="#fff4dc" opacity=".85">LIVE</text>']
    css = f"""
@keyframes mv{{from{{transform:translateX(0)}}to{{transform:translateX(-{tw:.0f}px)}}}}
.mv{{animation:mv {dur:.1f}s linear infinite}}
"""
    defs = (f'<clipPath id="wire"><rect x="150" y="4" width="{W-150}" height="38"/></clipPath>'
            '<pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1.1" fill="#000" opacity=".5"/></pattern>'
            '<linearGradient id="fadeL"><stop offset="0" stop-color="#140a03"/><stop offset="1" stop-color="#140a03" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="fadeR"><stop offset="0" stop-color="#140a03" stop-opacity="0"/><stop offset="1" stop-color="#140a03"/></linearGradient>')
    return write("00-tva-wire", svg(W, H, "TVA Wire — live ticker: " + " · ".join(items), "".join(b), css, defs, fonts=("type", "black")))


# ═════════════════════════════ 1. ARREST RECORD (hero) ═════════════════════════════
def arrest_record(data):
    st = stats(data)
    W, H = 900, 580
    T = Typist(1.4, 85)
    v = VARIANT

    def field(x, y, label, value, w, size=15):
        return (f'<text x="{x}" y="{y}" class="lb" font-size="8.5" fill="#7b5b3d" letter-spacing="1.6">{esc(label)}</text>'
                f'<path d="M{x} {y+25}H{x+w}" stroke="#7b5b3d" stroke-opacity=".55" stroke-dasharray="1.5 2.5"/>'
                + T(value, x, y + 20, size))

    b = ['<g class="drop"><rect x="34" y="36" width="846" height="524" rx="3" fill="#000" opacity=".55" filter="url(#shadow)"/><g class="shk">',
         paper(20, 20, 860, 528),
         f'<rect x="20" y="20" width="860" height="62" fill="{BROWN}"/>',
         '<rect x="20" y="82" width="860" height="10" fill="url(#deco)"/>',
         f'<path d="M20 82.5H880M20 92.5H880" stroke="{ORANGE}" stroke-width="1.2"/>',
         f'<g transform="translate(58 51)"><circle r="19" fill="none" stroke="{ORANGE}" stroke-width="1.6"/><circle r="14.5" fill="none" stroke="{ORANGE}" stroke-opacity=".5"/>'
         f'<path d="M-7 -9H7L0 0L7 9H-7L0 0Z" fill="{ORANGE}"/></g>',
         '<text x="90" y="49" class="se" font-size="21" fill="#f1dcb6" letter-spacing="5.5">TIME VARIANCE AUTHORITY</text>',
         f'<text x="91" y="67" class="lb" font-size="8.5" fill="{ORANGE}" letter-spacing="3.2">FOR ALL TIME · ALWAYS</text>',
         '<text x="860" y="46" text-anchor="end" class="lb" font-size="10" fill="#f1dcb6" letter-spacing="3">VARIANT ARREST RECORD</text>',
         f'<text x="860" y="64" text-anchor="end" class="ty" font-size="10" fill="{ORANGE}" letter-spacing="1">FORM TVA-07/B  ·  SECTOR 12</text>',
         '<circle cx="306" cy="64" r="3.5" fill="#ff5a2a" class="lamp"/><text x="314" y="67" class="lb" font-size="8" fill="#ff8a5a" letter-spacing="2">LIVE CASE</text>']
    fx, fx2 = 362, 622
    b.append(field(fx, 120, "VARIANT NAME", v["name"], 230))
    b.append(field(fx2, 120, "VARIANT Nº", v["no"], 228))
    b.append(field(fx, 166, "ALIAS", v["alias"], 230))
    b.append(field(fx2, 166, "SECTOR", v["sector"], 228))
    b.append(field(fx, 212, "CLASSIFICATION", v["cls"], 230, 14))
    b.append(field(fx2, 212, "HEIGHT", v["height"] + "  (FUN-SIZED)", 228, 14))
    b.append(field(fx, 258, "FIELD OF STUDY", v["field"], 488))
    b.append(field(fx, 304, "BASE OF OPERATIONS", v["base"], 488))
    b.append(field(fx, 350, "KNOWN ASSOCIATES", v["associates"], 488, 13.5))
    b.append(f'<rect x="{fx}" y="384" width="488" height="96" fill="none" stroke="{INK}" stroke-opacity=".7"/>'
             f'<rect x="{fx}" y="384" width="74" height="16" fill="{INK}"/>'
             f'<text x="{fx+8}" y="395.5" class="lb" font-size="8.5" fill="{PAPER}" letter-spacing="1.8">CHARGES</text>')
    T.t += .1
    for i, c in enumerate(CHARGES):
        b.append(T(c, fx + 12, 420 + i * 22, 13))
    b.append('<g class="photo"><rect x="52" y="112" width="276" height="372" fill="#000" opacity=".25" filter="url(#shadow)"/>'
             '<rect x="46" y="104" width="280" height="374" fill="#f6efe0"/>'
             f'<image x="56" y="114" width="260" height="325" href="{photo("mugshot.jpg")}" preserveAspectRatio="xMidYMid slice"/>'
             '<rect x="56" y="114" width="260" height="325" fill="#fff" class="flash"/>'
             f'<text x="60" y="462" class="ty" font-size="12" fill="{INK}">{v["no"]}</text>'
             '</g>')
    b.append('<g class="clp"><path d="M150 132V84a12 12 0 0 1 24 0v58a8 8 0 0 1-16 0V92" fill="none" stroke="url(#clipMetal)" stroke-width="3.4" stroke-linecap="round"/></g>')
    b.append(f'<path d="M40 500H860" stroke="{INK}" stroke-opacity=".35"/>')
    b.append(f'<text x="44" y="528" class="ty fi" font-size="10.5" fill="{INK}" {d(1)}>CASE Nº 372-H20-S12-0211</text>')
    b.append(f'<text x="250" y="512" class="lb fi" font-size="7.5" fill="#7b5b3d" letter-spacing="1.6" {d(1)}>FIELD ACTIVITY · LIVE FROM GITHUB</text>')
    b.append(f'<text x="250" y="530" class="ty fi" font-size="11" fill="{INK}" xml:space="preserve" {d(1.1)}>REPOS {st["repos"]:02d}  ·  COMMITS (90D) {st["commits"]:02d}  ·  TOP LANG {st["top"].upper()}  ·  LAST ACTIVE {st["last"]}</text>')
    b.append('<text x="742" y="540" class="lb" font-size="7" fill="#7b5b3d" letter-spacing="1.6">CASE OFFICER</text>')
    t1 = T.t + .25
    b.append('<path class="sg" d="M742 524c8-14 14-16 12-2s-6 12 2 0 12-14 14-4-4 10 4 2 10-10 14-6 2 8 8 4 8-8 12-6 4 6 10 2c6-4 12-6 22-2s16 2 24-2" '
             f'fill="none" stroke="#1d2a6b" stroke-width="1.8" stroke-linecap="round" style="animation-delay:{t1+.6:.2f}s"/>')
    b.append(stamp(64, 414, 264, 56, "APPREHENDED", RED, t1, -8, 32))
    b.append(f'<g class="stamp" style="animation-delay:{t1+1:.2f}s;--r:7deg;--r0:14deg" filter="url(#roughInk)">'
             f'<rect x="690" y="120" width="170" height="52" rx="26" fill="none" stroke="{GREEN}" stroke-width="3.5"/>'
             f'<text x="775" y="142" text-anchor="middle" class="lb" font-size="9.5" fill="{GREEN}" letter-spacing="2.2">STATUS</text>'
             f'<text x="775" y="161" text-anchor="middle" class="bk" font-size="15" fill="{GREEN}" letter-spacing="1.2">OPEN TO WORK</text></g>')
    b.append('</g></g>')
    css = f"""
@keyframes drop{{0%{{opacity:0;transform:translate(0,-46px) rotate(-4.5deg)}}60%{{opacity:1}}100%{{opacity:1;transform:rotate(-.7deg)}}}}
@keyframes photoIn{{0%{{opacity:0;transform:translate(-30px,-20px) rotate(-9deg)}}100%{{opacity:1;transform:rotate(-2.4deg)}}}}
@keyframes flash{{0%{{opacity:0}}8%{{opacity:1}}100%{{opacity:0}}}}
@keyframes clipIn{{from{{opacity:0;transform:translateY(-14px)}}to{{opacity:1;transform:none}}}}
.drop{{transform-box:view-box;transform-origin:450px 300px;animation:drop .9s cubic-bezier(.2,.85,.25,1) both}}
.shk{{transform-box:view-box;transform-origin:450px 300px;animation:shake .32s linear {t1+.25:.2f}s 1}}
.photo{{transform-box:view-box;transform-origin:188px 290px;animation:photoIn .7s cubic-bezier(.2,.9,.3,1.1) .55s both}}
.flash{{animation:flash .9s ease-out 1.1s both}}

.clp{{animation:clipIn .35s ease-out 1.15s both}}
.sg{{stroke-dasharray:420;stroke-dashoffset:420;animation:draw 1.1s ease-in-out forwards}}
"""
    defs = "".join(T.defs) + ('<clipPath id="printClip"><rect x="56" y="114" width="260" height="325"/></clipPath>'
                              '<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd9a0" stop-opacity="0"/>'
                              '<stop offset=".8" stop-color="#ffd9a0" stop-opacity=".22"/><stop offset="1" stop-color="#fff2d8" stop-opacity=".55"/></linearGradient>')
    return write("01-arrest-record", svg(W, H, f"TVA Variant Arrest Record: {v['name']}, Variant {v['no']}. {v['cls']}, {v['field']}, {v['base']}. Height {v['height']}. Status: open to work.",
                                         "".join(b), css, defs))


# ═════════════════════════════ 2. SECTION TABS ═════════════════════════════
def tab(file, label, title, sub, color=MANILA):
    W, H = 900, 78
    b = [f'<g class="tab"><path d="M20 78V30q0-8 8-8h250l18 18h584v38Z" fill="{color}"/>'
         f'<path d="M20 78V30q0-8 8-8h250l18 18h584v38Z" filter="url(#paperTex)"/>'
         f'<text x="38" y="44" class="lb" font-size="9" fill="{BROWN}" letter-spacing="2.4">{esc(label)}</text>'
         f'<text x="38" y="68" class="bk" font-size="22" fill="{BROWN}" letter-spacing="3">{esc(title)}</text>'
         f'<text x="864" y="66" text-anchor="end" class="ty" font-size="11" fill="{BROWN}" opacity=".8">{esc(sub)}</text></g>']
    css = "@keyframes tabUp{from{transform:translateY(40px);opacity:0}to{transform:none;opacity:1}}.tab{animation:tabUp .6s cubic-bezier(.2,.9,.3,1.15) both}"
    return write(file, svg(W, H, title, "".join(b), css, fonts=("type", "black", "label")))


# ═════════════════════════════ 3. EVIDENCE FOLDERS ═════════════════════════════
def exhibit(e, idx, data):
    W, H = 440, 320
    T = Typist(1.05, 90, prefix=f"e{idx}")
    rnd = random.Random(idx)
    b = []
    # folder back + tab
    b.append(f'<path d="M14 64V44q0-6 6-6h110l14 14h276q6 0 6 6v248q0 6-6 6H20q-6 0-6-6Z" fill="{MANILA2}"/>')
    b.append(f'<text x="30" y="58" class="lb" font-size="9" fill="{BROWN}" letter-spacing="2.2">EXHIBIT {e["ex"]}</text>')
    # index card sliding up out of the folder
    b.append('<g class="card">'
             + paper(34, 62, 372, 212, "#f3ead6", "#cbb894")
             + "".join(f'<path d="M34 {104+i*18}H406" stroke="#8fb3d9" stroke-opacity=".35"/>' for i in range(9))
             + f'<path d="M34 86H406" stroke="{RED}" stroke-opacity=".5"/>'
             f'<text x="46" y="80" class="lb" font-size="8" fill="#7b5b3d" letter-spacing="2">CODENAME</text>'
             f'<text x="350" y="80" text-anchor="end" class="ty" font-size="9" fill="#7b5b3d">CASE 372-{e["ex"]}-S12</text>'
             '</g>')
    b.append(f'<text x="46" y="117" class="bk card2" font-size="26" fill="{INK}" letter-spacing="1.5">{esc(e["code"])}</text>')
    live = next((r for r in data["repos"] if r["name"] == e["repo"]), None)
    if live:
        meta = f'{e["repo"]} · {(live.get("language") or "—").upper()} · STARS {live.get("stars", 0)}'
        if live.get("pushed"):
            meta += f' · UPD {fmt_date(live.get("pushed"))}'
        if live.get("fork"):
            meta += " · FORK"
    else:
        meta = "REPO: COMING SOON · IN THE FORGE"
    b.append(T(meta, 46, 138, 11, "#7b5b3d"))
    for i, ln in enumerate(e["lines"]):
        b.append(T(ln, 46, 166 + i * 18, 12))
    # dymo label tape tags
    x = 46
    tapes = []
    for i, t in enumerate(e["tape"]):
        w = len(t) * 8.2 + 18
        tapes.append(f'<g class="dymo" style="animation-delay:{T.t+.1+i*.12:.2f}s"><rect x="{x}" y="226" width="{w:.0f}" height="20" rx="2" fill="#141414"/>'
                     f'<rect x="{x}" y="226" width="{w:.0f}" height="20" rx="2" fill="url(#tapeShine)"/>'
                     f'<text x="{x+9}" y="240.5" class="bk" font-size="11" fill="#f2f2f2" letter-spacing="1.6">{esc(t)}</text></g>')
        x += w + 8
    b += tapes
    # folder front pocket (covers the bottom of the card)
    b.append(f'<path d="M10 252h420v54q0 6-6 6H16q-6 0-6-6Z" fill="{MANILA}"/>'
             f'<path d="M10 252h420v54q0 6-6 6H16q-6 0-6-6Z" filter="url(#paperTex)"/>'
             f'<path d="M10 252h420" stroke="#a88849"/>'
             f'<text x="24" y="276" class="ty" font-size="11" fill="{BROWN}">{esc(e["note"])}</text>'
             f'<text x="24" y="296" class="lb" font-size="7.5" fill="{BROWN}" opacity=".7" letter-spacing="1.6">PROPERTY OF THE TVA · DO NOT REMOVE FROM SECTOR 12</text>')
    # evidence tag on string, swinging
    b.append(f'<g class="tag"><path d="M372 40C376 52 380 60 386 70" fill="none" stroke="#6b5132" stroke-width="1.2"/>'
             f'<path d="M370 70h34l8 10v44h-50v-44Z" fill="#efe3c6" stroke="#a88849"/>'
             f'<circle cx="387" cy="78" r="3" fill="{MANILA2}" stroke="#6b5132"/>'
             f'<text x="387" y="104" text-anchor="middle" class="bk" font-size="22" fill="{RED}">{e["ex"]}</text>'
             f'<text x="387" y="118" text-anchor="middle" class="lb" font-size="6" fill="{BROWN}" letter-spacing="1">EVIDENCE</text></g>')
    st = T.t + .5
    b.append(stamp(236, 214, 170, 44, e["stamp"], e["ink"], st, rnd.choice([-7, -5, 6, 8]), 19))
    css = """
@keyframes cardUp{from{transform:translateY(120px)}to{transform:none}}
@keyframes dymo{from{opacity:0;transform:translateX(-12px)}to{opacity:1;transform:none}}
.card,.card2{animation:cardUp .8s cubic-bezier(.2,.9,.25,1.05) .2s both}
.card2{animation-delay:.2s}
.dymo{animation:dymo .35s ease-out both}
.tag{transform-box:view-box;transform-origin:372px 40px;animation:swing 3.2s ease-in-out infinite}
"""
    defs = "".join(T.defs) + ('<linearGradient id="tapeShine" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".18"/>'
                              '<stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".3"/></linearGradient>')
    return write(e["file"], svg(W, H, f"Exhibit {e['ex']}: {e['code']} ({e['repo']}). {' '.join(e['lines'])} Status: {e['stamp']}.",
                                "".join(b), css, defs))


# ═════════════════════════════ 4. SACRED TIMELINE MONITOR ═════════════════════════════
def monitor(data):
    W, H = 900, 540
    sx, sy, sw, sh = 70, 64, 620, 400   # screen
    T = Typist(2.6, 120, prefix="m")
    b = []
    # bezel (70s beige plastic)
    b.append('<rect x="24" y="22" width="852" height="496" rx="26" fill="url(#bezel)"/>'
             '<rect x="24" y="22" width="852" height="496" rx="26" filter="url(#paperTex)" opacity=".6"/>'
             '<rect x="46" y="42" width="668" height="444" rx="22" fill="#3a2f22"/>')
    b.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="26" fill="#140a03"/>')
    # control column
    b.append('<rect x="736" y="52" width="118" height="430" rx="10" fill="#b8a582"/>'
             '<text x="795" y="80" text-anchor="middle" class="lb" font-size="8" fill="#4a3a26" letter-spacing="2">TEMPORAL</text>'
             '<text x="795" y="92" text-anchor="middle" class="lb" font-size="8" fill="#4a3a26" letter-spacing="2">MONITOR MK-II</text>')
    for i, (lbl, ang) in enumerate([("BRANCH", 40), ("FLUX", -60)]):
        cy = 140 + i * 92
        b.append(f'<circle cx="795" cy="{cy}" r="30" fill="#2b2118"/><circle cx="795" cy="{cy}" r="24" fill="url(#knob)"/>'
                 f'<g class="knob{i}" style="transform-origin:795px {cy}px"><path d="M795 {cy-20}V{cy-8}" stroke="#f2e6cc" stroke-width="3" stroke-linecap="round"/></g>'
                 f'<text x="795" y="{cy+46}" text-anchor="middle" class="lb" font-size="7.5" fill="#4a3a26" letter-spacing="1.6">{lbl}</text>')
    for i in range(9):
        b.append(f'<rect x="760" y="{340+i*9}" width="70" height="4" rx="2" fill="#4a3a26" opacity=".75"/>')
    b.append(f'<circle cx="772" cy="452" r="5" fill="#ff5a2a" class="lamp"/><text x="784" y="455" class="lb" font-size="7.5" fill="#4a3a26" letter-spacing="1.4">NEXUS</text>')
    # screen contents (clipped to the tube)
    s = []
    s.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="url(#phosphor)"/>')
    s.append(f'<text x="{sx+24}" y="{sy+30}" class="ty" font-size="11" fill="{AMBER}" letter-spacing="1">SACRED TIMELINE  ·  BRANCH S-12</text>')
    s.append(f'<text x="{sx+sw-24}" y="{sy+30}" text-anchor="end" class="ty lamp" font-size="11" fill="{AMBER2}">● LIVE</text>')
    s.append(f'<path d="M{sx+20} {sy+40}H{sx+sw-20}" stroke="{AMBER}" stroke-opacity=".4"/>')
    # the filament: main strand + branches sprouting at events
    my = sy + 132
    main = f"M{sx+20} {my} C {sx+150} {my-6}, {sx+260} {my+6}, {sx+330} {my} S {sx+520} {my-4}, {sx+sw-20} {my}"
    s.append(f'<path class="dr fil" d="{main}" fill="none" stroke="#fff3d6" stroke-width="2.2" filter="url(#glow)" style="--len:700;stroke-dasharray:700;stroke-dashoffset:700"/>')
    s.append(f'<path class="dr fil" d="{main}" fill="none" stroke="{AMBER2}" stroke-width="7" stroke-opacity=".25" style="stroke-dasharray:700;stroke-dashoffset:700"/>')
    pts = [(sx + 60, -1), (sx + 160, 1), (sx + 270, -1), (sx + 370, 1), (sx + 455, -1), (sx + 525, 1)]
    for i, ((x, dirn), (ev, *_rest, state)) in enumerate(zip(pts, TIMELINE)):
        l = 34 + (i % 3) * 10
        x2 = x + 34
        y2 = my + dirn * l
        sub = f"M{x} {my} Q {x+12} {my+dirn*l*.8}, {x2} {y2}"
        sub2 = f"M{x+14} {my+dirn*l*.45} q 10 {dirn*6}, 22 {dirn*4}"
        op = "1" if state in ("past", "now") else ".55"
        dash = "" if state != "secret" else 'stroke-dasharray="3 4"'
        s.append(f'<g opacity="{op}"><path d="{sub}" fill="none" stroke="#ffe1a8" stroke-width="1.4" filter="url(#glow)" class="br" style="animation-delay:{1+i*.18:.2f}s" {dash}/>'
                 f'<path d="{sub2}" fill="none" stroke="#ffe1a8" stroke-width="1" class="br" style="animation-delay:{1.2+i*.18:.2f}s"/>'
                 f'<circle cx="{x}" cy="{my}" r="{5 if state=="now" else 3.4}" fill="{"#fff" if state!="secret" else "none"}" stroke="#fff3d6" filter="url(#glow)"/>'
                 f'<text x="{x2+4}" y="{y2 + (4 if dirn>0 else 0) + dirn*8:.0f}" class="ty fi" font-size="9.5" fill="{AMBER}" {d(1.4+i*.18)}>{ev}</text></g>')
    nx = pts[2][0]
    s.append(f'<circle cx="{nx}" cy="{my}" r="6" fill="none" stroke="#fff" class="ping"/><circle cx="{nx}" cy="{my}" r="6" fill="none" stroke="#fff" class="ping" style="animation-delay:1s"/>')
    # pulse travelling along the strand
    s.append(f'<circle r="4" fill="#fff" filter="url(#glow)"><animateMotion path="{main}" dur="3.5s" begin="2s" repeatCount="indefinite"/></circle>')
    # live activity feed (GitHub events) — falls back to milestones when quiet
    ty0 = sy + 222
    s.append(f'<text x="{sx+24}" y="{ty0}" class="ty" font-size="10.5" fill="{AMBER2}" xml:space="preserve">TYPE    REPO                  DETAIL           DATE</text>')
    s.append(f'<text x="{sx+sw-24}" y="{ty0}" text-anchor="end" class="ty" font-size="9" fill="{AMBER}" opacity=".7">LIVE FEED · GITHUB</text>')
    s.append(f'<path d="M{sx+24} {ty0+7}H{sx+sw-24}" stroke="{AMBER}" stroke-opacity=".35"/>')
    feed = [(e["type"], e["repo"], e["detail"], fmt_date(e["date"])) for e in data.get("events", [])][:6]
    if len(feed) < 6:
        feed += [("PLAN", ev, st_, dt) for ev, dt, loc, st_, state in TIMELINE if state in ("now", "next", "secret")][:6 - len(feed)]
    for i, (typ, repo, det, dt) in enumerate(feed):
        row = f"{typ:<8}{repo[:20]:<22}{det[:15]:<17}{dt}"
        col = "#fff3d6" if i == 0 else (AMBER if typ != "PLAN" else "#c98a3c")
        s.append(T(row, sx + 24, ty0 + 26 + i * 19, 10.5, col))
    # alarm box
    s.append(f'<g class="alarm"><rect x="{sx+sw-210}" y="{sy+52}" width="186" height="26" fill="{AMBER2}"/>'
             f'<text x="{sx+sw-117}" y="{sy+69}" text-anchor="middle" class="ty" font-size="10.5" fill="#140a03">NEXUS EVENT DETECTED</text></g>')
    # menu bar
    s.append(f'<rect x="{sx}" y="{sy+sh-30}" width="{sw}" height="30" fill="{AMBER}" opacity=".92"/>'
             f'<text x="{sx+24}" y="{sy+sh-11}" class="ty" font-size="10.5" fill="#140a03" xml:space="preserve">F1 LOG   F2 PRUNE   F3 BRANCH   F4 HIRE THIS VARIANT</text>')
    s.append(f'<rect x="{sx+sw-36}" y="{sy+sh-21}" width="8" height="12" fill="#140a03" class="lamp"/>')
    # CRT overlays
    s.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="url(#scan)"/>')
    s.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="url(#vign)"/>')
    s.append(f'<rect class="roll" x="{sx}" y="{sy}" width="{sw}" height="60" fill="url(#rollG)"/>')
    s.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="#fff" class="powerOn"/>')
    b.append(f'<g clip-path="url(#tube)"><g class="flick">{"".join(s)}</g></g>')
    b.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="26" fill="url(#glass)"/>')
    b.append('<text x="380" y="506" text-anchor="middle" class="lb" font-size="8" fill="#5a4730" letter-spacing="3">PROPERTY OF THE TIME VARIANCE AUTHORITY</text>')
    css = """
@keyframes flick{0%,100%{opacity:1}48%{opacity:.94}50%{opacity:.99}52%{opacity:.92}}
@keyframes powerOn{0%{opacity:1;transform:scaleY(.01)}35%{opacity:1;transform:scaleY(.02)}60%{opacity:.8;transform:scaleY(1)}100%{opacity:0;transform:scaleY(1)}}
@keyframes roll{from{transform:translateY(-60px)}to{transform:translateY(470px)}}
@keyframes ping{0%{transform:scale(.6);opacity:.9}100%{transform:scale(3.2);opacity:0}}
@keyframes alarm{0%,49%{opacity:1}50%,100%{opacity:0}}
@keyframes k0{0%,100%{transform:rotate(-40deg)}50%{transform:rotate(60deg)}}
@keyframes k1{0%,100%{transform:rotate(30deg)}50%{transform:rotate(-70deg)}}
.flick{animation:flick 4s steps(8) infinite}
.powerOn{transform-box:view-box;transform-origin:380px 264px;animation:powerOn .9s ease-out .2s both}
.roll{animation:roll 6s linear infinite}
.ping{transform-box:fill-box;transform-origin:center;animation:ping 2s ease-out 2s infinite}
.alarm{animation:alarm 1s steps(1) 2.4s infinite;opacity:0}
.fil{animation:draw 1.4s cubic-bezier(.6,0,.2,1) .6s forwards}
.br{stroke-dasharray:90;stroke-dashoffset:90;animation:draw .7s ease-out forwards}
.knob0{animation:k0 9s ease-in-out infinite}.knob1{animation:k1 7s ease-in-out infinite}
"""
    defs = "".join(T.defs) + (
        f'<clipPath id="tube"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="26"/></clipPath>'
        '<linearGradient id="bezel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e3d3b2"/><stop offset="1" stop-color="#b09a74"/></linearGradient>'
        '<radialGradient id="knob" cx=".35" cy=".3"><stop offset="0" stop-color="#6a5a48"/><stop offset="1" stop-color="#2b2118"/></radialGradient>'
        '<radialGradient id="phosphor" cx=".5" cy=".45" r=".75"><stop offset="0" stop-color="#2a1404"/><stop offset="1" stop-color="#0d0602"/></radialGradient>'
        '<radialGradient id="vign" cx=".5" cy=".5" r=".72"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient>'
        '<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".1"/><stop offset=".35" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="rollG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb347" stop-opacity="0"/><stop offset=".5" stop-color="#ffb347" stop-opacity=".06"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></linearGradient>'
        '<pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1.2" fill="#000" opacity=".45"/></pattern>')
    return write("03-sacred-timeline", svg(W, H, "Temporal Monitor: the Sacred Timeline of Variant S-12. " +
                                           "; ".join(f"{e} {dt} {loc} {st}" for e, dt, loc, st, _ in TIMELINE), "".join(b), css, defs))


# ═════════════════════════════ 5. REQUISITION TICKETS (vintage stubs) ═════════════════════════════
def ticket(file, word, line, serial, stock, ink, accent, delay):
    W, H = 430, 156
    shape = "M8 10H88A10 10 0 0 0 108 10H422V146H108A10 10 0 0 0 88 146H8Z"
    b = [f'<g class="tk" style="animation-delay:{delay}s">',
         f'<path d="{shape}" fill="#000" opacity=".35" transform="translate(4 5)" filter="url(#shadow)"/>',
         f'<path d="{shape}" fill="{stock}"/>',
         f'<path d="{shape}" filter="url(#paperTex)"/>',
         f'<path d="{shape}" filter="url(#blotch)" opacity=".35"/>',
         f'<rect x="114" y="18" width="300" height="120" fill="none" stroke="{ink}" stroke-width="1.6"/>',
         f'<rect x="118" y="22" width="292" height="112" fill="none" stroke="{ink}" stroke-width=".6"/>',
         f'<path d="M98 22V136" stroke="{ink}" stroke-width="1.4" stroke-dasharray="2 4"/>',
         # stub
         f'<g class="stub" style="transform-origin:98px 146px">'
         f'<rect x="16" y="18" width="74" height="120" fill="none" stroke="{ink}" stroke-width="1.2"/>'
         f'<text transform="translate(44 78) rotate(-90)" text-anchor="middle" class="bk" font-size="17" fill="{ink}" letter-spacing="2">ADMIT ONE</text>'
         f'<text transform="translate(70 78) rotate(-90)" text-anchor="middle" class="ty" font-size="10" fill="{accent}">Nº {serial}</text></g>',
         # main
         f'<text x="130" y="40" class="lb" font-size="7.5" fill="{ink}" letter-spacing="2.2">TVA · REQUISITION FORM {"27-B" if word == "EMAIL" else "27-C"}</text>',
         f'<text x="129" y="94" class="bk" font-size="50" fill="{ink}" textLength="{min(len(word) * 31, 182)}" lengthAdjust="spacingAndGlyphs">{esc(word)}</text>',
         f'<text x="130" y="114" class="ty" font-size="10.5" fill="{ink}">{esc(line)}</text>',
         f'<text x="130" y="128" class="lb" font-size="7" fill="{ink}" letter-spacing="1.8" opacity=".75">TO: VARIANT S-12 · VALID FOR ALL TIME</text>',
         f'<text transform="translate(404 78) rotate(90)" text-anchor="middle" class="ty" font-size="9.5" fill="{accent}">Nº {serial}</text>',
         # round date stamp
         f'<g class="stamp" style="animation-delay:{delay+.8:.2f}s;--r:-14deg;--r0:-6deg" filter="url(#roughInk)">'
         f'<circle cx="358" cy="82" r="26" fill="none" stroke="{RED}" stroke-width="2.4"/><circle cx="358" cy="82" r="20.5" fill="none" stroke="{RED}" stroke-width=".9"/>'
         f'<text x="358" y="79" text-anchor="middle" class="bk" font-size="8.5" fill="{RED}" letter-spacing="1">OPEN</text>'
         f'<text x="358" y="91" text-anchor="middle" class="bk" font-size="8.5" fill="{RED}" letter-spacing="1">24 / 7</text></g>',
         '</g>']
    css = """
@keyframes tk{0%{opacity:0;transform:translateY(-26px) rotate(-2.5deg)}100%{opacity:1;transform:none}}
@keyframes tear{0%,82%,100%{transform:none}86%{transform:rotate(-4deg)}90%{transform:rotate(1.5deg)}94%{transform:rotate(-1deg)}}
.tk{animation:tk .6s cubic-bezier(.2,.9,.3,1.2) both}
.stub{animation:tear 5s ease-in-out 2s infinite}
"""
    return write(file, svg(W, H, f"{word}: {line}", "".join(b), css))


# ═════════════════════════════ 6. CIRCULATION RECORD (live footer) ═════════════════════════════
def footer(now, data):
    W, H = 900, 330
    rows = [("02 NOV 2026", "FILE OPENED · FIRST REPOSITORY", "TVA", "#1d2a6b")]
    for e in [e for e in data.get("events", []) if not (e["type"] == "CREATE" and e["date"] <= "2026-11-02")][:2]:
        if e["date"] >= "2026-11-02":
            dt = datetime.strptime(e["date"], "%Y-%m-%d").strftime("%d %b %Y").upper()
            rows.append((dt, f'{e["type"]} · {e["repo"]} · {e["detail"]}'[:40], "S-12", "#6b2a7a"))
    rows.sort(key=lambda r: datetime.strptime(r[0], "%d %b %Y"))
    rows.append((now.strftime("%d %b %Y").upper(), "DAILY SYNC · FILE RE-FORGED", "TVA", "#1d2a6b"))
    days = (DOOMSDAY.date() - now.date()).days
    rows.append(("18 DEC 2026", "DATE DUE · DOOMSDAY" + (f"  (T-{days})" if days > 0 else ""), "V.V.D.", RED))
    rnd = random.Random(7)
    b = ['<g class="drop">',
         '<rect x="30" y="30" width="852" height="286" rx="3" fill="#000" opacity=".5" filter="url(#shadow)"/>',
         paper(20, 20, 860, 290, "#efe6cf", "#c4b08a"),
         f'<rect x="20" y="20" width="860" height="8" fill="{ORANGE}"/>',
         '<text x="44" y="62" class="se" font-size="19" fill="#2a1a10" letter-spacing="4">CIRCULATION RECORD</text>',
         f'<text x="44" y="80" class="lb" font-size="8" fill="#7b5b3d" letter-spacing="2.2">CASE FILE S-12 · DO NOT REMOVE THIS CARD FROM THE TIMELINE</text>']
    # grid
    gx0, gx1, gx2, gx3 = 44, 184, 520, 596
    gy0, rh = 96, 30
    b.append(f'<rect x="{gx0}" y="{gy0}" width="{gx3-gx0}" height="{rh*7}" fill="none" stroke="#7b5b3d" stroke-opacity=".7"/>')
    for i in range(1, 7):
        b.append(f'<path d="M{gx0} {gy0+i*rh}H{gx3}" stroke="#8fb3d9" stroke-opacity=".55"/>')
    for x in (gx1, gx2):
        b.append(f'<path d="M{x} {gy0}V{gy0+rh*7}" stroke="{RED}" stroke-opacity=".45"/>')
    for x, t in ((gx0 + 10, "DATE"), (gx1 + 10, "ACTIVITY"), (gx2 + 10, "BY")):
        b.append(f'<text x="{x}" y="{gy0+19}" class="lb" font-size="8.5" fill="#7b5b3d" letter-spacing="2">{t}</text>')
    for i, (dt, act, by, ink) in enumerate(rows[:6]):
        y = gy0 + rh * (i + 1) + 20
        rot = rnd.uniform(-2.5, 2.5)
        dl = .7 + i * .35
        b.append(f'<g class="stamp" style="animation-delay:{dl:.2f}s;--r:{rot:.1f}deg;--r0:{rot+5:.1f}deg" filter="url(#inkLight)">'
                 f'<text x="{gx0+10}" y="{y}" class="bk" font-size="14.5" fill="{ink}" letter-spacing="1">{dt}</text></g>')
        b.append(f'<text x="{gx1+10}" y="{y}" class="ty fi" font-size="11.5" fill="{INK}" {d(dl+.15)}>{esc(act)}</text>')
        b.append(f'<text x="{gx2+10}" y="{y}" class="ty fi" font-size="11" fill="#7b5b3d" {d(dl+.15)}>{esc(by)}</text>')
        if ink == RED:
            b.append(f'<rect x="{gx1+6}" y="{y-16}" width="{len(act)*6.9+10:.0f}" height="22" fill="none" stroke="{RED}" stroke-width="1.3" class="fi" {d(dl+.3)}/>')
    # clock + sign-off
    cx, cy = 744, 128
    ticks = "".join(f'<line x1="{cx+46*math.cos(math.radians(i*30)):.1f}" y1="{cy+46*math.sin(math.radians(i*30)):.1f}" '
                    f'x2="{cx+38*math.cos(math.radians(i*30)):.1f}" y2="{cy+38*math.sin(math.radians(i*30)):.1f}" stroke="{BROWN}" stroke-width="{3 if i % 3 == 0 else 1.6}"/>' for i in range(12))
    b += [f'<circle cx="{cx}" cy="{cy}" r="58" fill="{BROWN}"/><circle cx="{cx}" cy="{cy}" r="52" fill="#f3e3c0"/>{ticks}',
          f'<g class="hh" style="transform-origin:{cx}px {cy}px"><path d="M{cx} {cy}V{cy-24}" stroke="{BROWN}" stroke-width="5" stroke-linecap="round"/></g>',
          f'<g class="mh" style="transform-origin:{cx}px {cy}px"><path d="M{cx} {cy}V{cy-38}" stroke="{BROWN}" stroke-width="3" stroke-linecap="round"/></g>',
          f'<g class="sh" style="transform-origin:{cx}px {cy}px"><path d="M{cx} {cy+8}V{cy-42}" stroke="{RED}" stroke-width="1.4"/></g>',
          f'<circle cx="{cx}" cy="{cy}" r="4" fill="{RED}"/>',
          f'<text x="{cx}" y="222" text-anchor="middle" class="se" font-size="15" fill="#2a1a10" letter-spacing="2.4">FOR ALL TIME. ALWAYS.</text>',
          f'<text x="{cx}" y="246" text-anchor="middle" class="lb" font-size="8" fill="{ORANGE}" letter-spacing="2">THIS FILE UPDATES ITSELF</text>',
          f'<text x="{cx}" y="260" text-anchor="middle" class="lb" font-size="8" fill="{ORANGE}" letter-spacing="2">DO NOT PRUNE</text>',
          f'<text x="{cx}" y="292" text-anchor="middle" class="ty" font-size="8.5" fill="#7b5b3d">fan-made · not affiliated with Marvel</text>',
          '</g>']
    css = DROP_CSS + """
@keyframes rot{to{transform:rotate(360deg)}}
.sh{animation:rot 60s steps(60) infinite}
.mh{animation:rot 3600s linear infinite}
.hh{animation:rot 43200s linear infinite}
"""
    return write("09-circulation-record", svg(W, H, "TVA circulation record: " + "; ".join(f"{a} {b_}" for a, b_, _, _ in rows) + ". For all time. Always.",
                                              "".join(b), css))


def main():
    now = datetime.now(IST)
    data = load_data(now)
    built = [ticker(now, data), arrest_record(data),
             tab("02-tab-evidence", "TVA · PROPERTY ROOM", "EVIDENCE LOCKER", "PROJECTS  ·  SHIPPED & IN THE FORGE"),
             *[exhibit(e, i, data) for i, e in enumerate(EXHIBITS)],
             monitor(data), quartermaster(data),
             tab("06-tab-requisition", "TVA · FORMS & REQUESTS", "REQUISITION DESK", "CONTACT THE VARIANT  ·  NO WAITING LINE", "#e0a35e"),
             ticket("07-ticket-email", "EMAIL", "send a transmission to the variant", "000427", "#e9d8b4", BROWN, RED, 0),
             ticket("08-ticket-linkedin", "LINKEDIN", "connect on the professional timeline", "000428", "#e2965c", BROWN, "#5a1c0c", .2),
             footer(now, data)]
    for p in built:
        print(f"forged {os.path.relpath(p, ROOT):34s} {os.path.getsize(p)//1024:>4} KB")


if __name__ == "__main__":
    main()
