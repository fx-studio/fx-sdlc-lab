#!/usr/bin/env python3
"""T0 của plan khach-khong-mat-viec, chạy bằng máy: dữ liệu do bản CŨ ghi (commit fdf3791), mở bằng bản MỚI, trong Chromium headless.

    ~/.fx-voice/venv/bin/python demo/sdlc-3/t0-chromium.py <thư-mục-tạm>

Không thay người kiểm tay: chỉ Chromium (không Safari iOS, không Chrome Android), không trình đọc màn hình, không nhìn giao diện.
Thêm hai việc Khoa gợi ý ở R3c: sao lưu rồi nhập lại chính dữ liệu đó, và dữ liệu hỏng (T9) không bị ghi đè.
"""
import functools, http.server, json, shutil, subprocess, sys, threading, time
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[2]
TMP = Path(sys.argv[1]).resolve()
SITE = TMP / "site"


def serve():
    class Im(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    h = functools.partial(Im, directory=str(SITE))
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return f"http://localhost:{s.server_port}"


def put():
    """/cu/ = app/ ở commit fdf3791 (trước thay đổi), /moi/ = app/ ở cây làm việc. Cùng origin nên dùng chung localStorage,
    khác đường dẫn nên trình duyệt không lấy nhầm store.js của bản này cho bản kia."""
    shutil.rmtree(SITE, ignore_errors=True)
    shutil.copytree(REPO / "app", SITE / "moi")
    (SITE / "cu").mkdir(parents=True)
    tar = subprocess.run(["git", "archive", "fdf3791", "app"], cwd=REPO, capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(SITE / "cu"), "--strip-components=1"], input=tar, check=True)


def state(page):
    return page.evaluate("""() => ({
      li: document.querySelectorAll('#list li').length,
      raw: localStorage.getItem('todo.v1'),
      banner: !document.querySelector('#unreadable')?.hidden,
      empty: !document.querySelector('#empty')?.hidden,
      message: document.querySelector('#message')?.textContent || '',
      count: document.querySelector('#count')?.textContent || '' })""")


def add(page, title):
    page.fill("#title", title)
    page.press("#title", "Enter")


def kiem(ten, dung, chi_tiet=""):
    print(f"{'ĐẠT ' if dung else 'TRƯỢT'} · {ten}{' · ' + chi_tiet if chi_tiet else ''}")
    return dung


def main():
    put()
    base = serve()
    cu, moi = base + "/cu/index.html", base + "/moi/index.html"
    ok = True
    with sync_playwright() as p:
        b = p.chromium.launch()
        for ten, n in (("3 việc thêm bằng tay ở bản cũ", 3), ("2.000 việc do store.save của bản cũ ghi", 2000)):
            print(f"\n## {ten}")
            ctx = b.new_context(accept_downloads=True)
            page = ctx.new_page()
            page.goto(cu)
            if n == 3:
                for t in ("Mua sữa", "  Gọi cho Hà  ", "Trả sách <b>thư viện</b> 📚"):
                    add(page, t)
                page.click("#list li:nth-child(2) input[type=checkbox]")
            else:
                page.evaluate("""n => { const t0 = Date.now(); store.save(Array.from({length: n}, (_, i) => ({
                  id: crypto.randomUUID(), title: 'Việc số ' + (i + 1) + ' — ' + 'x'.repeat(i % 120), done: i % 3 === 0,
                  createdAt: t0 - i * 60000 }))) }""", n)
            ghi_cu = json.loads(state(page)["raw"])
            ok &= kiem("bản cũ đã ghi", len(ghi_cu) == n, f"{len(ghi_cu)} việc, {len(state(page)['raw'])} ký tự")

            t = time.time()
            page.goto(moi)
            s = state(page)
            ok &= kiem("bản mới mở ra đủ việc", s["li"] == n, f"{s['li']} dòng, {time.time() - t:.2f} s")
            ok &= kiem("không dải báo đọc lỗi, không dòng trống", not s["banner"] and not s["empty"])
            ok &= kiem("mở ra không ghi lại dữ liệu", s["raw"] == json.dumps(ghi_cu, ensure_ascii=False, separators=(",", ":"))
                       or json.loads(s["raw"]) == ghi_cu)
            add(page, "Việc thêm ở bản mới")
            page.reload()
            s = state(page)
            ok &= kiem("thêm một việc rồi tải lại", s["li"] == n + 1 and len(json.loads(s["raw"])) == n + 1, f"{s['li']} dòng")
            truoc = json.loads(s["raw"])

            with page.expect_download() as d:
                page.click("#export")
            f = TMP / f"sao-luu-{n}.json"
            d.value.save_as(f)
            tep = json.loads(f.read_text())
            ok &= kiem("file sao lưu", len(tep["todos"]) == n + 1, f"{d.value.suggested_filename}, {f.stat().st_size} byte")

            t = time.time()
            page.set_input_files("#import", str(f))
            page.wait_for_selector("#confirm[open]")
            hoi = page.text_content("#confirm-text")
            page.click("#confirm button[value=yes]")
            page.wait_for_function("() => !document.querySelector('#confirm').open")
            page.wait_for_timeout(300)
            s = state(page)
            ok &= kiem("nhập lại chính file đó: hỏi trước khi thay", str(n + 1) in hoi.replace(".", ""), hoi)
            ok &= kiem("nhập lại: danh sách y như trước", json.loads(s["raw"]) == truoc and s["li"] == n + 1,
                       f"{time.time() - t:.2f} s, thông báo: {s['message']}")
            ctx.close()

        print("\n## Dữ liệu hỏng (T9)")
        ctx = b.new_context()
        page = ctx.new_page()
        page.goto(moi)
        page.evaluate("() => localStorage.setItem('todo.v1', '{hỏng')")
        page.reload()
        s = state(page)
        ok &= kiem("dải báo hiện, dòng trống ẩn", s["banner"] and not s["empty"], s["message"] or "")
        add(page, "Thêm khi dữ liệu hỏng")
        page.reload()
        ok &= kiem("thêm việc rồi tải lại: dữ liệu hỏng vẫn nguyên", state(page)["raw"] == "{hỏng")
        b.close()
    print("\nTất cả đạt" if ok else "\nCÓ MỤC TRƯỢT")


if __name__ == "__main__":
    main()
