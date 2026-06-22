#!/usr/bin/env python3
"""Inject a '看房 / Viewing' link into each KL scorecard's nav-actions.

Idempotent: skips files that already have the link. Building name is read from
<h1 class="proj-name">, language from the _en/_zh filename suffix, and the
checklist mode (completed / offplan) from the building's status.code in
kl-check.html's `projects` array so the link opens the right viewing mode.
"""
import glob, re, os, json, urllib.parse, html as _html

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, '..')
KLDIR = os.path.join(ROOT, 'kl')

# --- map scorecard filename -> mode (offplan / completed) from kl-check data ---
def load_mode_map():
    html = open(os.path.join(ROOT, 'kl-check.html'), encoding='utf-8').read()
    i = html.index('const projects =')
    start = html.index('[', i)
    depth = 0
    for j in range(start, len(html)):
        if html[j] == '[': depth += 1
        elif html[j] == ']':
            depth -= 1
            if depth == 0:
                end = j + 1; break
    arr = json.loads(html[start:end])
    m = {}
    for p in arr:
        mode = 'offplan' if p.get('status', {}).get('code') == 'offplan' else 'completed'
        for lang in ('en', 'zh'):
            u = p.get('urls', {}).get(lang)
            if u:
                m[os.path.basename(u)] = mode
    return m

mode_map = load_mode_map()
proj_re = re.compile(r'<h1 class="proj-name">(.*?)</h1>', re.S)
tag_re = re.compile(r'<[^>]+>')

changed, skipped, missing = [], [], []
for f in sorted(glob.glob(os.path.join(KLDIR, 'SC_*.html'))):
    base = os.path.basename(f)
    with open(f, encoding='utf-8') as fh:
        html = fh.read()
    if 'viewing.html?b=' in html:
        skipped.append(base); continue
    m = proj_re.search(html)
    if not m:
        missing.append(base); continue
    name = re.sub(r'\s+', ' ', _html.unescape(tag_re.sub('', m.group(1)))).strip()
    lang = 'zh' if f.endswith('_zh.html') else 'en'
    label = '看房' if lang == 'zh' else 'Viewing'
    mode = mode_map.get(base, 'completed')
    enc = urllib.parse.quote(name, safe='')
    link = ('<a class="back-link" href="viewing.html?b=%s&amp;lang=%s&amp;mode=%s" '
            'style="color:var(--gold-deep);font-weight:600">\U0001F4CB %s</a>\n      '
            % (enc, lang, mode, label))
    anchor = '<a class="lang-link"'
    if anchor not in html:
        missing.append(base + ' (no lang-link)'); continue
    html = html.replace(anchor, link + anchor, 1)
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(html)
    changed.append('%s -> %s [%s · %s]' % (base, name, lang, mode))

print('CHANGED (%d):' % len(changed))
for c in changed: print('  ', c)
if skipped: print('SKIPPED already-linked (%d)' % len(skipped))
if missing:
    print('!! MISSING (%d):' % len(missing))
    for x in missing: print('  ', x)
