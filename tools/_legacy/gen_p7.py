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
    ("prologue",  "P00", "讓結果活過程式"),
    ("paths",     "P01", "路徑：pathlib"),
    ("read",      "P02", "讀檔"),
    ("write",     "P03", "寫檔與 JSON"),
    ("net",       "P04", "從網路讀資料"),
    ("errors",    "P05", "例外是什麼"),
    ("raise",     "P06", "raise 與自訂例外"),
    ("exercises", "EX",  "隨堂練習"),
    ("reference", "REF", "速查表"),
]
TOC_NAMES = {
    "prologue": "讓結果活過程式", "paths": "路徑：pathlib", "read": "讀檔：with open",
    "write": "寫檔與 JSON", "net": "從網路讀資料", "errors": "例外是什麼",
    "raise": "raise 與自訂例外", "exercises": "隨堂練習", "reference": "速查表",
}
nav = "\n".join(f'  <a href="#{i}" data-target="{i}"><span class="fn-num">{n}</span><span class="fn-name">{t}</span></a>'
                for i, n, t in NAV)
toc = "\n".join(f'    <a href="#{i}"><span class="toc-num">{n}</span>{TOC_NAMES[i]}</a>' for i, n, _ in NAV)

C_PATH = '''from pathlib import Path

p = Path("data") / "words.txt"      # 用 / 串路徑，Windows 與 macOS 都對

print("路徑物件        :", p)
print("副檔名          :", p.suffix)
print("檔名（不含副檔）:", p.stem)
print("父目錄          :", p.parent)
print("存在嗎          :", p.exists())'''
O_PATH = """路徑物件        : data/words.txt
副檔名          : .txt
檔名（不含副檔）: words
父目錄          : data
存在嗎          : False"""

C_RW = '''from pathlib import Path

Path("data").mkdir(exist_ok=True)             # 沒有就建，有了也不報錯
p = Path("data") / "words.txt"

words = ["FOOL", "POOL", "POLL", "POLE", "PALE", "SALE", "SAGE"]

with open(p, "w", encoding="utf-8") as f:     # "w" 會清空重寫
    for w in words:
        f.write(w + "\\n")                     # write 不會自動換行

with open(p, encoding="utf-8") as f:          # 不寫模式就是唯讀
    lines = [line.strip() for line in f]      # 逐行迭代，不必一次讀進記憶體

print("讀回幾行:", len(lines))
print("前三行  :", lines[:3])'''
O_RW = """讀回幾行: 7
前三行  : ['FOOL', 'POOL', 'POLL']"""

C_ERRS = '''cases = [
    ("開不存在的檔案", lambda: open("no_such_file.txt")),
    ("串列索引超界",   lambda: [1, 2, 3][10]),
    ("字典查無此鍵",   lambda: {"a": 1}["b"]),
    ("字串轉整數失敗", lambda: int("FOOL")),
    ("除以零",         lambda: 1 / 0),
]

for label, fn in cases:
    try:
        fn()
    except Exception as e:
        print(f"{label:8s} -> {type(e).__name__}: {e}")'''
O_ERRS = """開不存在的檔案  -> FileNotFoundError: [Errno 2] No such file or directory: 'no_such_file.txt'
串列索引超界   -> IndexError: list index out of range
字典查無此鍵   -> KeyError: 'b'
字串轉整數失敗  -> ValueError: invalid literal for int() with base 10: 'FOOL'
除以零      -> ZeroDivisionError: division by zero"""

C_TRY = '''def read_count(path):
    try:
        f = open(path, encoding="utf-8")
    except FileNotFoundError:
        print("  except ：檔案不存在，回傳 0")
        return 0
    else:
        print("  else   ：開檔成功才會跑到這裡")
        return len(f.readlines())
    finally:
        print("  finally：不管成功失敗都會跑")


print("存在的檔:", read_count("data/words.txt"))
print("不存在  :", read_count("data/nope.txt"))'''
O_TRY = """  else   ：開檔成功才會跑到這裡
  finally：不管成功失敗都會跑
存在的檔: 7
  except ：檔案不存在，回傳 0
  finally：不管成功失敗都會跑
不存在  : 0"""

C_RAISE = '''class EmptyStackError(Exception):
    """對空堆疊做 pop 時拋出。"""


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
    print("接住了:", type(e).__name__, "-", e)'''
O_RAISE = "接住了: EmptyStackError - 堆疊是空的，沒有東西可以彈出"

body = f'''<nav class="float-nav" id="floatNav" aria-label="章節導覽">
  <div class="fn-title">章節導覽</div>
{nav}
  <a href="#top" class="fn-top" title="回到頂端"><span class="fn-num">↑ TOP</span></a>
</nav>

<div class="hero" id="top">
  <div class="hero-grid"></div>
  <svg class="hero-graph" width="300" height="260" viewBox="0 0 300 260">
  <g stroke="#fff" stroke-width="2.5" fill="none" opacity=".85">
    <path d="M70 40 h110 l40 40 v140 h-150 z"/>
    <path d="M180 40 v40 h40"/>
    <line x1="95" y1="120" x2="200" y2="120"/>
    <line x1="95" y1="146" x2="200" y2="146"/>
    <line x1="95" y1="172" x2="160" y2="172"/>
  </g>
</svg>
  <div class="hero-content">
    <div class="chapter-tag">PREREQ P7</div>
    <h1><span class="green">檔案</span>與<span class="blue">例外</span>：讓結果活過程式</h1>
    <div class="subtitle">先備知識複習 · 選讀，不列入作業與考試範圍</div>
    <div class="big-formula">pathlib｜with open｜json｜urllib｜try / except / else / finally｜raise</div>
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
  <h2>程式結束，變數就消失了</h2>
  <p>你的變數住在記憶體裡，程式一結束就什麼都沒了。要讓資料活過這一次執行，就得寫進檔案；要讓別人的資料進到你的程式，就得從檔案（或網路）讀進來。</p>
  <p>而只要牽涉到「外面的世界」——檔案可能不存在、路徑可能打錯、網路可能斷線——程式就有失敗的可能。<strong>例外處理就是在說「失敗的時候該怎麼辦」</strong>。這兩件事天生綁在一起，所以放同一頁。</p>
  <div class="info-box">
    <div class="info-label">💡 這一頁在資料結構課的位置</div>
    <p style="margin-bottom:0;">第 08 章的字梯問題要<strong>從檔案讀進四千多個英文單字</strong>再建圖；第 05 章對空堆疊 <code>pop</code> 會拋例外；第 06 章遞迴沒收斂會拋 <code>RecursionError</code>。這一頁讓你看到那些訊息時知道發生了什麼事。</p>
  </div>
  <div class="warn-box">
    <div class="info-label">📌 本頁定位</div>
    <p style="margin-bottom:0;">選讀的先備知識複習，不列入作業與考試範圍。第 01 章已經有例外處理的一節，這裡是更完整的版本。</p>
  </div>
</section>

<section id="paths">
  <div class="section-number">PART 01 · 路徑</div>
  <h2><code>pathlib</code>：不要再自己串字串了</h2>
  <p>路徑分隔符在 Windows 是反斜線、在 macOS／Linux 是斜線。自己用字串拼會在換平台時壞掉；<code>pathlib.Path</code> 幫你處理掉這件事。</p>

  {card("Path 的基本操作", C_PATH, O_PATH,
        "<code>Path('data') / 'words.txt'</code> 用除號串路徑，是 <code>__truediv__</code> 這個 dunder 的運算子重載"
        "（見 <a href='p9_oop_advanced.html'>P9</a>）。最後一行是 <code>False</code>，因為這個檔案還沒被建立。")}

  <div class="cmp-table-wrap">
  <table class="cmp-table">
    <thead><tr><th>寫法</th><th>意思</th></tr></thead>
    <tbody>
      <tr><td class="mono">Path("a") / "b" / "c.txt"</td><td>組出 <code>a/b/c.txt</code>，跨平台正確</td></tr>
      <tr><td class="mono">p.exists()</td><td>檔案或目錄存在嗎</td></tr>
      <tr><td class="mono">p.suffix / p.stem / p.name</td><td>副檔名／不含副檔的檔名／完整檔名</td></tr>
      <tr><td class="mono">p.parent</td><td>上一層目錄</td></tr>
      <tr><td class="mono">Path("data").mkdir(exist_ok=True)</td><td>建目錄，已存在也不報錯</td></tr>
      <tr><td class="mono">list(Path(".").glob("*.txt"))</td><td>列出符合樣式的所有檔案</td></tr>
    </tbody>
  </table>
  </div>

  <div class="info-box green">
    <div class="info-label">📍 相對路徑是相對於「執行時的工作目錄」</div>
    <p style="margin-bottom:0;">不是相對於程式檔所在的位置。這是「在我電腦上跑得動，在 Colab 上就找不到檔案」的頭號原因。不確定的時候印一下 <code>Path.cwd()</code> 看看你到底站在哪。</p>
  </div>
</section>

<section id="read">
  <div class="section-number">PART 02 · 讀檔</div>
  <h2><code>with open(...)</code>：開了一定會關</h2>
  <p><code>with</code> 區塊結束時會自動關閉檔案，<strong>即使中間拋出例外也一樣</strong>。這是唯一該用的寫法。</p>

  {card("寫進去再讀回來", C_RW, O_RW,
        "三個重點：① <code>with</code> 保證關檔。② <code>f.write()</code> <strong>不會</strong>自動換行，要自己加。"
        "③ 直接對檔案物件跑 <code>for</code> 迴圈就是逐行讀取——處理大檔時這比 <code>read()</code> 一次吞進記憶體好太多。")}

  <div class="cmp-table-wrap">
  <table class="cmp-table">
    <thead><tr><th>模式</th><th>行為</th><th>檔案不存在時</th></tr></thead>
    <tbody>
      <tr><td class="mono">"r"（預設）</td><td>唯讀</td><td><code>FileNotFoundError</code></td></tr>
      <tr><td class="mono">"w"</td><td>寫入，<strong>先清空原內容</strong></td><td>自動建立</td></tr>
      <tr><td class="mono">"a"</td><td>附加到結尾</td><td>自動建立</td></tr>
      <tr><td class="mono">"x"</td><td>只在檔案不存在時建立</td><td>自動建立；已存在則報錯</td></tr>
    </tbody>
  </table>
  </div>

  <div class="warn-box">
    <div class="info-label">⚠️ <code>"w"</code> 會直接清空整個檔案</div>
    <p style="margin-bottom:0;">而且不會問你。想接著寫請用 <code>"a"</code>。另外處理文字檔時養成習慣加 <code>encoding="utf-8"</code>，否則在 Windows 上讀中文很容易變亂碼。</p>
  </div>

  {hook("第 08 章", "字梯問題（word ladder）要讀一份四千多個五字母單字的檔案，逐行 strip 之後建立 bucket 再建圖。那一整段就是這一節的內容。")}
</section>

<section id="write">
  <div class="section-number">PART 03 · 寫檔與 JSON</div>
  <h2>把結構化資料存下來</h2>
  <p>純文字適合一行一筆的資料。如果你要存的是巢狀的字典與串列（例如一張相鄰串列、一份實驗結果），用 <code>json</code> 最省事。</p>

  {code('''import json
from pathlib import Path

graph = {"FOOL": ["POOL", "FOIL"], "POOL": ["FOOL", "POLL"]}

with open("graph.json", "w", encoding="utf-8") as f:
    json.dump(graph, f, ensure_ascii=False, indent=2)   # 寫出去

with open("graph.json", encoding="utf-8") as f:
    back = json.load(f)                                  # 讀回來

print(back["FOOL"])        # ['POOL', 'FOIL']
print(back == graph)       # True''')}

  <div class="info-box">
    <div class="info-label">💡 四個名字別搞混</div>
    <p style="margin-bottom:0;"><code>json.dump</code> 寫到<strong>檔案</strong>、<code>json.dumps</code> 轉成<strong>字串</strong>（s = string）；<code>json.load</code> 從檔案讀、<code>json.loads</code> 從字串讀。本站的詞彙卡與題庫母檔（<code>data/</code> 底下那些 <code>.json</code>）就是這樣存的。</p>
  </div>
</section>

<section id="net">
  <div class="section-number">PART 04 · 從網路讀</div>
  <h2>資料不在你電腦上的時候 <span class="sec-badge">課程真的會用到</span></h2>
  <p>課程 notebook 用 <code>urllib.request</code> 直接把網路上的字典檔抓下來，這樣在 Colab 上也不用先上傳檔案。</p>

  {code('''import urllib.request

URL = "https://raw.githubusercontent.com/.../words.txt"

with urllib.request.urlopen(URL) as resp:
    text = resp.read().decode("utf-8")      # 拿到的是 bytes，要自己解碼

words = [w.strip() for w in text.splitlines() if w.strip()]
print(len(words), words[:3])''')}

  <div class="info-box green">
    <div class="info-label">✅ 為什麼不直接 open()</div>
    <p style="margin-bottom:0;">因為在 Colab 上你的本機檔案不存在。從網址讀讓同一份 notebook 在任何環境都跑得動——這是很值得養成的習慣。缺點是需要網路，而且對方的檔案可能哪天就搬家了。</p>
  </div>

  {hook("第 08 章", "圖演算法那一章的第一步就是把單字表抓下來。抓不到檔案，後面的 BFS、字梯、最短路徑全部無從開始。")}
</section>

<section id="errors">
  <div class="section-number">PART 05 · 例外</div>
  <h2>例外不是「壞掉」，是「這條路走不通，換你決定怎麼辦」</h2>

  {card("五個你一定會遇到的例外", C_ERRS, O_ERRS,
        "認得例外的<strong>名字</strong>比背細節重要：看到 <code>KeyError</code> 就知道是查了不存在的鍵，"
        "看到 <code>IndexError</code> 就知道是索引超出範圍。這是 debug 最快的捷徑。")}

  <div class="viz-layout">
    <div>
      <div class="viz-panel">
        <div id="exStage" style="min-height:170px;"></div>
        <div class="status-banner" id="exStatus"><span class="status-icon">›</span><span class="status-text">選一種情況，看 try / except / else / finally 各自什麼時候跑。</span></div>
        <div class="controls-bar">
          <button class="btn btn-play" onclick="exStart('ok')">▶ 檔案存在</button>
          <button class="btn btn-play" onclick="exStart('missing')">▶ 檔案不存在</button>
          <button class="btn btn-step" onclick="exPlayer &amp;&amp; exPlayer.step()">→ 單步</button>
          <button class="btn btn-reset" onclick="exReset()">⟲ 重設</button>
        </div>
      </div>
    </div>
    <div class="side-panel">
      <div class="info-card">
        <div class="ic-title">虛擬碼 <span class="ic-badge">CODE</span></div>
        <div class="pseudo-code" id="exCode" style="font-size:.78rem;">{hl('''try:
    f = open(path)
except FileNotFoundError:
    return 0
else:
    return len(f.readlines())
finally:
    close_things()''')}</div>
      </div>
      <div class="info-card">
        <div class="ic-title">四個區塊的分工 <span class="ic-badge">RULE</span></div>
        <p style="font-size:.86rem;margin-bottom:0;"><b>try</b>：可能失敗的那幾行，<strong>只放會失敗的部分</strong>。<br>
        <b>except</b>：失敗時的處理。<br>
        <b>else</b>：<strong>沒有失敗</strong>才跑，放「成功之後才有意義」的程式。<br>
        <b>finally</b>：成功失敗都跑，用來收尾。</p>
      </div>
    </div>
  </div>

  {card("完整的執行順序（真的跑過的輸出）", C_TRY, O_TRY,
        "注意 <code>finally</code> 的位置：<strong>連 <code>return</code> 都攔不住它</strong>，函式回傳之前一定會先跑完 finally。"
        "這就是它用來關檔、釋放資源的原因。")}

  <div class="warn-box">
    <div class="info-label">⚠️ 不要寫裸的 <code>except:</code></div>
    <p style="margin-bottom:0;"><code>except:</code> 或 <code>except Exception:</code> 會把<strong>所有</strong>錯誤一起吞掉，包括你自己打錯字造成的 <code>&#78;ameError</code>。結果就是程式默默給出錯的答案，而你完全不知道。<strong>接住你預期會發生的那一種就好。</strong></p>
  </div>
</section>

<section id="raise">
  <div class="section-number">PART 06 · 主動拋出</div>
  <h2><code>raise</code> 與自訂例外</h2>
  <p>你自己寫的資料結構也該在被誤用時抗議。<code>raise</code> 就是「這個狀況我處理不了，交給呼叫我的人決定」。</p>

  {card("Stack 對空的 pop 抗議", C_RAISE, O_RAISE,
        "自訂例外只要繼承 <code>Exception</code>，連內容都不用寫。好處是呼叫端可以<strong>精準地只接住這一種</strong>，"
        "而不是用一個 except 把所有 bug 一起吞掉。這就是 <a href='p9_oop_advanced.html'>P9</a> 繼承的實際應用。")}

  <div class="info-box purple">
    <div class="info-label">🎯 什麼時候該 raise</div>
    <p style="margin-bottom:0;">當函式<strong>無法完成它承諾的事</strong>時。空堆疊沒有東西可以彈出、除數是零、參數型別根本不對——這些都不該悄悄回傳 <code>&#78;one</code> 假裝沒事，因為那會讓錯誤在很遠的地方才爆出來，難以追查。</p>
  </div>

  {hook("第 05、06 章", "第 05 章的堆疊與佇列在空的時候操作會拋例外；第 06 章遞迴沒有正確收斂時會拋 <code>RecursionError</code>——那不是環境壞掉，是你的基底情況沒寫對。")}
</section>

<section id="exercises">
  <div class="section-number">EX · 隨堂練習</div>
  <h2>兩題確認觀念</h2>

  <div class="quiz-box">
    <div class="quiz-label">EXERCISE 1 · 模式選錯的代價</div>
    <p>你想在既有的紀錄檔後面「再加一行」，結果用了 <code>open(p, "w")</code>。會發生什麼事？</p>
    <div class="quiz-options" id="q1Options">
      <div class="quiz-opt" data-correct="false" data-fb="不會報錯，這正是它危險的地方——它安靜地把你原本的資料全部刪掉了。" onclick="quizCheck('q1', this)"><span class="opt-letter">(A)</span> 會報錯，因為檔案已經存在</div>
      <div class="quiz-opt" data-correct="true" data-fb="正確。&quot;w&quot; 會先清空整個檔案再寫。想附加到結尾要用 &quot;a&quot;。這是不可逆的資料遺失，而且完全不會有警告。" onclick="quizCheck('q1', this)"><span class="opt-letter">(B)</span> 原本的內容全部被清空，只剩新加的那一行</div>
      <div class="quiz-opt" data-correct="false" data-fb="那是 &quot;a&quot; 模式的行為。&quot;w&quot; 是清空重寫。" onclick="quizCheck('q1', this)"><span class="opt-letter">(C)</span> 新的一行會被加在檔案結尾</div>
    </div>
    <div class="quiz-feedback" id="q1Feedback"></div>
  </div>

  <div class="quiz-box">
    <div class="quiz-label">EXERCISE 2 · else 存在的理由</div>
    <p><code>try / except / else</code> 的 <code>else</code> 區塊，跟「直接把那段程式寫在 <code>try</code> 裡面」有什麼差別？</p>
    <div class="quiz-options" id="q2Options">
      <div class="quiz-opt" data-correct="false" data-fb="兩者都能執行，差別不在能不能，在「誰被 try 保護著」。" onclick="quizCheck('q2', this)"><span class="opt-letter">(A)</span> 沒有差別，純粹是風格問題</div>
      <div class="quiz-opt" data-correct="true" data-fb="正確。寫在 try 裡面的話，這段程式自己拋出的同型別例外也會被 except 接住，於是你以為是「開檔失敗」，其實是後面那段出錯。else 讓 try 只保護真正可能失敗的那幾行，錯誤來源才不會被混淆。" onclick="quizCheck('q2', this)"><span class="opt-letter">(B)</span> 寫在 <code>try</code> 裡會讓這段程式的錯誤也被 <code>except</code> 誤接</div>
      <div class="quiz-opt" data-correct="false" data-fb="不對。else 沒有失敗時就會執行，並不是永遠跳過。永遠會跑的是 finally。" onclick="quizCheck('q2', this)"><span class="opt-letter">(C)</span> <code>else</code> 永遠不會被執行</div>
    </div>
    <div class="quiz-feedback" id="q2Feedback"></div>
  </div>
</section>

<section id="reference">
  <div class="section-number">REFERENCE · 速查表</div>
  <h2>P7 速查表</h2>

  <h3 style="font-family:'Noto Serif TC',serif;font-size:1.12rem;margin:1.2rem 0 .5rem;color:var(--accent2);">常見例外一覽</h3>
  <div class="cmp-table-wrap">
  <table class="cmp-table">
    <thead><tr><th>例外</th><th>什麼時候發生</th><th>本站哪裡會遇到</th></tr></thead>
    <tbody>
      <tr><td class="mono">FileNotFoundError</td><td>開啟不存在的檔案</td><td>第 08 章讀字典檔</td></tr>
      <tr><td class="mono">IndexError</td><td>串列索引超出範圍</td><td>第 03、05 章</td></tr>
      <tr><td class="mono">KeyError</td><td>字典查不到那個鍵</td><td>第 07、08 章</td></tr>
      <tr><td class="mono">ValueError</td><td>型別對但值不合理，如 int("abc")</td><td>資料前處理</td></tr>
      <tr><td class="mono">TypeError</td><td>型別根本不對，如物件之間比大小</td><td>第 07、09 章（見 <a href="p9_oop_advanced.html#lt">P9</a>）</td></tr>
      <tr><td class="mono">ZeroDivisionError</td><td>除以零</td><td>平均值、成長率計算</td></tr>
      <tr><td class="mono">RecursionError</td><td>遞迴太深沒有收斂</td><td>第 06 章</td></tr>
      <tr><td class="mono">AttributeError</td><td>物件沒有那個屬性或方法</td><td>忘記 <code>super().__init__()</code> 時</td></tr>
    </tbody>
  </table>
  </div>

  <h3 style="font-family:'Noto Serif TC',serif;font-size:1.12rem;margin:1.4rem 0 .5rem;color:var(--accent2);">語法骨架</h3>
  {code('''from pathlib import Path
import json

p = Path("data") / "words.txt"

with open(p, encoding="utf-8") as f:       # 讀
    lines = [line.strip() for line in f]

with open(p, "a", encoding="utf-8") as f:  # 附加
    f.write("NEW\\n")

with open("out.json", "w", encoding="utf-8") as f:
    json.dump(obj, f, ensure_ascii=False, indent=2)

try:
    risky()
except SpecificError as e:                 # 只接住你預期的那一種
    handle(e)
else:
    only_when_no_error()
finally:
    always_cleanup()''')}

  <h3 style="font-family:'Noto Serif TC',serif;font-size:1.12rem;margin:1.4rem 0 .5rem;color:var(--accent2);">延伸閱讀</h3>
  <table class="cmp-table">
    <thead><tr><th>資源</th><th>看什麼</th></tr></thead>
    <tbody>
      <tr><td><a href="https://docs.python.org/zh-tw/3/tutorial/errors.html" target="_blank" rel="noopener">Python 官方教學 · 錯誤與例外</a></td><td>完整的例外語法與例外階層。</td></tr>
      <tr><td><a href="https://docs.python.org/zh-tw/3/library/pathlib.html" target="_blank" rel="noopener">pathlib 官方文件</a></td><td>Path 的所有方法。</td></tr>
      <tr><td><a href="introduction.html">本站第 01 章</a></td><td>例外處理的互動版簡介。</td></tr>
      <tr><td><a href="graphs.html">本站第 08 章</a></td><td>看讀檔在字梯問題裡實際怎麼用。</td></tr>
    </tbody>
  </table>
</section>

</div>

<footer>
  先備知識 P7 · 檔案與例外 · 資料結構 × Python 互動自學網站<br>
  <span style="font-family:'JetBrains Mono',monospace;font-size:.78rem;color:var(--accent3);">Designed for NSYSU · Interactive Python self-study</span>
</footer>
'''
(SP / "body_p7.html").write_text(body)
print("body_p7.html", len(body), "bytes")
