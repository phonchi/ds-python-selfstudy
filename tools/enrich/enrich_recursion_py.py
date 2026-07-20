#!/usr/bin/env python3
"""recursion.html（Python 版）完整自學充實。冪等。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib_py import card, ensure_style, insert_end_of_section, run_py

PAGE = Path.home() / "ds-python-selfstudy/recursion.html"
s = PAGE.read_text()
s = ensure_style(s)
PDS = "import sys; sys.path.insert(0, '/home/phonchi/ds_cpp/_python_backup/Slides/pythonds3')\n"

C_STK = """from pythonds3.basic import Stack

def to_str(n, base):
    r_stack = Stack()
    convert_string = "0123456789ABCDEF"
    while n > 0:
        r_stack.push(convert_string[n % base])
        n = n // base
    res = ""
    while not r_stack.is_empty():
        res = res + str(r_stack.pop())
    return res

print(to_str(1453, 16))"""

C_DEPTH = """import inspect

def to_str(n, base):
    print(f"  depth={len(inspect.stack())}, n={n}")
    if n < base:
        return "0123456789ABCDEF"[n]
    return to_str(n // base, base) + "0123456789ABCDEF"[n % base]

print(to_str(10, 2))"""

fr = f'''<h3 id="dx-fr">講義完整範例：用 stack 模擬遞迴、用 inspect 看見遞迴</h3>
{card("講義 06 · 遞迴拿掉、換成自己管理的 stack", C_STK, run_py(PDS + C_STK),
note="這版沒有遞迴：自己開一個 Stack 存餘數字元、最後倒出來。它證明了一件事：<strong>遞迴版其實是把同一個 stack 藏進了「呼叫堆疊」</strong>，每一層呼叫的區域變數就是一格 stack frame。")}
{card("講義 06 · 用 inspect.stack() 印出深度", C_DEPTH, run_py(C_DEPTH),
note="inspect.stack() 回傳目前的呼叫堆疊：n 每 // 一次 2 就多一層 frame，深度一路加一。最深那層（n=1）先回傳「1」，然後一路「回程」把餘數黏在後面，1010 是回程時由左往右組出來的。")}'''
s, c1 = insert_end_of_section(s, "frames", fr, 'id="dx-fr"')

C_HANOI = """def move_tower(height, from_pole, to_pole, with_pole):
    if height >= 1:
        move_tower(height - 1, from_pole, with_pole, to_pole)
        move_disk(from_pole, to_pole)
        move_tower(height - 1, with_pole, to_pole, from_pole)

def move_disk(from_p, to_p):
    print("moving disk from", from_p, "to", to_p)

move_tower(3, "A", "B", "C")"""

hn = f'''{card("講義 06 · move_tower 完整程式與 3 層塔的輸出", C_HANOI, run_py(C_HANOI),
note='<span id="dx-hn"></span>7 行輸出 = 2³ − 1 步，跟理論下限一模一樣。注意基底情況是「height &lt; 1 什麼都不做」：它藏在 if 的反面，這種「隱形 base case」是遞迴的常見寫法。拿上面的互動動畫對照，每一行輸出對應一次圓盤移動。')}'''
s, c2 = insert_end_of_section(s, "hanoi", hn, 'id="dx-hn"')

C_MAZE = """def search_from(maze, row, column):
    # 基底情況們：
    if maze[row][column] == OBSTACLE:          # 1. 撞牆
        return False
    if maze[row][column] in [TRIED, DEAD_END]: # 2. 走過的格子
        return False
    if maze.is_exit(row, column):              # 3. 找到出口！
        maze.update_position(row, column, PART_OF_PATH)
        return True
    maze.update_position(row, column, TRIED)

    # 短路串接：北、南、西、東，找到一條就收工
    found = (
        search_from(maze, row - 1, column)
        or search_from(maze, row + 1, column)
        or search_from(maze, row, column - 1)
        or search_from(maze, row, column + 1)
    )
    if found:
        maze.update_position(row, column, PART_OF_PATH)
    else:
        maze.update_position(row, column, DEAD_END)
    return found"""

mz = f'''{card("講義 06 · search_from 的完整回溯邏輯", C_MAZE, None,
note='<span id="dx-mz"></span>or 的<strong>短路特性</strong>就是回溯引擎：往北找到出路，南西東連試都不試；四個方向全 False 才標成死路。三個基底情況缺一不可：少了「走過的格子」那條，遞迴會在兩格之間永遠彈跳。講義的完整版把迷宮畫在 turtle 視窗上，跑起來能看到 TRIED 與 DEAD_END 一格格擴散。')}'''
s, c3 = insert_end_of_section(s, "maze", mz, 'id="dx-mz"')

PAGE.write_text(s)
print("inserted:", [n for n, ok in zip("frames hanoi maze".split(), [c1, c2, c3]) if ok])
