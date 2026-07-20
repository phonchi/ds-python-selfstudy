#!/usr/bin/env python3
"""ds-python-selfstudy：三舊頁加中文題庫自測區（來源 data/questions_zh/）。冪等。"""
import json, re
from pathlib import Path

SITE = Path.home() / "ds-python-selfstudy"
QZH = SITE / "data/questions_zh"

TARGETS = [
    ("searching_sorting", "ch7", "搜尋、雜湊與排序"),
    ("graphs", "ch8", "圖演算法"),
    ("trees", "ch9", "樹結構"),
]

CSS = """
/* ===== 題庫自測區 ===== */
.sq-item{background:var(--card);border:1px solid var(--card-border);border-radius:12px;padding:1.1rem 1.3rem;margin-bottom:1.1rem;}
.sq-item .sq-q{font-weight:700;margin-bottom:.7rem;}
.sq-item .sq-q .sq-num{font-family:'JetBrains Mono',monospace;color:var(--accent);margin-right:.4rem;}
.sq-opts{display:flex;flex-direction:column;gap:.45rem;}
.sq-opt{text-align:left;font-family:'Noto Sans TC',sans-serif;font-size:.9rem;line-height:1.6;padding:.55rem .9rem;border-radius:8px;border:1px solid var(--card-border);background:var(--paper);color:var(--ink);cursor:pointer;transition:all .15s;}
.sq-opt:hover{border-color:var(--accent2);}
.sq-opt.correct{border-color:var(--accent3);background:rgba(26,107,74,.10);}
.sq-opt.wrong{border-color:var(--accent);background:rgba(192,57,43,.08);}
.sq-fb{display:none;margin-top:.7rem;font-size:.86rem;line-height:1.7;border-left:4px solid var(--accent2);padding:.5rem .9rem;background:var(--paper);border-radius:0 8px 8px 0;}
.sq-fb.show{display:block;}
.sq-fb.good{border-left-color:var(--accent3);}
.sq-fb.bad{border-left-color:var(--accent);}
"""

JS = """
(function(){
  document.querySelectorAll('.sq-item').forEach(item => {
    const fb = item.querySelector('.sq-fb');
    item.querySelectorAll('.sq-opt').forEach(btn => btn.addEventListener('click', () => {
      const good = btn.dataset.c === '1';
      item.querySelectorAll('.sq-opt').forEach(b => b.classList.remove('correct','wrong'));
      btn.classList.add(good ? 'correct' : 'wrong');
      fb.textContent = btn.dataset.fb;
      fb.classList.add('show');
      fb.classList.toggle('good', good);
      fb.classList.toggle('bad', !good);
    }));
  });
})();
"""

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

for page, ch, note in TARGETS:
    path = SITE / f"{page}.html"
    s = path.read_text()
    if 'id="bankquiz"' in s:
        print(f"skip {page}"); continue
    qs = json.loads((QZH / f"{ch}.json").read_text())
    items = []
    for i, q in enumerate(qs, 1):
        opts = "\n".join(
            f'      <button class="sq-opt" data-c="{1 if a["correct"] else 0}" data-fb="{esc(a["feedback"])}">{esc(a["answer"])}</button>'
            for a in q["answers"])
        items.append(f'''  <div class="sq-item">
    <div class="sq-q"><span class="sq-num">Q{i}.</span>{esc(q["question"])}</div>
    <div class="sq-opts">
{opts}
    </div>
    <div class="sq-fb"></div>
  </div>''')
    section = f'''<section id="bankquiz">
  <div class="section-number">QUIZ · 自我檢測</div>
  <h2>自我檢測：{note} <span class="sec-badge">課程題庫 · {len(qs)} 題</span></h2>
  <p>題目取自課程題庫（已譯為繁體中文），每個選項都有解說：選錯也點開看看為什麼錯。全對之後再往下翻詞彙卡。</p>
{chr(10).join(items)}
</section>
'''
    s = s.replace("/* ===== 網站化附加樣式", CSS + "\n/* ===== 網站化附加樣式", 1)
    assert s.count('<section id="cards">') == 1
    s = s.replace('<section id="cards">', section + '<section id="cards">', 1)
    m = re.search(r'(  <a href="#cards" data-target="cards">)', s)
    assert m
    s = s[:m.start()] + f'  <a href="#bankquiz" data-target="bankquiz"><span class="fn-num">QUIZ</span><span class="fn-name">自我檢測（{len(qs)} 題）</span></a>\n' + s[m.start():]
    tocm = re.search(r'(    <a href="#cards"><span class="toc-num">CARD</span>)', s)
    if tocm:
        s = s[:tocm.start()] + f'    <a href="#bankquiz"><span class="toc-num">QUIZ</span>自我檢測（{len(qs)} 題）</a>\n' + s[tocm.start():]
    s = s.replace("</body>", f"<script>{JS}</script>\n</body>")
    path.write_text(s)
    print(f"ok {page}: {len(qs)} 題")
