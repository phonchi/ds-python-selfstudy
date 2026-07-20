#!/usr/bin/env python3
"""linked_lists.html（Python 版）完整自學充實。冪等。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib_py import card, ensure_style, insert_end_of_section, run_py

PAGE = Path.home() / "ds-python-selfstudy/linked_lists.html"
s = PAGE.read_text()
s = ensure_style(s)
PDS = "import sys; sys.path.insert(0, '/home/phonchi/ds_cpp/_python_backup/Slides/pythonds3')\n"

C_NODE = """from pythonds3.basic.linked_list import Node

temp = Node(93)
print(temp.data)
print(temp.next)   # 還沒接上任何人：None"""

node = f'''{card("講義 04 · Node 的使用畫面", C_NODE, run_py(PDS + C_NODE),
note='<span id="dx-node"></span>data 和 next 都是 property：底層其實是 get_data() / set_data()，但用起來像普通屬性。next 是 None：Python 用 None 扮演「沒有下一個」的角色。')}'''
s, c1 = insert_end_of_section(s, "node", node, 'id="dx-node"')

C_UNO = """from pythonds3.basic import UnorderedList

my_list = UnorderedList()
for x in [31, 77, 17, 93, 26, 54]:
    my_list.add(x)

print(my_list)
print(my_list.size())
print(my_list.search(93))

my_list.remove(54)
my_list.remove(93)
my_list.remove(31)
print(my_list)"""

uno = f'''<h3 id="dx-uno">講義完整範例：UnorderedList 全套操作</h3>
{card("講義 04 · add / size / search / remove", C_UNO, run_py(PDS + C_UNO),
note="第一行輸出印證了 add 是<strong>頭插</strong>：最後加入的 54 排最前面。三次 remove 分別打中「中間、中間、尾巴」三種位置，下一張卡把參考的動作攤開看。")}
<div class="deck-extra">
  <div class="dx-label">講義 04 · remove(26) 的參考舞步逐格看</div>
  <table style="width:100%;border-collapse:collapse;font-size:.88rem;">
    <tr style="border-bottom:2px solid var(--card-border);"><th style="text-align:left;padding:.4rem;">步驟</th><th style="text-align:left;">previous</th><th style="text-align:left;">current</th><th style="text-align:left;">動作</th></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.4rem;">開始</td><td>None</td><td>head（54）</td><td>兩個名字起跑</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.4rem;">比對 54</td><td>54</td><td>26</td><td>不是目標：previous 跟上、current 前進</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.4rem;">比對 26</td><td>54</td><td>26</td><td>找到了，break</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.4rem;">摘除</td><td colspan="2">previous.next = current.next</td><td>54 直接指向 93，26 被跳過</td></tr>
    <tr><td style="padding:.4rem;">收尾</td><td colspan="2">目標是 head 時 previous 是 None</td><td>改成 self.head = current.next；找不到則 raise ValueError</td></tr>
  </table>
  <p class="dx-note">要背的只有一件事：<strong>單向串列摘節點需要「前一個」的協助</strong>，所以永遠帶著 previous、current 兩個名字同行；被跳過的節點沒人參考之後，交給垃圾回收收走。</p>
</div>'''
s, c2 = insert_end_of_section(s, "unordered", uno, 'id="dx-uno"')

C_ODR = """from pythonds3.basic import OrderedList

my_list = OrderedList()
for x in [31, 77, 17, 93, 26, 54]:
    my_list.add(x)

print(my_list)
print(my_list.size())
print(my_list.search(93))
print(my_list.search(100))"""

odr = f'''{card("講義 04 · OrderedList：一樣的介面、排好的內容", C_ODR, run_py(PDS + C_ODR),
note='<span id="dx-odr"></span>同樣六次 add、同樣的呼叫介面，印出來卻是由小到大：差別全在 add 內部「找到正確位置再插」。search(100) 也更聰明：一碰到比 100 大的節點就能 return False（這條串列裡沒有更大的希望了）。')}'''
s, c3 = insert_end_of_section(s, "ordered", odr, 'id="dx-odr"')

exx = f'''<div class="deck-extra" id="dx-exx">
  <div class="dx-label">pythonds §3 課後題精選（自我挑戰）</div>
  <ol style="font-size:.92rem;line-height:1.9;padding-left:1.4rem;">
    <li><strong>size 的 O(1) 版</strong>：現在的 size() 要走訪整條串列。把「節點數」存成屬性，改寫 add / remove / size，讓 size() 變 O(1)。</li>
    <li><strong>防呆 remove</strong>：目前的 remove 對「不存在的元素」raise ValueError。改成安靜回傳 False 的版本，並說明兩種設計的取捨。</li>
    <li><strong>補完 ADT</strong>：實作 append、index、pop、insert 四個缺席的方法，並分析各自的 Big-O。</li>
    <li><strong>slice(start, stop)</strong>：回傳從 start 到 stop（不含）的新串列。</li>
    <li><strong>用繼承減少重複</strong>：OrderedList 與 UnorderedList 大量方法相同。設計繼承階層，讓共同的部分只寫一次。</li>
    <li><strong>串列版 Stack／Queue／Deque</strong>：用鏈結串列各實作一次，跟 list 版比效能。哪些操作變快、哪些變慢？</li>
  </ol>
  <p class="dx-note">完整題目在 <a href="https://github.com/RunestoneInteractive/pythonds/blob/master/_sources/BasicDS/ProgrammingExercises.rst" target="_blank" rel="noopener">pythonds ProgrammingExercises</a>；第 5 題會逼你把兩個類別的差異想透。</p>
</div>'''
s, c4 = insert_end_of_section(s, "exercises", exx, 'id="dx-exx"')

PAGE.write_text(s)
print("inserted:", [n for n, ok in zip("node uno odr exx".split(), [c1, c2, c3, c4]) if ok])
