#!/usr/bin/env python3
"""ds-python-selfstudy 網站化注入：導讀框、中文詞彙卡、上下章導覽、float-nav/TOC 補項。冪等（已含 id="cards" 跳過）。"""
import json, re
from pathlib import Path

SITE = Path.home() / "ds-python-selfstudy"
FC_ZH = SITE / "data/flashcards_zh"
GH_SLIDES = "https://github.com/phonchi/nsysu-math208-2025/blob/main/static_files/presentations"
GH_BOOK = "https://github.com/RunestoneInteractive/pythonds/tree/master/_sources"

# 授課順序：file, 短標題, deck 檔名, pythonds slug(None=外部教材), 章徽章, flashcards json
PAGES = [
    ("introduction",      "Python 導論",        "01_Introduction",             "Introduction",      "pythonds Ch.1", "ch1"),
    ("analysis",          "演算法分析",         "02_Analysis",                 "AlgorithmAnalysis", "pythonds Ch.2", "ch2"),
    ("arrays",            "陣列與稀疏矩陣",     "03_Arrays",                   None,                "附錄 A（講義 03）", "ch3"),
    ("linked_lists",      "鏈結串列",           "04_Linear_Linked_Structure",  "BasicDS",           "pythonds §3.19–3.23", "ch4"),
    ("linear_structures", "堆疊、佇列與 Deque", "05_Linear_Structure",         "BasicDS",           "pythonds Ch.3", "ch5"),
    ("recursion",         "遞迴",               "06_Recursion",                "Recursion",         "pythonds Ch.4", "ch6"),
    ("searching_sorting", "搜尋與排序",         "07_Searching and Sorting",    "SortSearch",        "pythonds Ch.5", "ch7"),
    ("graphs",            "圖與圖演算法",       "08_Graphs and Graphing Algorithms", "Graphs",      "pythonds Ch.7", "ch8"),
    ("trees",             "樹與樹演算法",       "09_Trees and Tree Algorithms","Trees",             "pythonds Ch.6", "ch9"),
]

CSS = """
/* ===== 網站化附加樣式（study-guide / flashcards / chapter-nav）===== */
.study-guide{background:var(--card);border:1px solid var(--card-border);border-left:5px solid var(--accent3);border-radius:12px;padding:1.2rem 1.4rem;margin:0 0 2.2rem;}
.study-guide .sg-title{font-family:'JetBrains Mono',monospace;font-size:.75rem;font-weight:700;letter-spacing:1.5px;color:var(--accent3);margin-bottom:.5rem;}
.study-guide p{font-size:.92rem;margin-bottom:.5rem;}
.study-guide .sg-links{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.7rem;}
.study-guide .sg-links a{font-family:'JetBrains Mono',monospace;font-size:.78rem;font-weight:600;color:var(--accent2);border:1px solid var(--card-border);border-radius:999px;padding:.3rem .85rem;text-decoration:none;transition:all .2s;}
.study-guide .sg-links a:hover{background:var(--accent2);color:#fff;}
.fc-controls{display:flex;gap:.5rem;flex-wrap:wrap;margin:.8rem 0 1.2rem;}
.fc-controls button{font-family:'JetBrains Mono',monospace;font-size:.8rem;font-weight:600;padding:.45rem 1rem;border-radius:6px;border:1px solid var(--card-border);cursor:pointer;background:var(--card);color:var(--ink);transition:all .2s;}
.fc-controls button:hover{background:var(--accent2);color:#fff;border-color:var(--accent2);}
.fc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(215px,1fr));gap:.9rem;}
.fc-card{perspective:900px;height:170px;cursor:pointer;}
.fc-card .fc-inner{position:relative;width:100%;height:100%;transition:transform .5s;transform-style:preserve-3d;}
.fc-card.flipped .fc-inner{transform:rotateY(180deg);}
.fc-card .fc-face{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;border-radius:12px;display:flex;align-items:center;justify-content:center;padding:.9rem;text-align:center;box-shadow:0 3px 12px rgba(0,0,0,.08);}
.fc-card .fc-front{background:linear-gradient(150deg,var(--accent2),var(--ink));color:#fff;font-family:'Noto Serif TC',serif;font-size:1rem;font-weight:700;letter-spacing:.02em;flex-direction:column;gap:.4rem;}
.fc-card .fc-front .fc-hint{font-size:.62rem;color:rgba(255,255,255,.5);font-family:'JetBrains Mono',monospace;font-weight:400;letter-spacing:.1em;}
.fc-card .fc-back{background:var(--card);border:2px solid var(--accent3);color:var(--ink);font-size:.78rem;line-height:1.55;transform:rotateY(180deg);overflow-y:auto;}
.chapter-nav{display:grid;grid-template-columns:1fr auto 1fr;gap:.8rem;align-items:stretch;margin:2.5rem 0 1rem;}
.chapter-nav a{display:block;border:1px solid var(--card-border);border-radius:12px;padding:.8rem 1.1rem;text-decoration:none;color:var(--ink);background:var(--card);transition:all .2s;}
.chapter-nav a:hover{border-color:var(--accent2);box-shadow:0 4px 14px rgba(0,0,0,.08);}
.chapter-nav .nav-dir{font-family:'JetBrains Mono',monospace;font-size:.68rem;font-weight:700;letter-spacing:1px;color:var(--muted);margin-bottom:.2rem;}
.chapter-nav .nav-title{font-family:'Noto Serif TC',serif;font-weight:700;font-size:.95rem;color:var(--accent2);}
.chapter-nav a.next{text-align:right;}
.chapter-nav a.home{display:flex;flex-direction:column;justify-content:center;text-align:center;}
@media(max-width:700px){.chapter-nav{grid-template-columns:1fr;}}
"""

JS = """
/* ===== Flashcards engine ===== */
(function(){
  const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const grid = document.getElementById('fcGrid');
  if (!grid) return;
  const render = cards => {
    grid.innerHTML = cards.map(c =>
      `<div class="fc-card"><div class="fc-inner">
         <div class="fc-face fc-front"><div>${esc(c.front)}</div><div class="fc-hint">CLICK TO FLIP</div></div>
         <div class="fc-face fc-back">${esc(c.back)}</div>
       </div></div>`).join('');
  };
  render(FLASHCARDS);
  grid.addEventListener('click', e => {
    const card = e.target.closest('.fc-card');
    if (card) card.classList.toggle('flipped');
  });
  document.getElementById('fcShuffle').addEventListener('click', () => render([...FLASHCARDS].sort(() => Math.random() - .5)));
  document.getElementById('fcUnflip').addEventListener('click', () => grid.querySelectorAll('.fc-card').forEach(c => c.classList.remove('flipped')));
  document.getElementById('fcFlipAll').addEventListener('click', () => grid.querySelectorAll('.fc-card').forEach(c => c.classList.add('flipped')));
})();
"""

def enc(name):
    return name.replace(" ", "%20")

def inject(idx):
    fname, title, deck, slug, badge, fc = PAGES[idx]
    path = SITE / f"{fname}.html"
    s = path.read_text()
    if 'id="cards"' in s:
        print(f"skip {fname}"); return
    cards = json.loads((FC_ZH / f"{fc}.json").read_text())
    n = len(cards)
    prev_p = PAGES[idx-1] if idx > 0 else None
    next_p = PAGES[idx+1] if idx < len(PAGES)-1 else None

    assert s.count("</head>") == 1
    s = s.replace("</head>", f"<style>{CSS}</style>\n</head>")

    m = re.search(r'(<a href="#top" class="fn-top")', s)
    assert m, fname
    card_nav = ('  <a href="#cards" data-target="cards"><span class="fn-num">CARD</span>'
                '<span class="fn-name">關鍵詞彙卡</span></a>\n  ')
    s = s[:m.start()] + card_nav + s[m.start():]

    tocm = re.search(r'(<a href="#(?:reference|summary)"><span class="toc-num">REF</span>[^\n]*</a>)', s)
    if tocm:
        s = s[:tocm.end()] + f'\n    <a href="#cards"><span class="toc-num">CARD</span>關鍵詞彙卡（{n} 張）</a>' + s[tocm.end():]

    deck_num = deck[:2]
    links = [f'<a href="{GH_SLIDES}/{enc(deck)}.pdf" target="_blank" rel="noopener">📑 講義 {deck_num} PDF</a>',
             f'<a href="{GH_SLIDES}/{enc(deck)}.html" target="_blank" rel="noopener">🖥 講義 {deck_num} HTML</a>']
    if slug:
        links.append(f'<a href="{GH_BOOK}/{slug}" target="_blank" rel="noopener">📖 pythonds 原文（{slug}）</a>')
    links.append('<a href="index.html">🏠 章節總覽</a>')
    guide = f'''<div class="study-guide">
  <div class="sg-title">📌 本頁使用方式（{badge}｜講義 {deck_num}）</div>
  <p>① <strong>照節次讀</strong>：每一節先讀說明、動手玩互動元件，預測結果再按按鈕驗證。
  ② <strong>對照講義</strong>：頁上 §徽章對應 pythonds 章節；細節與完整程式請回講義 {deck_num} 與 pythonds 原文。
  ③ <strong>每節做 quiz</strong>：答錯就回到該節重讀，不要往下跳。
  ④ 最後翻 <a href="#cards">關鍵詞彙卡（{n} 張）</a>自測術語（中文為主、術語附英文），並用 REF 總覽區當速查表。標「講義補充」的節是課堂沒細講的延伸，第一輪可略過。</p>
  <div class="sg-links">{''.join(links)}</div>
</div>
'''
    assert s.count('<div class="container">') == 1
    s = s.replace('<div class="container">', '<div class="container">\n' + guide, 1)

    nav_items = []
    if prev_p:
        nav_items.append(f'<a class="prev" href="{prev_p[0]}.html"><div class="nav-dir">◂ 上一章</div><div class="nav-title">{prev_p[1]}</div></a>')
    else:
        nav_items.append('<span></span>')
    nav_items.append('<a class="home" href="index.html"><div class="nav-dir">INDEX</div><div class="nav-title">章節總覽</div></a>')
    if next_p:
        nav_items.append(f'<a class="next" href="{next_p[0]}.html"><div class="nav-dir">下一章 ▸</div><div class="nav-title">{next_p[1]}</div></a>')
    else:
        nav_items.append('<span></span>')
    tail = f'''<section id="cards">
  <div class="section-number">CARDS · 關鍵詞彙卡</div>
  <h2>關鍵詞彙卡：點卡片翻面 <span class="sec-badge">課程題庫 · {n} 張</span></h2>
  <p>詞彙卡取自本章課程題庫，已譯為繁體中文，正面附英文原名。先看正面術語，心中默想定義再翻面對答案；洗牌後再過一輪，直到每張都能不假思索說出來。</p>
  <div class="fc-controls">
    <button id="fcShuffle">🔀 洗牌</button>
    <button id="fcFlipAll">全部翻面</button>
    <button id="fcUnflip">全部翻回</button>
  </div>
  <div class="fc-grid" id="fcGrid"></div>
</section>
<div class="chapter-nav">{''.join(nav_items)}</div>
'''
    m2 = re.search(r'</div>\s*<footer>', s)
    assert m2, fname
    s = s[:m2.start()] + tail + s[m2.start():]

    data = json.dumps(cards, ensure_ascii=False)
    script = f'<script>\nconst FLASHCARDS = {data};\n{JS}</script>\n</body>'
    assert s.count("</body>") == 1
    s = s.replace("</body>", script)

    path.write_text(s)
    print(f"ok {fname}: {n} 卡, prev={prev_p[0] if prev_p else '-'} next={next_p[0] if next_p else '-'}")

for i in range(len(PAGES)):
    inject(i)
