"""Site health check: JSON-LD, broken internal links, title/description length, one H1, canonical, sitemap coverage."""
import re, glob, json, os, html as H
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
B = "https://acornhousebuyer.com"
locs = set(re.findall(r"<loc>([^<]+)</loc>", open("sitemap.xml").read()))
files = [f for f in glob.glob("**/*.html", recursive=True) if not f.startswith("_")]
p, titles = [], {}
for f in sorted(files):
    s = open(f, encoding="utf-8").read()
    url = "/" + (f[:-10] if f.endswith("index.html") else f)
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(b)
        except Exception as e: p.append(f"bad JSON-LD: {f} {e}")
    for h in re.findall(r'href="(/[^"#?]*)', s):
        q = h.lstrip("/")
        if not (os.path.isfile(q) or os.path.isfile(os.path.join(q, "index.html"))): p.append(f"broken link: {f} -> {h}")
    t = re.search(r"<title>(.*?)</title>", s, re.S); d = re.search(r'name="description" content="([^"]*)', s)
    if not t or len(H.unescape(t.group(1))) > 60: p.append(f"title: {f}")
    elif t.group(1) in titles: p.append(f"duplicate title: {f} = {titles[t.group(1)]}")
    else: titles[t.group(1)] = f
    if not d or not 70 <= len(H.unescape(d.group(1))) <= 160: p.append(f"description: {f}")
    if len(re.findall(r"<h1[\s>]", s)) != 1: p.append(f"h1 count: {f}")
    if f'<link rel="canonical" href="{B}{url}">' not in s: p.append(f"canonical: {f}")
    if "noindex" not in s and B + url not in locs: p.append(f"not in sitemap: {f}")
    if "noindex" in s and B + url in locs: p.append(f"noindex page in sitemap: {f}")
print("\n".join(p) or "All checks passed", f"({len(files)} pages)")
