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
    ("prologue", "P00", "資料結構就是類別"),
    ("classes",  "P01", "類別與實例"),
    ("init",     "P02", "__init__ 與 self"),
    ("attrs",    "P03", "屬性與方法"),
    ("encap",    "P04", "封裝與 property"),
    ("strrepr",  "P05", "__str__ 與 __repr__"),
    ("compose",  "P06", "組合：蓋出 Stack"),
    ("build",    "P07", "動手寫一個 Node"),
    ("exercises","EX",  "隨堂練習"),
    ("reference","REF", "速查表"),
]
TOC_NAMES = {
    "prologue": "為什麼資料結構就是類別", "classes": "類別與實例", "init": "__init__ 與 self",
    "attrs": "屬性與方法", "encap": "封裝與 @property", "strrepr": "__str__ 與 __repr__",
    "compose": "組合：蓋出一個 Stack", "build": "動手寫一個 Node",
    "exercises": "隨堂練習", "reference": "速查表",
}

nav = "\n".join(
    f'  <a href="#{i}" data-target="{i}"><span class="fn-num">{n}</span><span class="fn-name">{t}</span></a>'
    for i, n, t in NAV)
toc = "\n".join(
    f'    <a href="#{i}"><span class="toc-num">{n}</span>{TOC_NAMES[i]}</a>' for i, n, _ in NAV)

# ---------- 範例卡 ----------
C_NODE = '''class Node:
    """鏈結串列的節點：存一個值，再指向下一個節點。"""

    def __init__(self, node_data):
        self._data = node_data
        self._next = None

    def __str__(self):
        return f"Node({self._data})"


n = Node(93)
print(n)
print(n._data, n._next)
print(type(n), isinstance(n, Node))'''
O_NODE = """Node(93)
93 None
<class '__main__.Node'> True"""

C_SELF = '''class Broken:
    def __init__(self, x):
        self.x = x

    def show():          # ← 忘了寫 self
        return "hi"


b = Broken(1)
b.show()'''
O_SELF = "TypeError: Broken.show() takes 0 positional arguments but 1 was given"

C_CLSATTR = '''class Counter:
    total = 0                 # 類別屬性：整個 Counter 家族共用一份

    def __init__(self, name):
        self.name = name      # 實例屬性：每個物件各自一份
        Counter.total += 1


a, b = Counter("a"), Counter("b")
print("a.name =", a.name, " b.name =", b.name)
print("Counter.total =", Counter.total, " a.total =", a.total)

a.total = 99                  # 這行沒有改到類別屬性，而是「新建」了一個實例屬性
print("a.total =", a.total, " Counter.total =", Counter.total, " b.total =", b.total)'''
O_CLSATTR = """a.name = a  b.name = b
Counter.total = 2  a.total = 2
a.total = 99  Counter.total = 2  b.total = 2"""

C_PLAIN = '''class Plain:
    def __init__(self, v):
        self.v = v


p = Plain(7)
print(p)'''
O_PLAIN = "<__main__.Plain object at 0x7f3c9c1d4e50>"

C_STACK = '''class Stack:
    """堆疊 ADT：後進先出。內部用一個 list 存元素（這叫「組合」）。"""

    def __init__(self):
        self._items = []              # has-a：Stack 擁有一個 list

    def push(self, item):
        self._items.append(item)      # list 尾端是堆疊頂端，append/pop 都是 O(1)

    def pop(self):
        return self._items.pop()

    def peek(self):
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def size(self):
        return len(self._items)

    def __len__(self):                # 讓內建的 len() 也能用
        return len(self._items)

    def __str__(self):                # 讓 print() 印得出人看得懂的東西
        return "底 " + " | ".join(map(str, self._items)) + " 頂"


s = Stack()
for c in "abc":
    s.push(c)

print(s)
print("len(s) =", len(s), " s.size() =", s.size())
print("pop ->", s.pop(), " 剩下:", s)'''
O_STACK = """底 a | b | c 頂
len(s) = 3  s.size() = 3
pop -> c  剩下: 底 a | b 頂"""

body = f'''<nav class="float-nav" id="floatNav" aria-label="章節導覽">
  <div class="fn-title">章節導覽</div>
{nav}
  <a href="#top" class="fn-top" title="回到頂端"><span class="fn-num">↑ TOP</span></a>
</nav>

<div class="hero" id="top">
  <div class="hero-grid"></div>
  <svg class="hero-graph" width="300" height="260" viewBox="0 0 300 260">
  <g stroke="#fff" stroke-width="2.5" fill="none" opacity=".85">
    <rect x="90" y="26" width="120" height="52" rx="8"/>
    <line x1="150" y1="78" x2="150" y2="104"/>
    <line x1="60" y1="104" x2="240" y2="104"/>
    <line x1="60" y1="104" x2="60" y2="130"/>
    <line x1="150" y1="104" x2="150" y2="130"/>
    <line x1="240" y1="104" x2="240" y2="130"/>
    <rect x="20" y="130" width="80" height="44" rx="7"/>
    <rect x="110" y="130" width="80" height="44" rx="7"/>
    <rect x="200" y="130" width="80" height="44" rx="7"/>
  </g>
  <g fill="#fff" opacity=".75" font-family="monospace" font-size="12">
    <text x="112" y="57">class</text>
    <text x="43" y="157">obj</text><text x="133" y="157">obj</text><text x="223" y="157">obj</text>
  </g>
</svg>
  <div class="hero-content">
    <div class="chapter-tag">PREREQ P8</div>
    <h1><span class="blue">物件導向</span>（基礎）：資料＋操作打包成一個東西</h1>
    <div class="subtitle">先備知識複習 · 選讀，不列入作業與考試範圍</div>
    <div class="big-formula">class｜物件｜__init__｜self｜屬性｜方法｜__str__｜組合</div>
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
  <h2>一個資料結構，就是一個類別</h2>
  <p>先看本站首頁那段裝飾用的程式碼 —— 它不是隨便挑的：</p>
  {code("""class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()""")}
  <p>這就是這門課的形狀。<strong>資料結構 = 資料（要存什麼）＋ 操作（能對它做什麼）</strong>，而 Python 用來把這兩件事包在一起的工具就是 <code>class</code>。</p>

  <div class="cmp-table-wrap">
  <table class="cmp-table">
    <thead><tr><th>抽象資料型別（ADT）的說法</th><th>Python 的說法</th><th>例子</th></tr></thead>
    <tbody>
      <tr><td>這個結構「存什麼」</td><td>屬性（attribute）</td><td><code>self._items</code></td></tr>
      <tr><td>這個結構「能做什麼」</td><td>方法（method）</td><td><code>push()</code>、<code>pop()</code></td></tr>
      <tr><td>結構的規格（介面）</td><td><code>class</code> 定義</td><td><code>class Stack:</code></td></tr>
      <tr><td>實際被建立出來的一個結構</td><td>物件／實例（object / instance）</td><td><code>s = Stack()</code></td></tr>
    </tbody>
  </table>
  </div>

  <div class="info-box">
    <div class="info-label">💡 這一頁的目標</div>
    <p style="margin-bottom:0;">讀完你要能<strong>從空白檔案寫出一個 <code>Node</code> 和一個 <code>Stack</code></strong>，並且說得出 <code>self</code> 是什麼、<code>__init__</code> 什麼時候被呼叫、為什麼要寫 <code>__str__</code>。這三件事撐起第 03 章之後的每一章。</p>
  </div>

  <div class="warn-box">
    <div class="info-label">📌 本頁定位</div>
    <p style="margin-bottom:0;">這是<strong>選讀的先備知識複習</strong>，不列入作業與考試範圍。但如果 P1–P9 只能挑兩頁讀，請讀 P8 和 <a href="p9_oop_advanced.html">P9</a> —— 第 04 章之後每個資料結構都是一個 <code>class</code>。</p>
  </div>
</section>

<section id="classes">
  <div class="section-number">PART 01 · 類別與實例</div>
  <h2>藍圖與成品 <span class="sec-badge">四個必背詞</span></h2>
  <p><strong>類別（class）是藍圖，物件（object）是照著藍圖蓋出來的東西。</strong>藍圖只有一份，蓋出來的房子可以有很多間，每一間的門牌、住戶各自不同。</p>

  <div class="cmp-table-wrap">
  <table class="cmp-table">
    <thead><tr><th>詞</th><th>是什麼</th><th>在程式裡長什麼樣</th></tr></thead>
    <tbody>
      <tr><td><strong>類別</strong> class</td><td>藍圖／規格</td><td><code>class Node:</code></td></tr>
      <tr><td><strong>物件／實例</strong> object / instance</td><td>照藍圖做出來的一個具體東西</td><td><code>n = Node(93)</code></td></tr>
      <tr><td><strong>屬性</strong> attribute</td><td>物件身上存的資料</td><td><code>n._data</code></td></tr>
      <tr><td><strong>方法</strong> method</td><td>綁在物件上的函數</td><td><code>n.get_data()</code></td></tr>
    </tbody>
  </table>
  </div>

  {card("最小可用的 Node 類別（第 04 章鏈結串列的主角）", C_NODE, O_NODE,
        "三個觀察：① <code>Node(93)</code> 看起來像呼叫函數，其實是<strong>建立一個實例</strong>，會自動去跑 <code>__init__</code>。"
        "② <code>_next</code> 一開始是 <code>&#78;one</code>，代表「後面還沒接東西」。"
        "③ <code>type()</code> 告訴你它是哪個類別的實例。")}

  {hook("第 04 章", "<code>Node</code> 是鏈結串列的基本磚塊。整章都在做同一件事：建立 Node、修改它的 <code>_next</code>、沿著 <code>_next</code> 走訪。看不懂 class，那一章就只能死背。")}
</section>

<section id="init">
  <div class="section-number">PART 02 · 建構式</div>
  <h2><code>__init__</code> 與 <code>self</code>：兩個最容易卡住的地方</h2>

  <h3 style="font-family:'Noto Serif TC',serif;font-size:1.12rem;margin:1.3rem 0 .5rem;color:var(--accent2);"><code>__init__</code> 不是「建立物件」，是「把剛建好的物件初始化」</h3>
  <p>你寫 <code>n = Node(93)</code> 的時候，Python 做兩件事：先配置一個空的物件，然後<strong>自動</strong>呼叫 <code>n.__init__(93)</code> 把它填好。所以 <code>__init__</code> 裡面做的事就是「這個物件一出生要帶著哪些資料」。</p>
  <p>名字前後各兩條底線的方法叫 <strong>dunder method</strong>（double underscore），它們是 Python 跟你的類別溝通的暗號：你不會直接呼叫 <code>__init__</code>，是 Python 在對的時機幫你叫。</p>

  <h3 style="font-family:'Noto Serif TC',serif;font-size:1.12rem;margin:1.3rem 0 .5rem;color:var(--accent2);"><code>self</code> 不是關鍵字，它只是第一個參數</h3>
  <p>方法被呼叫時，Python 會<strong>自動把「是誰呼叫的」塞進第一個參數</strong>。<code>n.get_data()</code> 實際上等同於 <code>Node.get_data(n)</code>。習慣上這個參數命名為 <code>self</code>，但那只是慣例 —— 重點是它一定要存在。</p>

  {card("忘記寫 self 的典型錯誤（值得認得這個訊息）", C_SELF, O_SELF,
        "訊息在說：「你這個方法宣告成不吃參數，可是我傳了一個進去」——那個被傳進去的就是 <code>b</code> 自己。"
        "看到 <em>takes 0 positional arguments but 1 was given</em>，九成是漏了 <code>self</code>。")}

  <div class="quiz-box">
    <div class="quiz-label">隨堂 1 · self 到底是誰</div>
    <p>已知 <code>n = Node(93)</code>，下列哪一句跟 <code>n.get_data()</code> 完全等價？</p>
    <div class="quiz-options" id="qsOptions">
      <div class="quiz-opt" data-correct="false" data-fb="get_data 是定義在類別裡的，不是一個獨立的全域函數，直接這樣呼叫會 &#78;ameError。" onclick="quizCheck('qs', this)"><span class="opt-letter">(A)</span> <code>get_data(n)</code></div>
      <div class="quiz-opt" data-correct="true" data-fb="正確。點號呼叫只是語法糖：Python 會把點號左邊的物件當成第一個參數（也就是 self）傳進去。" onclick="quizCheck('qs', this)"><span class="opt-letter">(B)</span> <code>Node.get_data(n)</code></div>
      <div class="quiz-opt" data-correct="false" data-fb="這樣沒有把 n 傳進去，Python 會抱怨少了一個位置參數。" onclick="quizCheck('qs', this)"><span class="opt-letter">(C)</span> <code>Node.get_data()</code></div>
    </div>
    <div class="quiz-feedback" id="qsFeedback"></div>
  </div>
</section>

<section id="attrs">
  <div class="section-number">PART 03 · 屬性與方法</div>
  <h2>實例屬性、類別屬性，還有 Python 找屬性的順序</h2>
  <p><strong>實例屬性</strong>寫在 <code>__init__</code> 裡、掛在 <code>self</code> 上，每個物件各有一份。<strong>類別屬性</strong>寫在 class 區塊的最外層，整個類別共用一份。</p>

  {card("類別屬性的經典陷阱", C_CLSATTR, O_CLSATTR,
        "看最後一行：<code>a.total = 99</code> <strong>沒有</strong>改到 <code>Counter.total</code>，"
        "它在 <code>a</code> 身上<strong>新建</strong>了一個同名的實例屬性，從此把類別屬性遮住了。"
        "要改共用的那一份，必須寫 <code>Counter.total = 99</code>。")}

  <p>為什麼會這樣？因為 Python 找屬性有固定順序：<strong>先找實例自己，找不到才往類別找，再往父類別找</strong>。下面這個逐步器把這個過程演一次。</p>

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div class="mono" id="lkStage" style="font-size:.9rem;line-height:1.9;min-height:200px;"></div>
        <div class="status-banner" id="lkStatus"><span class="status-icon">›</span><span class="status-text">選一個要查的屬性，按「開始」看 Python 怎麼找。</span></div>
        <div class="controls-bar">
          <button class="btn btn-play" onclick="lkStart('name')">▶ 查 c.name</button>
          <button class="btn btn-play" onclick="lkStart('total')">▶ 查 c.total</button>
          <button class="btn btn-play" onclick="lkStart('missing')">▶ 查 c.missing</button>
          <button class="btn btn-step" onclick="lkPlayer &amp;&amp; lkPlayer.step()">→ 單步</button>
          <button class="btn btn-reset" onclick="lkReset()">⟲ 重設</button>
        </div>
      </div>
    </div>
    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">查找順序 <span class="ic-badge">MRO</span></div>
        <p style="font-size:.88rem;margin-bottom:0;">① 實例自己的 <code>__dict__</code><br>② 類別的 <code>__dict__</code><br>③ 父類別，一路往上到 <code>object</code><br>④ 都沒有 → <code>AttributeError</code></p>
      </div>
      <div class="info-card">
        <div class="ic-title">為什麼要懂 <span class="ic-badge">WHY</span></div>
        <p style="font-size:.88rem;margin-bottom:0;">這個順序解釋了兩件事：類別屬性為什麼會被實例屬性「遮住」，以及 <a href="p9_oop_advanced.html">P9</a> 的<strong>方法覆寫</strong>為什麼有效 —— 子類別的方法先被找到，父類別的就不會被用到。</p>
      </div>
    </div>
  </div>

  {hook("第 03、05 章", "<code>ArrayList</code> 用類別屬性存「預設容量」、用實例屬性存「目前有幾個元素」；<code>Stack</code> 的 <code>_items</code> 則一定要是實例屬性 —— 否則所有 Stack 會共用同一個 list，那就爆了。")}
</section>

<section id="encap">
  <div class="section-number">PART 04 · 封裝</div>
  <h2>底線慣例與 <code>@property</code></h2>
  <p>封裝的意思是：<strong>把內部怎麼存的細節藏起來，只暴露有意義的操作。</strong>使用 <code>Stack</code> 的人只該知道 <code>push</code> / <code>pop</code>，不該去戳 <code>s._items</code>；這樣你之後想把 list 換成鏈結串列，外面的程式碼完全不用改。</p>

  <div class="cmp-table-wrap">
  <table class="cmp-table">
    <thead><tr><th>寫法</th><th>意思</th><th>Python 真的會擋嗎</th></tr></thead>
    <tbody>
      <tr><td><code>self.data</code></td><td>公開，外面可以自由使用</td><td>—</td></tr>
      <tr><td><code>self._data</code></td><td><strong>慣例</strong>上的內部屬性，「請不要從外面碰」</td><td><strong>不會</strong>。純粹是給人看的約定</td></tr>
      <tr><td><code>self.__data</code></td><td>觸發名稱改寫（name mangling），實際變成 <code>_ClassName__data</code></td><td>只是變得比較難碰，仍然碰得到</td></tr>
    </tbody>
  </table>
  </div>

  <p>Python 沒有 <code>private</code> 關鍵字，靠的是「大家都是成年人」的約定。<code>pythonds3</code> 的原始碼大量使用單底線加上 <code>@property</code>：</p>

  {code('''class Node:
    def __init__(self, node_data):
        self._data = node_data
        self._next = None

    @property
    def data(self):            # 讀取：n.data（注意沒有括號）
        return self._data

    @data.setter
    def data(self, new_data):  # 寫入：n.data = 5
        self._data = new_data


n = Node(93)
print(n.data)     # 93     ← 讀起來像屬性，其實跑了一個方法
n.data = 26       #        ← 寫起來像屬性，其實跑了 setter
print(n.data)     # 26''')}

  <div class="info-box green">
    <div class="info-label">✅ <code>@property</code> 的好處</div>
    <p style="margin-bottom:0;">外面用起來像單純的屬性（<code>n.data</code>），但你隨時可以在 getter/setter 裡加檢查、加轉換、加記錄，而<strong>不用改任何呼叫端的程式碼</strong>。這就是封裝的實際價值。</p>
  </div>

  {hook("第 04、09 章", "<code>pythonds3</code> 的 <code>Node</code> 與 <code>BinaryTree</code> 都用 <code>@property</code> 包住 <code>data</code>、<code>next</code>、<code>left_child</code>。看原始碼時看到 <code>@property</code> 不要慌，它就是個加了檢查的屬性。")}
</section>

<section id="strrepr">
  <div class="section-number">PART 05 · 印得出來</div>
  <h2><code>__str__</code> 與 <code>__repr__</code>：讓你的物件說人話</h2>

  {card("沒有 __str__ 的下場", C_PLAIN, O_PLAIN,
        "這串東西只告訴你「它是個 Plain 物件、放在這個記憶體位址」——對 debug 完全沒有幫助。"
        "想像你 <code>print</code> 一棵有 20 個節點的樹，看到 20 行這種東西。")}

  <div class="cmp-table-wrap">
  <table class="cmp-table">
    <thead><tr><th>方法</th><th>誰會呼叫它</th><th>該寫成什麼樣</th></tr></thead>
    <tbody>
      <tr><td><code>__str__</code></td><td><code>str(x)</code>、<code>print(x)</code>、f-string</td><td>給人看的：好讀、簡潔</td></tr>
      <tr><td><code>__repr__</code></td><td>互動式直譯器直接打變數名、<code>repr(x)</code>、<strong>印一個裝著物件的 list 時</strong></td><td>給開發者看的：精確、最好能貼回程式碼重建物件</td></tr>
    </tbody>
  </table>
  </div>

  <div class="info-box">
    <div class="info-label">💡 只想寫一個的話，寫 <code>__repr__</code></div>
    <p style="margin-bottom:0;">因為當 <code>__str__</code> 沒定義時，<code>print()</code> 會退而使用 <code>__repr__</code>；反過來不成立。而且 <code>print(list_of_nodes)</code> 印出的是每個元素的 <strong><code>__repr__</code></strong>，不是 <code>__str__</code> —— 這是很多人第一次覺得「我明明寫了 <code>__str__</code> 為什麼還是亂碼」的原因。</p>
  </div>

  {hook("第 04、09 章", "沒有 <code>__str__</code>，你在 debug 鏈結串列與二元樹時等於瞎子摸象。第 09 章的 <code>BinaryTree.__str__</code> 甚至是遞迴寫的：印自己、再印左右子樹。")}
</section>

<section id="compose">
  <div class="section-number">PART 06 · 組合</div>
  <h2>用現成的東西蓋新的東西 <span class="sec-badge">has-a</span></h2>
  <p>要做一個 <code>Stack</code>，你不需要從零管理記憶體 —— 直接<strong>持有一個 list</strong> 就好。這種「A 擁有一個 B」的關係叫做<strong>組合（composition）</strong>，是資料結構課裡最常見的蓋法。</p>

  {card("完整的 Stack：這一份會在第 05 章反覆出現", C_STACK, O_STACK,
        "重點在 <code>self._items = []</code> 這一行：Stack <strong>不是</strong>一個 list，Stack <strong>有</strong>一個 list。"
        "外面的人只看得到 push/pop/peek，看不到裡面是 list ——"
        "所以你哪天要把它換成鏈結串列，外面一行都不用改。")}

  <div class="quiz-box">
    <div class="quiz-label">隨堂 2 · 選對那一端</div>
    <p>上面的 <code>Stack</code> 把 list 的<strong>尾端</strong>當成堆疊頂端。如果改成把 list 的<strong>開頭</strong>當頂端（<code>insert(0, x)</code> 與 <code>pop(0)</code>），會發生什麼事？</p>
    <div class="quiz-options" id="qcOptions">
      <div class="quiz-opt" data-correct="false" data-fb="結果會一樣正確沒錯，但成本完全不同——這正是本題的重點。" onclick="quizCheck('qc', this)"><span class="opt-letter">(A)</span> 完全一樣，只是寫法不同</div>
      <div class="quiz-opt" data-correct="true" data-fb="正確。在開頭插入或刪除，要把後面所有元素整批搬移，是 O(n)；尾端則是 O(1)。同樣的 ADT、同樣的正確結果，效能差一個數量級——第 02、05 章會詳細分析。" onclick="quizCheck('qc', this)"><span class="opt-letter">(B)</span> 行為一樣正確，但 push／pop 從 $O(1)$ 變成 $O(n)$</div>
      <div class="quiz-opt" data-correct="false" data-fb="不會錯，list 兩端都支援插入與刪除。問題不在對錯，在成本。" onclick="quizCheck('qc', this)"><span class="opt-letter">(C)</span> 會出錯，list 不支援從開頭刪除</div>
    </div>
    <div class="quiz-feedback" id="qcFeedback"></div>
  </div>

  {hook("第 05 章", "<code>Stack</code>、<code>Queue</code>、<code>Deque</code> 三個 ADT 在 pythonds3 裡全部用同一招：持有一個 list，只是選擇從哪一端操作。選錯端就是 O(n)。")}
</section>

<section id="build">
  <div class="section-number">PART 07 · 動手做</div>
  <h2>從空白檔案寫一個 <code>Node</code> 與最小串列</h2>
  <p>讀到這裡，把網頁關掉，開一個空的 notebook，試著不看答案寫出來：</p>

  <div class="info-card">
    <div class="ic-title">練習規格 <span class="ic-badge">TRY IT</span></div>
    <p style="font-size:.9rem;margin-bottom:0;">① 寫一個 <code>Node</code> 類別，建構式吃一個值，存成 <code>_data</code>，並把 <code>_next</code> 設成 <code>&#78;one</code>。<br>
    ② 幫它加上 <code>__repr__</code>，讓 <code>print</code> 一個 Node 的 list 看得懂。<br>
    ③ 寫一個 <code>MiniList</code>，內部只存一個 <code>_head</code>；提供 <code>add(item)</code>（加在最前面）與 <code>__str__</code>（沿著 <code>_next</code> 走一遍，用箭頭串起來）。<br>
    ④ 加入 31、17、93、26 之後，<code>print</code> 出來應該是 <code>26 -&gt; 93 -&gt; 17 -&gt; 31</code>。</p>
  </div>

  {code('''class Node:
    def __init__(self, node_data):
        self._data = node_data
        self._next = None

    def __repr__(self):
        return f"Node({self._data})"


class MiniList:
    def __init__(self):
        self._head = None

    def add(self, item):
        new = Node(item)
        new._next = self._head     # 新節點指向原本的第一個
        self._head = new           # 頭換成新節點

    def __str__(self):
        out, cur = [], self._head
        while cur is not None:
            out.append(str(cur._data))
            cur = cur._next
        return " -> ".join(out)


lst = MiniList()
for v in [31, 17, 93, 26]:
    lst.add(v)
print(lst)                          # 26 -> 93 -> 17 -> 31''')}

  <div class="info-box purple">
    <div class="info-label">🎯 過關標準</div>
    <p style="margin-bottom:0;">如果你能不看上面這段、憑理解把 <code>add</code> 那兩行的順序寫對（先接上舊的頭，再把頭換成新的），你已經準備好進第 04 章了。順序寫反會怎樣？把它跑一次就知道 —— 那個錯誤本身就是最好的教材。</p>
  </div>
</section>

<section id="exercises">
  <div class="section-number">EX · 隨堂練習</div>
  <h2>再兩題確認觀念 <span class="sec-badge">答錯就回上一節</span></h2>

  <div class="quiz-box">
    <div class="quiz-label">EXERCISE 1 · __init__ 的時機</div>
    <p><code>__init__</code> 是什麼時候被呼叫的？</p>
    <div class="quiz-options" id="q1Options">
      <div class="quiz-opt" data-correct="false" data-fb="類別定義被讀到的時候，只是把方法登記起來，並不會執行它們。" onclick="quizCheck('q1', this)"><span class="opt-letter">(A)</span> Python 讀到 <code>class Node:</code> 那一行的時候</div>
      <div class="quiz-opt" data-correct="true" data-fb="正確。每次建立實例（例如 Node(93)）時，Python 先配置物件，然後自動呼叫它的 __init__ 把初始狀態填好。你不會自己去呼叫它。" onclick="quizCheck('q1', this)"><span class="opt-letter">(B)</span> 每次建立一個新實例的時候，Python 自動呼叫</div>
      <div class="quiz-opt" data-correct="false" data-fb="要手動呼叫的是一般方法。dunder 方法的特色就是由 Python 在對的時機替你呼叫。" onclick="quizCheck('q1', this)"><span class="opt-letter">(C)</span> 要自己寫 <code>n.__init__()</code> 才會執行</div>
    </div>
    <div class="quiz-feedback" id="q1Feedback"></div>
  </div>

  <div class="quiz-box">
    <div class="quiz-label">EXERCISE 2 · 印出來的是哪一個</div>
    <p>某個類別同時寫了 <code>__str__</code> 與 <code>__repr__</code>。執行 <code>print([obj1, obj2])</code> 時，會用到哪一個？</p>
    <div class="quiz-options" id="q2Options">
      <div class="quiz-opt" data-correct="false" data-fb="直接 print&#40;obj) 才會用 __str__。但這裡 print 的是一個 list。" onclick="quizCheck('q2', this)"><span class="opt-letter">(A)</span> <code>__str__</code></div>
      <div class="quiz-opt" data-correct="true" data-fb="正確。容器（list、dict、tuple）在印出內容時，對每個元素呼叫的是 __repr__ 而不是 __str__。這就是「我明明寫了 __str__ 卻還是印出亂碼」的典型原因。" onclick="quizCheck('q2', this)"><span class="opt-letter">(B)</span> <code>__repr__</code></div>
      <div class="quiz-opt" data-correct="false" data-fb="不會兩個都用。容器內的元素一律走 __repr__。" onclick="quizCheck('q2', this)"><span class="opt-letter">(C)</span> 兩個都會用到</div>
    </div>
    <div class="quiz-feedback" id="q2Feedback"></div>
  </div>
</section>

<section id="reference">
  <div class="section-number">REFERENCE · 速查表</div>
  <h2>P8 速查表</h2>

  <h3 style="font-family:'Noto Serif TC',serif;font-size:1.12rem;margin:1.2rem 0 .5rem;color:var(--accent2);">語法骨架</h3>
  {code('''class 類別名稱:
    類別屬性 = 值                    # 整個類別共用一份

    def __init__(self, 參數):        # 建立實例時自動呼叫
        self.實例屬性 = 參數          # 每個物件各一份

    def 方法名稱(self, 其他參數):     # 第一個參數一定是 self
        return ...

    def __str__(self):               # print() 會用到
        return "人看得懂的字串"

    @property
    def 唯讀屬性(self):               # 讀起來像屬性，其實是方法
        return self._內部值


物件 = 類別名稱(參數)                 # 建立實例
物件.方法名稱(參數)                   # 呼叫方法''')}

  <h3 style="font-family:'Noto Serif TC',serif;font-size:1.12rem;margin:1.4rem 0 .5rem;color:var(--accent2);">本頁出現的 dunder</h3>
  <div class="cmp-table-wrap">
  <table class="cmp-table">
    <thead><tr><th>dunder</th><th>被什麼觸發</th><th>本站哪裡用到</th></tr></thead>
    <tbody>
      <tr><td class="mono">__init__</td><td>建立實例 <code>Node(93)</code></td><td>幾乎每一章</td></tr>
      <tr><td class="mono">__str__</td><td><code>print(x)</code>、<code>str(x)</code>、f-string</td><td>第 04、05、09 章印出結構</td></tr>
      <tr><td class="mono">__repr__</td><td><code>repr(x)</code>、印出裝著物件的容器</td><td>debug 時</td></tr>
      <tr><td class="mono">__len__</td><td><code>len(x)</code></td><td>第 03、05 章</td></tr>
    </tbody>
  </table>
  </div>
  <p style="font-size:.9rem;color:var(--muted);">更多 dunder（<code>__lt__</code>、<code>__eq__</code>、<code>__getitem__</code>、<code>__iter__</code>…）以及繼承、多型，見 <a href="p9_oop_advanced.html"><strong>P9 · 物件導向（進階）</strong></a>。</p>

  <h3 style="font-family:'Noto Serif TC',serif;font-size:1.12rem;margin:1.4rem 0 .5rem;color:var(--accent2);">延伸閱讀</h3>
  <table class="cmp-table">
    <thead><tr><th>資源</th><th>看什麼</th></tr></thead>
    <tbody>
      <tr><td><a href="https://docs.python.org/zh-tw/3/tutorial/classes.html" target="_blank" rel="noopener">Python 官方教學 · 類別</a></td><td>最權威的說明，含名稱空間與作用域。</td></tr>
      <tr><td><a href="https://github.com/RunestoneInteractive/pythonds/tree/master/_sources/Introduction" target="_blank" rel="noopener">pythonds · Introduction</a></td><td>教科書用 <code>Fraction</code> 與邏輯閘介紹類別，本站<a href="introduction.html">第 01 章</a>有完整互動版。</td></tr>
      <tr><td><a href="https://pythontutor.com/" target="_blank" rel="noopener">Python Tutor</a></td><td>把上面的 <code>MiniList</code> 貼進去，逐步看 <code>_next</code> 怎麼接起來。</td></tr>
    </tbody>
  </table>
</section>

</div>

<footer>
  先備知識 P8 · 物件導向（基礎）· 資料結構 × Python 互動自學網站<br>
  <span style="font-family:'JetBrains Mono',monospace;font-size:.78rem;color:var(--accent3);">Designed for NSYSU · Interactive Python self-study</span>
</footer>
'''

(SP / "body_p8.html").write_text(body)
print("body_p8.html", len(body), "bytes")
