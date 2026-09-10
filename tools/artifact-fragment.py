#!/usr/bin/env python3
"""Turn index.html into the fragment the claude.ai artifact platform expects.

The platform supplies <!doctype>, <html>, <head> and <body>; everything we
author — <title>, font links, the <style>, the markup, the <script> — must
arrive as one fragment. This keeps the head *contents* (title, metas, links,
style) and the body *contents*, and drops only the document wrapper.

    python3 tools/artifact-fragment.py index.html /path/to/out.html
"""
import sys
src, dst = sys.argv[1], sys.argv[2]
h = open(src, encoding="utf-8").read()
head_inner = h[h.index("<title>") : h.index("</head>")]
body_inner = h[h.index("<body>") + len("<body>") : h.rindex("</body>")]
frag = head_inner.rstrip() + "\n" + body_inner.strip() + "\n"
for bad in ("<!doctype", "<html", "</head>", "<body>", "</body>", "</html>"):
    assert bad not in frag, "wrapper leaked: " + bad
open(dst, "w", encoding="utf-8").write(frag)
print("fragment:", len(frag), "bytes ->", dst)
