#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / "ds-python-selfstudy/tools/enrich"))
from enrich_lib_py import hl, card

SP = Path(__file__).resolve().parent

def code(src, size=".8rem"):
    return f'<div class="pseudo-code" style="font-size:{size};">{hl(src)}</div>'

def hook(title, body):
    return (f'<div class="ds-hook"><div class="dh-title">🔗 這在資料結構課哪裡會用到 · {title}</div>'
            f'{body}</div>')

NAV = [
    ("prologue",  "P00", "從一個類別到一族"),
    ("inherit",   "P01", "繼承與 super()"),
    ("override",  "P02", "覆寫與多型"),
    ("eqhash",    "P03", "__eq__ 與 __hash__"),
    ("lt",        "P04", "__lt__ 與排序"),
    ("protocol",  "P05", "容器協定"),
    ("versus",    "P06", "組合 vs 繼承"),
    ("dataclass", "P07", "dataclass 與例外"),
    ("exercises", "EX",  "隨堂練習"),
    ("reference", "REF", "dunder 速查表"),
]
TOC_NAMES = {
    "prologue": "從一個類別到一整族", "inherit": "繼承與 super()", "override": "覆寫與多型",
    "eqhash": "__eq__ 與 __hash__", "lt": "__lt__：排序的關鍵", "protocol": "容器協定 dunder",
    "versus": "組合 vs 繼承", "dataclass": "dataclass 與自訂例外",
    "exercises": "隨堂練習", "reference": "dunder 速查表",
}

nav = "\n".join(
    f'  <a href="#{i}" data-target="{i}"><span class="fn-num">{n}</span><span class="fn-name">{t}</span></a>'
    for i, n, t in NAV)
toc = "\n".join(
    f'    <a href="#{i}"><span class="toc-num">{n}</span>{TOC_NAMES[i]}</a>' for i, n, _ in NAV)

C_INHERIT = '''class UnorderedList:
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.insert(0, item)      # 無序：一律插在最前面

    def __str__(self):
        return " -> ".join(map(str, self._items))


class OrderedList(UnorderedList):        # ← 括號裡是父類別
    def add(self, item):                 # ← 覆寫：同名方法，不同做法
        i = 0
        while i < len(self._items) and self._items[i] < item:
            i += 1
        self._items.insert(i, item)      # 有序：插到該在的位置


u, o = UnorderedList(), OrderedList()
for v in [31, 17, 93, 26]:
    u.add(v)
    o.add(v)

print("UnorderedList:", u)
print("OrderedList  :", o)
print("是子類別嗎:", issubclass(OrderedList, UnorderedList))
print("MRO:", [c.__name__ for c in OrderedList.__mro__])'''
O_INHERIT = """UnorderedList: 26 -> 93 -> 17 -> 31
OrderedList  : 17 -> 26 -> 31 -> 93
是子類別嗎: True
MRO: ['OrderedList', 'UnorderedList', 'object']"""

C_HASH = '''class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)


{Point(1, 2)}          # 想把它放進 set'''
O_HASH = "TypeError: unhashable type: 'Point'"

C_HASH2 = '''class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):                       # 相等的物件必須有相同的雜湊值
        return hash((self.x, self.y))


print(len({Point(1, 2), Point(1, 2), Point(3, 4)}))'''
O_HASH2 = "2"

C_NOLT = '''class Task:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def __repr__(self):
        return f"Task({self.name!r}, {self.priority})"


sorted([Task("備份", 5), Task("修 bug", 1), Task("回信", 3)])'''
O_NOLT = "TypeError: '<' not supported between instances of 'Task' and 'Task'"

C_LT = '''import functools
import heapq


@functools.total_ordering          # 有了 __eq__ 與 __lt__，其餘比較運算子自動補齊
class Task:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def __repr__(self):
        return f"Task({self.name!r}, {self.priority})"

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):       # 定義「什麼叫比較小」
        return self.priority < other.priority


ts = [Task("備份", 5), Task("修 bug", 1), Task("回信", 3)]

print("sorted  ->", sorted(ts))
print("min     ->", min(ts))

heapq.heapify(ts)                  # 同一份物件，直接丟進二元堆積
print("heappop ->", heapq.heappop(ts), heapq.heappop(ts))
print("total_ordering 送的 >= :", Task("a", 5) >= Task("b", 1))'''
O_LT = """sorted  -> [Task('修 bug', 1), Task('回信', 3), Task('備份', 5)]
min     -> Task('修 bug', 1)
heappop -> Task('修 bug', 1) Task('回信', 3)
total_ordering 送的 >= : True"""

C_PROTO = '''class Bag:
    def __init__(self, items):
        self._items = list(items)

    def __len__(self):                 # len(b)
        return len(self._items)

    def __getitem__(self, i):          # b[1]
        return self._items[i]

    def __contains__(self, x):         # x in b
        return x in self._items

    def __iter__(self):                # for x in b
        return iter(self._items)


b = Bag(["紅", "綠", "藍"])
print("len(b)    ->", len(b))
print("b[1]      ->", b[1])
print("'綠' in b ->", "綠" in b)
print("for 迴圈  ->", [x for x in b])'''
O_PROTO = """len(b)    -> 3
b[1]      -> 綠
'綠' in b -> True
for 迴圈  -> ['紅', '綠', '藍']"""

C_BADDEQUE = '''class BadDeque(list):              # 繼承 list：看似省事
    def add_front(self, x):
        self.insert(0, x)


d = BadDeque()
d.add_front(1)
d.add_front(2)

print("內容:", d)
print("但外面還能呼叫:", [m for m in ("sort", "reverse", "insert") if hasattr(d, m)])'''
O_BADDEQUE = """內容: [2, 1]
但外面還能呼叫: ['sort', 'reverse', 'insert']"""

C_DATACLASS = '''from dataclasses import dataclass


@dataclass(order=True)             # 自動生成 __init__ / __repr__ / __eq__ / __lt__
class Item:
    priority: int                  # 比較時按照欄位宣告順序
    name: str


items = [Item(5, "備份"), Item(1, "修 bug")]
print(items[0])
print("自動有 __eq__      :", Item(1, "x") == Item(1, "x"))
print("order=True 就有 __lt__:", sorted(items))'''
O_DATACLASS = """Item(priority=5, name='備份')
自動有 __eq__      : True
order=True 就有 __lt__: [Item(priority=1, name='修 bug'), Item(priority=5, name='備份')]"""

body = f'''<nav class="float-nav" id="floatNav" aria-label="章節導覽">
  <div class="fn-title">章節導覽</div>
{nav}
  <a href="#top" class="fn-top" title="回到頂端"><span class="fn-num">↑ TOP</span></a>
</nav>

<div class="hero" id="top">
  <div class="hero-grid"></div>
  <svg class="hero-graph" width="300" height="260" viewBox="0 0 300 260">
  <g stroke="#fff" stroke-width="2.5" fill="none" opacity=".85">
    <rect x="100" y="24" width="100" height="42" rx="8"/>
    <line x1="150" y1="66" x2="150" y2="92"/>
    <line x1="75" y1="92" x2="225" y2="92"/>
    <line x1="75" y1="92" x2="75" y2="118"/><line x1="225" y1="92" x2="225" y2="118"/>
    <rect x="30" y="118" width="90" height="40" rx="7"/>
    <rect x="180" y="118" width="90" height="40" rx="7"/>
    <line x1="75" y1="158" x2="75" y2="184"/>
    <rect x="30" y="184" width="90" height="40" rx="7"/>
  </g>
  <g fill="#fff" opacity=".75" font-family="monospace" font-size="11">
    <text x="112" y="50">Parent</text>
    <text x="47" y="143">Child</text><text x="196" y="143">Child</text>
    <text x="44" y="209">GChild</text>
  </g>
</svg>
  <div class="hero-content">
    <div class="chapter-tag">PREREQ P9</div>
    <h1><span class="blue">物件導向</span>（進階）：繼承、多型與 dunder</h1>
    <div class="subtitle">先備知識複習 · 選讀，不列入作業與考試範圍</div>
    <div class="big-formula">繼承｜super()｜多型｜__eq__｜__hash__｜__lt__｜容器協定｜dataclass</div>
    <div class="scroll-hint">向下捲動開始互動<span>↓</span></div>
  </div>
</div>

<div class="container">

<div class="toc">
  <div class="toc-title">CONTENTS · 內容目錄</div>
  <div class="toc-grid">
{toc}
  </div>
</div>

<section id="prologue">
  <div class="section-number">PROLOGUE · 開場</div>
  <h2>從一個類別，到一整族類別</h2>
  <p><a href="p8_oop_basics.html">P8</a> 教你把「資料 + 操作」包成一個 <code>class</code>。這一頁處理接下來必然發生的三件事：</p>
  <div class="cmp-table-wrap">
  <table class="cmp-table">
    <thead><tr><th>問題</th><th>Python 的答案</th><th>對應章節</th></tr></thead>
    <tbody>
      <tr><td>兩個類別有一半的程式碼一樣，要複製貼上嗎？</td><td><strong>繼承</strong>與 <code>super()</code></td><td>本頁 P01–P02</td></tr>
      <tr><td>怎麼讓 <code>len(x)</code>、<code>x[i]</code>、<code>a &lt; b</code>、<code>for i in x</code> 對我自己寫的結構也能用？</td><td><strong>dunder 方法</strong></td><td>本頁 P03–P05</td></tr>
      <tr><td>該用繼承還是「持有一個」？</td><td>看是 <strong>is-a</strong> 還是 <strong>has-a</strong></td><td>本頁 P06</td></tr>
    </tbody>
  </table>
  </div>
  <div class="info-box">
    <div class="info-label">💡 一句話抓重點</div>
    <p style="margin-bottom:0;">Python 的內建語法（<code>len</code>、<code>in</code>、<code>&lt;</code>、<code>for</code>、<code>[]</code>）<strong>全部都是在偷偷呼叫你的 dunder 方法</strong>。學會 dunder，你自己寫的資料結構就能用得跟內建型別一樣自然 —— 這正是 <code>pythonds3</code> 在做的事。</p>
  </div>
  <div class="warn-box">
    <div class="info-label">📌 本頁定位</div>
    <p style="margin-bottom:0;">選讀的先備知識複習，不列入作業與考試範圍。但 P04（<code>__lt__</code>）與 P05（容器協定）直接決定你能不能讀懂第 09 章的優先佇列與 Map ADT。</p>
  </div>
</section>

<section id="inherit">
  <div class="section-number">PART 01 · 繼承</div>
  <h2>is-a：子類別自動拿到父類別的一切 <span class="sec-badge">DRY</span></h2>
  <p>「有序串列<strong>是一種</strong>串列」—— 這種 is-a 關係就用繼承。子類別自動擁有父類別所有的屬性與方法，只需要寫「不一樣的那部分」。</p>

  {card("OrderedList 繼承 UnorderedList，只覆寫 add()", C_INHERIT, O_INHERIT,
        "兩個類別的 <code>__init__</code> 與 <code>__str__</code> 完全共用，只有 <code>add</code> 不同。"
        "<code>__mro__</code>（Method Resolution Order）就是<a href='p8_oop_basics.html#attrs'>屬性查找順序</a>："
        "先找 OrderedList，沒有才往 UnorderedList 找，最後是 object。")}

  <h3 style="font-family:'Noto Serif TC',serif;font-size:1.12rem;margin:1.3rem 0 .5rem;color:var(--accent2);"><code>super()</code>：擴充而不是取代</h3>
  <p>如果子類別的 <code>__init__</code> 需要「父類別做的事 <strong>再加上</strong> 我自己的事」，用 <code>super()</code> 呼叫父類別的版本：</p>
  {code('''class BinaryTree:
    def __init__(self, root_obj):
        self.key = root_obj
        self.left_child = None
        self.right_child = None


class AVLTree(BinaryTree):
    def __init__(self, root_obj):
        super().__init__(root_obj)     # 先讓父類別把三個欄位設好
        self.balance_factor = 0        # 再補上 AVL 自己需要的欄位''')}

  <div class="warn-box">
    <div class="info-label">⚠️ 最常見的錯誤</div>
    <p style="margin-bottom:0;">子類別寫了 <code>__init__</code> 卻忘記呼叫 <code>super().__init__()</code>，於是父類別的欄位<strong>根本沒被建立</strong>。之後某個繼承來的方法用到那個欄位，就噴 <code>AttributeError</code>——而且錯誤發生的位置離真正的原因很遠，很難找。</p>
  </div>

  {hook("第 01、09 章", "第 01 章的邏輯閘電路是完整的繼承階層（<code>LogicGate → BinaryGate → AndGate</code>）；第 09 章的 <code>AVLTree</code> 繼承 <code>BinarySearchTree</code>，只覆寫需要維持平衡的那幾個方法。")}
</section>

<section id="override">
  <div class="section-number">PART 02 · 多型</div>
  <h2>同一段程式碼，餵不同的東西進去都能動</h2>
  <p><strong>多型（polymorphism）</strong>的意思是：呼叫端不用知道拿到的是哪一個子類別，只要它「會做這件事」就好。</p>

  {code('''def print_all(container):
    """只要傳進來的東西有 __str__ 跟 add()，這個函數就能用。"""
    for item in [31, 17, 93]:
        container.add(item)
    print(container)


print_all(UnorderedList())   # 26 -> 93 -> 17 -> 31 的那種
print_all(OrderedList())     # 排好序的那種
# print_all 完全不需要知道自己拿到的是哪一種''')}

  <div class="info-box green">
    <div class="info-label">🦆 鴨子型別（Duck Typing）</div>
    <p style="margin-bottom:0;">「走起來像鴨子、叫起來像鴨子，那就當它是鴨子。」Python 不檢查型別，只在<strong>真的呼叫的時候</strong>看方法在不在。所以多型在 Python 裡甚至不需要繼承 —— 兩個毫無關係的類別，只要都有 <code>add()</code>，就能餵進同一個函數。</p>
  </div>

  {hook("第 05、07 章", "第 07 章的六種排序全部長成 <code>sort(a_list)</code>，你可以把它們互換而不改呼叫端；第 05 章的 Stack 與 Queue 也能被同一段走訪程式碼吃下去。")}
</section>

<section id="eqhash">
  <div class="section-number">PART 03 · 相等與雜湊</div>
  <h2><code>__eq__</code> 與 <code>__hash__</code>：一對不能拆開的搭檔</h2>
  <p>預設情況下，兩個物件只有在<strong>是同一個物件</strong>時才相等。要讓「內容一樣就算相等」，得自己寫 <code>__eq__</code>。</p>

  {card("只寫 __eq__ 會發生的事", C_HASH, O_HASH,
        "Python 的規則是：<strong>一旦你定義了 <code>__eq__</code>，物件就自動變成不可雜湊</strong>。"
        "因為它無法保證你的相等定義跟預設的雜湊值一致 —— 而 set 與 dict 的 key 都需要雜湊值。")}

  {card("補上 __hash__ 之後", C_HASH2, O_HASH2,
        "三個 Point 放進 set 只剩兩個，因為兩個 <code>Point(1, 2)</code> 被視為同一個。"
        "鐵則：<strong>a == b 為真時，hash(a) 必須等於 hash(b)</strong>。"
        "所以雜湊值要從「決定相等的那些欄位」算出來。")}

  {hook("第 07 章", "這正是雜湊表能運作的前提。第 07 章會講雜湊函數、碰撞與線性探查——而你自訂的物件想當 dict 的 key，就必須讓 <code>__eq__</code> 與 <code>__hash__</code> 說法一致，否則同一個 key 會查不到、或出現兩份。")}
</section>

<section id="lt">
  <div class="section-number">PART 04 · 排序的關鍵</div>
  <h2><code>__lt__</code>：定義了「小於」，整個生態系就能用你的物件</h2>

  {card("沒有 __lt__ 的下場", C_NOLT, O_NOLT,
        "<code>sorted()</code>、<code>min()</code>、<code>heapq</code>、二元堆積、快速排序……"
        "全部都只做一件事：<strong>兩兩比大小</strong>。你沒告訴 Python 怎麼比，它就罷工。")}

  {card("補上 __lt__ 與 __eq__ 之後，同一份物件到處都能用", C_LT, O_LT,
        "只寫了兩個方法，就換到 <code>sorted</code>、<code>min</code>、<code>heapq</code> 全部能用。"
        "<code>@functools.total_ordering</code> 會用你的 <code>__lt__</code> 與 <code>__eq__</code> 自動補出 "
        "<code>&gt;</code>、<code>&lt;=</code>、<code>&gt;=</code>——這門課的 notebook 有 import <code>functools</code>，就是這個用途。")}

  <p>下面這個逐步器把 <code>sorted()</code> 拆開來看：每一次比較都是一次 <code>__lt__</code> 呼叫。</p>

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div id="ltStage" style="min-height:150px;"></div>
        <div class="status-banner" id="ltStatus"><span class="status-icon">›</span><span class="status-text">按「開始」看排序過程中每一次 __lt__ 被呼叫的樣子。</span></div>
        <div class="controls-bar">
          <button class="btn btn-play" onclick="ltStart()">▶ 開始排序</button>
          <button class="btn btn-step" onclick="ltPlayer &amp;&amp; ltPlayer.step()">→ 單步</button>
          <button class="btn btn-reset" onclick="ltReset()">⟲ 重設</button>
          <span class="mono" style="font-size:.78rem;color:var(--muted);">已呼叫 __lt__：<b id="ltCount">0</b> 次</span>
        </div>
      </div>
    </div>
    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">虛擬碼 <span class="ic-badge">CODE</span></div>
        <div class="pseudo-code" id="ltCode" style="font-size:.78rem;">{hl('''def insertion_sort(a):
    for i in range(1, len(a)):
        cur = a[i]
        j = i - 1
        while j >= 0 and cur < a[j]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = cur''')}</div>
      </div>
      <div class="info-card">
        <div class="ic-title">關鍵那一行 <span class="ic-badge">WHY</span></div>
        <p style="font-size:.88rem;margin-bottom:0;"><code>cur &lt; a[j]</code> 就是 <code>cur.__lt__(a[j])</code>。你沒定義它，這一行就 <code>TypeError</code>；你定義錯了，整個排序就悄悄排錯 —— 而且不會噴任何錯誤。</p>
      </div>
    </div>
  </div>

  {hook("第 07、09 章", "第 07 章六種排序法的核心都是這一次比較；第 09 章的 <code>PriorityQueue</code>（二元堆積）在 percolate up/down 時每一步都在比大小。想把自訂的工作物件丟進優先佇列？先給它 <code>__lt__</code>。")}
</section>

<section id="protocol">
  <div class="section-number">PART 05 · 容器協定</div>
  <h2>讓自訂結構支援 <code>len()</code>、<code>[]</code>、<code>in</code>、<code>for</code></h2>
  <p>Python 的內建語法其實都是 dunder 的門面。實作對應的 dunder，你的類別就能用得跟內建型別一樣。</p>

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <table class="cmp-table" id="dunderTable" style="margin:0;">
          <thead><tr><th>你寫的語法</th><th>Python 實際呼叫</th><th>本站哪一章用到</th></tr></thead>
          <tbody></tbody>
        </table>
        <div class="status-banner" id="dnStatus"><span class="status-icon">›</span><span class="status-text">點表格任一列，看那個 dunder 的說明與課程對應。</span></div>
      </div>
    </div>
    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">說明 <span class="ic-badge">DETAIL</span></div>
        <div id="dnDetail" style="font-size:.88rem;">點左邊表格的任一列。</div>
      </div>
    </div>
  </div>

  {card("一次實作四個協定", C_PROTO, O_PROTO,
        "<code>Bag</code> 從頭到尾沒有繼承任何東西，卻已經能用 <code>len()</code>、下標、<code>in</code> 與 <code>for</code>。"
        "這就是鴨子型別的力量：<strong>能力來自你實作了哪些協定，不是來自你繼承了誰</strong>。")}

  {hook("第 03、09 章", "第 03 章的 <code>ArrayList</code> 要能寫 <code>arr[5]</code> 就靠 <code>__getitem__</code> / <code>__setitem__</code>；第 09 章把二元搜尋樹當 Map 用，<code>tree['key'] = 1</code>、<code>'key' in tree</code>、<code>del tree['key']</code>、<code>len(tree)</code> 全部是 dunder。")}
</section>

<section id="versus">
  <div class="section-number">PART 06 · 設計抉擇</div>
  <h2>組合 vs 繼承：<code>Deque</code> 該繼承 <code>list</code> 嗎？</h2>
  <p>做一個雙端佇列，最省事的寫法看起來是直接繼承 <code>list</code>。試試看會怎樣：</p>

  {card("繼承 list 的陷阱", C_BADDEQUE, O_BADDEQUE,
        "問題不在它不能動，而在它<strong>能做的事太多了</strong>："
        "使用者可以對你的 Deque 呼叫 <code>sort()</code>、<code>reverse()</code>、<code>insert(3, x)</code>——"
        "這些操作全都違反雙端佇列「只能從兩端進出」的契約，而你完全擋不住。")}

  <div class="cmp-table-wrap">
  <table class="cmp-table">
    <thead><tr><th></th><th>繼承（is-a）</th><th>組合（has-a）</th></tr></thead>
    <tbody>
      <tr><td>寫法</td><td class="mono">class Deque(list):</td><td class="mono">self._items = []</td></tr>
      <tr><td>對外露出什麼</td><td>父類別<strong>所有</strong>方法，擋不掉</td><td>只有你自己寫的方法</td></tr>
      <tr><td>能換底層實作嗎</td><td>不能，已經綁死 list</td><td>能，改內部一行就好</td></tr>
      <tr><td>什麼時候該用</td><td>子類別<strong>真的是</strong>一種父類別，而且父類別的每個方法對它都合理</td><td>絕大多數的資料結構</td></tr>
    </tbody>
  </table>
  </div>

  <div class="info-box purple">
    <div class="info-label">🎯 判斷法則</div>
    <p style="margin-bottom:0;">問自己一句：<strong>「父類別的每一個方法，用在子類別身上都說得通嗎？」</strong>只要有一個說不通（例如對 Deque 呼叫 <code>sort()</code>），就不要繼承，改用組合。<br>
    <code>OrderedList</code> 繼承 <code>UnorderedList</code> 是合理的（父類別的每個方法對它都成立）；<code>Deque</code> 繼承 <code>list</code> 不合理。</p>
  </div>

  {hook("第 05 章", "pythonds3 的 <code>Stack</code>、<code>Queue</code>、<code>Deque</code> 全部採用組合而非繼承 list——現在你知道為什麼了。")}
</section>

<section id="dataclass">
  <div class="section-number">PART 07 · 收尾</div>
  <h2><code>@dataclass</code> 與自訂例外</h2>

  <h3 style="font-family:'Noto Serif TC',serif;font-size:1.12rem;margin:1.2rem 0 .5rem;color:var(--accent2);">少寫一點樣板：<code>@dataclass</code></h3>
  {card("一個裝飾器換掉四個 dunder", C_DATACLASS, O_DATACLASS,
        "<code>@dataclass</code> 自動生成 <code>__init__</code>、<code>__repr__</code>、<code>__eq__</code>；"
        "加上 <code>order=True</code> 連 <code>__lt__</code> 都有了，比較時按欄位宣告順序。"
        "適合單純裝資料的類別；但需要自訂邏輯（例如 Node 的 <code>_next</code> 串接）時，還是自己寫 class。")}

  <h3 style="font-family:'Noto Serif TC',serif;font-size:1.12rem;margin:1.4rem 0 .5rem;color:var(--accent2);">自訂例外：讓錯誤訊息說人話</h3>
  {code('''class EmptyStackError(Exception):
    """對空堆疊做 pop 或 peek 時拋出。"""


class Stack:
    def __init__(self):
        self._items = []

    def pop(self):
        if not self._items:
            raise EmptyStackError("堆疊是空的，沒有東西可以彈出")
        return self._items.pop()


s = Stack()
try:
    s.pop()
except EmptyStackError as e:
    print("接住了:", e)''')}
  <p style="font-size:.9rem;">自訂例外只要繼承 <code>Exception</code> 就好，通常連內容都不用寫。好處是呼叫端可以<strong>精準地只接住這一種錯誤</strong>，而不是用一個 <code>except</code> 把所有 bug 一起吞掉。例外的完整語法見 <a href="p7_files_exceptions.html">P7</a>。</p>

  {hook("第 05、09 章", "pythonds3 的 Stack 對空的 pop 會拋 <code>IndexError</code>；自己實作時，拋一個講得清楚的自訂例外會讓 debug 快很多。")}
</section>

<section id="exercises">
  <div class="section-number">EX · 隨堂練習</div>
  <h2>三題確認觀念 <span class="sec-badge">答錯就回該節</span></h2>

  <div class="quiz-box">
    <div class="quiz-label">EXERCISE 1 · 優先佇列排不動</div>
    <p>你寫了一個 <code>Job</code> 類別，把一堆 Job 丟進 <code>heapq</code>，結果噴 <code>TypeError: '&lt;' not supported</code>。最直接的解法是？</p>
    <div class="quiz-options" id="q1Options">
      <div class="quiz-opt" data-correct="false" data-fb="__eq__ 只定義「相等」，堆積需要的是「誰比較小」。加了 __eq__ 反而會讓物件變成不可雜湊。" onclick="quizCheck('q1', this)"><span class="opt-letter">(A)</span> 加上 <code>__eq__</code></div>
      <div class="quiz-opt" data-correct="true" data-fb="正確。heapq、sorted、min 全部靠 &lt; 運算子，也就是 __lt__。定義它之後，同一份物件在排序、堆積、優先佇列裡都能用。" onclick="quizCheck('q1', this)"><span class="opt-letter">(B)</span> 加上 <code>__lt__</code></div>
      <div class="quiz-opt" data-correct="false" data-fb="__str__ 只影響印出來的樣子，跟能不能比大小無關。" onclick="quizCheck('q1', this)"><span class="opt-letter">(C)</span> 加上 <code>__str__</code></div>
    </div>
    <div class="quiz-feedback" id="q1Feedback"></div>
  </div>

  <div class="quiz-box">
    <div class="quiz-label">EXERCISE 2 · 該繼承還是該持有</div>
    <p>你要實作一個「只能從兩端進出」的 <code>Deque</code>。下列哪個設計比較好？</p>
    <div class="quiz-options" id="q2Options">
      <div class="quiz-opt" data-correct="false" data-fb="這樣使用者可以對你的 Deque 呼叫 sort()、insert(3, x)，直接違反雙端佇列的契約，而你擋不住。" onclick="quizCheck('q2', this)"><span class="opt-letter">(A)</span> <code>class Deque(list):</code> 直接繼承</div>
      <div class="quiz-opt" data-correct="true" data-fb="正確。組合（has-a）讓你只暴露 add_front / add_rear / remove_front / remove_rear，內部想換成鏈結串列也不用動到呼叫端。" onclick="quizCheck('q2', this)"><span class="opt-letter">(B)</span> 內部持有一個 list，只提供四個端點操作</div>
      <div class="quiz-opt" data-correct="false" data-fb="兩者差很多。差別不在能不能動，而在你對介面還有沒有控制權。" onclick="quizCheck('q2', this)"><span class="opt-letter">(C)</span> 兩者完全等價</div>
    </div>
    <div class="quiz-feedback" id="q2Feedback"></div>
  </div>

  <div class="quiz-box">
    <div class="quiz-label">EXERCISE 3 · 放進 set 卻爆掉</div>
    <p>某個類別定義了 <code>__eq__</code>，然後把實例放進 <code>set</code> 時噴 <code>TypeError: unhashable type</code>。為什麼？</p>
    <div class="quiz-options" id="q3Options">
      <div class="quiz-opt" data-correct="false" data-fb="set 當然可以裝自訂物件——前提是那個物件可雜湊。" onclick="quizCheck('q3', this)"><span class="opt-letter">(A)</span> set 只能裝內建型別</div>
      <div class="quiz-opt" data-correct="true" data-fb="正確。定義 __eq__ 會讓 Python 把 __hash__ 設成 &#78;one，因為它無法保證你的相等定義與預設雜湊一致。要放進 set 或當 dict 的 key，就得自己補一個與 __eq__ 說法一致的 __hash__。" onclick="quizCheck('q3', this)"><span class="opt-letter">(B)</span> 定義 <code>__eq__</code> 會讓物件自動失去 <code>__hash__</code></div>
      <div class="quiz-opt" data-correct="false" data-fb="順序無關。這是 Python 的規則：定義 __eq__ 就必須自己處理 __hash__。" onclick="quizCheck('q3', this)"><span class="opt-letter">(C)</span> <code>__eq__</code> 要寫在 <code>__init__</code> 前面</div>
    </div>
    <div class="quiz-feedback" id="q3Feedback"></div>
  </div>
</section>

<section id="reference">
  <div class="section-number">REFERENCE · 速查表</div>
  <h2>dunder 全表：語法 ↔ 方法 ↔ 課程對應</h2>
  <div class="cmp-table-wrap">
  <table class="cmp-table">
    <thead><tr><th>你寫的</th><th>Python 呼叫</th><th>用途</th><th>本站對應</th></tr></thead>
    <tbody>
      <tr><td class="mono">X(...)</td><td class="mono">__init__</td><td>建立實例時初始化</td><td>每一章</td></tr>
      <tr><td class="mono">print(x)</td><td class="mono">__str__</td><td>給人看的字串</td><td>第 04、05、09 章</td></tr>
      <tr><td class="mono">repr(x)、[x]</td><td class="mono">__repr__</td><td>給開發者看的字串</td><td>debug</td></tr>
      <tr><td class="mono">len(x)</td><td class="mono">__len__</td><td>元素個數</td><td>第 03、05 章</td></tr>
      <tr><td class="mono">x[i]</td><td class="mono">__getitem__</td><td>讀取下標</td><td>第 03、09 章</td></tr>
      <tr><td class="mono">x[i] = v</td><td class="mono">__setitem__</td><td>寫入下標</td><td>第 03、09 章</td></tr>
      <tr><td class="mono">del x[i]</td><td class="mono">__delitem__</td><td>刪除下標</td><td>第 09 章 Map ADT</td></tr>
      <tr><td class="mono">v in x</td><td class="mono">__contains__</td><td>成員檢查</td><td>第 07、09 章</td></tr>
      <tr><td class="mono">for v in x</td><td class="mono">__iter__</td><td>走訪</td><td>第 04、09 章</td></tr>
      <tr><td class="mono">a == b</td><td class="mono">__eq__</td><td>相等判斷</td><td>第 07 章雜湊</td></tr>
      <tr><td class="mono">hash(a)、set、dict key</td><td class="mono">__hash__</td><td>雜湊值</td><td>第 07 章雜湊</td></tr>
      <tr><td class="mono">a &lt; b、sorted、heapq</td><td class="mono">__lt__</td><td>排序依據</td><td>第 07、09 章</td></tr>
      <tr><td class="mono">a + b</td><td class="mono">__add__</td><td>加法／串接</td><td>第 01 章 Fraction</td></tr>
      <tr><td class="mono">a * b</td><td class="mono">__mul__</td><td>乘法</td><td>第 03 章矩陣</td></tr>
    </tbody>
  </table>
  </div>

  <h3 style="font-family:'Noto Serif TC',serif;font-size:1.12rem;margin:1.4rem 0 .5rem;color:var(--accent2);">四條記得住的規則</h3>
  <div class="info-box green">
    <p>① 子類別的 <code>__init__</code> 幾乎一定要呼叫 <code>super().__init__()</code>。<br>
    ② 定義了 <code>__eq__</code>，就要一併定義 <code>__hash__</code>（除非你不打算放進 set／dict）。<br>
    ③ 想被排序，給 <code>__lt__</code>；想少寫幾個，加 <code>@functools.total_ordering</code>。<br>
    ④ 不確定該繼承還是組合時，<strong>選組合</strong>。</p>
  </div>

  <h3 style="font-family:'Noto Serif TC',serif;font-size:1.12rem;margin:1.4rem 0 .5rem;color:var(--accent2);">延伸閱讀</h3>
  <table class="cmp-table">
    <thead><tr><th>資源</th><th>看什麼</th></tr></thead>
    <tbody>
      <tr><td><a href="https://docs.python.org/zh-tw/3/reference/datamodel.html#special-method-names" target="_blank" rel="noopener">Python 資料模型 · 特殊方法名稱</a></td><td>所有 dunder 的權威清單。</td></tr>
      <tr><td><a href="https://docs.python.org/zh-tw/3/library/functools.html#functools.total_ordering" target="_blank" rel="noopener">functools.total_ordering</a></td><td>只寫 <code>__lt__</code> 與 <code>__eq__</code> 就補齊全部比較運算子。</td></tr>
      <tr><td><a href="https://docs.python.org/zh-tw/3/library/dataclasses.html" target="_blank" rel="noopener">dataclasses</a></td><td><code>order</code>、<code>frozen</code>、<code>field</code> 的完整選項。</td></tr>
      <tr><td><a href="trees.html">本站第 09 章 · 樹與樹演算法</a></td><td>看 <code>__lt__</code> 在二元堆積裡怎麼被用。</td></tr>
    </tbody>
  </table>
</section>

</div>

<footer>
  先備知識 P9 · 物件導向（進階）· 資料結構 × Python 互動自學網站<br>
  <span style="font-family:'JetBrains Mono',monospace;font-size:.78rem;color:var(--accent3);">Designed for NSYSU · Interactive Python self-study</span>
</footer>
'''

(SP / "body_p9.html").write_text(body)
print("body_p9.html", len(body), "bytes")
