#!/usr/bin/env python3
"""linear_structures.html（Python 版）完整自學充實。冪等。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib_py import card, ensure_style, insert_end_of_section, run_py

PAGE = Path.home() / "ds-python-selfstudy/linear_structures.html"
s = PAGE.read_text()
s = ensure_style(s)
PDS = "import sys; sys.path.insert(0, '/home/phonchi/ds_cpp/_python_backup/Slides/pythonds3')\n"

C_BASE = """from pythonds3.basic import Stack

def divide_by_2(decimal_num):
    rem_stack = Stack()
    while decimal_num > 0:
        rem = decimal_num % 2
        rem_stack.push(rem)
        decimal_num = decimal_num // 2
    bin_string = ""
    while not rem_stack.is_empty():
        bin_string = bin_string + str(rem_stack.pop())
    return bin_string

def base_converter(decimal_num, base):
    digits = "0123456789ABCDEF"
    rem_stack = Stack()
    while decimal_num > 0:
        rem_stack.push(decimal_num % base)
        decimal_num = decimal_num // base
    new_string = ""
    while not rem_stack.is_empty():
        new_string = new_string + digits[rem_stack.pop()]
    return new_string

print(divide_by_2(42), divide_by_2(31))
print(base_converter(25, 2), base_converter(25, 16))"""

base = f'''<h3 id="dx-base">講義完整實作：從虛擬碼到 Python</h3>
{card("講義 05 · divide_by_2 與萬用 base_converter", C_BASE, run_py(PDS + C_BASE),
note="兩個函式的骨架一模一樣：餘數進 stack、商繼續 //、最後把 stack 倒出來。base_converter 只多了一張 digits 對照表，base 16 的餘數 10~15 才印得出 A~F。注意除法一定要用 //：/ 會給你 float。")}'''
s, c1 = insert_end_of_section(s, "base", base, 'id="dx-base"')

C_I2P = """from pythonds3.basic import Stack

def infix_to_postfix(infix_expr):
    prec = {"*": 3, "/": 3, "+": 2, "-": 2, "(": 1}
    op_stack = Stack()
    postfix_list = []
    token_list = infix_expr.split()

    for token in token_list:
        if token.isalnum():
            postfix_list.append(token)          # 運算元直接輸出
        elif token == '(':
            op_stack.push(token)
        elif token == ')':
            while (not op_stack.is_empty()) and op_stack.peek() != '(':
                postfix_list.append(op_stack.pop())
            op_stack.pop()                      # 丟掉那個 '('
        else:
            # 優先級 >= 自己的都先請出來
            while (not op_stack.is_empty()) and (prec[op_stack.peek()] >= prec[token]):
                postfix_list.append(op_stack.pop())
            op_stack.push(token)

    while not op_stack.is_empty():
        postfix_list.append(op_stack.pop())
    return ' '.join(postfix_list)

print(infix_to_postfix("A * B + C * D"))
print(infix_to_postfix("( A + B ) * C - ( D - E ) * ( F + G )"))"""

C_PEVAL = """from pythonds3.basic import Stack

def do_math(op, op1, op2):
    if op == "*":
        return op1 * op2
    elif op == "/":
        return op1 / op2
    elif op == "+":
        return op1 + op2
    else:
        return op1 - op2

def postfix_eval(postfix_expr):
    operand_stack = Stack()
    for token in postfix_expr.split():
        if token in "0123456789":
            operand_stack.push(int(token))
        else:
            operand2 = operand_stack.pop()   # 先彈出的是右運算元！
            operand1 = operand_stack.pop()
            operand_stack.push(do_math(token, operand1, operand2))
    return operand_stack.pop()

print(postfix_eval("7 8 + 3 2 + /"))"""

infix = f'''<h3 id="dx-infix">講義完整實作：轉換器與求值器的 Python 全文</h3>
{card("講義 05 · infix_to_postfix 完整程式", C_I2P, run_py(PDS + C_I2P),
note="prec 表把「(」設成最低的 1 是關鍵巧思：左括號躺在 stack 裡時，誰都「贏不過」它，自然不會被提前彈出。token 之間要有空白（程式用 split() 切）。第二條把五組括號全部「編譯」掉了：後序完全不需要括號。")}
<div class="deck-extra">
  <div class="dx-label">講義 05 · A * B + C * D 逐 token 追蹤</div>
  <table style="width:100%;border-collapse:collapse;font-size:.86rem;font-family:'JetBrains Mono',monospace;">
    <tr style="border-bottom:2px solid var(--card-border);"><th style="text-align:left;padding:.35rem;">token</th><th style="text-align:left;">op_stack（頂在右）</th><th style="text-align:left;">輸出串</th></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.35rem;">A</td><td></td><td>A</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.35rem;">*</td><td>*</td><td>A</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.35rem;">B</td><td>*</td><td>A B</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.35rem;">+</td><td>+&nbsp;&nbsp;<span style="color:var(--muted)">← * 優先級較高，先彈出</span></td><td>A B *</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.35rem;">C</td><td>+</td><td>A B * C</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.35rem;">*</td><td>+ *&nbsp;&nbsp;<span style="color:var(--muted)">← * 比 + 高，疊上去</span></td><td>A B * C</td></tr>
    <tr style="border-bottom:1px solid var(--card-border);"><td style="padding:.35rem;">D</td><td>+ *</td><td>A B * C D</td></tr>
    <tr><td style="padding:.35rem;">收尾</td><td><span style="color:var(--muted)">全部倒出</span></td><td>A B * C D * +</td></tr>
  </table>
</div>
{card("講義 05 · postfix_eval 完整程式", C_PEVAL, run_py(PDS + C_PEVAL),
note="彈出順序是天大的事：<strong>先彈出的是 operand2（右運算元）</strong>。加法乘法看不出差別，除法減法一交換就錯：7 8 + 3 2 + / 是 15 ÷ 5 = 3.0，弄反就變 0.333…。輸出是 3.0 不是 3：do_math 用的 / 是真除法。")}
{card("講義 05 · 課後練習：讓 ^ 右結合", """def infix_to_postfix(infix_expr):
    # 你的程式碼：加入次方運算子 ^（優先級最高、右結合）
    # 提示：右結合代表「同優先級不彈出」，
    #       prec[op_stack.peek()] >= prec[token] 的 >= 要對 ^ 改成 >
    return ' '.join(postfix_list)

print(infix_to_postfix("5 * 3 ^ ( 4 - 2 )"))""",
"5 3 4 2 - ^ *", out_label="完成後的預期輸出",
note="右結合是指 2 ^ 3 ^ 2 = 2 ^ (3 ^ 2) = 512，不是 (2 ^ 3) ^ 2 = 64。只改優先級不夠，還得改「同級要不要彈」的判斷。")}'''
s, c2 = insert_end_of_section(s, "infix", infix, 'id="dx-infix"')

C_PAL = """from pythonds3.basic import Deque

def pal_checker(a_string):
    char_deque = Deque()
    for ch in a_string:
        char_deque.add_rear(ch)          # 全部從尾端進
    while char_deque.size() > 1:
        first = char_deque.remove_front()
        last = char_deque.remove_rear()
        if first != last:
            return False
    return True

print(pal_checker("lsdkjfskf"))
print(pal_checker("radar"))"""

dq = f'''{card("講義 05 · pal_checker 的 Python 全文", C_PAL, run_py(PDS + C_PAL),
note='<span id="dx-dq"></span>while 條件是 size() &gt; 1 而不是 not is_empty()：剩一個字元（奇數長度的中點）不用比，它自己跟自己一定相等。兩端各取一個、兩邊往中間夾，deque 兩端 O(1) 的能力在這裡剛好用滿。')}'''
s, c3 = insert_end_of_section(s, "deque", dq, 'id="dx-dq"')

PAGE.write_text(s)
print("inserted:", [n for n, ok in zip("base infix deque".split(), [c1, c2, c3]) if ok])
