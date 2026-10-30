# acornhousebuyer.com

Static site for Acorn House Buyer (North Carolina cash home buyer), hosted on GitHub Pages.

## Edit and rebuild
- Business details (phone, address, form endpoint, GA4, Search Console): top of `_src/build.py`
- City / situation / FAQ text: `_src/content.py`
- Design: `assets/styles.css`

```
python3 _src/build.py   # regenerates every page, sitemap.xml, robots.txt, llms.txt
python3 _src/check.py   # SEO checks: titles, descriptions, H1, canonical, schema, links, sitemap
```
Images (`_src/make_images.py`) need Pillow. Folders starting with `_` are not published.
