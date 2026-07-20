#!/usr/bin/env python3
"""searching_sorting.html（Python 版）完整自學充實。冪等。頁面已有六排序完整碼；
本輪補：三種搜尋全文、雜湊示範三卡、每個排序的「使用畫面＋逐 pass 實跑輸出」。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib_py import card, ensure_style, insert_end_of_section, run_py

PAGE = Path.home() / "ds-python-selfstudy/searching_sorting.html"
s = PAGE.read_text()
s = ensure_style(s)
PDS = "import sys; sys.path.insert(0, '/home/phonchi/ds_cpp/_python_backup/Slides/pythonds3')\n"

# ---------- 搜尋 ----------
C_SEQ = """def sequential_search(a_list, item):
    pos = 0
    while pos < len(a_list):
        if a_list[pos] == item:
            return True
        pos = pos + 1
    return False

test_list = [54, 26, 93, 17, 77, 31, 44, 55, 20, 65]
print(sequential_search(test_list, 44))
print(sequential_search(test_list, 50))"""

C_BIN = """def binary_search(a_list, item):
    first = 0
    last = len(a_list) - 1
    while first <= last:
        midpoint = (first + last) // 2
        if a_list[midpoint] == item:
            return True
        elif item < a_list[midpoint]:
            last = midpoint - 1
        else:
            first = midpoint + 1
    return False

def binary_search_rec(a_list, item):
    if len(a_list) == 0:
        return False
    midpoint = (len(a_list) - 1) // 2
    if a_list[midpoint] == item:
        return True
    if item < a_list[midpoint]:
        return binary_search_rec(a_list[:midpoint], item)
    return binary_search_rec(a_list[midpoint + 1:], item)

test_list = [17, 20, 26, 31, 44, 54, 55, 65, 77, 93]
print(binary_search(test_list, 44), binary_search(test_list, 50))
print(binary_search_rec(test_list, 44), binary_search_rec(test_list, 50))"""

srch = f'''<h3 id="dx-srch">講義完整實作：三種搜尋的 Python 全文</h3>
{card("講義 07 · sequential_search", C_SEQ, run_py(C_SEQ))}
{card("講義 07 · binary_search：迴圈版與遞迴版", C_BIN, run_py(C_BIN),
note="遞迴版每層都用切片 a_list[:midpoint] <strong>複製</strong>半條串列：好懂，但切片本身是 O(k)，反而毀了 O(log n)。實務上用迴圈版，或改傳索引範圍（first, last）而不是切片。自我檢測區 Q1 的「中點取 (長度-1)//2」講的就是遞迴版。")}'''
s, c1 = insert_end_of_section(s, "prologue", srch, 'id="dx-srch"')

# ---------- 雜湊 ----------
C_HFN = """def remainder_method(item, divisor):
    return item % divisor

def midsquare_method(item, divisor):
    squared = str(item ** 2)
    if len(squared) % 2 != 0:          # 位數補齊，才好取正中間
        squared = "0" + squared
    middle = len(squared) // 2
    mid_digits = int(squared[max(0, middle - 1):middle + 1])
    return mid_digits % divisor

print(f"{'Item':>6}{'Remainder':>11}{'Mid-Square':>12}")
for item in [54, 26, 93, 17]:
    print(f"{item:>6}{remainder_method(item, 11):>11}{midsquare_method(item, 11):>12}")"""

C_PROBE = """items = [54, 26, 93, 17, 77, 31, 44, 55, 20]
hash_table = [None] * 11
for item in items:
    hash_index = item % 11
    while hash_table[hash_index] is not None:   # 碰撞就往下找（線性探查）
        hash_index = (hash_index + 1) % 11
    hash_table[hash_index] = item

for idx, item in enumerate(hash_table):
    print(f"{idx}:{item}", end="  ")
print()"""

C_HT = """from pythonds3.searching import HashTable

h = HashTable(size=11)
h[54], h[26] = "cat",  "dog"
h[93], h[17] = "lion", "tiger"
h[77], h[31] = "bird", "cow"
h[44], h[55] = "goat", "pig"
h[20] = "chicken"

print(h._slots)
print(h._data)
print(h[20], h[17])
h[20] = "duck"           # 同鍵：換值
print(h[20])
print(h[99])             # 不在表裡：None"""

hsh = f'''<h3 id="dx-hash">講義完整範例：從雜湊函數到 Map 的使用畫面</h3>
{card("講義 07 · 兩種雜湊函數對照", C_HFN, run_py(C_HFN),
note="平方取中：54² = 2916，取中間兩位 91，再 91 % 11 = 3。同一批鍵、兩種函數，落點完全不同：雜湊函數的選擇直接決定碰撞多寡。")}
{card("講義 07 · 線性探查的最終快照", C_PROBE, run_py(C_PROBE),
note="值得手算一次：44 想進 0（44 % 11 = 0）但 77 已入住，探查到 1；55 探查到 2；20 想進 9，被一路擋到 3。這串「探查鏈」就是群聚（clustering）的長相。")}
{card("講義 07 · HashTable 類別的 put / get 使用畫面", C_HT, run_py(PDS + C_HT),
note="h[54] = 'cat' 這種語法靠 __setitem__ / __getitem__ 轉接到 put / get。_slots 的排列跟上一張卡完全一致：類別只是把「鍵探查」和「值跟著住進同一格」包起來。put 遇到同鍵是<strong>更新</strong>不是再探查，get 沿著同一條探查鏈找、繞回起點就回 None。")}'''
s, c2 = insert_end_of_section(s, "hashing", hsh, 'id="dx-hash"')

# ---------- 六排序使用畫面（函式全文頁面已有；exec 用 deck 的逐 pass 版跑真輸出）----------
DEF_BUB = """def bubble_sort(a_list):
    for i in range(len(a_list) - 1, 0, -1):
        print(a_list)
        for j in range(i):
            if a_list[j] > a_list[j + 1]:
                a_list[j], a_list[j + 1] = a_list[j + 1], a_list[j]
"""
DEF_SEL = """def selection_sort(a_list):
    n = len(a_list)
    for i in range(n - 1):
        print(a_list)
        min_idx = i
        for j in range(i + 1, n):
            if a_list[j] < a_list[min_idx]:
                min_idx = j
        if min_idx != i:
            a_list[i], a_list[min_idx] = a_list[min_idx], a_list[i]
"""
DEF_INS = """def insertion_sort(a_list):
    for i in range(1, len(a_list)):
        print(a_list)
        cur_val = a_list[i]
        cur_pos = i
        while cur_pos > 0 and a_list[cur_pos - 1] > cur_val:
            a_list[cur_pos] = a_list[cur_pos - 1]
            cur_pos = cur_pos - 1
        a_list[cur_pos] = cur_val
"""
DEF_SHL = """def gap_insertion_sort(a_list, start, gap):
    for i in range(start + gap, len(a_list), gap):
        cur_val = a_list[i]
        cur_pos = i
        while cur_pos >= gap and a_list[cur_pos - gap] > cur_val:
            a_list[cur_pos] = a_list[cur_pos - gap]
            cur_pos = cur_pos - gap
        a_list[cur_pos] = cur_val

def shell_sort(a_list):
    sublist_count = len(a_list) // 2
    while sublist_count > 0:
        for pos_start in range(sublist_count):
            gap_insertion_sort(a_list, pos_start, sublist_count)
        print("After increments of size", sublist_count, "the list is", a_list)
        sublist_count = sublist_count // 2
"""
DEF_MRG = """def merge_sort(a_list):
    print("Splitting", a_list)
    if len(a_list) > 1:
        mid = len(a_list) // 2
        left_half, right_half = a_list[:mid], a_list[mid:]
        merge_sort(left_half)
        merge_sort(right_half)
        i, j, k = 0, 0, 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] <= right_half[j]:
                a_list[k] = left_half[i]; i += 1
            else:
                a_list[k] = right_half[j]; j += 1
            k += 1
        while i < len(left_half):
            a_list[k] = left_half[i]; i += 1; k += 1
        while j < len(right_half):
            a_list[k] = right_half[j]; j += 1; k += 1
    print("Merging", a_list)
"""
DEF_QCK = """def partition(a_list, first, last):
    pivot_val = a_list[first]
    left_mark = first + 1
    right_mark = last
    done = False
    while not done:
        while left_mark <= right_mark and a_list[left_mark] <= pivot_val:
            left_mark = left_mark + 1
        while left_mark <= right_mark and a_list[right_mark] >= pivot_val:
            right_mark = right_mark - 1
        if right_mark < left_mark:
            done = True
        else:
            a_list[left_mark], a_list[right_mark] = a_list[right_mark], a_list[left_mark]
    a_list[first], a_list[right_mark] = a_list[right_mark], a_list[first]
    return right_mark

def quick_sort_helper(a_list, first, last):
    if first < last:
        split = partition(a_list, first, last)
        print(a_list)
        quick_sort_helper(a_list, first, split - 1)
        quick_sort_helper(a_list, split + 1, last)

def quick_sort(a_list):
    quick_sort_helper(a_list, 0, len(a_list) - 1)
"""

SORTS = [
    ("bubble", "dx-bub", "bubble_sort", DEF_BUB, "[4, 14, 5, 21, 29, 12, 16]",
     "每一行是「該 pass 開始前」的內容：最大的值一輪一輪往右浮。最後一行是排序完成的結果。頁面上方的 bubble_sort_short 版本：某一輪完全沒交換就提前收工。"),
    ("selection", "dx-sel", "selection_sort", DEF_SEL, "[11, 7, 12, 14, 19, 1, 6, 18, 8, 20]",
     "跟氣泡排序同樣 O(n²) 次比較，但每輪只交換一次：觀察每行開頭，已排序的前綴一格一格長大。"),
    ("insertion", "dx-ins", "insertion_sort", DEF_INS, "[9, 2, 5, 5, 7, 9, 1]",
     "cur_val 抽出來、比它大的往右挪、找到洞再放回去：注意這裡是「挪動」不是「交換」。重複值 5、9 的相對順序不變：插入排序是穩定排序。"),
    ("shell", "dx-shl", "shell_sort", DEF_SHL, "[5, 16, 20, 12, 3, 8, 9, 17, 19, 7, 11]",
     "gap 從 n//2 一路砍半到 1。gap=1 那一輪就是普通的插入排序，但這時序列已經「幾乎有序」，所以很便宜。"),
    ("merge", "dx-mrg", "merge_sort", DEF_MRG, "[54, 26, 93, 17]",
     "Splitting 一路劈到單元素（基底情況），Merging 從最小的開始兩兩合併回來。最後一行 Merging 就是排序結果。切片複製讓它需要 O(n) 的額外空間。"),
    ("quick", "dx-qck", "quick_sort", DEF_QCK, "[54, 26, 93, 17, 77, 31, 44, 55, 20]",
     "每一行是一次 partition 之後的全貌：第一行 pivot 54 落定（左邊全 ≤ 54、右邊全 ≥ 54），之後輪流處理左右子區段，每行都多一個「就定位」的 pivot。"),
]
results = []
for sec, marker, fname, deff, init, note in SORTS:
    usage = f"""a_list = {init}
{fname}(a_list)
print(a_list)""" if sec != "merge" else f"""a_list = {init}
{fname}(a_list)"""
    out = run_py(deff + "\n" + usage)
    html = card("使用畫面＋逐 pass 實跑輸出", usage, out,
                out_label="輸出（每個 pass 一行）",
                note=f'<span id="{marker}"></span>' + note)
    s, ok = insert_end_of_section(s, sec, html, marker)
    results.append((sec, ok))

PAGE.write_text(s)
print("inserted:", ["srch" if c1 else "", "hash" if c2 else ""], results)
