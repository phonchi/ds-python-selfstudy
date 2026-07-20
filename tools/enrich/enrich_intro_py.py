#!/usr/bin/env python3
"""introduction.html（Python 版）完整自學充實。冪等。輸出以 run_py 實跑取得。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib_py import card, ensure_style, insert_end_of_section, run_py

PAGE = Path.home() / "ds-python-selfstudy/introduction.html"
s = PAGE.read_text()
s = ensure_style(s)

C_ARITH = """print(2 + 3 * 4)
print((2 + 3) * 4)
print(2 ** 10)
print(6 / 3)      # / 是真除法：結果一律 float
print(7 / 3)
print(7 // 3)     # // 才是整數除法（往下取整）
print(7 % 3)
print(2 ** 100)   # 整數任意精度：一位都不少"""

C_CMP = """print(5 == 10)
print(10 > 5)
print((5 >= 1) and (5 <= 10))
print((1 < 5) or (10 < 1))
print(1 < 5 < 10)   # 連鎖比較：Python 真的懂數學課的寫法"""

C_SUM = """the_sum = 0
print(the_sum)

the_sum = the_sum + 1
print(the_sum)

the_sum = True   # 同一個名字改綁到 bool 物件
print(the_sum)"""

types_html = f'''<h3 id="dx-types">講義完整範例：把運算子親手跑一遍</h3>
<p>下面三段是講義 01 的原始示範，值得抄進直譯器跑一次。第一段的重點是 <code>/</code> 是<strong>真除法</strong>：
就算兩邊都是整數，結果也是 float；要整數除法得用 <code>//</code>。</p>
{card("講義 01 · 算術運算子與兩種除法", C_ARITH, run_py(C_ARITH),
note="最後一行值得多看一眼：2<sup>100</sup> 每一位都是精確的。Python 的 int 是任意精度整數，沒有溢位這回事，代價是大數運算比固定寬度整數慢。")}
{card("講義 01 · 比較運算子與連鎖比較", C_CMP, run_py(C_CMP),
note="1 &lt; 5 &lt; 10 在 Python 是真正的「數學課寫法」：等價於 (1 &lt; 5) and (5 &lt; 10)。這是 Python 的貼心設計，別的語言多半不是這個意思。")}
{card("講義 01 · 名字可以改綁任何物件", C_SUM, run_py(C_SUM),
note="the_sum 先綁 int、後綁 bool，完全合法：Python 的變數是「名字」，型別跟著<strong>物件</strong>走、不跟著名字走。方便，但也表示打錯字綁錯東西時，直譯器不會攔你。")}'''
s, c1 = insert_end_of_section(s, "types", types_html, 'id="dx-types"')

C_LIST = """my_list = [1024, 3, True, 6.5]
my_list.append(False)
print(my_list)
my_list.insert(2, 4.5)
print(my_list)
print(my_list.pop())     # 不給索引：拿走最後一個（會回傳！）
print(my_list)
print(my_list.pop(1))
print(my_list)"""

C_LIST2 = """my_list = [1024, 3, 4.5, 6.5]
my_list.sort()
print(my_list)
my_list.reverse()
print(my_list)
print(my_list.count(6.5))
print(my_list.index(4.5))
my_list.remove(6.5)      # 按值移除
print(my_list)
del my_list[0]           # 按索引刪除
print(my_list)"""

C_STR = """my_name = "David"
print(my_name[3])
print(my_name * 2)        # 重複
print(len(my_name))
print(my_name.upper())
print(my_name.center(10))
print(my_name.find("v"))
print(my_name.split("v"))"""

C_TUP = """my_tuple = (2, True, 4.96)
print(my_tuple)
print(len(my_tuple))
print(my_tuple[0])
print(my_tuple[0:2])

my_tuple[1] = False   # tuple 不可變：這行會爆"""

C_SET = """my_set = {3, 6, "cat", 4.5, False}
your_set = {99, 3, 100}
print(my_set.union(your_set))         # 也可寫 my_set | your_set
print(my_set.intersection(your_set))  # my_set & your_set
print(my_set.difference(your_set))    # my_set - your_set
print({3, 100}.issubset(your_set))    # {3, 100} <= your_set

my_set.add("house")
my_set.remove(4.5)
print(my_set)"""

C_DICT = """phone_ext = {"david": 1410, "brad": 1137, "roman": 1171}
phone_ext["kent"] = 2001              # 加新配對
print(list(phone_ext.keys()))
print(list(phone_ext.values()))
print(list(phone_ext.items()))
print(phone_ext.get("alice"))              # 不存在：回 None、不爆
print(phone_ext.get("alice", "NO ENTRY"))  # 給預設值
print(phone_ext["alice"])                  # [] 就沒這麼客氣了"""

coll_html = f'''<h3 id="dx-coll">講義完整範例：五種容器逐一跑過</h3>
<p>表格看熟之後，把講義的示範程式親手跑一遍，輸出先用腦袋預測再對答案。</p>
{card("講義 01 · list：增刪改", C_LIST, run_py(C_LIST),
note="list 什麼型別都能混裝（1024、True、6.5 同住一屋）。pop() 會<strong>回傳</strong>被拿走的元素，這點跟很多語言不同：取值和移除一步完成。")}
{card("講義 01 · list 的整理術：sort、reverse、count、index", C_LIST2, run_py(C_LIST2),
note="sort() 是就地排序、回傳 None：寫 my_list = my_list.sort() 是經典錯誤，會把串列弄丟。remove 按值、del 按索引，兩條路分清楚。")}
{card("講義 01 · string 的常用操作", C_STR, run_py(C_STR),
note="字串是<strong>不可變</strong>的：upper()、center() 都回傳新字串，原字串動也不動。split 回傳 list，是文字處理的萬用刀。")}
{card("講義 01 · tuple：不可變的代價與保障", C_TUP, run_py(C_TUP), out_label="輸出（最後一行故意爆）",
note="tuple 幾乎就是「鎖起來的 list」：能索引、能切片、能重複，但不能改。最後一行的 TypeError 是保障：確定不會被改的資料，才能當 dict 的鍵、才容易被多處安心共用。")}
{card("講義 01 · set：去重、查成員、集合運算", C_SET, run_py(C_SET),
note="集合運算有兩套寫法：方法名（union/intersection/difference/issubset）和運算子（| &amp; - &lt;=），效果相同。注意 set 印出來的順序不固定：它本來就是無序集合。")}
{card("講義 01 · dict：鍵值對、走訪、安全查詢", C_DICT, run_py(C_DICT), out_label="輸出（最後一行故意爆）",
note="get() 是安全查詢：查無此鍵回 None 或你給的預設值；[] 查無此鍵直接 KeyError。純查詢用 get，確定存在才用 []。")}'''
s, c2 = insert_end_of_section(s, "collections", coll_html, 'id="dx-coll"')

C_FSTR = """price = 24
item = "banana"
print(f"The {item:10} costs {price:10.2f} cents")
print(f"The {item:<10} costs {price:<10.2f} cents")
print(f"The {item:^10} costs {price:^10.2f} cents")
print(f"The {item:>10} costs {price:>10.2f} cents")
print(f"The {item:>10} costs {price:>010.2f} cents")
itemdict = {"item": "banana", "price": 24}
print(f"Item:{itemdict['item']:.>10}\\n" +
    f"Price:{'$':.>4}{itemdict['price']:5.2f}")"""

C_OLDFMT = """price = 24
item = "banana"
print("The %s costs %d cents" % (item, price))          # 格式化運算子（老）
print("The {} costs {} cents".format(item, price))      # str.format（中生代）
print(f"The {item} costs {price} cents")                 # f-string（現役）"""

io_html = f'''<h3 id="dx-io">講義完整範例：輸入與格式化輸出</h3>
{card("講義 01 · input 永遠給你字串", """s_radius = input("Please enter the radius of the circle ")
print(s_radius)
radius = float(s_radius)   # 要算數，得自己轉型
print(radius)
diameter = 2 * radius
print(diameter)""",
"Please enter the radius of the circle 4.5\\n4.5\\n4.5\\n9.0", out_label="示範執行（輸入 4.5）",
note="input() 回傳的<strong>一律是字串</strong>：s_radius 印出來像數字，其實是「'4.5'」。忘了 float() 轉型，2 * s_radius 會得到「'4.54.5'」（字串重複），這是新手第一大坑。")}
{card("講義 01 · f-string 的對齊全家餐", C_FSTR, run_py(C_FSTR),
note="冒號後面是格式規格：寬度 10、&lt; 靠左、^ 置中、&gt; 靠右、010.2f 補零、.&gt;10 用點填滿。花括號裡直接放運算式（連 dict 取值都行）是 f-string 最好用的地方。")}
{card("講義 01 · 三代格式化寫法同場", C_OLDFMT, run_py(C_OLDFMT),
note="% 運算子和 .format() 在舊程式碼裡到處都是，讀得懂就好；自己寫一律用 f-string：短、直觀、錯誤訊息清楚。")}'''
s, c3 = insert_end_of_section(s, "io", io_html, 'id="dx-io"')

C_NEST = """word_list = ["cat", "dog", "rabbit"]
letter_list = []
for a_word in word_list:
    for a_letter in a_word:
        letter_list.append(a_letter)
print(letter_list)"""

C_LC = """sq_list = []
for x in range(1, 11):
    sq_list.append(x * x)
print(sq_list)

sq_list = [x * x for x in range(1, 11)]           # 串列生成式：一行等價
print(sq_list)

sq_list = [x * x for x in range(1, 11) if x % 2 != 0]
print(sq_list)"""

ctrl_html = f'''<h3 id="dx-ctrl">講義完整範例：巢狀迴圈、生成式與一個練習</h3>
{card("講義 01 · 巢狀 for：攤平字母", C_NEST, run_py(C_NEST),
note="外層走訪每個單字、內層走訪單字裡的每個字母。這種「攤平」也能寫成生成式：[letter for word in word_list for letter in word]。")}
{card("講義 01 · 串列生成式三段式", C_LC, run_py(C_LC),
note="生成式讀法固定：先看 for（資料從哪來）、再看 if（誰能留下）、最後看最前面的運算式（留下的變成什麼）。第三段只留奇數的平方。")}
{card("講義 01 · 練習：把 average() 寫完", """def average(a_list):
    if not a_list:
        print("List is empty")
        return
    # 你的程式碼：算出 avg，及格與否放進 status（"pass"/"fail"），然後：
    # print(f"{status} (Average: {avg:.1f})")

average([99, 100, 74, 63, 100, 100])
average([22, 19, 74, 63, 100, 44])""",
"pass (Average: 89.3)\\nfail (Average: 53.7)", out_label="完成後的預期輸出",
note="提示：sum(a_list) / len(a_list) 一行搞定平均（/ 是真除法，不用擔心整數截斷）。if not a_list 是「空串列判斷」的慣用寫法：空容器在布林脈絡下是 False。")}'''
s, c4 = insert_end_of_section(s, "control", ctrl_html, 'id="dx-ctrl"')

C_UNCAUGHT = """import math
a_number = -23
print(math.sqrt(a_number))"""

exc_html = f'''<h3 id="dx-exc">講義補充：沒接住會怎樣？</h3>
{card("講義 01 · 沒有 try/except 的下場", C_UNCAUGHT, run_py(C_UNCAUGHT), out_label="執行期錯誤訊息",
note="對照上面接住的版本：同一行程式，有 try/except 就能優雅收場，沒有就整支程式陣亡，traceback 直接甩在你臉上。ValueError 這一行就是該接的訊號。")}'''
s, c5 = insert_end_of_section(s, "exceptions", exc_html, 'id="dx-exc"')

C_SQ = """def square(n):
    return n ** 2

print(square(3))
print(square(square(3)))   # 先算內層 9，再平方"""

fn_html = f'''{card("講義 01 · 函式可以疊著呼叫", C_SQ, run_py(C_SQ),
note='<span id="dx-fn"></span>square(square(3)) 由內往外算：內層回傳 9，外層拿 9 再平方。這種「函式結果餵給函式」的組合思維是遞迴章的前菜。')}'''
s, c6 = insert_end_of_section(s, "functions", fn_html, 'id="dx-fn"')

C_FRACFULL = """def gcd(m, n):
    while m % n != 0:
        m, n = n, m % n
    return n

class Fraction:
    def __init__(self, top, bottom):
        self._num = top
        self._den = bottom

    def __str__(self):
        return f"{self._num}/{self._den}"

    def __eq__(self, other):
        return self._num * other._den == other._num * self._den

    def __add__(self, other):
        new_num = self._num * other._den + self._den * other._num
        new_den = self._den * other._den
        cmmn = gcd(new_num, new_den)
        return Fraction(new_num // cmmn, new_den // cmmn)

x = Fraction(1, 2)
y = Fraction(2, 3)
print(y)
print(x + y)
print(x == y)

z = Fraction(2, 4)
print(x == z)   # 深相等：1/2 == 2/4"""

cls_html = f'''<h3 id="dx-cls">收工驗收：完整 Fraction 的使用畫面</h3>
{card("講義 01 · 五步蓋完之後：__str__ / __add__ / __eq__", C_FRACFULL, run_py(C_FRACFULL),
note="最後一行是<strong>深相等</strong>的驗收：x 和 z 是兩個不同的物件，但 __eq__ 用交叉相乘比「值」，所以 1/2 == 2/4 是 True。沒寫 __eq__ 時，== 預設比「是不是同一個物件」（跟 is 一樣），那叫淺相等。")}
{card("講義 01 · 課後練習：負分母與大小比較", """class Fraction:
    # 你的程式碼：
    #  - __init__ 把負分母正規化（9/-10 → -9/10）
    #  - __gt__(self, other)、__lt__(self, other)

a = Fraction(3, 5)
b = Fraction(9, -10)
print(a > b)""",
"True", out_label="完成後的預期輸出",
note="提示：比大小跟 __eq__ 一樣用交叉相乘就好，不用真的除；但要先把「負號都搬到分子」，交叉相乘的不等號方向才不會被負分母翻轉。")}'''
s, c7 = insert_end_of_section(s, "classes", cls_html, 'id="dx-cls"')

inh_html = f'''<h3 id="dx-inh">講義完整範例：整座電路的程式版</h3>
{card("講義 01 · 用類別把電路接起來", """g1 = AndGate("gand1")
g2 = AndGate("gand2")
g3 = OrGate("gor3")
g4 = NotGate("gnot4")
c1 = Connector(g1, g3)   # g1 輸出 → g3 輸入
c2 = Connector(g2, g3)
c3 = Connector(g3, g4)
print(g4.get_output())""",
"Enter input for gate gand1 -->1\\nEnter input for gate gand1 -->1\\nEnter input for gate gand2 -->0\\nEnter input for gate gand2 -->0\\n0", out_label="示範執行（A=B=1、C=D=0）",
note="呼叫 g4.get_output() 會沿著 Connector 一路「往上游要值」：NOT 問 OR、OR 問兩個 AND、AND 才向使用者要輸入。所以 NOT((1 AND 1) OR (0 AND 0)) = NOT(1) = 0。拿上面的互動電路對照：同樣輸入應該得到同樣的 0。")}'''
s, c8 = insert_end_of_section(s, "inherit", inh_html, 'id="dx-inh"')

PAGE.write_text(s)
print("inserted:", [n for n, ok in zip("types coll io ctrl exc fn cls inh".split(),
      [c1, c2, c3, c4, c5, c6, c7, c8]) if ok])
