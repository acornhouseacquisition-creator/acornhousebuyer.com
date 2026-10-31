"""Builds the whole acornhousebuyer.com static site (GitHub Pages).
Run:  python3 _src/build.py      (from the repo root or anywhere)
Then: python3 _src/check.py
Folders starting with "_" are not published by GitHub Pages."""
import json, os, html, datetime
from content import CITIES, SITUATIONS, FAQ_HOME

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Business details: edit here, then rebuild --------------------------------
SITE = "https://acornhousebuyer.com"
BRAND = "Acorn House Buyer"
LEGAL_NAME = ""            # e.g. "Acorn House Acquisition LLC" (shown in footer + schema when set)
PHONE_DISPLAY = "(704) 246-3399"
PHONE_TEL = "+17042463399"
EMAIL = "info@acornhousebuyer.com"
STREET = ""                # street address for schema/footer; leave "" to show city only
CITY, STATE, ZIP = "Charlotte", "NC", ""
FORM_ENDPOINT = ""         # e.g. Formspree/Close form URL. Empty = form opens a pre-filled email
CLOSE_FORM_ID = "form_034pBun8a92JhCSDTxnwlV"  # Close saves the page URL on each submission (source_url)
CLOSE_SCRIPT = '<script src="https://webforms.closeiocdn.com/webforms.js" type="module" crossorigin="anonymous" defer></script>'
GA4_ID = ""                # e.g. "G-XXXXXXX"
GSC_VERIFY = ""            # Google Search Console HTML-tag verification code
BING_VERIFY = ""
SAME_AS = []               # Google Business Profile, Facebook, etc. URLs
TODAY = datetime.date.today().isoformat()
# -------------------------------------------------------------------------------

E = html.escape
LOGO_RATIO = 2.8111  # logo width / height
ORG_ID = SITE + "/#business"
PAGES = []  # (path, priority)


def city_url(slug): return f"/we-buy-houses-{slug}-nc/"


CITY_BY_SLUG = {c["slug"]: c for c in CITIES}

ICONS = {
    "alert": '<path d="M12 3 2 21h20L12 3z"/><path d="M12 10v5M12 18h.01"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l3 3M15 8l2 2"/>',
    "split": '<path d="M12 21V11M12 11 5 4M12 11l7-7M5 4v5M5 4h5M19 4v5M19 4h-5"/>',
    "home": '<path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "tool": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4 2.5-2.5z"/>',
    "move": '<path d="M3 7h11v10H3zM14 10h4l3 3v4h-7"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
    "check": '<path d="m5 12 5 5L20 7"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
}


def icon(name, cls="ic"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def logo_img(src, height):
    width = round(height * LOGO_RATIO)
    return f'<img class="logo-img" src="{src}" alt="{BRAND}" width="{width}" height="{height}">'


def business_schema():
    addr = {"@type": "PostalAddress", "addressLocality": CITY, "addressRegion": STATE, "addressCountry": "US"}
    if STREET: addr["streetAddress"] = STREET
    if ZIP: addr["postalCode"] = ZIP
    b = {
        "@type": "LocalBusiness", "@id": ORG_ID, "name": BRAND, "url": SITE + "/",
        "logo": SITE + "/assets/logo.png", "image": SITE + "/assets/og-image.png",
        "telephone": PHONE_TEL, "email": EMAIL, "address": addr, "priceRange": "Free cash offer",
        "description": "Acorn House Buyer buys houses for cash across North Carolina, as-is and in any condition, with no commissions or repairs.",
        "areaServed": [{"@type": "State", "name": "North Carolina"}] +
                      [{"@type": "City", "name": f"{c['name']}, NC"} for c in CITIES],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                                       "opens": "08:00", "closes": "20:00"}],
        "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_TEL, "email": EMAIL,
                         "contactType": "customer service", "areaServed": "US-NC", "availableLanguage": "English"},
    }
    if LEGAL_NAME: b["legalName"] = LEGAL_NAME
    if SAME_AS: b["sameAs"] = SAME_AS
    return b


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(trail)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def ld(graph):
    s = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    return '<script type="application/ld+json">' + s.replace("</", "<\\/") + "</script>"


NAV = [("How It Works", "/how-it-works/"), ("Areas We Buy", "/north-carolina/"),
       ("Situations", "/situations/"), ("Cash vs. Agent", "/sell-to-cash-buyer-vs-agent-nc/"),
       ("FAQ", "/faq/"), ("About", "/about/")]


def header(path):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{u}"{cur if u == path else ""}>{n}</a>' for n, u in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap hdr">
<a class="brand" href="/" aria-label="{BRAND} home">{logo_img("/assets/logo-header.png", 60)}</a>
<nav class="nav" id="nav" aria-label="Main">{links}<a class="btn btn-sm" href="/get-cash-offer/">Get My Offer</a></nav>
<a class="hdr-phone" href="tel:{PHONE_TEL}">{icon("phone")}<span>{PHONE_DISPLAY}</span></a>
<button class="menu-btn" aria-controls="nav" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button>
</div></header>'''


def footer():
    city_links = "".join(f'<li><a href="{city_url(c["slug"])}">{c["name"]}</a></li>' for c in CITIES)
    sit_links = "".join(f'<li><a href="/{s["slug"]}/">{s["short"]}</a></li>' for s in SITUATIONS)
    addr = ", ".join(x for x in [STREET, f"{CITY}, {STATE} {ZIP}".strip()] if x)
    legal = LEGAL_NAME or BRAND
    return f'''<footer class="site-footer"><div class="wrap">
<div class="f-grid">
<div><a class="brand brand-light" href="/" aria-label="{BRAND} home">{logo_img("/assets/logo-light.png", 60)}</a>
<p>We buy houses for cash across North Carolina. Any condition, no commissions, close on your date.</p>
<p class="nap"><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><br>{E(addr)}</p></div>
<div><h2 class="f-h">Areas We Buy</h2><ul class="f-cities">{city_links}</ul><a href="/north-carolina/">All North Carolina areas &rarr;</a></div>
<div><h2 class="f-h">Situations</h2><ul>{sit_links}</ul></div>
<div><h2 class="f-h">Company</h2><ul><li><a href="/how-it-works/">How It Works</a></li><li><a href="/about/">About Us</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/contact/">Contact</a></li><li><a href="/get-cash-offer/">Get a Cash Offer</a></li><li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms/">Terms of Use</a></li></ul></div>
</div>
<p class="disclaimer">{E(legal)} is a real estate investment company that buys property directly from owners. We are not real estate agents or brokers and do not list homes for sale. We may buy a property ourselves or assign our purchase contract to a partner investor; your agreed price and terms stay the same. All sales close through a licensed North Carolina closing attorney. Requesting an offer is free and creates no obligation.</p>
<p class="copy">&copy; {datetime.date.today().year} {E(legal)}. All rights reserved.</p>
</div></footer>
<div class="sticky-cta" aria-label="Quick contact"><a href="tel:{PHONE_TEL}">{icon("phone")}Call</a><a href="sms:{PHONE_TEL}">Text</a><a class="go" href="/get-cash-offer/">Get Cash Offer</a></div>'''


def lead_form(heading="Get Your Free Cash Offer", sub="No obligation. We usually reply within a few hours.", fid="f"):
    action = E(FORM_ENDPOINT)
    return f'''<form class="lead-form" data-endpoint="{action}" data-email="{EMAIL}" novalidate>
<h2 class="form-h">{heading}</h2><p class="form-sub">{sub}</p>
<label for="{fid}-addr">Property address</label><input id="{fid}-addr" name="address" autocomplete="street-address" required placeholder="123 Main St, Charlotte, NC">
<div class="row2"><div><label for="{fid}-name">Your name</label><input id="{fid}-name" name="name" autocomplete="name" required></div>
<div><label for="{fid}-phone">Phone</label><input id="{fid}-phone" name="phone" type="tel" autocomplete="tel" required></div></div>
<label for="{fid}-email">Email <span class="opt">(optional)</span></label><input id="{fid}-email" name="email" type="email" autocomplete="email">
<label for="{fid}-why">What's going on with the house? <span class="opt">(optional)</span></label>
<select id="{fid}-why" name="situation"><option value="">Choose one</option><option>Needs repairs</option><option>Inherited / probate</option><option>Behind on payments / foreclosure</option><option>Divorce</option><option>Rental / tenant problems</option><option>Relocating</option><option>Just want a fast sale</option><option>Other</option></select>
<input class="hp" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="btn btn-block" type="submit">Get My Cash Offer</button>
<p class="form-note">By submitting, you agree we may contact you by call, text or email about your property. Msg &amp; data rates may apply. Reply STOP to opt out. See our <a href="/privacy-policy/">Privacy Policy</a>.</p>
<p class="form-status" role="status" aria-live="polite"></p>
</form>'''


def close_form(heading="Get Your Free Cash Offer", sub="No obligation. We usually reply within a few hours."):
    return f'''<div class="close-card"><h2 class="form-h">{heading}</h2><p class="form-sub">{sub}</p>
<close-form id="{CLOSE_FORM_ID}"></close-form>
<noscript><p>Please call or text <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> for your offer.</p></noscript></div>'''


def page(path, title, desc, body, schema=(), trail=None, priority="0.7", robots="index,follow", in_sitemap=True, head_extra=""):
    graph = [business_schema(),
             {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": BRAND, "publisher": {"@id": ORG_ID}},
             {"@type": "WebPage", "@id": SITE + path + "#webpage", "url": SITE + path, "name": title,
              "description": desc, "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": ORG_ID},
              "inLanguage": "en-US", "dateModified": TODAY}]
    if trail: graph.append(crumbs_schema(trail))
    graph += list(schema)
    assert len(title) <= 60, (path, len(title), title)
    assert 70 <= len(desc) <= 160, (path, len(desc))
    bc = ""
    if trail and len(trail) > 1:
        bc = '<nav class="crumbs wrap" aria-label="Breadcrumb"><ol>' + "".join(
            (f'<li><a href="{u}">{E(n)}</a></li>' if i < len(trail) - 1 else f'<li aria-current="page">{E(n)}</li>')
            for i, (n, u) in enumerate(trail)) + "</ol></nav>"
    verify = (f'<meta name="google-site-verification" content="{E(GSC_VERIFY)}">' if GSC_VERIFY else "") + \
             (f'<meta name="msvalidate.01" content="{E(BING_VERIFY)}">' if BING_VERIFY else "")
    ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script><script>'
          f"window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA4_ID}');</script>") if GA4_ID else ""
    doc = f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="{robots},max-image-preview:large">
<link rel="canonical" href="{SITE}{path}">
<meta name="geo.region" content="US-NC">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Acorn House Buyer: we buy houses for cash in North Carolina">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1f4d3a">
<link rel="icon" href="/favicon-48.png" sizes="48x48" type="image/png">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="/assets/styles.css?v={TODAY}">
{verify}{ga}{head_extra}
{ld(graph)}
</head>
<body>
{header(path)}
{bc}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/main.js?v={TODAY}" defer></script>
</body>
</html>
'''
    out = os.path.join(ROOT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f: f.write(doc)
    if in_sitemap: PAGES.append((path, priority))


# ---------------------------------------------------------------- shared blocks
def steps_block(place="North Carolina"):
    return f'''<section class="sec"><div class="wrap">
<p class="eyebrow">How it works</p><h2>Sell your house in 3 simple steps</h2>
<ol class="steps">
<li><span class="n">1</span><h3>Tell us about the house</h3><p>Call {PHONE_DISPLAY} or fill out the short form. It takes about two minutes.</p></li>
<li><span class="n">2</span><h3>Get a fair cash offer</h3><p>We walk through the home once, then give you a written offer with no obligation, usually within 24 hours.</p></li>
<li><span class="n">3</span><h3>Close on your date</h3><p>Close with a {place} closing attorney in as little as 7 to 14 days, or later if you need more time. You get paid at closing.</p></li>
</ol></div></section>'''


def trust_strip():
    items = ["No agent commissions", "No repairs or cleaning", "We pay normal closing costs", "Close in 7 to 14 days"]
    return '<div class="trust"><div class="wrap trust-in">' + "".join(f'<span>{icon("check")}{t}</span>' for t in items) + "</div></div>"


def faq_block(faqs, heading="Frequently asked questions"):
    items = "".join(f'<details class="faq"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faqs)
    return f'<section class="sec alt"><div class="wrap narrow"><h2>{heading}</h2>{items}</div></section>'


def cta_band(text="Ready to see your cash offer?"):
    return f'''<section class="cta-band"><div class="wrap">
<h2>{text}</h2><p>Free, no-obligation offer. Talk to a real person, not a call center.</p>
<div class="cta-btns"><a class="btn" href="/get-cash-offer/">Get My Cash Offer</a><a class="btn btn-ghost" href="tel:{PHONE_TEL}">{icon("phone")}Call {PHONE_DISPLAY}</a></div>
</div></section>'''


def situation_cards():
    return '<div class="cards">' + "".join(
        f'<a class="card" href="/{s["slug"]}/">{icon(s["icon"], "card-ic")}<h3>{s["short"]}</h3><p>{E(s["desc"][:110].rsplit(" ", 1)[0])}&hellip;</p></a>'
        for s in SITUATIONS) + "</div>"


def city_grid():
    regions = {}
    for c in CITIES: regions.setdefault(c["region"], []).append(c)
    return '<div class="regions">' + "".join(
        f'<div class="region"><h3>{r}</h3><ul>' + "".join(f'<li><a href="{city_url(c["slug"])}">We buy houses in {c["name"]}</a></li>' for c in cs) + "</ul></div>"
        for r, cs in regions.items()) + "</div>"


COMPARE = f'''<div class="table-wrap"><table class="compare">
<caption>Selling to Acorn House Buyer vs. listing with an agent in North Carolina</caption>
<thead><tr><th scope="col"></th><th scope="col">Acorn House Buyer</th><th scope="col">Listing with an agent</th></tr></thead>
<tbody>
<tr><th scope="row">Commissions</th><td>None</td><td>Negotiable, often 5% to 6% total</td></tr>
<tr><th scope="row">Repairs and prep</th><td>None, sold as-is</td><td>Usually expected before listing or after inspection</td></tr>
<tr><th scope="row">Closing costs</th><td>We pay the normal seller costs</td><td>Seller pays, including NC excise tax ($1 per $500)</td></tr>
<tr><th scope="row">Showings and open houses</th><td>One walkthrough</td><td>As many as it takes</td></tr>
<tr><th scope="row">Financing risk</th><td>Cash, no lender approval</td><td>Buyer loans and appraisals can fall through</td></tr>
<tr><th scope="row">Time to close</th><td>7 to 14 days, or your date</td><td>Often 60 to 90+ days including time on market</td></tr>
<tr><th scope="row">Best when</th><td>House needs work or you need speed and certainty</td><td>House is updated and you can wait for top dollar</td></tr>
</tbody></table></div>'''


# ---------------------------------------------------------------- pages
def build_home():
    body = f'''<section class="hero"><div class="wrap hero-in">
<div class="hero-copy">
<p class="eyebrow light">North Carolina cash home buyers</p>
<h1>We Buy Houses for Cash in North Carolina</h1>
<p class="lead">Sell your house as-is, with no repairs, no commissions and no showings. Get a fair written cash offer, usually within 24 hours, and close with a local attorney on the date you choose.</p>
<ul class="ticks">{"".join(f"<li>{icon('check')}{t}</li>" for t in ["Any condition: we handle the repairs and cleanout", "Foreclosure, inherited, divorce, rentals, relocation", "Charlotte, Triangle, Triad, the coast and the mountains"])}</ul>
<p class="hero-call">Prefer to talk? <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
</div>
<div class="hero-form">{close_form()}</div>
</div></section>
{trust_strip()}
{steps_block()}
<section class="sec alt"><div class="wrap">
<p class="eyebrow">Every situation</p><h2>We help homeowners in tough spots</h2>
<p class="sec-lead">Most of the houses we buy come with a story. Whatever yours is, we have probably seen it, and we can usually help.</p>
{situation_cards()}
</div></section>
<section class="sec"><div class="wrap">
<p class="eyebrow">Compare your options</p><h2>Cash sale or list with an agent?</h2>
<p class="sec-lead">A cash sale isn't right for every house. Here's an honest side-by-side so you can decide what works for you.</p>
{COMPARE}
<p class="center"><a href="/sell-to-cash-buyer-vs-agent-nc/">Read the full comparison &rarr;</a></p>
</div></section>
<section class="sec alt"><div class="wrap">
<p class="eyebrow">Where we buy</p><h2>We buy houses all across North Carolina</h2>
<p class="sec-lead">We're based in the Charlotte area and buy from the mountains to the coast. Don't see your town? Call us. If we can't buy it, we'll tell you who can.</p>
{city_grid()}
</div></section>
<section class="sec"><div class="wrap two-col">
<div><p class="eyebrow">Transparent offers</p><h2>How we calculate your cash offer</h2>
<p>We don't play games with lowball numbers. Our offer starts with what your house would sell for once it's fully fixed up, based on recent nearby sales. Then we subtract:</p>
<ul class="list"><li>The cost of repairs and updates</li><li>Our closing, holding and resale costs</li><li>A fair profit margin for the risk we take on</li></ul>
<p>We'll show you how we got to our number. If listing with an agent would clearly put more money in your pocket, we'll tell you that too.</p></div>
<div class="callout"><h3>Every sale is handled by a closing attorney</h3><p>North Carolina is an attorney-closing state. A licensed closing attorney checks the title, pays off your mortgage and any liens, and sends you your money. You'll never hand money to us, and we never ask you to.</p><a class="btn" href="/how-it-works/">See the full process</a></div>
</div></section>
{faq_block(FAQ_HOME)}
{cta_band()}'''
    page("/", "We Buy Houses for Cash in NC | Acorn House Buyer",
         "Sell your North Carolina house fast for cash. Any condition, no repairs, no commissions. Get a fair written offer in 24 hours and close on your date.",
         body, schema=[faq_schema(FAQ_HOME)], priority="1.0", head_extra=CLOSE_SCRIPT)


def build_city(c):
    n = c["name"]
    path = city_url(c["slug"])
    nearby = [CITY_BY_SLUG[s] for s in c["nearby"] if s in CITY_BY_SLUG]
    faqs = [
        (f"How fast can you buy my house in {n}?", f"In most cases we can make a written cash offer within 24 hours of seeing the house and close in 7 to 14 days through a {c['county']} County area closing attorney. If you need more time, you choose the closing date."),
        (f"Do you buy houses in any condition in {n}?", f"Yes. We buy {n} houses that need major repairs, have tenants, are full of belongings, or have fire, water or foundation damage. You don't need to fix or clean anything."),
        (f"Are there any fees to sell my {n} house to you?", "No. There are no commissions or fees, and we pay the normal seller closing costs. Your mortgage and any liens are paid off from the sale at closing."),
        (f"What areas near {n} do you buy in?", f"We buy throughout {c['county']} County and the surrounding area, including {', '.join(c['hoods'][:-1])} and {c['hoods'][-1]}."),
    ]
    hoods = "".join(f"<li>{E(h)}</li>" for h in c["hoods"])
    near = "".join(f'<li><a href="{city_url(x["slug"])}">Sell my house fast in {x["name"]}</a></li>' for x in nearby)
    body = f'''<section class="hero hero-sm"><div class="wrap hero-in">
<div class="hero-copy">
<p class="eyebrow light">{E(c["county"])} County cash home buyer</p>
<h1>We Buy Houses in {n}, NC for Cash</h1>
<p class="lead">{E(c["intro"])}</p>
<ul class="ticks">{"".join(f"<li>{icon('check')}{t}</li>" for t in ["As-is: no repairs, cleaning or showings", "No commissions; we pay normal closing costs", "Close in 7 to 14 days or on your date"])}</ul>
<p class="hero-call">Call or text: <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
</div>
<div class="hero-form">{lead_form(f"Get Your {n} Cash Offer", fid="city")}</div>
</div></section>
{trust_strip()}
<section class="sec"><div class="wrap two-col">
<div><p class="eyebrow">Selling in {n}</p><h2>Why {n} homeowners sell to us</h2><p>{E(c["local"])}</p>
<p>Selling to a cash buyer won't be the right move for everyone. If your home is updated and you have time, listing with a good local agent may get you a higher price. But if you need speed, certainty, or don't want to deal with repairs, our offer can save you months.</p></div>
<div class="callout"><h3>Areas we buy in and around {n}</h3><ul class="pill-list">{hoods}</ul><p class="small">Plus every other part of {E(c["county"])} County. Not sure if we cover your street? Just ask.</p></div>
</div></section>
{steps_block()}
<section class="sec alt"><div class="wrap">
<h2>We buy {n} houses in any situation</h2>
{situation_cards()}
</div></section>
{faq_block(faqs, f"Selling your house in {n}: common questions")}
<section class="sec"><div class="wrap"><h2>We also buy houses near {n}</h2><ul class="link-list">{near}<li><a href="/north-carolina/">All North Carolina areas</a></li></ul></div></section>
{cta_band(f"Get a fair cash offer for your {n} house")}'''
    title = f"We Buy Houses {n} NC | Sell Fast for Cash"
    if len(title) > 60: title = f"We Buy Houses {n}, NC for Cash"
    desc = f"Sell your house fast in {n}, NC. We buy houses for cash in any condition across {c['county']} County. No repairs or commissions; close on your date."
    if len(desc) > 160: desc = f"Sell your {n}, NC house fast for cash, in any condition. No repairs, no commissions. Get a fair offer in 24 hours."
    service = {"@type": "Service", "name": f"We buy houses for cash in {n}, NC", "serviceType": "Cash home buying",
               "provider": {"@id": ORG_ID}, "areaServed": {"@type": "City", "name": f"{n}, NC",
               "containedInPlace": {"@type": "AdministrativeArea", "name": f"{c['county']} County, North Carolina"}}}
    page(path, title, desc, body, schema=[service, faq_schema(faqs)],
         trail=[("Home", "/"), ("North Carolina", "/north-carolina/"), (n, path)], priority="0.8")


def build_situation(s):
    path = f"/{s['slug']}/"
    secs = "".join(f"<h2>{E(h)}</h2><p>{E(p)}</p>" for h, p in s["sections"])
    others = "".join(f'<li><a href="/{o["slug"]}/">{o["short"]}</a></li>' for o in SITUATIONS if o is not s)
    body = f'''<section class="hero hero-sm"><div class="wrap hero-in">
<div class="hero-copy"><p class="eyebrow light">{E(s["short"])}</p><h1>{E(s["h1"])}</h1><p class="lead">{E(s["intro"])}</p>
<p class="hero-call">Talk it through with us: <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p></div>
<div class="hero-form">{lead_form(fid="sit")}</div></div></section>
{trust_strip()}
<section class="sec"><div class="wrap prose-wrap"><article class="prose">{secs}
<p class="note">This page is general information, not legal or financial advice. For your specific situation, talk with a North Carolina attorney or a HUD-approved housing counselor.</p></article>
<aside class="side"><h2 class="side-h">Other situations we help with</h2><ul>{others}</ul><h2 class="side-h">Popular areas</h2><ul>{"".join(f'<li><a href="{city_url(c["slug"])}">{c["name"]}</a></li>' for c in CITIES[:8])}</ul></aside></div></section>
{steps_block()}
{cta_band()}'''
    page(path, s["title"], s["desc"], body,
         schema=[{"@type": "Service", "name": s["h1"], "serviceType": "Cash home buying", "provider": {"@id": ORG_ID},
                  "areaServed": {"@type": "State", "name": "North Carolina"}}],
         trail=[("Home", "/"), ("Situations", "/situations/"), (s["short"], path)], priority="0.8")


def build_simple_pages():
    # North Carolina hub
    body = f'''<section class="page-head"><div class="wrap"><h1>We Buy Houses Anywhere in North Carolina</h1>
<p class="lead">From Charlotte and Lake Norman to the Triangle, the Triad, the coast and the mountains, we buy houses for cash in any condition. Pick your area below, or call {PHONE_DISPLAY}.</p></div></section>
<section class="sec"><div class="wrap">{city_grid()}
<p class="sec-lead">We also buy in smaller towns and rural areas between these cities, including homes on land, manufactured homes on owned lots, and properties with well and septic.</p></div></section>
{steps_block()}{cta_band()}'''
    page("/north-carolina/", "Areas We Buy Houses in North Carolina | Acorn",
         "We buy houses for cash all over North Carolina: Charlotte, Raleigh, Durham, Greensboro, Winston-Salem, Fayetteville, Wilmington, Asheville and more.",
         body, trail=[("Home", "/"), ("North Carolina", "/north-carolina/")], priority="0.9")

    # Situations hub
    body = f'''<section class="page-head"><div class="wrap"><h1>Sell Your House Fast in Any Situation</h1>
<p class="lead">Life doesn't always line up with a 90-day listing. Here's how we help North Carolina homeowners in the situations we see most.</p></div></section>
<section class="sec"><div class="wrap">{situation_cards()}</div></section>{cta_band()}'''
    page("/situations/", "Sell Your House in Any Situation | NC Cash Buyer",
         "Foreclosure, inherited homes, divorce, tired landlords, major repairs or relocation: see how a cash sale works for your situation in North Carolina.",
         body, trail=[("Home", "/"), ("Situations", "/situations/")], priority="0.7")

    # How it works
    faqs = FAQ_HOME[:5]
    body = f'''<section class="page-head"><div class="wrap"><h1>How Selling Your House to Us Works</h1>
<p class="lead">A simple, transparent process with a licensed North Carolina closing attorney handling the money and paperwork.</p></div></section>
<section class="sec"><div class="wrap prose-wrap"><article class="prose">
<h2>1. Tell us about your property</h2><p>Call {PHONE_DISPLAY} or send the short form. We'll ask about the house, its condition and your timeline. There's no cost and no pressure.</p>
<h2>2. We see the house once</h2><p>We schedule one walkthrough at a time that suits you, usually within a day or two. If you're out of town, a family member, tenant or lockbox works too, and some homes we can price from photos and video.</p>
<h2>3. You get a written cash offer</h2><p>Usually within 24 hours. We explain how we arrived at the number, including the repair estimate. The offer is all cash, so there's no lender approval or appraisal to wait for.</p>
<h2>4. Sign the agreement and pick a date</h2><p>If you accept, we sign a simple purchase agreement and send it to a North Carolina closing attorney. They search the title and order a payoff from your lender. You decide the closing date.</p>
<h2>5. Close and get paid</h2><p>You sign at the attorney's office or remotely with a mobile notary. The attorney pays off your mortgage and liens and sends your proceeds by wire or check. Leave anything you don't want; we take care of it.</p>
</article><aside class="side">{lead_form("Start With a Free Offer", "Takes about 2 minutes.", "hiw")}</aside></div></section>
{faq_block(faqs)}{cta_band()}'''
    page("/how-it-works/", "How It Works: Sell Your NC House for Cash",
         "See how selling your house for cash to Acorn House Buyer works, step by step: one walkthrough, a written offer and an attorney closing on your date.",
         body, schema=[faq_schema(faqs)], trail=[("Home", "/"), ("How It Works", "/how-it-works/")], priority="0.8")

    # Cash vs agent
    faqs = [("Will I get less selling to a cash buyer?", "Usually the headline price is lower than a fully updated retail listing. But after commissions, repairs, closing costs and months of mortgage, tax and insurance payments, the net difference is often smaller than people expect, and sometimes there is none."),
            ("When should I list with an agent instead?", "If your home is in good, updated condition, you're not in a hurry and you can handle showings and inspection repairs, listing will often get you a higher price. We'll tell you if we think that's the case."),
            ("How do I compare offers fairly?", "Compare your net proceeds, not the sale price: price minus commissions, repairs, closing costs, and the costs of holding the house until it sells.")]
    body = f'''<section class="page-head"><div class="wrap"><h1>Cash Buyer vs. Listing With an Agent in NC</h1>
<p class="lead">An honest look at both options, so you can pick the one that puts you in the best position.</p></div></section>
<section class="sec"><div class="wrap">{COMPARE}</div></section>
<section class="sec alt"><div class="wrap prose-wrap"><article class="prose">
<h2>Compare net proceeds, not list price</h2><p>A listing price is only the starting point. Agent commissions are negotiable but often total 5% to 6% of the price. Then come pre-listing repairs, buyer inspection requests, concessions, NC excise tax of $1 per $500 of the price, attorney fees, and every month of mortgage, taxes, insurance and utilities while the house is on the market.</p>
<h2>Example: a $300,000 house that needs work</h2><p>Say a house would sell for $300,000 fully updated, but needs $35,000 of repairs. Listing as-is means fewer buyers, and many can't get loans on it. Fixing it first means paying for the work, taking on contractor risk and waiting. A cash offer accounts for those repairs up front, so you skip the work, the commissions and the wait.</p>
<h2>When a cash sale makes the most sense</h2><p>Major repairs, inherited homes you don't want to manage, tenants in place, foreclosure deadlines, divorce, or a move on a fixed date. In these cases, certainty and speed are often worth more than a higher price that may never close.</p>
<h2>When listing makes more sense</h2><p>If your home is updated, in a high-demand area, and you have time, an agent will often get you more. We would rather tell you that than make an offer that doesn't fit.</p>
</article><aside class="side">{lead_form("Compare With a Real Offer", "Free, no obligation.", "cmp")}</aside></div></section>
{faq_block(faqs)}{cta_band()}'''
    page("/sell-to-cash-buyer-vs-agent-nc/", "Cash Home Buyer vs. Realtor in NC: Honest Compare",
         "Should you sell your North Carolina house to a cash buyer or list with an agent? Compare fees, repairs, timelines and net proceeds side by side.",
         body, schema=[faq_schema(faqs)], trail=[("Home", "/"), ("Cash vs. Agent", "/sell-to-cash-buyer-vs-agent-nc/")], priority="0.8")

    # FAQ
    body = f'''<section class="page-head"><div class="wrap"><h1>Frequently Asked Questions</h1>
<p class="lead">Straight answers about selling your house for cash in North Carolina. Don't see your question? Call {PHONE_DISPLAY}.</p></div></section>
{faq_block(FAQ_HOME, "Selling your house to Acorn House Buyer")}{cta_band()}'''
    page("/faq/", "FAQ: Selling Your House for Cash in NC",
         "Answers to common questions about selling your house for cash in North Carolina: offers, fees, closing costs, timelines, repairs and closing attorneys.",
         body, schema=[faq_schema(FAQ_HOME)], trail=[("Home", "/"), ("FAQ", "/faq/")], priority="0.7")

    # About
    body = f'''<section class="page-head"><div class="wrap"><h1>About Acorn House Buyer</h1>
<p class="lead">A North Carolina home buying company built on straight answers and fair offers.</p></div></section>
<section class="sec"><div class="wrap prose-wrap"><article class="prose">
<h2>Who we are</h2><p>Acorn House Buyer is a real estate investment company based in the Charlotte area. We buy houses directly from homeowners across North Carolina, mostly homes that need work or owners who need a fast, certain sale.</p>
<h2>How we work</h2><p>Like an acorn that grows into something strong, we believe good deals start small and honest: a real conversation, a fair number with the math shown, and a closing handled by a licensed North Carolina attorney. We don't use pressure tactics, and we're happy to tell you when listing with an agent would serve you better.</p>
<h2>What we are not</h2><p>We are not real estate agents and we don't list houses. We are buyers. When we make you an offer, we either buy the property ourselves or, in some cases, assign the contract to a partner investor, which we will disclose to you. Either way, your price and terms don't change, and you never pay us anything.</p>
<h2>Our promise</h2><ul class="list"><li>Fair, written offers with the reasoning explained</li><li>No fees, no commissions, no surprise deductions</li><li>Every sale closed through a licensed NC closing attorney</li><li>Your information stays private and is never sold</li></ul>
</article><aside class="side">{lead_form("Talk to Us About Your House", "No obligation.", "abt")}</aside></div></section>{cta_band()}'''
    page("/about/", "About Acorn House Buyer | NC Cash Home Buyers",
         "Acorn House Buyer is a Charlotte-based real estate investment company buying houses for cash across North Carolina with fair, transparent offers.",
         body, trail=[("Home", "/"), ("About", "/about/")], priority="0.6")

    # Contact
    body = f'''<section class="page-head"><div class="wrap"><h1>Contact Acorn House Buyer</h1>
<p class="lead">Call, text or email. You'll reach a real person on our team.</p></div></section>
<section class="sec"><div class="wrap two-col">
<div class="contact-list">
<a class="contact-item" href="tel:{PHONE_TEL}">{icon("phone", "card-ic")}<span><b>Call or text</b>{PHONE_DISPLAY}</span></a>
<a class="contact-item" href="mailto:{EMAIL}">{icon("mail", "card-ic")}<span><b>Email</b>{EMAIL}</span></a>
<p>Hours: Monday to Saturday, 8am to 8pm. Leave a message any time and we'll call you back.</p>
<p>We buy houses throughout <a href="/north-carolina/">North Carolina</a>.</p></div>
<div>{lead_form("Send Us Your Property", "We usually reply within a few hours.", "ct")}</div>
</div></section>'''
    page("/contact/", "Contact Us | Acorn House Buyer, North Carolina",
         f"Contact Acorn House Buyer to sell your North Carolina house for cash. Call or text {PHONE_DISPLAY} or email {EMAIL}.",
         body, schema=[{"@type": "ContactPage", "url": SITE + "/contact/", "about": {"@id": ORG_ID}}],
         trail=[("Home", "/"), ("Contact", "/contact/")], priority="0.6")

    # Get offer
    body = f'''<section class="page-head"><div class="wrap"><h1>Get Your Free Cash Offer</h1>
<p class="lead">Tell us about your North Carolina property. We'll reach out to ask a few questions and set up a quick walkthrough.</p></div></section>
<section class="sec"><div class="wrap two-col">
<div>{lead_form("Your Property", "Takes about 2 minutes. No obligation.", "go")}</div>
<div class="callout"><h3>What happens next</h3><ol class="list"><li>We call you, usually within a few hours</li><li>We schedule one walkthrough</li><li>You get a written cash offer, usually within 24 hours</li><li>You choose whether to accept, and when to close</li></ol>
<p>Rather talk now? Call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p></div>
</div></section>{trust_strip()}'''
    page("/get-cash-offer/", "Get a Free Cash Offer for Your NC House",
         "Request a free, no-obligation cash offer for your North Carolina house. Any condition, no repairs or commissions. We usually reply within hours.",
         body, trail=[("Home", "/"), ("Get a Cash Offer", "/get-cash-offer/")], priority="0.9")

    # Thank you (noindex)
    body = f'''<section class="page-head"><div class="wrap"><h1>Thank You! We Got Your Info</h1>
<p class="lead">Someone from our team will reach out shortly, usually within a few hours during business hours. Need us sooner? Call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
<p><a class="btn" href="/how-it-works/">See what happens next</a></p></div></section>'''
    page("/thank-you/", "Thank You | Acorn House Buyer",
         "Thanks for contacting Acorn House Buyer. We received your property information and will reach out shortly.",
         body, robots="noindex,follow", in_sitemap=False)

    legal = LEGAL_NAME or BRAND
    privacy = f'''<section class="page-head"><div class="wrap"><h1>Privacy Policy</h1><p>Last updated {TODAY}</p></div></section>
<section class="sec"><div class="wrap narrow prose">
<p>This policy explains how {E(legal)} ("we", "us") collects and uses information on acornhousebuyer.com.</p>
<h2>Information we collect</h2><p>When you submit a form, call, text or email us, we collect what you provide, such as your name, phone number, email, property address and details about the property. Like most websites, we may also collect basic technical data such as browser type, pages visited and approximate location through cookies and analytics tools.</p>
<h2>How we use it</h2><p>We use your information to respond to you, evaluate your property, make offers, and communicate about a potential purchase. We may share property and contact details with closing attorneys, title companies, and, when relevant to a purchase, partner investors, only as needed to complete the transaction.</p>
<h2>Text messages</h2><p>If you give us your phone number, you agree we may contact you by call or text about your property. Message frequency varies. Message and data rates may apply. Reply STOP to opt out or HELP for help. We do not sell or share your mobile number or SMS consent with third parties or affiliates for their marketing purposes.</p>
<h2>We don't sell your information</h2><p>We do not sell your personal information.</p>
<h2>Your choices</h2><p>You can ask us to stop contacting you, or to access or delete your information, by emailing <a href="mailto:{EMAIL}">{EMAIL}</a> or calling {PHONE_DISPLAY}.</p>
<h2>Security</h2><p>We use reasonable safeguards to protect your information, but no method of transmission over the internet is 100% secure.</p>
<h2>Changes</h2><p>We may update this policy. The date above shows the latest version.</p>
</div></section>'''
    page("/privacy-policy/", "Privacy Policy | Acorn House Buyer",
         "How Acorn House Buyer collects, uses and protects the information you share with us, including our text message (SMS) policy.",
         privacy, trail=[("Home", "/"), ("Privacy Policy", "/privacy-policy/")], priority="0.2")

    terms = f'''<section class="page-head"><div class="wrap"><h1>Terms of Use</h1><p>Last updated {TODAY}</p></div></section>
<section class="sec"><div class="wrap narrow prose">
<p>By using acornhousebuyer.com you agree to these terms.</p>
<h2>No offer or advice</h2><p>Content on this site is general information only and is not legal, tax or financial advice. Nothing on this site is an offer to buy any specific property. Any purchase is subject to a written purchase agreement signed by both parties.</p>
<h2>Not a brokerage</h2><p>{E(legal)} is a real estate investment company, not a licensed real estate brokerage. We buy property for our own account and may assign purchase contracts to partner investors, which we will disclose.</p>
<h2>Accuracy</h2><p>We try to keep information accurate but make no warranties about completeness or accuracy. Timelines such as "close in 7 to 14 days" depend on title, payoff and other factors.</p>
<h2>Contact</h2><p>Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>'''
    page("/terms/", "Terms of Use | Acorn House Buyer",
         "Terms of use for acornhousebuyer.com, a North Carolina real estate investment company that buys houses for cash.",
         terms, trail=[("Home", "/"), ("Terms of Use", "/terms/")], priority="0.2")

    # 404 (GitHub Pages serves /404.html)
    body = f'''<section class="page-head"><div class="wrap"><h1>Page Not Found</h1>
<p class="lead">That page doesn't exist, but we can still make you an offer on your house.</p>
<p><a class="btn" href="/">Go to the home page</a> <a class="btn btn-ghost-dark" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></p></div></section>'''
    page("/404.html", "Page Not Found | Acorn House Buyer",
         "The page you were looking for doesn't exist. Sell your North Carolina house for cash with Acorn House Buyer.",
         body, robots="noindex,follow", in_sitemap=False)


def build_meta_files():
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for p, pr in PAGES)
    w = lambda name, s: open(os.path.join(ROOT, name), "w", encoding="utf-8").write(s)
    w("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    w("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /thank-you/\n\nSitemap: {SITE}/sitemap.xml\n")
    w("CNAME", SITE.split("//")[1] + "\n")
    w("site.webmanifest", json.dumps({"name": BRAND, "short_name": "Acorn", "start_url": "/", "display": "standalone",
                                      "background_color": "#faf6ef", "theme_color": "#1f4d3a",
                                      "icons": [{"src": "/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
                                                {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1))
    cities = "\n".join(f"- [{c['name']}, NC]({SITE}{city_url(c['slug'])}): {c['county']} County" for c in CITIES)
    sits = "\n".join(f"- [{s['short']}]({SITE}/{s['slug']}/)" for s in SITUATIONS)
    w("llms.txt", f"""# {BRAND}

> {BRAND} buys houses for cash across North Carolina, as-is and in any condition. No repairs, no commissions, and we pay the normal seller closing costs. Written cash offer usually within 24 hours; close in 7 to 14 days or on the seller's date, through a licensed NC closing attorney.

{BRAND} is a real estate investment company, not a brokerage. It buys directly from owners and may assign purchase contracts to partner investors (disclosed to the seller).

- Phone: {PHONE_DISPLAY}
- Email: {EMAIL}
- Based in: {CITY}, {STATE}

## Main pages
- [Home]({SITE}/)
- [How it works]({SITE}/how-it-works/)
- [Cash buyer vs. agent]({SITE}/sell-to-cash-buyer-vs-agent-nc/)
- [FAQ]({SITE}/faq/)
- [Get a cash offer]({SITE}/get-cash-offer/)

## Situations
{sits}

## North Carolina areas
{cities}
""")


if __name__ == "__main__":
    build_home()
    for c in CITIES: build_city(c)
    for s in SITUATIONS: build_situation(s)
    build_simple_pages()
    build_meta_files()
    print(f"Built {len(PAGES)} indexable pages + 404 + thank-you")
