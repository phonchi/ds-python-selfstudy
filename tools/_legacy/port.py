#!/usr/bin/env python3
"""把 PythonForMath 的六頁移植成本站的先備頁 P1–P6。"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from terms import TERMS, ZH_TW

SP = Path(__file__).resolve().parent
SRC = SP / "PythonForMath"
SITE = Path.home() / "ds-python-selfstudy"

def tw(s):
    for a, b in ZH_TW:
        s = s.replace(a, b)
    return s

# src, 目標檔名, PREREQ 編號, 標題, hero h1, hero subtitle 用的一句話, DS 掛鉤 HTML
PAGES = [
 ("01_python", "p1_python_basics", "P1", "Python 基礎",
  '<span class="blue">Python 基礎</span>：型別、變數與運算式',
  "數值型別、名字與物件的綁定、運算子優先順序，以及三種錯誤的分辨。",
  "<p><b>第 02 章</b>要你估算成本，前提是看得懂運算式；<b>第 07 章</b>的雜湊函數大量使用 <code>%</code> 與 <code>//</code>；"
  "<b>第 06 章</b>的進位制轉換也是整除與取餘的組合。三種錯誤的分辨（語法／語意／執行期）則是整學期 debug 的基本功。</p>"),
 ("02_flow_control", "p2_flow_control", "P2", "流程控制",
  '<span class="blue">流程控制</span>：條件、迴圈與縮排',
  "布林運算式、if / elif / else、while 與 for，以及 Python 用縮排界定區塊的規則。",
  "<p><b>第 07 章</b>二分搜尋的骨架就是一個 <code>while low &lt;= high</code>；六種排序法全部是巢狀 <code>for</code>；"
  "<b>第 08 章</b>的 BFS 是「<code>while</code> 佇列不空」。看不懂迴圈的終止條件，就無法分析複雜度。</p>"),
 ("03_function", "p3_functions", "P3", "函數",
  '<span class="blue">函數</span>：把一段邏輯包起來重複使用',
  "定義與呼叫、引數的各種傳法、回傳值與 None，以及區域與全域範圍。",
  "<p>函數呼叫會在<strong>呼叫堆疊</strong>上開一個堆疊框——這正是 <b>第 06 章</b>遞迴的核心機制。"
  "而「函數」加上綁定的物件就成了「方法」，那是 <a href='p8_oop_basics.html'>P8</a> 與 <b>第 04 章</b>之後每個類別的組成單位。</p>"),
 ("04_lists_tuples", "p4_lists_tuples", "P4", "串列與元組",
  '<span class="blue">串列</span>與<span class="green">元組</span>：第一個容器',
  "索引與切片、可變與不可變、參照與複製，以及串列生成式。",
  "<p>這頁是整個課程成本分析的起點：<b>第 02 章</b>會實測 <code>append</code> 與 <code>pop(0)</code> 差多少；"
  "<b>第 03 章</b>自己動手把 <code>ArrayList</code> 從零蓋出來；<b>第 05 章</b>的 Stack 與 Queue 內部持有的就是一個 list。"
  "「參照 vs 複製」那一節則直接是 <b>第 04 章</b> Node 串接的前置知識。</p>"),
 ("052_dictionaries", "p5_dicts_sets", "P5", "字典與集合",
  '<span class="blue">字典</span>與<span class="green">集合</span>：用鍵找值',
  "鍵值對、get 與 setdefault、字典生成式、memoization，以及集合的成員檢查。",
  "<p><b>第 07 章</b>整章都在解釋「字典為什麼能 $O(1)$ 查到」——答案是雜湊表，而字典就是它的成品。"
  "P08 那一節的費波那契 memoization 正是 <b>第 06 章</b>動態規劃的入門；"
  "<b>第 08 章</b>的相鄰串列、字梯 bucket 也全部用字典表示。</p>"),
 ("05_string", "p6_strings", "P6", "字串操作",
  '<span class="blue">字串</span>操作：不可變的字元序列',
  "索引與切片、跳脫字元、f-string 格式化，以及常用字串方法。",
  "<p><b>第 02 章</b>用 anagram 比較四種解法的成本；<b>第 05 章</b>用 Deque 做回文判斷；"
  "<b>第 06 章</b>的 <code>to_str</code> 把整數轉成任意進位的字串；<b>第 08 章</b>的字梯問題整章都在操作五個字母的單字。</p>"),
]

def convert_quiz(raw, page):
    """p4m QUIZ_DATA -> 本站 questions_zh 格式；複選題改寫成單選。"""
    out = []
    for q in raw:
        item = {"question": tw(q["question"])}
        if q.get("code"):
            item["code"] = q["code"]
        item["answers"] = [{"answer": tw(a["answer"]), "correct": bool(a["correct"]),
                            "feedback": tw(a.get("feedback", ""))} for a in q["answers"]]
        out.append(item)
    return out

def fix_multi(qs, page):
    """把複選題改寫成剛好一個正確答案。"""
    def find(idx_pred):
        return next(i for i, q in enumerate(qs) if idx_pred(q))

    if page == "p1_python_basics":
        q = qs[0]
        q["question"] = "下列哪一項<b>最完整</b>地描述演算法的定義？"
        for a in q["answers"]:
            if a["answer"].startswith("針對可能發生"):
                a["correct"] = False
                a["feedback"] = "這句話沒有錯，但少了兩個關鍵條件：步驟必須明確無歧義，而且必須在有限時間內結束。"
    elif page == "p2_flow_control":
        q = qs[0]
        q["question"] = "下列哪一項<b>不是</b>布林運算式？"
        keep = ["True", "3 == 4", "3 + 4", "3 + 4 == 7"]
        q["answers"] = [a for a in q["answers"] if a["answer"] in keep]
        for a in q["answers"]:
            if a["answer"] == "3 + 4":
                a["correct"] = True
                a["feedback"] = "正確。3 + 4 是算術運算式，結果是整數 7，不是 True 或 False。布林運算式的結果必須是布林值。"
            else:
                a["correct"] = False
                a["feedback"] = f"{a['answer']} 的求值結果是布林值，所以它<b>是</b>布林運算式。"
        q2 = qs[1]
        q2["question"] = "要檢查變數 x 是否介於 0 與 5 之間，下列哪一項是 Python 特有的「連鎖比較」寫法？"
        for a in q2["answers"]:
            if a["answer"] == "x > 0 and x < 5":
                a["correct"] = False
                a["feedback"] = "這個寫法也正確，但它是所有語言都通用的寫法。Python 額外支援連鎖比較，可以直接寫成 0 < x < 5。"
    elif page == "p4_lists_tuples":
        q = qs[-1]
        q["question"] = "下列關於串列與元組的說法，哪一項是<b>錯誤</b>的？"
        drop = "元組的大小可以在建立後改變。"
        q["answers"] = [a for a in q["answers"] if a["answer"] != drop]
        for a in q["answers"]:
            if a["answer"].startswith("元組是可變的"):
                a["correct"] = True
                a["feedback"] = "正確，這句話是錯的。元組是不可變的：建立之後不能修改元素，也不能改變大小。這正是它可以當字典的鍵、而串列不行的原因。"
            else:
                a["correct"] = False
                a["feedback"] = "這句話是對的，所以不是本題要選的答案。"
    for q in qs:
        n = sum(1 for a in q["answers"] if a["correct"])
        assert n == 1, f"{page}: 「{q['question'][:30]}」有 {n} 個正確答案"
    return qs

def convert_cards(raw):
    out = []
    for c in raw:
        front = TERMS.get(c["front"], c["front"])
        out.append({"front": front, "back": tw(c["back"])})
    return out

def transform_html(s, src_name, entry):
    _, dst, num, title, h1, subtitle, dshook = entry

    # 1. title / hero / footer
    s = re.sub(r"<title>.*?</title>", f"<title>{title} — 先備 {num}（Python）</title>", s, count=1, flags=re.S)
    s = re.sub(r'<div class="chapter-tag">[^<]*</div>',
               f'<div class="chapter-tag">PREREQ {num}</div>', s, count=1)
    s = re.sub(r'(<div class="hero-content">.*?)<h1>.*?</h1>', lambda m: m.group(1) + f"<h1>{h1}</h1>",
               s, count=1, flags=re.S)
    s = re.sub(r'(<div class="hero-content">.*?)<div class="subtitle">.*?</div>',
               lambda m: m.group(1) + f'<div class="subtitle">先備知識複習 · 選讀，不列入作業與考試範圍</div>',
               s, count=1, flags=re.S)
    s = re.sub(r"<footer>.*?</footer>",
               f'<footer>\n  先備知識 {num} · {title} · 資料結構 × Python 互動自學網站<br>\n'
               f'  <span style="font-family:\'JetBrains Mono\',monospace;font-size:.78rem;color:var(--accent3);">'
               f'Designed for NSYSU · Interactive Python self-study</span>\n</footer>',
               s, count=1, flags=re.S)

    # 2. 拿掉 p4m 的 quiz / cards 區與舊的 chapter-nav
    s, n = re.subn(r'<section id="quiz">.*?</section>\n', "", s, count=1, flags=re.S)
    assert n == 1, f"{src_name}: quiz section"
    s, n = re.subn(r'<section id="cards">.*?</section>\n', "", s, count=1, flags=re.S)
    assert n == 1, f"{src_name}: cards section"
    s, n = re.subn(r'\n *<div class="chapter-nav">.*?</div>\n', "\n", s, count=1, flags=re.S)
    assert n == 1, f"{src_name}: old chapter-nav"

    # 3. float-nav / TOC 拿掉 QUIZ、CARD（改由 inject_prereq_py 依本站順序補在 REF 之後）
    s = re.sub(r' *<a href="#(?:quiz|cards)" data-target="[^"]*">.*?</a>\n', "", s)
    s = re.sub(r' *<a href="#(?:quiz|cards)"><span class="toc-num">(?:QUIZ|CARD)</span>[^<]*</a>\n', "", s)

    # 4. 尾段 JS：拿掉 buildQuiz / buildFlashcards 定義與資料
    s = re.sub(r"function buildQuiz\(.*?\n\}\n", "", s, count=1, flags=re.S)
    s = re.sub(r"function buildFlashcards\(.*?\n\}\n", "", s, count=1, flags=re.S)
    s = re.sub(r"const QUIZ_DATA = \[.*?\n\];\nbuildQuiz\([^)]*\);\n", "", s, count=1, flags=re.S)
    s = re.sub(r"const CARD_DATA = \[.*?\n\];\nbuildFlashcards\([^)]*\);\n", "", s, count=1, flags=re.S)
    for leftover in ("buildQuiz(", "buildFlashcards(", "QUIZ_DATA", "CARD_DATA"):
        assert leftover not in s, f"{src_name}: 殘留 {leftover}"

    # 5. 在 #reference 結尾補一個「資料結構課哪裡用到」的方框
    hook = (f'\n  <div class="ds-hook"><div class="dh-title">🔗 這一頁在資料結構課哪裡會用到</div>'
            f'{dshook}</div>\n')
    m = re.search(r'<section id="reference">.*?(?=\n</section>)', s, re.S)
    assert m, f"{src_name}: reference section"
    s = s[:m.end()] + hook + s[m.end():]
    return s

def main():
    for entry in PAGES:
        src_name, dst, num, title, *_ = entry
        raw = json.loads((SP / f"raw_{src_name}.json").read_text())
        qs = fix_multi(convert_quiz(raw["quiz"], dst), dst)
        cards = convert_cards(raw["cards"])
        (SITE / f"data/questions_zh/{dst.split('_')[0]}.json").write_text(
            json.dumps(qs, ensure_ascii=False, indent=1) + "\n")
        (SITE / f"data/flashcards_zh/{dst.split('_')[0]}.json").write_text(
            json.dumps(cards, ensure_ascii=False, indent=0) + "\n")
        html = transform_html((SRC / f"{src_name}.html").read_text(), src_name, entry)
        (SITE / f"{dst}.html").write_text(html)
        bad = [c["front"] for c in cards if "（" not in c["front"]]
        print(f"ok {dst}: {len(qs)} 題 / {len(cards)} 卡 / {len(html)} bytes" +
              (f"  ⚠ 缺括號 {bad}" if bad else ""))

main()
