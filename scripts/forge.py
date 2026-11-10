#!/usr/bin/env python3
"""
DOOMSDAY BUILD — renders every panel of the srivathsa12 GitHub profile as an animated SVG.

Standard library only, so the nightly GitHub Action runs it with no installs.
Live data (repos, activity, languages) comes from the GitHub API and is cached in data.json.
Edit the CONTENT block, then run:  python scripts/forge.py
"""
import base64
import hashlib
import json
import math
import os
import random
import textwrap
import urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "scripts")
OUT = os.path.join(ROOT, "assets")
IST = timezone(timedelta(hours=5, minutes=30))
USER = "srivathsa12"

# ═════════════════════════════ CONTENT ═════════════════════════════
NAME = "Srivathsa Sherla"
LINE_1 = "AI & Machine Learning undergrad at Newton School of Technology."
LINE_2 = "I build agents, automations and interactive things for the web."

PROJECTS = [  # title, repo (or None), status, description, tags
    ("Interactive 3D Portfolio", "my-portfolio", "live",
     "A personal portfolio with a Three.js particle portrait that reacts to the cursor, "
     "plus a terminal-style log of what I'm learning. One HTML file, no build step.",
     ["THREE.JS", "JAVASCRIPT", "HTML / CSS"]),
    ("Digital Detective", "digital-detective-8490", "coursework",
     "A Python assignment in nine missions (0–8). Each mission is solved with its own "
     "script and committed step by step, from setup to the final case.",
     ["PYTHON", "GIT", "COMMAND LINE"]),
    ("Scheduled Python Tasks", "scheduled-tasks", "fork",
     "Runs a Python script automatically on a schedule using GitHub Actions cron jobs. "
     "Forked to learn how CI automation works end to end.",
     ["PYTHON", "GITHUB ACTIONS"]),
    ("WhatsApp Auto-Reply Bot", None, "building",
     "Replies to customers instantly: sends a welcome image, lists the services and "
     "shares contact buttons. Built for a local wellness centre.",
     ["WHATSAPP", "AUTOMATION"]),
    ("WhatsApp Business Automation", None, "building",
     "Follow-ups, appointment reminders and routine replies on autopilot, so a small "
     "business owner isn't stuck answering the same questions all day.",
     ["WHATSAPP", "AUTOMATION", "NODE / PYTHON"]),
    ("Self-Updating GitHub Profile", "srivathsa12", "live",
     "This page. A Python script draws every panel as an animated SVG from live GitHub "
     "data, and GitHub Actions rebuilds it every night.",
     ["PYTHON", "SVG", "GITHUB ACTIONS"]),
]
TOOLKIT = [("Python", "#86efac"), ("JavaScript", "#86efac"), ("HTML", "#86efac"), ("CSS", "#86efac"),
           ("Three.js", "#6b7178"), ("Git", "#6b7178"), ("GitHub Actions", "#6b7178"), ("VS Code", "#6b7178")]
LEARNING = [("Agentic AI", "tools · memory · planning loops"),
            ("Generative AI", "LLM APIs · prompting · RAG")]
EMAIL = "sherlasrivathsa12@gmail.com"
LINKEDIN = "linkedin.com/in/srivathsa-sherla"

# ═════════════════════════════ DESIGN TOKENS ═════════════════════════════
BG, SURF, CARD = "#08090a", "#0c0d0f", "#101214"
HAIR, HAIR2 = "rgba(255,255,255,.08)", "rgba(255,255,255,.14)"
TXT, MUTED, DIM = "#f7f8f8", "#8a8f98", "#5b6169"
G, G2, GOLD = "#86efac", "#34d399", "#e2c47a"
EXPO = "cubic-bezier(.19,1,.22,1)"

B64 = {n: open(os.path.join(HERE, "fonts", n + ".b64")).read().strip() for n in ("disp", "dispL", "body", "med", "mono", "blk")}


ANTON = open(os.path.join(HERE, "fonts", "anton.b64")).read().strip()


def tex(name):
    with open(os.path.join(HERE, "tex", name + ".jpg"), "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


FONT_CSS = f"@font-face{{font-family:'DAnton';src:url(data:font/woff2;base64,{ANTON}) format('woff2')}}" + "".join(f"@font-face{{font-family:'D{n}';src:url(data:font/woff;base64,{v}) format('woff')}}" for n, v in B64.items()) + (
    ".h{font-family:'Ddisp','Inter',system-ui,sans-serif;font-weight:600}"
    ".hl{font-family:'DdispL','Inter',system-ui,sans-serif;font-weight:300}"
    ".b{font-family:'Dbody','Inter',system-ui,sans-serif;font-weight:400}"
    ".m{font-family:'Dmed','Inter',system-ui,sans-serif;font-weight:500}"
    ".a{font-family:'DAnton',Impact,'Arial Narrow Bold',sans-serif;font-weight:400}"
    ".x{font-family:'Dblk','Inter',system-ui,sans-serif;font-weight:900}"
    ".c{font-family:'Dmono','SFMono-Regular',Menlo,Consolas,monospace}")

BASE_CSS = f"""
@keyframes in{{from{{opacity:0;transform:translateY(14px);filter:blur(8px)}}to{{opacity:1;transform:none;filter:blur(0)}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
@keyframes pulse{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}
@keyframes ping{{0%{{transform:scale(1);opacity:.7}}100%{{transform:scale(2.8);opacity:0}}}}
.in{{animation:in 1.1s {EXPO} both}}
.fa{{animation:fade 1.4s ease both}}
.pu{{animation:pulse 2.6s ease-in-out infinite}}
.pg{{transform-box:fill-box;transform-origin:center;animation:ping 2.2s ease-out infinite}}
@keyframes rise{{from{{transform:translateY(1.15em)}}to{{transform:none}}}}
@keyframes pop{{0%{{opacity:0;transform:scale(.6)}}60%{{opacity:1;transform:scale(1.06)}}100%{{opacity:1;transform:scale(1)}}}}
.rise{{animation:rise 1.1s {EXPO} both}}
.pop{{transform-box:fill-box;transform-origin:center;animation:pop .7s cubic-bezier(.34,1.56,.64,1) both}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""

GRAIN = ('<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="3" stitchTiles="stitch"/>'
         '<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .07 0"/></filter>')


def dl(s):
    return f'style="animation-delay:{s:.2f}s"'


def svg(w, h, label, body, css="", defs="", radius=16, frame=True):
    border = f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{radius}" fill="none" stroke="{HAIR}"/>' if frame else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
            f'<title>{esc(label)}</title><defs><clipPath id="frame"><rect width="{w}" height="{h}" rx="{radius}"/></clipPath>{GRAIN}{defs}</defs>'
            f'<style>{FONT_CSS}{BASE_CSS}{css}</style>'
            f'<g clip-path="url(#frame)">{body}' + (f'<rect width="{w}" height="{h}" filter="url(#grain)"/>' if frame else '') + f'</g>{border}</svg>')


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name + ".svg")
    with open(p, "w") as f:
        f.write(content)
    return p


def tw(text, size, k=.54):
    """Approximate rendered width of Inter text."""
    return len(text) * size * k


def embers(n, x0, x1, ybase, rise, seed, color=G, size=(0.8, 2.2), dur=(5, 9)):
    """Glowing particles drifting upward; each loops on its own rhythm."""
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = rnd.uniform(x0, x1)
        r = rnd.uniform(*size)
        d = rnd.uniform(*dur)
        dx = rnd.uniform(-22, 22)
        out.append(f'<circle cx="{x:.1f}" cy="{ybase}" r="{r:.1f}" fill="{color}" opacity="0">'
                   f'<animate attributeName="cy" values="{ybase};{ybase-rise:.0f}" dur="{d:.1f}s" begin="{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="cx" values="{x:.1f};{x+dx:.1f}" dur="{d:.1f}s" begin="{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="opacity" values="0;.9;.6;0" keyTimes="0;.2;.7;1" dur="{d:.1f}s" begin="{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def counter(x, y, final, size, begin, cls="h", fill=TXT, anchor="start", ls="-.8"):
    """Counts up to a number, or 'decodes' text from scrambled glyphs, then holds."""
    if final.isdigit():
        n = int(final)
        steps = sorted(set([round(n * k / 12) for k in range(13)]))
        frames = [str(v) for v in steps]
    else:
        rnd = random.Random(final)
        pool = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789#%&*"
        frames = []
        for k in range(9):
            keep = round(len(final) * k / 8)
            frames.append("".join(c if (i < keep or c == " ") else rnd.choice(pool) for i, c in enumerate(final)))
    out = []
    step = .07
    for i, fr in enumerate(frames):
        t0 = begin + i * step
        last = i == len(frames) - 1
        sets = f'<set attributeName="opacity" to="1" begin="{t0:.2f}s"/>'
        if not last:
            sets += f'<set attributeName="opacity" to="0" begin="{t0+step:.2f}s"/>'
        out.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}" font-size="{size}" fill="{fill}" letter-spacing="{ls}" opacity="0">{esc(fr)}{sets}</text>')
    return "".join(out)


def heading(x, y, text, size=36, delay=.05, fill=TXT, cid="hc", anchor="start"):
    """Poster heading in Anton that rises out of a hidden edge."""
    return (f'<clipPath id="{cid}"><rect x="{x-6 if anchor == "start" else 0}" y="{y-size*1.02:.0f}" width="900" height="{size*1.22:.0f}"/></clipPath>'
            f'<g clip-path="url(#{cid})"><text x="{x}" y="{y}" text-anchor="{anchor}" class="a rise" font-size="{size}" fill="{fill}" letter-spacing=".6" {dl(delay)}>{esc(text.upper())}</text></g>')


def kicker(x, y, num, label, color=G, delay=0):
    return (f'<text x="{x}" y="{y}" class="c in" font-size="11" fill="{color}" letter-spacing="1.6" {dl(delay)}>{num}</text>'
            f'<text x="{x+30}" y="{y}" class="c in" font-size="11" fill="{DIM}" letter-spacing="1.6" {dl(delay)}>{esc(label)}</text>')


# ═════════════════════════════ LIVE DATA ═════════════════════════════
DATA_FILE = os.path.join(HERE, "data.json")
SEED = {
    "repos": [
        {"name": "my-portfolio", "language": "HTML", "stars": 0, "fork": False, "pushed": "2026-11-02"},
        {"name": "scheduled-tasks", "language": "Python", "stars": 0, "fork": True, "pushed": ""},
        {"name": "srivathsa12", "language": "Python", "stars": 0, "fork": False, "pushed": "2026-11-07"},
        {"name": "digital-detective-8490", "language": "Python", "stars": 0, "fork": False, "pushed": "2026-11-09"},
    ],
    "events": [
        {"type": "PUSH", "repo": "digital-detective-8490", "detail": "commits", "date": "2026-11-09", "n": 3},
        {"type": "CREATE", "repo": "digital-detective-8490", "detail": "new repository", "date": "2026-11-08", "n": 0},
        {"type": "PUSH", "repo": "srivathsa12", "detail": "commits", "date": "2026-11-07", "n": 2},
        {"type": "PUSH", "repo": "my-portfolio", "detail": "commits", "date": "2026-11-02", "n": 1},
        {"type": "CREATE", "repo": "my-portfolio", "detail": "new repository", "date": "2026-11-02", "n": 0},
    ],
    "synced": "seed",
}


def _api(path):
    req = urllib.request.Request("https://api.github.com" + path, headers={
        "Accept": "application/vnd.github+json", "User-Agent": f"{USER}-profile"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", "Bearer " + tok)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def load_data(now):
    data = SEED
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            data = json.load(f)
    if os.environ.get("FORGE_OFFLINE"):
        return data
    try:
        repos = _api(f"/users/{USER}/repos?per_page=100&sort=pushed")
        events = _api(f"/users/{USER}/events/public?per_page=100")
        ev = []
        for e in events:
            t, repo, date, p = e["type"], e["repo"]["name"].split("/")[-1], e["created_at"][:10], e.get("payload", {})
            if t == "PushEvent":
                n = p.get("size") or len(p.get("commits", [])) or 1
                ev.append({"type": "PUSH", "repo": repo, "detail": "commits", "date": date, "n": n})
            elif t == "CreateEvent":
                ev.append({"type": "CREATE", "repo": repo, "detail": "new " + (p.get("ref_type") or "repository"), "date": date, "n": 0})
            elif t == "PullRequestEvent":
                ev.append({"type": "PR", "repo": repo, "detail": "pull request " + (p.get("action") or ""), "date": date, "n": 0})
            elif t == "IssuesEvent":
                ev.append({"type": "ISSUE", "repo": repo, "detail": "issue " + (p.get("action") or ""), "date": date, "n": 0})
            elif t == "ForkEvent":
                ev.append({"type": "FORK", "repo": repo, "detail": "forked", "date": date, "n": 0})
        data = {"repos": [{"name": r["name"], "language": r.get("language"), "stars": r.get("stargazers_count", 0),
                           "fork": r.get("fork", False), "pushed": (r.get("pushed_at") or "")[:10]} for r in repos],
                "events": ev, "synced": now.strftime("%Y-%m-%d")}
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=1)
        print("live data:", len(data["repos"]), "repos,", len(ev), "events")
    except Exception as ex:
        print("using cached data:", ex)
    return data


def fmt(iso, long=False):
    try:
        d = datetime.strptime(iso, "%Y-%m-%d")
        return d.strftime("%d %b %Y" if long else "%d %b")
    except Exception:
        return "—"


def stats(data, now):
    repos = data["repos"]
    langs = {}
    for r in repos:
        if r.get("language"):
            langs[r["language"]] = langs.get(r["language"], 0) + 1
    cutoff = (now - timedelta(days=90)).strftime("%Y-%m-%d")
    commits = sum(e.get("n", 0) for e in data["events"] if e["type"] == "PUSH" and e["date"] >= cutoff)
    weeks = [0] * 12
    for e in data["events"]:
        if e["type"] == "PUSH":
            try:
                age = (now.date() - datetime.strptime(e["date"], "%Y-%m-%d").date()).days
            except Exception:
                continue
            if 0 <= age < 84:
                weeks[11 - age // 7] += e.get("n", 1)
    days30 = [0] * 30
    repos30 = set()
    for e in data["events"]:
        if e["type"] == "PUSH":
            try:
                age = (now.date() - datetime.strptime(e["date"], "%Y-%m-%d").date()).days
            except Exception:
                continue
            if 0 <= age < 30:
                days30[29 - age] += e.get("n", 1)
                repos30.add(e["repo"])
    last = max((r["pushed"] for r in repos if r.get("pushed")), default="")
    return dict(repos=len(repos), langs=langs, commits=commits, weeks=weeks, last=last, days30=days30, repos30=len(repos30),
                top=max(langs, key=langs.get) if langs else "—")


# ═════════════════════════════ 1. HERO ═════════════════════════════
def hero():
    W, H = 900, 480
    cx, cy, r = 450, 148, 64
    flare = []
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<image href="{tex("hero")}" width="{W}" height="540" y="-30" opacity=".55" mask="url(#heroMask)" class="fa" {dl(.1)}/>',
         f'<rect width="{W}" height="{H}" fill="url(#vign)"/>',
         # film dust flicker (two offset copies alternate)
         f'<g opacity=".22" style="mix-blend-mode:screen"><image href="{tex("film")}" width="{W}" height="540" y="-30" class="d1"/>'
         f'<image href="{tex("film")}" width="{W}" height="540" y="-30" transform="translate({W} 0) scale(-1 1)" class="d2"/></g>',
         # eclipse
         f'<circle cx="{cx}" cy="{cy}" r="{r*2.6}" fill="url(#corona)" class="cor"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r+3}" fill="none" stroke="{G}" stroke-width="2.2" filter="url(#glow)" class="ring" '
         f'style="stroke-dasharray:{2*math.pi*(r+3):.0f};stroke-dashoffset:{2*math.pi*(r+3):.0f}" transform="rotate(-90 {cx} {cy})"/>',
         f'<g class="rays" style="transform-origin:{cx}px {cy}px">' + "".join(
             f'<path d="M{cx} {cy-r-10}L{cx} {cy-r-10-(26 if k % 3 == 0 else 12)}" stroke="{G}" stroke-opacity="{.35 if k % 3 == 0 else .15}" stroke-width="1.2" '
             f'transform="rotate({k*10} {cx} {cy})"/>' for k in range(36)) + '</g>',
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BG}"/>',
         embers(26, 120, 780, 470, 300, 11),
         f'<g class="orbit" style="transform-origin:{cx}px {cy}px"><circle cx="{cx+r+2}" cy="{cy}" r="3.2" fill="#fff" filter="url(#glow2)"/></g>',
         # type
         f'<text x="{cx}" y="268" text-anchor="middle" class="hl in" font-size="13" fill="{G}" letter-spacing="13" {dl(1.0)}>DOOMSDAY</text>',
         f'<text x="{cx}" y="330" text-anchor="middle" class="h in" font-size="54" fill="{TXT}" letter-spacing="-1.6" {dl(1.15)}>{esc(NAME)}</text>',
         f'<text x="{cx}" y="370" text-anchor="middle" class="b in" font-size="17" fill="{TXT}" letter-spacing="-.2" {dl(1.3)}>{esc(LINE_1)}</text>',
         f'<text x="{cx}" y="394" text-anchor="middle" class="b in" font-size="17" fill="{MUTED}" letter-spacing="-.2" {dl(1.38)}>{esc(LINE_2)}</text>']
    # pills
    pills = [("Open to work", G, True), ("Learning Agentic AI", None, False), ("@srivathsa12", None, False)]
    widths = [tw(t, 12.5, .56) + (40 if dot else 28) for t, _, dot in pills]
    x = cx - (sum(widths) + 10 * (len(pills) - 1)) / 2
    for i, ((t, col, dot), w) in enumerate(zip(pills, widths)):
        stroke = "rgba(134,239,172,.35)" if col else HAIR2
        fill = "rgba(134,239,172,.07)" if col else "rgba(255,255,255,.03)"
        g = f'<rect x="{x:.1f}" y="420" width="{w:.1f}" height="30" rx="15" fill="{fill}" stroke="{stroke}"/>'
        tx = x + 14
        if dot:
            g += (f'<circle cx="{x+16:.1f}" cy="435" r="3.5" fill="{G}"/><circle cx="{x+16:.1f}" cy="435" r="3.5" fill="none" stroke="{G}" class="pg"/>')
            tx = x + 27
        g += f'<text x="{tx:.1f}" y="439.5" class="m" font-size="12.5" fill="{TXT if col else MUTED}">{esc(t)}</text>'
        b.append(f'<g class="in" {dl(1.5+i*.08)}>{g}</g>')
        x += w + 10
    css = f"""
@keyframes ring{{to{{stroke-dashoffset:0}}}}
@keyframes cor{{0%{{opacity:0;transform:scale(.6)}}100%{{opacity:1;transform:scale(1)}}}}
@keyframes breathe{{0%,100%{{opacity:.85;transform:scale(1)}}50%{{opacity:1;transform:scale(1.06)}}}}
@keyframes orbit{{to{{transform:rotate(360deg)}}}}
@keyframes d1{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
@keyframes d2{{0%,49%{{opacity:0}}50%,100%{{opacity:1}}}}
.ring{{animation:ring 1.6s {EXPO} .2s forwards}}
.cor{{transform-box:fill-box;transform-origin:center;animation:cor 1.8s {EXPO} .5s both,breathe 6s ease-in-out 2.3s infinite}}
.orbit{{animation:fade 1s ease 1.6s both,orbit 18s linear 1.6s infinite}}
.rays{{animation:fade 2s ease 1.2s both,orbit 120s linear infinite}}
.d1{{animation:d1 .24s steps(1) infinite}}.d2{{animation:d2 .24s steps(1) infinite}}
"""
    defs = (f'<radialGradient id="corona"><stop offset=".36" stop-color="{G}" stop-opacity=".55"/><stop offset=".45" stop-color="{G2}" stop-opacity=".22"/>'
            f'<stop offset=".7" stop-color="{G2}" stop-opacity=".05"/><stop offset="1" stop-color="{G2}" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="mg" cx=".5" cy=".3" r=".62"><stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<mask id="heroMask"><rect width="{W}" height="{H}" fill="url(#mg)"/></mask>'
            f'<linearGradient id="vign" x1="0" y1="0" x2="0" y2="1"><stop offset=".45" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}" stop-opacity=".95"/></linearGradient>'
            '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            '<filter id="glow2" x="-400%" y="-400%" width="900%" height="900%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    return write("01-hero", svg(W, H, f"{NAME} — {LINE_1} {LINE_2} Open to work.", "".join(b), css, defs))


# ═════════════════════════════ 2. ACTIVITY (live bento) ═════════════════════════════
def activity(data, now):
    W, H = 900, 430
    st = stats(data, now)
    b = [f'<rect width="{W}" height="{H}" fill="{SURF}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#topglow)"/>',
         kicker(32, 42, "01", "LIVE FROM GITHUB"),
         heading(32, 84, "Activity", 34, .08),
         f'<text x="868" y="80" text-anchor="end" class="c in" font-size="11.5" fill="{MUTED}" {dl(.15)}>synced {"daily" if data.get("synced") == "seed" else fmt(data["synced"], True)}</text>']
    cards = [("Public repos", str(st["repos"]), ""), ("Commits · 90 days", str(st["commits"]), ""),
             ("Top language", st["top"], ""), ("Last push", fmt(st["last"]), "")]
    cw, gap, y0 = 199, 12, 104
    for i, (lab, val, _) in enumerate(cards):
        x = 32 + i * (cw + gap)
        b.append(f'<g class="in" {dl(.2+i*.07)}><rect x="{x}" y="{y0}" width="{cw}" height="96" rx="12" fill="{CARD}" stroke="{HAIR}"/>'
                 f'<text x="{x+18}" y="{y0+30}" class="b" font-size="12.5" fill="{MUTED}">{esc(lab)}</text>'
                 + counter(x + 18, y0 + 72, val, 30 if len(val) < 8 else 24, .5 + i * .12) + '</g>')
    # weekly commits chart
    y1 = 216
    b.append(f'<g class="in" {dl(.5)}><rect x="32" y="{y1}" width="410" height="182" rx="12" fill="{CARD}" stroke="{HAIR}"/>'
             f'<text x="50" y="{y1+30}" class="b" font-size="12.5" fill="{MUTED}">Last 30 days</text>'
             f'<text x="424" y="{y1+30}" text-anchor="end" class="m" font-size="12.5" fill="{TXT}">{sum(st["days30"])} commits · {st["repos30"]} repos</text></g>')
    mx = max(st["days30"]) or 1
    bw, bx0, base = 9, 51, y1 + 156
    for i, v in enumerate(st["days30"]):
        h = 8 + 92 * v / mx if v else 3
        col = G if v else "rgba(255,255,255,.09)"
        b.append(f'<rect x="{bx0+i*12.5:.1f}" y="{base-h:.1f}" width="{bw}" height="{h:.1f}" rx="2" fill="{col}" class="bar" style="animation-delay:{.6+i*.025:.2f}s"/>')
    b.append(f'<path d="M50 {base+.5}H424" stroke="{HAIR}"/>')
    b.append(f'<rect x="50" y="{y1+44}" width="2" height="{base-y1-44}" fill="url(#scanV)" class="scan"/>')
    # feed
    fx = 458
    b.append(f'<g class="in" {dl(.58)}><rect x="{fx}" y="{y1}" width="410" height="182" rx="12" fill="{CARD}" stroke="{HAIR}"/>'
             f'<text x="{fx+18}" y="{y1+30}" class="b" font-size="12.5" fill="{MUTED}">Recent activity</text>'
             f'<circle cx="{fx+392}" cy="{y1+26}" r="3.5" fill="{G}" class="pu"/></g>')
    b.append(f'<rect x="{fx+10}" y="{y1+46}" width="390" height="24" rx="6" fill="rgba(134,239,172,.06)" class="hi"/>')
    icon = {"PUSH": "↑", "CREATE": "+", "PR": "⇄", "ISSUE": "!", "FORK": "⑂"}
    for i, e in enumerate(data["events"][:5]):
        y = y1 + 62 + i * 26
        what = f'{e["n"]} commit{"s" if e["n"] != 1 else ""}' if e["type"] == "PUSH" else e["detail"]
        b.append(f'<g class="in" {dl(.8+i*.08)}><text x="{fx+18}" y="{y}" class="c" font-size="11.5" fill="{G}">{icon.get(e["type"], "•")}</text>'
                 f'<text x="{fx+36}" y="{y}" class="m" font-size="12.5" fill="{TXT}">{esc(e["repo"][:22])}</text>'
                 f'<text x="{fx+218}" y="{y}" class="b" font-size="12.5" fill="{MUTED}">{esc(what[:18])}</text>'
                 f'<text x="{fx+392}" y="{y}" text-anchor="end" class="c" font-size="11" fill="{DIM}">{fmt(e["date"])}</text></g>')
    css = f"""
@keyframes grow{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
.bar{{transform-box:fill-box;transform-origin:bottom;animation:grow .9s {EXPO} both}}
@keyframes scan{{0%{{transform:translateX(0);opacity:0}}10%{{opacity:1}}90%{{opacity:1}}100%{{transform:translateX(372px);opacity:0}}}}
.scan{{animation:scan 4.5s ease-in-out 1.5s infinite;opacity:0}}
@keyframes hi{{0%,18%{{transform:translateY(0)}}20%,38%{{transform:translateY(26px)}}40%,58%{{transform:translateY(52px)}}60%,78%{{transform:translateY(78px)}}80%,98%{{transform:translateY(104px)}}100%{{transform:translateY(0)}}}}
.hi{{animation:fade 1s ease 1.4s both,hi 10s {EXPO} 1.4s infinite}}
"""
    defs = (f'<linearGradient id="scanV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{G}" stop-opacity="0"/><stop offset=".5" stop-color="{G}" stop-opacity=".8"/><stop offset="1" stop-color="{G}" stop-opacity="0"/></linearGradient>'
            f'<radialGradient id="topglow" cx=".5" cy="0" r=".7"><stop offset="0" stop-color="{G2}" stop-opacity=".09"/><stop offset="1" stop-color="{G2}" stop-opacity="0"/></radialGradient>')
    return write("02-activity", svg(W, H, f"Activity: {st['repos']} public repos, {st['commits']} commits in 90 days, top language {st['top']}, last push {fmt(st['last'], True)}.",
                                    "".join(b), css, defs))


# ═════════════════════════════ 3. PROJECTS ═════════════════════════════
def projects_header():
    W, H = 900, 96
    b = [kicker(4, 34, "02", "SELECTED WORK"),
         heading(4, 78, "Projects", 38, .08),
         f'<text x="{4+tw("PROJECTS", 38, .45)+18:.0f}" y="76" class="b in" font-size="17" fill="{MUTED}" {dl(.2)}>Shipped, in progress, and what I\'m learning from.</text>']
    return write("03-projects", svg(W, H, "Projects", "".join(b), frame=False, radius=0))


STATUS = {"live": ("Live", G), "building": ("In progress", GOLD), "fork": ("Fork", MUTED), "coursework": ("Coursework", "#93c5fd")}


def motif(kind, cx, cy):
    """A small living illustration per project (top-right of each card)."""
    m = []
    if kind == "sphere":                      # Three.js particle portrait → rotating particle sphere
        rnd = random.Random(5)
        R = 30
        for k in range(46):
            phi = math.acos(1 - 2 * (k + .5) / 46)
            th0 = k * 2.399963
            xs, ops = [], []
            for s in range(13):
                th = th0 + s * 2 * math.pi / 12
                x = cx + R * math.sin(phi) * math.cos(th)
                z = math.sin(phi) * math.sin(th)
                xs.append(f"{x:.1f}")
                ops.append(f"{.25 + .75 * (z + 1) / 2:.2f}")
            y = cy + R * math.cos(phi)
            m.append(f'<circle cx="{xs[0]}" cy="{y:.1f}" r="1.6" fill="{G}"><animate attributeName="cx" values="{";".join(xs)}" dur="9s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="{";".join(ops)}" dur="9s" repeatCount="indefinite"/></circle>')
    elif kind == "lens":                      # detective → magnifier sweeping a field of clues
        for gx in range(6):
            for gy in range(4):
                m.append(f'<circle cx="{cx-35+gx*14}" cy="{cy-21+gy*14}" r="1.4" fill="{MUTED}" opacity=".5"/>')
        m.append(f'<circle cx="{cx+7}" cy="{cy-7}" r="3" fill="{G}" class="pu"/>')
        loop = f"M{cx-18} {cy-6} C {cx-10} {cy-30}, {cx+26} {cy-26}, {cx+16} {cy+2} S {cx-30} {cy+22}, {cx-18} {cy-6}Z"
        m.append(f'<g><circle r="14" fill="rgba(134,239,172,.08)" stroke="{TXT}" stroke-width="1.6"/><path d="M10 10L20 20" stroke="{TXT}" stroke-width="2.6" stroke-linecap="round"/>'
                 f'<animateMotion path="{loop}" dur="6s" repeatCount="indefinite" calcMode="spline" keyPoints="0;1" keyTimes="0;1" keySplines=".45 0 .55 1"/></g>')
    elif kind == "clock":                     # scheduled tasks → ticking clock + day dots firing
        m.append(f'<circle cx="{cx-14}" cy="{cy}" r="22" fill="none" stroke="{HAIR2}" stroke-width="1.4"/>')
        for k in range(12):
            a = math.radians(k * 30)
            m.append(f'<path d="M{cx-14+18*math.cos(a):.1f} {cy+18*math.sin(a):.1f}L{cx-14+21*math.cos(a):.1f} {cy+21*math.sin(a):.1f}" stroke="{MUTED}"/>')
        m.append(f'<g style="transform-origin:{cx-14}px {cy}px" class="tick"><path d="M{cx-14} {cy}V{cy-16}" stroke="{G}" stroke-width="1.8" stroke-linecap="round"/></g>'
                 f'<circle cx="{cx-14}" cy="{cy}" r="2.4" fill="{G}"/>')
        for k in range(4):
            m.append(f'<rect x="{cx+18}" y="{cy-19+k*11}" width="18" height="6" rx="3" fill="{G}" class="cron" style="animation-delay:{k*.75:.2f}s"/>')
    elif kind == "chat":                      # auto-reply bot → message in, typing, reply out
        m.append(f'<g class="b1"><rect x="{cx-40}" y="{cy-30}" width="48" height="18" rx="9" fill="rgba(255,255,255,.08)"/>'
                 f'<rect x="{cx-33}" y="{cy-23}" width="30" height="4" rx="2" fill="{MUTED}"/></g>')
        m.append(f'<g class="ty">' + "".join(f'<circle cx="{cx+4+k*8}" cy="{cy}" r="2.6" fill="{G}" class="dot" style="animation-delay:{k*.15:.2f}s"/>' for k in range(3)) + '</g>')
        m.append(f'<g class="b2"><rect x="{cx-8}" y="{cy+12}" width="48" height="18" rx="9" fill="rgba(134,239,172,.22)" stroke="{G}" stroke-opacity=".5"/>'
                 f'<rect x="{cx-1}" y="{cy+19}" width="32" height="4" rx="2" fill="{G}"/></g>')
    elif kind == "flow":                      # business automation → nodes passing work around a loop
        pts = [(cx, cy - 26), (cx + 28, cy + 18), (cx - 28, cy + 18)]
        loop = f"M{pts[0][0]} {pts[0][1]} L{pts[1][0]} {pts[1][1]} L{pts[2][0]} {pts[2][1]} Z"
        m.append(f'<path d="{loop}" fill="none" stroke="{HAIR2}" stroke-width="1.2" stroke-dasharray="3 4"/>')
        for k, (x, y) in enumerate(pts):
            m.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{CARD}" stroke="{G}" stroke-width="1.4"/><circle cx="{x}" cy="{y}" r="3" fill="{G}" class="nd" style="animation-delay:{k*1:.1f}s"/>')
        m.append(f'<circle r="2.6" fill="#eafff1"><animateMotion path="{loop}" dur="3s" repeatCount="indefinite"/></circle>')
    elif kind == "refresh":                   # self-updating profile → rebuild loop
        m.append(f'<g style="transform-origin:{cx-16}px {cy}px" class="spin"><path d="M{cx-16+20} {cy} A20 20 0 1 1 {cx-16} {cy-20}" fill="none" stroke="{G}" stroke-width="1.8" stroke-linecap="round"/>'
                 f'<path d="M{cx-16} {cy-25}L{cx-10} {cy-20}L{cx-16} {cy-15}" fill="none" stroke="{G}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></g>')
        for k in range(4):
            m.append(f'<rect x="{cx+14+k*7}" y="{cy-20}" width="4" height="40" rx="2" fill="{G}" class="eq" style="animation-delay:{k*.22:.2f}s;transform-origin:{cx+16+k*7}px {cy+20}px"/>')
    return "".join(m)


MOTIF_CSS = f"""
@keyframes tick{{to{{transform:rotate(360deg)}}}}
@keyframes cron{{0%,100%{{opacity:.15}}12%,30%{{opacity:1}}}}
@keyframes dot{{0%,60%,100%{{transform:translateY(0)}}30%{{transform:translateY(-5px)}}}}
@keyframes b1{{0%{{opacity:0;transform:translateY(6px)}}8%,92%{{opacity:1;transform:none}}100%{{opacity:0}}}}
@keyframes tyk{{0%,10%{{opacity:0}}14%,40%{{opacity:1}}44%,100%{{opacity:0}}}}
@keyframes b2{{0%,42%{{opacity:0;transform:translateY(6px)}}50%,92%{{opacity:1;transform:none}}100%{{opacity:0}}}}
@keyframes nd{{0%,100%{{opacity:.3}}10%,25%{{opacity:1}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes eq{{0%,100%{{transform:scaleY(.35)}}50%{{transform:scaleY(1)}}}}
.tick{{animation:tick 12s steps(12) infinite}}
.cron{{animation:cron 3s ease-in-out infinite}}
.dot{{transform-box:fill-box;animation:dot 1s ease-in-out infinite}}
.b1{{animation:b1 5s {EXPO} infinite}}.ty{{animation:tyk 5s ease infinite}}.b2{{animation:b2 5s {EXPO} infinite}}
.nd{{animation:nd 3s ease-in-out infinite}}
.spin{{animation:spin 3.5s cubic-bezier(.65,0,.35,1) infinite}}
.eq{{animation:eq 1.6s ease-in-out infinite}}
"""
MOTIFS = ["sphere", "lens", "clock", "chat", "flow", "refresh"]


def project_card(i, p, data):
    title, repo, status, desc, tags = p
    W, H = 440, 268
    live = next((r for r in data["repos"] if r["name"] == repo), None) if repo else None
    lab, col = STATUS[status]
    b = [f'<rect width="{W}" height="{H}" fill="{CARD}"/>',
         f'<g mask="url(#cm)"><image href="{tex("cards")}" x="-30" width="{W+60}" height="320" opacity=".5" class="drift"/></g>',
         f'<g class="fa" {dl(.4)}>{motif(MOTIFS[i], 370, 54)}</g>',
         f'<text x="26" y="40" class="c in" font-size="11" fill="{G}" letter-spacing="1.4">{i+1:02d}</text>']
    pw = tw(lab, 11.5, .58) + 30
    b.append(f'<g class="pop" {dl(.15)}><rect x="62" y="25" width="{pw:.0f}" height="22" rx="11" fill="rgba(255,255,255,.03)" stroke="{HAIR2}"/>'
             f'<circle cx="75" cy="36" r="3" fill="{col}"/><circle cx="75" cy="36" r="3" fill="none" stroke="{col}" class="pg"/>'
             f'<text x="84" y="40" class="m" font-size="11.5" fill="{TXT}">{lab}</text></g>')
    b.append(heading(26, 112, title, 27, .2, cid="ct"))
    lines = textwrap.wrap(desc, 56)[:3]
    for j, ln in enumerate(lines):
        b.append(f'<text x="26" y="{142+j*20}" class="b in" font-size="13.2" fill="{MUTED}" {dl(.35+j*.06)}>{esc(ln)}</text>')
    x = 26
    for j, t in enumerate(tags):
        w = tw(t, 10, .62) + 18
        b.append(f'<g class="pop" {dl(.6+j*.08)}><rect x="{x:.0f}" y="210" width="{w:.0f}" height="22" rx="6" fill="rgba(255,255,255,.035)" stroke="{HAIR}"/>'
                 f'<text x="{x+9:.0f}" y="224.5" class="c" font-size="10" fill="#c3c7cd" letter-spacing=".4">{esc(t)}</text></g>')
        x += w + 6
    if live:
        meta = f'{repo} · {live.get("language") or "—"}' + (f' · updated {fmt(live["pushed"])}' if live.get("pushed") else "")
        arrow = True
    else:
        meta, arrow = "repository coming soon", False
    b.append(f'<text x="26" y="{H-16}" class="c in" font-size="11.5" fill="{MUTED}" {dl(.75)}>{esc(meta)}</text>')
    if arrow:
        b.append(f'<text x="{W-26}" y="{H-15}" text-anchor="end" class="m arr" font-size="13" fill="{TXT}">↗</text>')
    # focus brackets that snap onto the corners, then breathe
    c, o = 14, 8
    for k, (px, py, sx, sy) in enumerate([(o, o, 1, 1), (W - o, o, -1, 1), (W - o, H - o, -1, -1), (o, H - o, 1, -1)]):
        b.append(f'<path d="M{px} {py+sy*c}V{py}H{px+sx*c}" fill="none" stroke="{G}" stroke-width="1.5" class="br" style="transform-origin:{W/2}px {H/2}px;animation-delay:{.05+k*.04:.2f}s"/>')
    css = MOTIF_CSS + f"""
@keyframes arr{{0%,100%{{transform:none}}50%{{transform:translate(2px,-2px)}}}}
@keyframes drift{{from{{transform:translate(0,0)}}to{{transform:translate(28px,-14px)}}}}
@keyframes br{{0%{{opacity:0;transform:scale(1.08)}}30%{{opacity:1;transform:scale(1)}}60%,100%{{opacity:.35}}}}
.drift{{animation:drift 14s ease-in-out infinite alternate}}
.arr{{animation:arr 2s ease-in-out infinite}}
.br{{animation:br 1.4s {EXPO} both}}
"""
    defs = ('<radialGradient id="cmg" cx="1" cy="0" r="1"><stop offset="0" stop-color="#fff"/><stop offset=".7" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<mask id="cm"><rect width="{W}" height="{H}" fill="url(#cmg)"/></mask>')
    return write(f"card-{i+1:02d}", svg(W, H, f"{title} ({lab}). {desc} Built with {', '.join(tags)}.", "".join(b), css, defs))


# ═════════════════════════════ 4. TOOLKIT + NOW ═════════════════════════════
def toolkit():
    W, H = 900, 300
    b = [f'<rect width="{W}" height="{H}" fill="{SURF}"/>',
         kicker(32, 42, "03", "TOOLKIT"),
         heading(32, 84, "What I work with", 34, .08)]
    x, y = 32, 108
    for i, (t, c) in enumerate(TOOLKIT):
        w = tw(t, 12.5, .57) + 36
        if x + w > 456:
            x, y = 32, y + 52
        b.append(f'<g class="pop" {dl(.25+i*.07)}><rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="40" rx="10" fill="{CARD}" stroke="{HAIR}"/>'
                 f'<circle cx="{x+17:.0f}" cy="{y+20}" r="4.5" fill="{c}" class="dp" style="animation-delay:{i*.35:.2f}s"/>'
                 f'<text x="{x+30:.0f}" y="{y+24.5}" class="m" font-size="12.5" fill="{TXT}">{esc(t)}</text></g>')
        x += w + 8
    b.append(f'<text x="32" y="{H-34}" class="b in" font-size="13" fill="{MUTED}" {dl(.7)}>Learning by building: every project here ships through Git.</text>')
    # Now — gold branching threads (Loki)
    nx = 478
    b.append(f'<rect x="{nx}" y="24" width="398" height="{H-48}" rx="12" fill="{CARD}" stroke="{HAIR}" class="in" {dl(.3)}/>')
    b.append(f'<text x="{nx+22}" y="56" class="c in" font-size="11" fill="{GOLD}" letter-spacing="1.6" {dl(.35)}>GLORIOUS PURPOSE</text>')
    ox, oy = nx + 34, 160
    b.append(f'<circle cx="{ox}" cy="{oy}" r="5" fill="{GOLD}"/><circle cx="{ox}" cy="{oy}" r="5" fill="none" stroke="{GOLD}" class="pg"/>')
    ends = [(nx + 150, 112), (nx + 150, 208)]
    for i, ((ex, ey), (t, s)) in enumerate(zip(ends, LEARNING)):
        path = f"M{ox} {oy} C {ox+50} {oy}, {ex-60} {ey}, {ex} {ey}"
        b.append(f'<path d="{path}" fill="none" stroke="{GOLD}" stroke-width="1.6" stroke-opacity=".85" class="th" style="animation-delay:{.6+i*.2:.1f}s"/>')
        b.append(f'<circle cx="{ex}" cy="{ey}" r="3.5" fill="{GOLD}" class="fa" {dl(1.3+i*.2)}/>')
        b.append(f'<text x="{ex+16}" y="{ey+1}" class="h in" font-size="19" fill="{TXT}" letter-spacing="-.4" {dl(1.2+i*.2)}>{t}</text>')
        b.append(f'<text x="{ex+16}" y="{ey+22}" class="b in" font-size="12.5" fill="{MUTED}" {dl(1.3+i*.2)}>{s}</text>')
        b.append(f'<circle r="2.4" fill="#fff8e6"><animateMotion path="{path}" dur="2.6s" begin="{2+i*1.3:.1f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.8;1" dur="2.6s" begin="{2+i*1.3:.1f}s" repeatCount="indefinite"/></circle>')
    b.append(f'<text x="{nx+22}" y="{H-42}" class="b in" font-size="12.5" fill="{DIM}" {dl(1.6)}>Next up: shipping both WhatsApp projects.</text>')
    css = "@keyframes dp{0%,80%,100%{opacity:1;r:4.5px}88%{opacity:.4;r:6px}}.dp{animation:dp 2.8s ease-in-out infinite}.th{stroke-dasharray:240;stroke-dashoffset:240;animation:draw 1.4s cubic-bezier(.19,1,.22,1) forwards}"
    return write("04-toolkit", svg(W, H, "Toolkit: " + ", ".join(t for t, _ in TOOLKIT) + ". Now learning: " + ", ".join(t for t, _ in LEARNING),
                                   "".join(b), css))


# ═════════════════════════════ 5. CONTACT ═════════════════════════════
def contact_button(file, label, value, kind, delay):
    W, H = 440, 88
    if kind == "mail":
        icon = (f'<rect x="28" y="30" width="30" height="22" rx="4" fill="none" stroke="{TXT}" stroke-width="1.6"/>'
                f'<path d="M29 32l14 10 14-10" fill="none" stroke="{G}" stroke-width="1.6"><animate attributeName="d" values="M29 32l14 10 14-10;M29 32l14 -9 14 9;M29 32l14 10 14-10" keyTimes="0;.15;.3" dur="4s" repeatCount="indefinite"/></path>'
                f'<circle cx="57" cy="30" r="4" fill="{G}" class="pu"/>')
    else:
        icon = (f'<rect x="28" y="26" width="30" height="30" rx="6" fill="none" stroke="{TXT}" stroke-width="1.6"/>'
                f'<path d="M36 38v11M36 33v.5M42 49v-6.5c0-2.5 1.6-4 3.6-4s3.4 1.4 3.4 4V49M42 38v2" fill="none" stroke="{TXT}" stroke-width="1.8" stroke-linecap="round"/>')
    perim = 2 * (W - 2 + H - 2)
    b = [f'<rect width="{W}" height="{H}" fill="{CARD}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#cg)" class="gl"/>',
         f'<g class="pop" {dl(delay)}>{icon}</g><g class="in" {dl(delay+.1)}>'
         f'<text x="78" y="38" class="m" font-size="13" fill="{MUTED}">{label}</text>'
         f'<text x="78" y="60" class="m" font-size="{15.5 if len(value) < 30 else 14}" fill="{TXT}" letter-spacing="-.2">{esc(value)}</text></g>',
         f'<g class="arr"><text x="{W-28}" y="50" text-anchor="end" class="m" font-size="18" fill="{G}">↗</text></g>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15" fill="none" stroke="{G}" stroke-opacity=".35" class="gl"/>']
    css = f"""
@keyframes run{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-{perim}}}}}
@keyframes arr{{0%,100%{{transform:none}}50%{{transform:translate(3px,-3px)}}}}
@keyframes gl{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
.gl{{animation:gl 4s ease-in-out {delay:.1f}s infinite}}
.arr{{animation:arr 1.8s ease-in-out infinite}}
"""
    defs = (f'<radialGradient id="cg" cx="1" cy=".5" r=".8"><stop offset="0" stop-color="{G2}" stop-opacity=".12"/><stop offset="1" stop-color="{G2}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="edge"><stop offset="0" stop-color="{G}" stop-opacity="0"/><stop offset=".5" stop-color="{G}"/><stop offset="1" stop-color="{G}" stop-opacity="0"/></linearGradient>')
    return write(file, svg(W, H, f"{label}: {value}", "".join(b), css, defs))


def contact_header():
    W, H = 900, 96
    b = [kicker(4, 34, "04", "CONTACT"),
         heading(4, 78, "Open to AI/ML internships", 38, .08),
         f'<text x="{4+tw("OPEN TO AI/ML INTERNSHIPS", 38, .45)+12:.0f}" y="76" class="b in" font-size="17" fill="{MUTED}" {dl(.2)}>Email is fastest. LinkedIn works too.</text>']
    return write("05-contact", svg(W, H, "Contact", "".join(b), frame=False, radius=0))


# ═════════════════════════════ 6. FOOTER ═════════════════════════════
def footer(data, now):
    W, H = 900, 150
    cx, cy, r = 60, 75, 22
    synced = "rebuilt nightly" if data.get("synced") == "seed" else f"last rebuilt {fmt(data['synced'], True)}"
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<g opacity=".18"><image href="{tex("film")}" width="{W}" height="540" y="-200" class="d1"/></g>',
         f'<circle cx="{cx}" cy="{cy}" r="{r*2.4}" fill="url(#corona)" class="br"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r+1.5}" fill="none" stroke="{G}" stroke-width="1.6"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BG}"/>',
         f'<text x="118" y="70" class="h in" font-size="20" fill="{TXT}" letter-spacing="-.4">Thanks for stopping by.</text>',
         f'<text x="118" y="94" class="b in" font-size="13" fill="{MUTED}" {dl(.1)}>This profile draws itself from live GitHub data · {synced}.</text>',
         f'<text x="{W-32}" y="70" text-anchor="end" class="hl in" font-size="12" fill="{G}" letter-spacing="9" {dl(.2)}>DOOMSDAY</text>',
         f'<text x="{W-32}" y="94" text-anchor="end" class="c in" font-size="10.5" fill="{DIM}" {dl(.25)}>a Doom &amp; Loki fan · not affiliated with Marvel</text>']
    css = """
@keyframes d1{0%,49%{opacity:1}50%,100%{opacity:.3}}
@keyframes br{0%,100%{opacity:.7}50%{opacity:1}}
.d1{animation:d1 .3s steps(1) infinite}.br{animation:br 5s ease-in-out infinite}
"""
    defs = (f'<radialGradient id="corona"><stop offset=".4" stop-color="{G}" stop-opacity=".5"/><stop offset=".55" stop-color="{G2}" stop-opacity=".15"/>'
            f'<stop offset="1" stop-color="{G2}" stop-opacity="0"/></radialGradient>')
    return write("06-footer", svg(W, H, f"Thanks for stopping by. This profile draws itself from live GitHub data, {synced}.", "".join(b), css, defs))


# ═════════════════════════════ INTERLUDE (original scene, no characters) ═════════════════════════════
def interlude():
    W, H = 900, 320
    cx, cy, r = 450, 112, 62
    hz = 262                                   # horizon
    T = hz - 118

    def fig(flare=0, lean=0):
        return (f"M{448+lean} {T} C {462+lean} {T+1}, 470 {T+12}, 470 {T+26} C 470 {T+34}, 468 {T+40}, 471 {T+44} "
                f"L 485 {T+50} C 489 {T+52}, 491 {T+56}, 491 {T+63} L {495+flare} {T+130} L {405-flare} {T+130} L 409 {T+63} "
                f"C 409 {T+56}, 411 {T+52}, 415 {T+50} L 429 {T+44} C 432 {T+40}, 430 {T+34}, 430 {T+26} "
                f"C 430 {T+12}, {436+lean} {T+1}, {448+lean} {T} Z")
    fig_a, fig_b = fig(0, 0), fig(4, 1.2)
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#sky)"/>',
         # eclipse
         f'<circle cx="{cx}" cy="{cy}" r="{r*2.8}" fill="url(#corona)" class="br"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r+2.5}" fill="none" stroke="{G}" stroke-width="2" filter="url(#glow)"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BG}"/>',
         f'<g class="orbit" style="transform-origin:{cx}px {cy}px"><circle cx="{cx+r+2}" cy="{cy}" r="2.6" fill="#fff" filter="url(#glow2)"/></g>',
         # horizon light
         f'<ellipse cx="{cx}" cy="{hz}" rx="430" ry="16" fill="url(#hor)" class="br"/>',
         f'<rect y="{hz}" width="{W}" height="{H-hz}" fill="{BG}"/>',
         f'<ellipse cx="{cx}" cy="{hz+2}" rx="300" ry="6" fill="url(#hor)" opacity=".7"/>',
         # far fog
         f'<g opacity=".35" mask="url(#fogMask)"><g class="fog"><image href="{tex("hero")}" width="{W}" height="300" y="{hz-170}" filter="url(#soft)"/>'
         f'<image href="{tex("hero")}" x="{W}" width="{W}" height="300" y="{hz-170}" filter="url(#soft)" transform="translate({2*W} 0) scale(-1 1)"/></g></g>',
         # the figure
         f'<path d="{fig_a}" fill="#000"><animate attributeName="d" values="{fig_a};{fig_b};{fig_a}" dur="6s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></path>',
         f'<path d="{fig_a}" fill="none" stroke="url(#rim)" stroke-width="1.6" filter="url(#glow)"><animate attributeName="d" values="{fig_a};{fig_b};{fig_a}" dur="6s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></path>',
         f'<path d="M436 {T+70} L 431 {T+118}M462 {T+70} L 468 {T+118}" stroke="#0e1311" stroke-width="1" fill="none"/>',
         f'<ellipse cx="450" cy="{hz+3}" rx="70" ry="4" fill="#000" opacity=".8"/>',
         # near fog + embers
         f'<g opacity=".22" mask="url(#fogMask2)"><g class="fog2"><image href="{tex("hero")}" width="{W}" height="200" y="{hz-40}" filter="url(#soft)"/>'
         f'<image href="{tex("hero")}" x="{W}" width="{W}" height="200" y="{hz-40}" filter="url(#soft)"/></g></g>',
         embers(22, 200, 700, hz + 10, 230, 7, size=(.7, 1.9)),
         f'<g opacity=".16"><image href="{tex("film")}" width="{W}" height="540" y="-110" class="d1"/></g>',
         # letterbox
         f'<rect width="{W}" height="22" fill="#000"/><rect y="{H-22}" width="{W}" height="22" fill="#000"/>',
         f'<text x="28" y="{H-38}" class="c in" font-size="10.5" fill="{DIM}" letter-spacing="1.6">INTERLUDE</text>',
         f'<text x="{W-28}" y="{H-38}" text-anchor="end" class="hl in" font-size="12" fill="{G}" letter-spacing="6" {dl(.2)}>BUILT UNDER A GREEN ECLIPSE</text>']
    css = f"""
@keyframes br{{0%,100%{{opacity:.75}}50%{{opacity:1}}}}
@keyframes orbit{{to{{transform:rotate(360deg)}}}}
@keyframes fog{{to{{transform:translateX(-{W}px)}}}}
@keyframes d1{{0%,49%{{opacity:1}}50%,100%{{opacity:.35}}}}
.br{{animation:br 6s ease-in-out infinite}}
.orbit{{animation:orbit 16s linear infinite}}
.fog{{animation:fog 60s linear infinite}}.fog2{{animation:fog 38s linear infinite}}
.d1{{animation:d1 .26s steps(1) infinite}}
"""
    defs = (f'<radialGradient id="corona"><stop offset=".36" stop-color="{G}" stop-opacity=".5"/><stop offset=".46" stop-color="{G2}" stop-opacity=".2"/>'
            f'<stop offset=".75" stop-color="{G2}" stop-opacity=".04"/><stop offset="1" stop-color="{G2}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="hor"><stop offset="0" stop-color="#d9f99d" stop-opacity=".55"/><stop offset=".4" stop-color="{G2}" stop-opacity=".25"/><stop offset="1" stop-color="{G2}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset=".7" stop-color="#0b1a12"/><stop offset="1" stop-color="#16402a"/></linearGradient>'
            f'<linearGradient id="rim" x1="0" y1="0" x2="1" y2="0"><stop offset=".35" stop-color="{G}" stop-opacity="0"/><stop offset=".75" stop-color="{G}" stop-opacity=".8"/><stop offset="1" stop-color="#eafff1"/></linearGradient>'
            '<linearGradient id="fg1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".7" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="fogMask"><rect y="{hz-170}" width="{W}" height="190" fill="url(#fg1)"/></mask>'
            f'<mask id="fogMask2"><rect y="{hz-40}" width="{W}" height="90" fill="url(#fg1)"/></mask>'
            '<filter id="soft"><feGaussianBlur stdDeviation="6"/></filter>'
            '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            '<filter id="glow2" x="-400%" y="-400%" width="900%" height="900%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    return write("interlude", svg(W, H, "Interlude: a lone cloaked figure stands on the horizon beneath a green eclipse.", "".join(b), css, defs))


# ═════════════════════════════ DIVIDERS (living time-thread between sections) ═════════════════════════════
def divider(name, seed, accent=G):
    W, H = 900, 44
    rnd = random.Random(seed)
    y = 22
    branches = []
    for _ in range(3):
        x = rnd.uniform(160, 740)
        dirn = rnd.choice([-1, 1])
        branches.append(f'<path d="M{x:.0f} {y} C {x+18:.0f} {y}, {x+30:.0f} {y+dirn*10}, {x+56:.0f} {y+dirn*12}" fill="none" stroke="{accent}" '
                        f'stroke-opacity=".45" stroke-width="1" class="br" style="animation-delay:{rnd.uniform(0, 4):.1f}s"/>')
    b = [f'<path d="M450 {y}H{W}" stroke="url(#ln)" stroke-width="1" class="grow" style="stroke-dasharray:460;stroke-dashoffset:460"/>',
         f'<path d="M450 {y}H0" stroke="url(#ln)" stroke-width="1" class="grow" style="stroke-dasharray:460;stroke-dashoffset:460"/>',
         f'<g transform="translate(450 {y})" class="dm"><rect x="-14" y="-8" width="28" height="16" fill="{BG}"/><path d="M0 -7V7M-7 0H7M-4 -4L4 4M4 -4L-4 4" stroke="{accent}" stroke-width="1"/><circle r="2" fill="{accent}"/></g>']
    css = f"""
@keyframes run{{0%{{transform:translateX(0);opacity:0}}10%{{opacity:1}}90%{{opacity:1}}100%{{transform:translateX({W+120}px);opacity:0}}}}
@keyframes br{{0%,100%{{stroke-dashoffset:80;opacity:0}}20%,70%{{stroke-dashoffset:0;opacity:1}}}}
@keyframes dm{{0%,100%{{opacity:.5}}50%{{opacity:1}}}}
@keyframes grow{{0%{{stroke-dashoffset:460;opacity:1}}45%,80%{{stroke-dashoffset:0;opacity:1}}100%{{stroke-dashoffset:0;opacity:0}}}}
@keyframes turn{{to{{transform:rotate(360deg)}}}}
.grow{{animation:grow 5s {EXPO} infinite}}
.dm path{{transform-box:fill-box;transform-origin:center;animation:turn 8s linear infinite}}
.br{{stroke-dasharray:80;animation:br 5s ease-in-out infinite}}
.dm{{animation:dm 3s ease-in-out infinite}}
"""
    defs = (f'<linearGradient id="ln" gradientUnits="userSpaceOnUse" x1="0" x2="900" y1="0" y2="0"><stop offset="0" stop-color="{accent}" stop-opacity="0"/><stop offset=".5" stop-color="{accent}" stop-opacity=".35"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="pulse"><stop offset="0" stop-color="{accent}" stop-opacity="0"/><stop offset="1" stop-color="#eafff1"/></linearGradient>')
    return write(name, svg(W, H, "divider", "".join(b), css, defs, frame=False, radius=0))


# ═════════════════════════════ V3 · HERO — oversized type, texture inside the letters, sigil ═════════════════════════════
def sigil(cx, top, h, color="#e9f5ec", delay=0.0):
    """An original vertical 'cybersigil': science lines + sorcery marks, drawn stroke by stroke."""
    s = []
    def ln(d, w=1.1, op=1, k=0):
        L = 400
        s.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-opacity="{op}" stroke-linecap="round" '
                 f'class="sg" style="stroke-dasharray:{L};stroke-dashoffset:{L};animation-delay:{delay+k*.09:.2f}s"/>')
    y = top
    ln(f"M{cx} {y} V{y+h}", 1.2, .9, 0)                                         # spine
    ln(f"M{cx-6} {y+18} L{cx} {y+8} L{cx+6} {y+18}", 1, .8, 1)                  # arrow head
    ln(f"M{cx-15} {y+44} A15 15 0 1 0 {cx+15} {y+44}", 1.3, 1, 2)               # crescent bowl
    ln(f"M{cx-22} {y+70} H{cx+22}M{cx-12} {y+78} H{cx+12}", 1, .7, 3)           # crossbars
    ln(f"M{cx} {y+96} L{cx+16} {y+118} L{cx} {y+140} L{cx-16} {y+118} Z", 1.2, 1, 4)  # diamond
    ln(f"M{cx-30} {y+118} H{cx-20}M{cx+20} {y+118} H{cx+30}", 1, .6, 5)
    ln(f"M{cx} {y+162} C{cx+18} {y+170}, {cx+18} {y+188}, {cx} {y+194} C{cx-18} {y+200}, {cx-18} {y+218}, {cx} {y+226}", 1.2, .9, 6)  # serpent S
    ln(f"M{cx-8} {y+h-14} L{cx} {y+h} L{cx+8} {y+h-14}", 1, .8, 7)
    for i, (dx, dy, r) in enumerate([(0, 44, 3.2), (0, 118, 2.6), (-26, 70, 1.6), (26, 70, 1.6), (0, 250, 2.2)]):
        s.append(f'<circle cx="{cx+dx}" cy="{y+dy}" r="{r}" fill="{G}" class="spark" style="animation-delay:{delay+1+i*.4:.1f}s"/>')
    return "".join(s)


def hero_v3():
    W, H = 900, 500
    word = "SRIVATHSA"
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#bp)"/>',
         f'<rect width="{W}" height="{H}" fill="url(#hglow)"/>',
         # top bar
         f'<text x="28" y="40" class="c in" font-size="11" fill="{MUTED}" letter-spacing="1.4">SRIVATHSA SHERLA</text>',
         f'<text x="186" y="40" class="c in" font-size="11" fill="{DIM}" letter-spacing="1.4" {dl(.05)}>/ PORTFOLIO · 2026</text>',
         f'<g class="in" {dl(.1)}><circle cx="{W-150}" cy="36" r="3.5" fill="{G}"/><circle cx="{W-150}" cy="36" r="3.5" fill="none" stroke="{G}" class="pg"/>'
         f'<text x="{W-28}" y="40" text-anchor="end" class="c" font-size="11" fill="{TXT}" letter-spacing="1.4">OPEN TO WORK</text></g>',
         f'<path d="M28 56H{W-28}" stroke="{HAIR}"/>',
         # giant word: texture lives inside the letters
         f'<g clip-path="url(#nameBox)"><g class="rise" {dl(.25)}><g clip-path="url(#word)">'
         f'<rect width="{W}" height="{H}" fill="#e7efe9"/>'
         f'<image href="{tex("hero")}" x="-40" y="40" width="{W+80}" height="480" class="tdrift" opacity=".32" style="mix-blend-mode:multiply"/>'
         f'<rect width="{W}" height="{H}" fill="url(#lines)"/>'
         f'<rect y="0" width="{W}" height="60" fill="url(#sweep)" class="sweep"/></g>'
         f'<text x="24" y="290" class="a" font-size="178" fill="none" stroke="rgba(214,255,226,.25)" stroke-width="1" letter-spacing="3">{word}</text></g></g>',
         # glitch: colour-split slices that flash every few seconds
         f'<g class="gA" clip-path="url(#sl1)"><text x="24" y="290" class="a" font-size="178" fill="{G}" letter-spacing="3" opacity=".85">{word}</text></g>',
         f'<g class="gB" clip-path="url(#sl2)"><text x="24" y="290" class="a" font-size="178" fill="#ff4d6d" letter-spacing="3" opacity=".7">{word}</text></g>',
         f'<g class="gC" clip-path="url(#sl3)"><text x="24" y="290" class="a" font-size="178" fill="#e7efe9" letter-spacing="3">{word}</text></g>',
         # sigil (sorcery) on the right, over the type
         sigil(840, 74, 262, delay=1.2),
         # copy
         f'<text x="28" y="356" class="b in" font-size="19" fill="{TXT}" letter-spacing="-.3" {dl(1.1)}>{esc(LINE_1)}</text>',
         f'<text x="28" y="382" class="b in" font-size="19" fill="{MUTED}" letter-spacing="-.3" {dl(1.18)}>{esc(LINE_2)}</text>']
    rows = [("FOCUS", "Agentic AI · Generative AI"), ("BUILDING", "WhatsApp automation"), ("BASED", "Newton School of Technology")]
    for i, (k, v) in enumerate(rows):
        x = 28 + i * 290
        b.append(f'<g class="in" {dl(1.3+i*.08)}><path d="M{x} 418H{x+272}" stroke="{HAIR2}"/>'
                 f'<text x="{x}" y="440" class="c" font-size="10.5" fill="{G}" letter-spacing="1.4">{k}</text>'
                 f'<text x="{x}" y="463" class="m" font-size="14" fill="{TXT}">{esc(v)}</text></g>')
    b.append(f'<text x="{W-28}" y="{H-14}" text-anchor="end" class="c fa" font-size="11" fill="{MUTED}" letter-spacing="2" {dl(1.8)}>SCIENCE &amp; SORCERY · VARIANT S-12</text>')
    css = f"""
@keyframes rv{{from{{width:0}}to{{width:{W}px}}}}
@keyframes gA{{0%,90%,100%{{opacity:0;transform:none}}91%{{opacity:1;transform:translateX(-9px)}}93%{{opacity:1;transform:translateX(6px)}}95%{{opacity:0}}}}
@keyframes gB{{0%,91%,100%{{opacity:0;transform:none}}92%{{opacity:1;transform:translateX(8px)}}94%{{opacity:1;transform:translateX(-4px)}}96%{{opacity:0}}}}
@keyframes gC{{0%,92%,100%{{opacity:0;transform:none}}93%{{opacity:1;transform:translateX(14px)}}95%{{opacity:0}}}}
@keyframes tdrift{{from{{transform:translate(0,0)}}to{{transform:translate(36px,-18px)}}}}
@keyframes sweep{{0%{{transform:translateY(60px);opacity:0}}20%{{opacity:1}}100%{{transform:translateY(330px);opacity:0}}}}
@keyframes spark{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
.gA{{animation:gA 7s steps(1) 3s infinite;opacity:0}}.gB{{animation:gB 7s steps(1) 3s infinite;opacity:0}}.gC{{animation:gC 7s steps(1) 3s infinite;opacity:0}}
.tdrift{{animation:tdrift 16s ease-in-out infinite alternate}}
.sweep{{animation:sweep 5s ease-in-out 2s infinite;opacity:0}}
.sg{{animation:draw 1.4s {EXPO} forwards}}
.spark{{animation:fade 1s ease both,spark 2.8s ease-in-out infinite}}
"""
    defs = ('<filter id="lift"><feComponentTransfer><feFuncR type="linear" slope="1.9" intercept=".04"/><feFuncG type="linear" slope="1.9" intercept=".05"/><feFuncB type="linear" slope="1.7" intercept=".03"/></feComponentTransfer></filter>'
            f'<clipPath id="word"><text x="24" y="290" class="a" font-size="178" letter-spacing="3">{word}</text></clipPath>'
            f'<clipPath id="nameBox"><rect x="0" y="137" width="{W}" height="160"/></clipPath>'
            f'<clipPath id="sl1"><rect x="0" y="170" width="{W}" height="22"/></clipPath>'
            f'<clipPath id="sl2"><rect x="0" y="220" width="{W}" height="14"/></clipPath>'
            f'<clipPath id="sl3"><rect x="0" y="250" width="{W}" height="9"/></clipPath>'
            '<pattern id="bp" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="rgba(255,255,255,.035)"/></pattern>'
            '<pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="#000" opacity=".35"/></pattern>'
            f'<radialGradient id="hglow" cx=".9" cy=".2" r=".6"><stop offset="0" stop-color="{G2}" stop-opacity=".12"/><stop offset="1" stop-color="{G2}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="sweep" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{G}" stop-opacity="0"/><stop offset="1" stop-color="{G}" stop-opacity=".35"/></linearGradient>')
    return write("01-hero", svg(W, H, f"{NAME} — {LINE_1} {LINE_2} Open to work.", "".join(b), css, defs))


# ═════════════════════════════ V3 · VARIANTS interlude — generative timeline field ═════════════════════════════
def variants():
    W, H = 900, 260
    rnd = random.Random(42)
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    threads = []
    for i in range(64):
        y0 = rnd.uniform(-20, H + 20)
        y1 = rnd.uniform(-20, H + 20)
        mid = 118 + rnd.uniform(-8, 8)
        a1, a2 = rnd.uniform(.6, 1.4), rnd.uniform(.6, 1.4)
        d = (f"M-20 {y0:.1f} C 180 {y0*a1*.2+mid*.8:.1f}, 300 {mid+rnd.uniform(-6,6):.1f}, 450 {mid+rnd.uniform(-5,5):.1f} "
             f"S 720 {y1*a2*.25+mid*.75:.1f}, 920 {y1:.1f}")
        op = rnd.uniform(.18, .55)
        dash = rnd.choice(["120 240", "60 160", "200 300", "3 9"])
        threads.append(f'<path d="{d}" fill="none" stroke="{G}" stroke-opacity="{op:.2f}" stroke-width="{rnd.uniform(.6,1.4):.2f}" '
                       f'stroke-dasharray="{dash}" class="fl" style="animation-duration:{rnd.uniform(6,16):.1f}s;animation-delay:-{rnd.uniform(0,10):.1f}s"/>')
    b.append(f'<g mask="url(#edgeMask)">{"".join(threads)}</g>')
    # the main timeline + a gold variant that breaks away
    main = "M-20 118 C 200 118, 320 120, 450 118 S 700 116, 920 118"
    variant = "M560 118 C 620 118, 640 90, 690 70 S 790 34, 920 22"
    b += [f'<path d="{main}" fill="none" stroke="#eafff1" stroke-width="1.6" class="dr1" filter="url(#gl)"/>',
          f'<path d="{variant}" fill="none" stroke="{GOLD}" stroke-width="1.6" class="dr2" filter="url(#gl)"/>',
          f'<circle cx="560" cy="118" r="4" fill="{GOLD}" class="fa" {dl(1.6)}/><circle cx="560" cy="118" r="4" fill="none" stroke="{GOLD}" class="pg" {dl(1.6)}/>',
          f'<circle r="2.6" fill="#fff"><animateMotion path="{main}" dur="5s" repeatCount="indefinite"/></circle>',
          f'<circle r="2.6" fill="#fff6dc"><animateMotion path="{variant}" dur="3.2s" begin="2s" repeatCount="indefinite"/></circle>',
          f'<rect x="566" y="128" width="196" height="20" rx="4" fill="{BG}" fill-opacity=".92" class="fa" {dl(1.8)}/>'
          f'<text x="574" y="142" class="c fa" font-size="11" fill="{GOLD}" letter-spacing="1.4" {dl(1.8)}>VARIANT S-12 · BRANCHED</text>',
          # copy
          f'<rect y="{H-96}" width="{W}" height="96" fill="url(#base)"/>',
          f'<rect width="320" height="60" fill="url(#tl)"/>',
          f'<text x="28" y="40" class="c in" font-size="11" fill="{MUTED}" letter-spacing="1.6">INTERLUDE — THE SACRED TIMELINE</text>',
          f'<text x="28" y="212" class="h in" font-size="32" fill="{TXT}" letter-spacing="-1" {dl(.3)}>One timeline.</text>',
          f'<text x="234" y="212" class="h in" font-size="32" fill="{MUTED}" letter-spacing="-1" {dl(.4)}>I took the branch.</text>',
          f'<text x="28" y="238" class="b in" font-size="13.5" fill="{MUTED}" {dl(.5)}>From coursework to shipped tools, one commit at a time.</text>']
    css = f"""
@keyframes fl{{to{{stroke-dashoffset:-400}}}}
.fl{{animation:fl linear infinite}}
.dr1{{stroke-dasharray:1000;stroke-dashoffset:1000;animation:draw 2s {EXPO} .2s forwards}}
.dr2{{stroke-dasharray:420;stroke-dashoffset:420;animation:draw 1.6s {EXPO} 1.4s forwards}}
"""
    defs = (f'<linearGradient id="base" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}" stop-opacity="0"/><stop offset=".45" stop-color="{BG}" stop-opacity=".92"/><stop offset="1" stop-color="{BG}"/></linearGradient>'
            f'<linearGradient id="tl" x1="0" x2="1"><stop offset=".6" stop-color="{BG}" stop-opacity=".9"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="eg"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".12" stop-color="#fff"/><stop offset=".88" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="edgeMask"><rect width="{W}" height="{H}" fill="url(#eg)"/></mask>'
            '<filter id="gl" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    return write("interlude", svg(W, H, "Interlude: one timeline, and a gold variant that branches away from it. I took the branch.", "".join(b), css, defs))


# ═════════════════════════════ V3 · FOOTER — terminal sign-off ═════════════════════════════
def footer_v3(data, now):
    W, H = 900, 214
    synced = "rebuilt nightly" if data.get("synced") == "seed" else f"rebuilt {fmt(data['synced'], True)}"
    lines = [("$ ", "whoami", MUTED, TXT),
             ("", "srivathsa — builds agents, automations and things for the web", None, MUTED),
             ("$ ", "cat favourites.txt", MUTED, TXT),
             ("", "doom · loki · stark", None, G),
             ("$ ", "exit", MUTED, TXT)]
    t = .3
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#bp2)"/>',
         f'<circle cx="30" cy="26" r="5" fill="#3a3f45"/><circle cx="48" cy="26" r="5" fill="#3a3f45"/><circle cx="66" cy="26" r="5" fill="#3a3f45"/>',
         f'<text x="{W/2}" y="30" text-anchor="middle" class="c" font-size="10.5" fill="{DIM}">~/srivathsa12 — zsh</text>',
         f'<path d="M0 44H{W}" stroke="{HAIR}"/>']
    defs = []
    y = 76
    for i, (pre, txt, pc, tc) in enumerate(lines):
        full = pre + txt
        cw = 0.6 * 13
        dur = max(len(full) / (38 if pre else 120), .1)
        cid = f"ty{i}"
        defs.append(f'<clipPath id="{cid}"><rect x="27" y="{y-14}" height="20" width="0"><animate attributeName="width" from="0" to="{len(full)*cw+4:.0f}" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze" calcMode="discrete" values="{";".join(str(round(k*cw)) for k in range(len(full)+1))}"/></rect></clipPath>')
        pre_svg = f'<tspan fill="{G}">{esc(pre)}</tspan>' if pre else ""
        b.append(f'<text x="28" y="{y}" class="c" font-size="13" fill="{tc}" clip-path="url(#{cid})" xml:space="preserve">{pre_svg}{esc(txt)}</text>')
        t += dur + (.35 if pre else .15)
        y += 22
    b.append(f'<rect x="{28+len("$ exit")*7.8+4:.0f}" y="{y-22-12}" width="8" height="15" fill="{G}" opacity="0" class="blink" style="animation-delay:{t:.2f}s"/>')
    b.append(f'<text x="28" y="{H-18}" class="c" font-size="10" fill="{DIM}">this profile draws itself from live GitHub data · {synced} · a Doom &amp; Loki fan, not affiliated with Marvel</text>')
    css = "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}.blink{animation:blink 1s steps(1) infinite}"
    defs.append('<pattern id="bp2" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="rgba(255,255,255,.025)"/></pattern>')
    return write("06-footer", svg(W, H, f"whoami: srivathsa — builds agents, automations and things for the web. Favourites: Doom, Loki, Stark. {synced}.", "".join(b), css, "".join(defs)))


def main():
    now = datetime.now(IST)
    data = load_data(now)
    built = [hero_v3(), divider("div-1", 1), activity(data, now), divider("div-2", 2), projects_header(),
             *[project_card(i, p, data) for i, p in enumerate(PROJECTS)],
             variants(), toolkit(), divider("div-3", 3, GOLD), contact_header(),
             contact_button("btn-email", "Email", EMAIL, "mail", .1),
             contact_button("btn-linkedin", "LinkedIn", LINKEDIN, "in", .2),
             footer_v3(data, now)]
    for p in built:
        print(f"built {os.path.relpath(p, ROOT):24s} {os.path.getsize(p)//1024:>4} KB")


if __name__ == "__main__":
    main()
