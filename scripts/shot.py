#!/usr/bin/env python3
"""Screenshot of the app for the visual check loop: serves app/, loads 5 sample todos (2 done), shoots the page at phone width.

    <python with playwright> scripts/shot.py <out.png> [--filter all|open|done] [--css extra.css]

Needs Python Playwright with Chromium (this repo does not install it; the demo used the channel owner's existing one).
--css adds a stylesheet after style.css (used once to draw the mock).
"""
import functools, http.server, sys, threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
args = sys.argv[1:]
out = Path(args[0]).resolve()
flt = args[args.index("--filter") + 1] if "--filter" in args else "all"
css = Path(args[args.index("--css") + 1]).read_text() if "--css" in args else ""

TODOS = [{"id": f"m{i}", "title": t, "done": d, "createdAt": 1761700000000 + i} for i, (t, d) in enumerate(
    [("Đi chợ", True), ("Gọi mẹ", False), ("Trả tiền điện", False), ("Sửa xe", True), ("Đọc sách", False)])]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT / "app")))
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://localhost:{srv.server_port}/index.html"
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 420, "height": 560}, device_scale_factor=2)
    page.goto(url)
    page.evaluate("t => localStorage.setItem('todo.v1', JSON.stringify(t))", TODOS)
    page.reload()
    if css:
        page.add_style_tag(content=css)
    page.click(f'#filters button[data-filter="{flt}"]')
    out.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(out))
    b.close()
srv.shutdown()
print(f"saved {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out.name}")
