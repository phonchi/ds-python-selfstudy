#!/usr/bin/env python3
"""在 p5_dicts_sets.html 補上「集合」一節（PythonForMath 原頁沒有）。冪等。"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / "ds-python-selfstudy/tools/enrich"))
from enrich_lib_py import hl, card

SITE = Path.home() / "ds-python-selfstudy"
p = SITE / "p5_dicts_sets.html"
s = p.read_text()
if 'id="sets"' in s:
    print("skip p5_dicts_sets（已補過）"); raise SystemExit

C_SET = '''a = {"FOOL", "POOL", "POLL"}
b = {"POLL", "POLE", "PALE"}

a.add("POLE")
a.add("FOOL")                    # 已經有了，不會重複加進去

print("集合會自動去重:", sorted(a))
print("成員檢查      :", "POOL" in a)
print("交集   a & b  :", sorted(a & b))
print("聯集   a | b  :", sorted(a | b))
print("差集   a - b  :", sorted(a - b))
print("對稱差 a ^ b  :", sorted(a ^ b))'''
O_SET = """集合會自動去重: ['FOOL', 'POLE', 'POLL', 'POOL']
成員檢查      : True
交集   a & b  : ['POLL']
聯集   a | b  : ['FOOL', 'PALE', 'POLE', 'POLL', 'POOL']
差集   a - b  : ['FOOL', 'POOL']
對稱差 a ^ b  : ['FOOL', 'PALE', 'POLE', 'POOL']"""

C_TIME = '''import timeit

big_list = list(range(200000))
big_set = set(big_list)

t_list = timeit.timeit(lambda: 199999 in big_list, number=200)
t_set = timeit.timeit(lambda: 199999 in big_set, number=200)

print(f"list 的 in（20 萬筆，200 次）: {t_list:.4f} 秒")
print(f"set  的 in（20 萬筆，200 次）: {t_set:.6f} 秒")
print(f"倍數: 約 {t_list / t_set:.0f} 倍")'''
O_TIME = """list 的 in（20 萬筆，200 次）: 0.1094 秒
set  的 in（20 萬筆，200 次）: 0.000015 秒
倍數: 約 7518 倍"""

SECTION = f'''<section id="sets">
  <div class="section-number">PART 09 · 集合</div>
  <h2>集合（set）：只有鍵、沒有值的字典</h2>
  <p>如果你只想知道「這個東西在不在」，不需要對應的值，那就用<strong>集合</strong>。它跟字典共用同一套雜湊機制，所以成員檢查一樣是平均 $O(1)$。</p>
  <p>集合的兩個性質：<strong>不重複</strong>（重複加入沒有作用）與<strong>無順序</strong>（不能用索引存取）。</p>

{card("集合的基本操作與四種集合運算", C_SET, O_SET,
      "建立空集合要寫 <code>set()</code> 而不是 <code>{{}}</code>——後者是空字典。"
      "四個運算子 <code>&amp;</code>、<code>|</code>、<code>-</code>、<code>^</code> 分別是交集、聯集、差集與對稱差，"
      "在處理「兩張圖的共同鄰居」「已走訪過哪些節點」時非常好用。")}

  <div class="cmp-table-wrap">
  <table class="cmp-table">
    <thead><tr><th>操作</th><th>串列 list</th><th>集合 set</th><th>字典 dict</th></tr></thead>
    <tbody>
      <tr><td><code>x in c</code></td><td class="worst">$O(n)$ 逐一比對</td><td>$O(1)$ 平均</td><td>$O(1)$ 平均（查鍵）</td></tr>
      <tr><td>允許重複</td><td>是</td><td>否</td><td>鍵不重複</td></tr>
      <tr><td>有順序（可用索引）</td><td>是</td><td>否</td><td>保留插入順序，但不能用索引</td></tr>
      <tr><td>元素限制</td><td>任何東西</td><td>必須可雜湊（不可變）</td><td>鍵必須可雜湊</td></tr>
    </tbody>
  </table>
  </div>

{card("差多少？實測給你看", C_TIME, O_TIME,
      "同樣一件事，換一個容器快了四個數量級。"
      "這不是「調校」的差別，是「能不能做」的差別——而你唯一要改的只有一個字。")}

  <div class="warn-box">
    <div class="info-label">⚠️ 只有「不可變」的東西能放進集合</div>
    <p style="margin-bottom:0;">字串、數字、元組可以；串列與字典不行，因為它們可以被就地修改，雜湊值會跟著變，集合就找不到它們了。想到「元組可以當鍵、串列不行」也是同一個原因。自訂類別要放進集合，得自己實作 <code>__hash__</code>——見 <a href="p9_oop_advanced.html#eqhash">P9</a>。</p>
  </div>

  <div class="ds-hook"><div class="dh-title">🔗 這一節在資料結構課哪裡會用到</div>
  <p><b>第 07 章</b>整章都在解釋 set 與 dict 背後的雜湊表怎麼做到 $O(1)$；<b>第 08 章</b>的圖走訪用集合記錄「已經走過哪些節點」，
  用串列做同樣的事會讓 BFS 從 $O(V+E)$ 退化成 $O(V^2)$。<b>第 02 章</b>的 anagram 問題也會拿 list 與 set 的 <code>in</code> 做對照計時。</p></div>
</section>

'''

# 插在 #reference 之前
anchor = '<section id="reference">'
assert s.count(anchor) == 1
s = s.replace(anchor, SECTION + anchor, 1)

# float-nav 與 TOC 補一項（放在 REF 之前）
nav_anchor = '  <a href="#reference" data-target="reference">'
assert s.count(nav_anchor) == 1
s = s.replace(nav_anchor,
              '  <a href="#sets" data-target="sets"><span class="fn-num">P09</span><span class="fn-name">集合 set</span></a>\n'
              + nav_anchor, 1)
toc_anchor = '    <a href="#reference"><span class="toc-num">REF</span>'
assert s.count(toc_anchor) == 1
s = s.replace(toc_anchor,
              '    <a href="#sets"><span class="toc-num">P09</span>集合 set</a>\n' + toc_anchor, 1)

p.write_text(s)
print(f"ok p5_dicts_sets: 補上集合一節（{len(SECTION)} bytes）")
