#!/usr/bin/env python3
"""analysis.html（Python 版）完整自學充實。冪等。計時輸出實跑（數字依機器而異，卡上有標註）。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib_py import card, ensure_style, insert_end_of_section, run_py

PAGE = Path.home() / "ds-python-selfstudy/analysis.html"
s = PAGE.read_text()
s = ensure_style(s)

C_SUM = """def sum_of_n(n):
    the_sum = 0
    for i in range(1, n + 1):
        the_sum = the_sum + i
    return the_sum

print(sum_of_n(10))"""

C_FOO = """def foo(tom):
    fred = 0
    for bill in range(1, tom + 1):
        barney = bill
        fred = fred + barney
    return fred

print(foo(10))"""

C_TIME = """import time

def sum_of_n_2(n):
    start = time.time()
    the_sum = 0
    for i in range(1, n + 1):
        the_sum = the_sum + i
    end = time.time()
    return the_sum, end - start

for i in range(3):
    print("Sum is %d required %10.7f seconds" % sum_of_n_2(1_000_000))

def sum_of_n_3(n):          # 等差級數公式：迴圈整個消失
    start = time.time()
    the_sum = (n * (n + 1)) // 2
    end = time.time()
    return the_sum, end - start

print("Sum is %d required %10.7f seconds" % sum_of_n_3(1_000_000))
print("Sum is %d required %10.7f seconds" % sum_of_n_3(100_000_000))"""

pro = f'''<h3 id="dx-pro">講義完整範例：同一題的兩張臉，加上碼錶</h3>
{card("講義 02 · sum_of_n：好讀的版本", C_SUM, run_py(C_SUM))}
{card("講義 02 · foo：一樣的演算法、糟糕的可讀性", C_FOO, run_py(C_FOO),
note="foo 和 sum_of_n 做的事一模一樣、效率也一樣：<strong>可讀性</strong>跟<strong>效率</strong>是兩回事。演算法分析比的是後者：同一個問題，不同「解法」消耗的資源。")}
{card("講義 02 · 用 time.time() 量時間：迴圈版 vs 公式版", C_TIME, run_py(C_TIME), out_label="實跑輸出（秒數依機器而異）",
note="迴圈版加到一百萬要花得出感覺的時間；公式版 n(n+1)/2 不管 n 多大都幾乎是 0 秒：這就是 O(n) 與 O(1) 的差。函式回傳 (總和, 秒數) 這個 tuple，一次帶回兩個值。")}'''
s, c1 = insert_end_of_section(s, "prologue", pro, 'id="dx-pro"')

C_TN = """n = 100
# 從這裡開始數
a = 5
b = 6
c = 10
for i in range(n):
    for j in range(n):
        x = i * i
        y = j * j
        z = i * j
for k in range(n):
    w = a * k + 45
    v = b * b
d = 33"""

bigo = f'''{card("講義 02 · 練習題原始碼：T(n) 逐項數", C_TN, None,
note='<span id="dx-bigo"></span>逐項數：開頭 3 個指定；雙層迴圈本體 3 個指定，各跑 n² 次；單層迴圈 2 個指定，跑 n 次；收尾 1 個。T(n) = 3 + 3n² + 2n + 1，只留主導項就是 <strong>O(n²)</strong>。這題是講義的自我檢測題，先自己數完再看這段解說。')}'''
s, c2 = insert_end_of_section(s, "bigo", bigo, 'id="dx-bigo"')

C_ANA1 = """def anagram_solution_1(s1, s2):
    still_ok = True
    if len(s1) != len(s2):
        still_ok = False
    a_list = list(s2)
    pos_1 = 0
    while pos_1 < len(s1) and still_ok:
        pos_2 = 0
        found = False
        while pos_2 < len(a_list) and not found:
            if s1[pos_1] == a_list[pos_2]:
                found = True
            else:
                pos_2 = pos_2 + 1
        if found:
            del a_list[pos_2]     # 劃掉配對到的字元
        else:
            still_ok = False
        pos_1 = pos_1 + 1
    return still_ok

print(anagram_solution_1("apple", "pleap"))
print(anagram_solution_1("abcd", "dcba"))
print(anagram_solution_1("abcd", "dcda"))"""

ana = f'''{card("講義 02 · 解法 1 Checking Off 的完整程式", C_ANA1, run_py(C_ANA1),
note='<span id="dx-ana"></span>對 s1 的每個字元，去 s2 的副本裡線性找、找到就 del 劃掉：外層 n 次、內層平均 n/2 次，O(n²)。注意一定要 list(s2) 複製一份：字串本身不可變，劃不了。')}'''
s, c3 = insert_end_of_section(s, "anagram", ana, 'id="dx-ana"')

C_LISTS = """from timeit import Timer

def test1():
    l = []
    for i in range(1000):
        l = l + [i]      # 串接：每次都造新串列

def test2():
    l = []
    for i in range(1000):
        l.append(i)

def test3():
    l = [i for i in range(1000)]

def test4():
    l = list(range(1000))

for name, label in [("test1", "concatenation"), ("test2", "appending"),
                    ("test3", "list comprehension"), ("test4", "list range")]:
    t = Timer(f"{name}()", f"from __main__ import {name}")
    print(f"{label:<20}{t.timeit(number=1000):8.2f} seconds")"""

C_POP = """from timeit import Timer

pop_zero = Timer("x.pop(0)", "from __main__ import x")
pop_end = Timer("x.pop()", "from __main__ import x")
print(f"{'n':10s}{'pop(0)':>15s}{'pop()':>15s}")
for i in range(1_000_000, 4_000_001, 1_000_000):
    x = list(range(i))
    pop_zero_t = pop_zero.timeit(number=1000)
    x = list(range(i))
    pop_end_t = pop_end.timeit(number=1000)
    print(f"{i:<10d}{pop_zero_t:>15.5f}{pop_end_t:>15.5f}")"""

lst = f'''<h3 id="dx-lst">講義完整範例：把四種寫法真的量一次</h3>
{card("講義 02 · 四種填滿 list 的方式（timeit）", C_LISTS, run_py(C_LISTS), out_label="實跑輸出（秒數依機器而異，看量級）",
note="串接版每一圈都複製整條串列，慢一個量級以上。timeit 的套路：Timer(要量的敘述, 準備工作)，timeit(number=N) 跑 N 次回傳總秒數。")}
{card("講義 02 · pop(0) vs pop()：n 變大會怎樣", C_POP, run_py(C_POP), out_label="實跑輸出（秒數依機器而異，看走勢）",
note="重點在<strong>走勢</strong>：n 翻倍，pop(0) 的時間跟著翻倍（O(n)：整條往前搬）；pop() 文風不動（O(1)：從尾端拿）。這就是「量測驗證 Big-O」的標準做法。")}'''
s, c4 = insert_end_of_section(s, "lists", lst, 'id="dx-lst"')

C_DICT = """import timeit
import random

print(f"{'n':10s}{'list':>10s}{'dict':>10s}")
for i in range(200_000, 1_000_001, 200_000):
    t = timeit.Timer(f"random.randrange({i}) in x",
                     "from __main__ import random, x")
    x = list(range(i))
    lst_time = t.timeit(number=1000)
    x = {j: None for j in range(i)}
    dict_time = t.timeit(number=1000)
    print(f"{i:<10,}{lst_time:>10.3f}{dict_time:>10.3f}")"""

hsh = f'''<h3 id="dx-hash">講義完整範例：in 的兩個世界</h3>
{card("講義 02 · list 線性掃描 vs dict 雜湊", C_DICT, run_py(C_DICT), out_label="實跑輸出（秒數依機器而異，看走勢）",
note="同一個 in 運算子，底層是兩個世界：list 逐格比對，n 翻倍時間翻倍；dict 雜湊直達，n 翻五倍也不動。代價在搜尋與排序一章的雜湊節會算清楚：空間、雜湊函數品質、碰撞。")}'''
s, c5 = insert_end_of_section(s, "hash", hsh, 'id="dx-hash"')

PAGE.write_text(s)
print("inserted:", [n for n, ok in zip("pro bigo ana lists hash".split(), [c1, c2, c3, c4, c5]) if ok])
