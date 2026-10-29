#!/usr/bin/env python3
"""Bảng kiểm tay T0–T13 của plan khach-khong-mat-viec, phần MÁY chạy được, trên Chromium headless (demo SDLC-4).

    ~/.fx-voice/venv/bin/python demo/sdlc-4/kiem-tay-may.py

Không thay người kiểm: chỉ Chromium (không Safari, không điện thoại), không bàn phím thật, không trình đọc màn hình (T12), không ai
nhìn giao diện. Mỗi dòng một phiên trình duyệt sạch. Ghi kết quả từng phép kiểm ra demo/sdlc-4/runs/T-kiem-may/ket-qua.md.
"""
import functools, http.server, json, sys, threading, time
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
FILES = HERE / "kiem-tay-files"
OUT = HERE / "runs" / "T-kiem-may"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(REPO))
MESSAGES = json.loads(__import__("subprocess").run(
    ["node", "-e", "console.log(JSON.stringify(require('./app/backup.js').MESSAGES))"], cwd=REPO, capture_output=True,
    text=True).stdout)


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(REPO / "app")))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://localhost:{srv.server_port}/index.html"

rows, cur = [], None


def check(name, ok, note=""):
    cur["checks"].append((name, bool(ok), note))


def seed_js(n, title="'Việc ' + i", done="i % 3 === 0"):
    return (f"localStorage.setItem('todo.v1', JSON.stringify(Array.from({{length: {n}}}, (_, i) => "
            f"({{id: crypto.randomUUID(), title: {title}, done: {done}, createdAt: Date.now() - i}}))))")


# Fills storage until not even one more character fits (big chunks first, then smaller), so the app's next write fails.
FILL = ("() => { let i = 0; for (const size of [200000, 10000, 500, 20, 1]) { try { for (;; i++) "
        "localStorage.setItem('day' + i, 'x'.repeat(size)) } catch (e) {} } return i }")


class App:
    def __init__(self, browser):
        self.ctx = browser.new_context(accept_downloads=True)
        self.page = self.ctx.new_page()
        self.alerts = []
        self.page.on("dialog", lambda d: (self.alerts.append(d.message), d.dismiss()))
        self.requests = []
        self.page.on("request", lambda r: self.requests.append(r.url))
        self.page.goto(URL)

    def js(self, code, arg=None):
        return self.page.evaluate(code, arg) if arg is not None else self.page.evaluate(code)

    def reload(self):
        self.page.reload()

    def seed(self, n, **kw):
        self.js(seed_js(n, **kw))
        self.reload()

    def raw(self, key="todo.v1"):
        return self.js(f"localStorage.getItem('{key}')")

    def li(self):
        return self.page.locator("#list li").count()

    def msg(self):
        return self.page.locator("#message").text_content()

    def banner(self):
        return self.page.locator("#unreadable").is_visible()

    def empty_shown(self):
        return self.page.locator("#empty").is_visible()

    def add(self, title):
        self.page.fill("#title", title)
        self.page.press("#title", "Enter")

    def dialog_open(self):
        return self.js("document.querySelector('#confirm').open")

    def dialog_text(self):
        return self.page.locator("#confirm-text").text_content()

    def answer(self, yes):
        self.page.click('#confirm button[value="yes"]' if yes else '#confirm button[value="no"]')
        self.page.wait_for_timeout(150)

    def pick(self, path):
        self.page.set_input_files("#import", str(path))
        self.page.wait_for_function(f"() => document.querySelector('#message').textContent !== {json.dumps(MESSAGES['reading'])}"
                                    " || document.querySelector('#confirm').open", timeout=10000)
        self.page.wait_for_timeout(150)

    def export(self):
        try:
            with self.page.expect_download(timeout=3000) as d:
                self.page.click("#export")
            p = OUT / d.value.suggested_filename
            d.value.save_as(p)
            return d.value.suggested_filename, p
        except Exception:
            return None, None

    def close(self):
        self.ctx.close()


def row(t, title):
    global cur
    cur = {"t": t, "title": title, "checks": []}
    rows.append(cur)


def fill(tpl, **v):
    for k, x in v.items():
        tpl = tpl.replace("{" + k + "}", f"{x:,}".replace(",", "."))
    return tpl


with sync_playwright() as p:
    b = p.chromium.launch()

    row("T0", "2.000 việc dạng cũ mở bằng bản mới; thêm, đánh dấu, xoá; tải lại vẫn giữ")
    a = App(b); a.seed(2000)
    check("đủ 2.000 việc", a.li() == 2000, str(a.li()))
    check("không dải báo", not a.banner())
    a.add("Việc mới T0"); a.page.locator("#list li input").first.click(); a.page.locator("#list li button").nth(1).click()
    a.reload()
    check("tải lại: 2.000 việc (thêm 1, xoá 1)", a.li() == 2000, str(a.li()))
    check("việc mới còn sau tải lại", "Việc mới T0" in (a.raw() or ""))
    check("dòng đếm đúng số việc chưa xong", a.page.locator("#count").text_content() ==
          fill("{n} việc chưa xong", n=sum(1 for t in json.loads(a.raw()) if not t["done"])), a.page.locator("#count").text_content())
    a.close()

    row("T1", "Sao lưu 3 việc; danh sách trống thì không tải file")
    a = App(b); a.seed(3)
    name, path = a.export()
    check("có file tải về", path is not None)
    if path:
        text = path.read_text()
        data = json.loads(text)
        check("tên todo-sao-luu-<hôm nay>.json", name == f"todo-sao-luu-{time.strftime('%Y-%m-%d')}.json", name)
        check("thụt lề", "\n  " in text)
        check("đúng 3 việc, đúng nội dung", len(data["todos"]) == 3 and data["todos"] == [
            {k: t[k] for k in ("id", "title", "done", "createdAt")} for t in json.loads(a.raw())])
        (OUT / "T1-3-viec.json").write_text(text)
    check("câu Đã sao lưu 3 việc", a.msg() == fill(MESSAGES["backedUp"], n=3), a.msg())
    a.js("localStorage.clear()"); a.reload()
    name2, _ = a.export()
    check("danh sách trống: không tải", name2 is None)
    check("danh sách trống: câu M1", a.msg() == MESSAGES["nothingToBackUp"], a.msg())
    a.close()

    row("T2", "Mất mạng: sao lưu và nhập vẫn chạy, không có request nào")
    a = App(b); a.seed(3)
    a.ctx.set_offline(True); a.requests.clear()
    name, _ = a.export()
    check("sao lưu khi mất mạng", name is not None)
    a.pick(OUT / "T1-3-viec.json"); a.answer(True)
    check("nhập khi mất mạng", a.li() == 3 and a.msg() == fill(MESSAGES["imported"], n=3), a.msg())
    check("không request nào trong lúc sao lưu và nhập", not [r for r in a.requests if not r.startswith("blob:")],
          ", ".join(a.requests))
    a.close()

    row("T3", "Xoá dữ liệu trang: câu danh sách trống; nhập file T1 không hỏi, đủ 3 việc, tải lại còn")
    a = App(b)
    check("câu danh sách trống", a.empty_shown() and a.page.locator("#empty").text_content() == MESSAGES["emptyList"])
    check("không dải báo", not a.banner())
    a.pick(OUT / "T1-3-viec.json")
    check("không hỏi", not a.dialog_open())
    check("đủ 3 việc", a.li() == 3, str(a.li()))
    a.reload()
    check("tải lại còn 3", a.li() == 3)
    a.close()

    row("T4", "12 việc, nhập 30: hỏi; huỷ giữ 12; đồng ý thành 30; lặp với 1 việc")
    for n in (12, 1):
        a = App(b); a.seed(n)
        a.pick(FILES / "T4-30-viec.json")
        check(f"{n} việc: hộp hỏi đúng câu", a.dialog_open() and a.dialog_text() == fill(MESSAGES["confirmReplace"], n=n, m=30),
              a.dialog_text())
        a.answer(False)
        check(f"{n} việc: huỷ giữ {n}", a.li() == n); a.reload(); check(f"{n} việc: huỷ, tải lại {n}", a.li() == n)
        a.pick(FILES / "T4-30-viec.json"); a.answer(True)
        check(f"{n} việc: đồng ý thành 30", a.li() == 30); a.reload(); check(f"{n} việc: tải lại 30", a.li() == 30)
        check(f"{n} việc: không có Undo", a.page.get_by_text("Hoàn tác").count() == 0 and a.page.get_by_text("Undo").count() == 0)
        a.close()

    row("T5", "Tám file sai: từng file bị từ chối, nói vì sao và làm gì tiếp, danh sách không đổi")
    a = App(b); a.seed(3); before = a.raw()
    for f in sorted(FILES.glob("T5-*")):
        a.pick(f)
        m = a.msg() or ""
        check(f"{f.name}: từ chối, không hỏi, không đổi", not a.dialog_open() and a.li() == 3 and a.raw() == before, m)
        check(f"{f.name}: câu có 'giữ nguyên' và 'Hãy'", "giữ nguyên" in m and "Hãy" in m)
    a.close()

    row("T6", "Tiêu đề <img src=x onerror=alert(1)> hiện đúng chữ, không alert")
    a = App(b)
    a.pick(FILES / "T6-tieu-de-html.json"); a.page.wait_for_timeout(500)
    check("hiện đúng chữ", a.page.locator("#list li span").first.text_content() == "<img src=x onerror=alert(1)>")
    check("không alert, không thẻ img", not a.alerts and a.page.locator("#list img").count() == 0, str(a.alerts))
    a.close()

    row("T7", "5.000 việc × 200 ký tự: file > 1 MB tải được, thấy câu M2")
    a = App(b); a.seed(5000, title="'x'.repeat(200)", done="false")
    name, path = a.export()
    check("tải được file > 1 MB", path is not None and path.stat().st_size > 1048576, f"{path.stat().st_size if path else 0} byte")
    check("câu M2", a.msg() == MESSAGES["backupTooBig"], a.msg())
    if path:
        path.unlink()
    a.close()

    row("T8", "Bộ nhớ đầy: thêm việc báo M3, tải lại mất; nhập 30 đồng ý báo M17, tải lại còn 12")
    a = App(b); a.seed(12); a.js(FILL)
    a.add("Việc khi đầy")
    check("câu M3", a.msg() == MESSAGES["notSaved"], a.msg())
    check("việc còn trên màn hình", a.li() == 13)
    a.reload(); check("tải lại mất việc đó", a.li() == 12, str(a.li()))
    a.pick(FILES / "T4-30-viec.json"); a.answer(True)
    check("nhập lỗi khi lưu: câu M17", a.msg() == MESSAGES["importNotSaved"], a.msg())
    a.reload(); check("tải lại còn 12", a.li() == 12, str(a.li()))
    a.close()

    row("T9", "Danh sách đã lưu hỏng: dải báo; thêm, đánh dấu, xoá không ghi đè; tải lại dải báo vẫn hiện")
    for bad in ("{hỏng", '{"a": 1}'):
        a = App(b); a.js(f"localStorage.setItem('todo.v1', {json.dumps(bad)})"); a.reload()
        keys = a.js("Object.keys(localStorage).length")
        check(f"{bad}: dải báo", a.banner()); check(f"{bad}: không câu danh sách trống", not a.empty_shown())
        a.add("A"); a.add("B"); a.page.locator("#list li input").first.click(); a.page.locator("#list li button").first.click()
        check(f"{bad}: không hộp thoại", not a.dialog_open() and not a.alerts)
        check(f"{bad}: giá trị giữ nguyên, không khoá mới", a.raw() == bad and a.js("Object.keys(localStorage).length") == keys)
        a.reload(); check(f"{bad}: tải lại không còn việc, dải báo vẫn hiện", a.li() == 0 and a.banner())
        a.close()

    row("T10", "Đọc lỗi rồi sao lưu, nhập (M6, M7), bộ nhớ đầy, file sai")
    a = App(b); a.js("localStorage.setItem('todo.v1', '{hỏng')"); a.reload()
    a.add("A"); a.add("B")
    name, path = a.export()
    check("sao lưu khi đọc lỗi: file đúng 2 việc", path is not None and len(json.loads(path.read_text())["todos"]) == 2)
    check("todo.v1 vẫn {hỏng", a.raw() == "{hỏng")
    a.close()
    a = App(b); a.js("localStorage.setItem('todo.v1', '{hỏng')"); a.reload()
    a.pick(FILES / "T4-30-viec.json")
    check("chưa thêm: câu M6", a.dialog_text() == fill(MESSAGES["confirmReplaceUnreadable"], m=30), a.dialog_text())
    a.answer(False); check("huỷ: dải báo vẫn hiện, vẫn {hỏng", a.banner() and a.raw() == "{hỏng")
    a.pick(FILES / "T4-30-viec.json"); a.answer(True)
    check("đồng ý: dải báo biến mất", not a.banner())
    a.add("C"); a.reload(); check("thêm 1, tải lại 31", a.li() == 31, str(a.li()))
    a.close()
    a = App(b); a.js("localStorage.setItem('todo.v1', '{hỏng')"); a.reload()
    for t in ("A", "B", "C"):
        a.add(t)
    a.pick(FILES / "T4-30-viec.json")
    check("đã thêm 3: câu M7", a.dialog_text() == fill(MESSAGES["confirmReplaceUnreadableAndUnsaved"], n=3, m=30), a.dialog_text())
    a.answer(False); check("huỷ: còn 3 việc, vẫn {hỏng", a.li() == 3 and a.raw() == "{hỏng")
    a.pick(FILES / "T4-30-viec.json"); a.answer(True); check("đồng ý: 30 việc, hết dải báo", a.li() == 30 and not a.banner())
    a.close()
    a = App(b); a.js("localStorage.setItem('todo.v1', '{hỏng')"); a.reload(); a.js(FILL)
    a.pick(FILES / "T4-30-viec.json"); a.answer(True)
    check("{hỏng + bộ nhớ đầy, đồng ý: dải báo vẫn hiện, vẫn {hỏng", a.banner() and a.raw() == "{hỏng", a.msg())
    a.close()
    a = App(b); a.js("localStorage.setItem('todo.v1', '{hỏng')"); a.reload()
    for f in ("T5-a-qua-lon.json", "T5-b-truong-la.json"):
        a.pick(FILES / f)
        check(f"đọc lỗi + {f}: từ chối, không hỏi", not a.dialog_open() and a.raw() == "{hỏng", a.msg())
    a.close()

    row("T11", "Màn hình chính có câu nơi lưu danh sách")
    a = App(b)
    check("có câu 'chỉ được lưu trên trình duyệt này'", a.page.locator("#where-kept").is_visible() and
          "chỉ được lưu trên trình duyệt này" in a.page.locator("#where-kept").text_content())
    a.close()

    row("T13", "Lọc 'Đã xong' khi chưa có việc xong: không hiện câu danh sách trống (chỗ lỗi T-014)")
    a = App(b); a.seed(4, done="false")
    a.page.click('#filters button[data-filter="done"]')
    check("không hiện câu danh sách trống", not a.empty_shown())
    check("dòng đếm vẫn 4 (chỗ lỗi T-013)", a.page.locator("#count").text_content() == "4 việc chưa xong",
          a.page.locator("#count").text_content())
    a.close()
    b.close()
srv.shutdown()

lines = [f"# Kiểm tay T0–T13, phần máy chạy (Chromium headless)\n\nChạy {time.strftime('%Y-%m-%d %H:%M')} bằng "
         "`demo/sdlc-4/kiem-tay-may.py` trên `app/` của cây làm việc. Không thay người kiểm: chỉ Chromium, không Safari, không "
         "điện thoại, không bàn phím thật, không trình đọc màn hình (T12 để người), không ai nhìn giao diện.\n"]
tot = ok = 0
for r in rows:
    good = all(c[1] for c in r["checks"])
    lines.append(f"\n## {r['t']} · {'đạt' if good else 'KHÔNG'} · {r['title']}\n")
    for name, k, note in r["checks"]:
        tot += 1; ok += k
        lines.append(f"- {'✅' if k else '❌'} {name}" + (f" — `{note}`" if note and not k else ""))
lines.append(f"\n**{ok}/{tot} phép kiểm đạt, {sum(all(c[1] for c in r['checks']) for r in rows)}/{len(rows)} dòng đạt.**\n")
(OUT / "ket-qua.md").write_text("\n".join(lines) + "\n")
for r in rows:
    print(r["t"], "đạt" if all(c[1] for c in r["checks"]) else "KHÔNG", *[f"[❌ {n}: {x}]" for n, k, x in r["checks"] if not k])
print(f"{ok}/{tot}")
