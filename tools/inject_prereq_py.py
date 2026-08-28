#!/usr/bin/env python3
"""ds-python-selfstudy 課前章（00A/00B）與先備頁（P1–P9）的尾段注入。

分工與既有腳本一致：本檔負責「結構」（導讀框、float-nav/TOC 補項、bankquiz 錨點、
詞彙卡區、上下頁導覽、CSS/JS 引擎），內容則交給 tools/apply_zh.py 從 data/ 灌入。

冪等：頁面出現 <!-- prereq-injected --> 即跳過。
CSS/JS 常數直接從 inject_site_py.py / inject_quiz_py.py 的原始碼取出（不 import，
避免那兩支模組載入時就對九章正課頁執行注入）。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
MARKER = "<!-- prereq-injected -->"

# 與九章正課頁完全相同的 MathJax 設定
MATHJAX = """<script>
  MathJax = { tex: { inlineMath: [['$','$']], displayMath: [['$$','$$']] }, svg: { fontCache: 'global' } };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
"""


def const(fname, name):
    """從 tools/<fname> 取出 NAME = \"\"\"...\"\"\" 的內容，不執行該模組。"""
    src = (TOOLS / fname).read_text()
    m = re.search(rf'^{name} = """(.*?)"""', src, re.S | re.M)
    assert m, f"{fname}: {name} not found"
    return m.group(1)


SITE_CSS = const("inject_site_py.py", "CSS")   # study-guide / flashcards / chapter-nav
SITE_JS  = const("inject_site_py.py", "JS")    # flashcards engine
QUIZ_CSS = const("inject_quiz_py.py", "CSS")   # .sq-item 題庫自測區
QUIZ_JS  = const("inject_quiz_py.py", "JS")    # .sq-item 點選判定

# 課前／先備頁專用的少量補充樣式（recursion.html 的樣板沒有這兩個）
PRE_CSS = """
.hero .chapter-tag{font-family:'JetBrains Mono',monospace;font-size:.85rem;color:#f5b82e;letter-spacing:.3em;margin-bottom:.8rem;}
.cmp-table-wrap{overflow-x:auto;margin-bottom:1rem;}
.ds-hook{background:var(--card);border:1px solid var(--card-border);border-left:5px solid var(--accent3);border-radius:10px;padding:.8rem 1.1rem;margin:1rem 0;font-size:.9rem;}
.ds-hook .dh-title{font-family:'JetBrains Mono',monospace;font-size:.72rem;font-weight:700;letter-spacing:1.2px;color:var(--accent3);margin-bottom:.3rem;}
"""

# apply_zh.py 會把題目的 code 欄位包成 <pre class="sq-code">
CODE_CSS = """
.sq-code{background:var(--code-bg);color:var(--code-fg);font-family:'JetBrains Mono',monospace;font-size:.82rem;line-height:1.55;padding:.7rem .9rem;border-radius:8px;margin:.2rem 0 .8rem;overflow-x:auto;white-space:pre;}
"""

# file, 短標題, 詞彙卡母檔, 題庫母檔(None=用頁內 .quiz-box), 類型, prev, next, next 標籤
PRE, PQ = "pre", "prereq"
PPAGES = [
    ("00a_why_code",        "為什麼還要學資料結構", "00a", None, PRE, None,                   "00b_setup",         "課前準備與環境安裝"),
    ("00b_setup",           "課前準備與環境安裝",   "00b", None, PRE, "00a_why_code",         "introduction",      "Python 導論"),
    ("p1_python_basics",    "Python 基礎",          "p1",  "p1", PQ,  None,                   "p2_flow_control",   "流程控制"),
    ("p2_flow_control",     "流程控制",             "p2",  "p2", PQ,  "p1_python_basics",     "p3_functions",      "函數"),
    ("p3_functions",        "函數",                 "p3",  "p3", PQ,  "p2_flow_control",      "p4_lists_tuples",   "串列與元組"),
    ("p4_lists_tuples",     "串列與元組",           "p4",  "p4", PQ,  "p3_functions",         "p5_dicts_sets",     "字典與集合"),
    ("p5_dicts_sets",       "字典與集合",           "p5",  "p5", PQ,  "p4_lists_tuples",      "p6_strings",        "字串操作"),
    ("p6_strings",          "字串操作",             "p6",  "p6", PQ,  "p5_dicts_sets",        "p7_files_exceptions", "檔案與例外"),
    ("p7_files_exceptions", "檔案與例外",           "p7",  "p7", PQ,  "p6_strings",           "p8_oop_basics",     "物件導向（基礎）"),
    ("p8_oop_basics",       "物件導向（基礎）",     "p8",  "p8", PQ,  "p7_files_exceptions",  "p9_oop_advanced",   "物件導向（進階）"),
    ("p9_oop_advanced",     "物件導向（進階）",     "p9",  "p9", PQ,  "p8_oop_basics",        "introduction",      "回到主線：Python 導論"),
]

PREV_LABEL = {p[0]: p[1] for p in PPAGES}

SG_PRE = """<div class="study-guide">
  <div class="sg-title">📌 本頁使用方式（課前準備 · 讀完再進第 01 章）</div>
  <p>① <strong>照節次讀</strong>：每一節都短，不要跳著看。
  ② <strong>動手驗證</strong>：有互動元件的地方先自己預測答案，再按按鈕對照。
  ③ <strong>做完自我檢核</strong>再往下：答錯就回頭重讀該節。
  ④ 最後翻 <a href="#cards">關鍵詞彙卡</a>，能不看答案講出定義才算過關。</p>
  <div class="sg-links">{links}</div>
</div>
"""

SG_PQ = """<div class="study-guide">
  <div class="sg-title">📌 本頁使用方式（先備複習 · 選讀，不列入評分）</div>
  <p>① 這頁複習資料結構課程<strong>預設你已經會</strong>的 Python。已經熟的可以直接跳過。
  ② 每節都附一個<strong>「這在資料結構課哪裡會用到」</strong>的小方框——那才是你該記住的部分。
  ③ 讀完做 <a href="#bankquiz">自我檢測</a>，再翻 <a href="#cards">關鍵詞彙卡</a>。
  <br><strong>本頁屬補充先備知識，不列入作業與考試範圍。</strong></p>
  <div class="sg-links">{links}</div>
</div>
"""

LINKS_COMMON = ('<a href="index.html">🏠 章節總覽</a>'
                '<a href="index.html#prereq">📚 先備頁總覽</a>'
                '<a href="https://pythontutor.com/" target="_blank" rel="noopener">🔬 Python Tutor</a>'
                '<a href="https://docs.python.org/zh-tw/3/tutorial/" target="_blank" rel="noopener">📖 Python 官方教學</a>')


def inject(entry):
    fname, short, fc, bq, kind, prev, nxt, nxt_label = entry
    path = ROOT / f"{fname}.html"
    if not path.exists():
        print(f"miss {fname}.html（尚未撰寫，略過）")
        return
    s = path.read_text()

    # MathJax：自 PythonForMath 移植的頁面 head 沒有它，但頁面裡有 $…$ 數學式。
    # 這一步刻意放在 MARKER 之前，已注入過的頁面重跑也會被補上（冪等）。
    if "MathJax" not in s:
        assert s.count("</head>") == 1, fname
        s = s.replace("</head>", MATHJAX + "</head>", 1)
        path.write_text(s)
        print(f"    + MathJax -> {fname}")

    if MARKER in s:
        print(f"skip {fname}")
        return

    # 1. CSS：頁面若不是從 recursion.html 複製而來（例如自 PythonForMath 移植），
    #    可能缺少網站化樣式，補上；題庫樣式一律補（recursion.html 沒有）。
    css = PRE_CSS
    if ".study-guide{" not in s:
        css += SITE_CSS
    if bq and ".sq-item{" not in s:
        css += QUIZ_CSS + CODE_CSS
    head_add = MARKER + "\n" + f"<style>{css}</style>\n"
    assert s.count("</head>") == 1, fname
    s = s.replace("</head>", head_add + "</head>", 1)

    # 2. float-nav 補 QUIZ / CARD（插在 ↑TOP 之前）
    m = re.search(r'  <a href="#top" class="fn-top"', s)
    assert m, f"{fname}: fn-top not found"
    nav_add = ""
    if bq:
        nav_add += ('  <a href="#bankquiz" data-target="bankquiz"><span class="fn-num">QUIZ</span>'
                    '<span class="fn-name">自我檢測</span></a>\n')
    nav_add += ('  <a href="#cards" data-target="cards"><span class="fn-num">CARD</span>'
                '<span class="fn-name">關鍵詞彙卡</span></a>\n')
    s = s[:m.start()] + nav_add + s[m.start():]

    # 3. TOC 補 QUIZ / CARD（接在 REF 之後）
    tocm = re.search(r'(<a href="#(?:reference|summary)"><span class="toc-num">REF</span>[^\n]*</a>)', s)
    if tocm:
        toc_add = ""
        if bq:
            toc_add += '\n    <a href="#bankquiz"><span class="toc-num">QUIZ</span>自我檢測</a>'
        toc_add += '\n    <a href="#cards"><span class="toc-num">CARD</span>關鍵詞彙卡</a>'
        s = s[:tocm.end()] + toc_add + s[tocm.end():]

    # 4. 導讀框
    tpl = SG_PRE if kind == PRE else SG_PQ
    guide = tpl.format(links=LINKS_COMMON)
    assert s.count('<div class="container">') == 1, fname
    s = s.replace('<div class="container">', '<div class="container">\n' + guide, 1)

    # 5. bankquiz 錨點 + 詞彙卡區 + 上下頁導覽
    tail = ""
    if bq:
        tail += '<section id="bankquiz"></section>\n'
    tail += """<section id="cards">
  <div class="section-number">CARDS · 關鍵詞彙卡</div>
  <h2>關鍵詞彙卡：點卡片翻面</h2>
  <p>先看正面術語，心中默想定義再翻面對答案；洗牌後再過一輪，直到每張都能不假思索說出來。</p>
  <div class="fc-controls">
    <button id="fcShuffle">🔀 洗牌</button>
    <button id="fcFlipAll">全部翻面</button>
    <button id="fcUnflip">全部翻回</button>
  </div>
  <div class="fc-grid" id="fcGrid"></div>
</section>
"""
    nav_items = []
    if prev:
        nav_items.append(f'<a class="prev" href="{prev}.html"><div class="nav-dir">◂ 上一頁</div>'
                         f'<div class="nav-title">{PREV_LABEL[prev]}</div></a>')
    else:
        nav_items.append("<span></span>")
    nav_items.append('<a class="home" href="index.html"><div class="nav-dir">INDEX</div>'
                     '<div class="nav-title">章節總覽</div></a>')
    if nxt:
        nav_items.append(f'<a class="next" href="{nxt}.html"><div class="nav-dir">下一頁 ▸</div>'
                         f'<div class="nav-title">{nxt_label}</div></a>')
    else:
        nav_items.append("<span></span>")
    tail += f'<div class="chapter-nav">{"".join(nav_items)}</div>\n'

    # 容忍 </div><!-- /container --> 這種註解（自 PythonForMath 移植的頁面會有）
    m2 = re.search(r"</div>(?:\s*<!--[^>]*-->)?\s*<footer>", s)
    assert m2, f"{fname}: container/footer boundary not found"
    s = s[:m2.start()] + tail + s[m2.start():]

    # 6. JS 引擎（詞彙卡陣列留空，由 apply_zh.py 灌資料）
    js = "\nconst FLASHCARDS = [];\n" + SITE_JS
    if bq:
        js += QUIZ_JS
    assert s.count("</body>") == 1, fname
    s = s.replace("</body>", f"<script>{js}</script>\n</body>")

    path.write_text(s)
    print(f"ok {fname}: fc={fc} bq={bq or '-'} prev={prev or '-'} next={nxt or '-'}")


if __name__ == "__main__":
    for e in PPAGES:
        inject(e)
