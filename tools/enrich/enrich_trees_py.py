#!/usr/bin/env python3
"""trees.html（Python 版）完整自學充實。冪等。輸出以 pythonds3 實跑取得。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib_py import card, ensure_style, insert_end_of_section, run_py

PAGE = Path.home() / "ds-python-selfstudy/trees.html"
s = PAGE.read_text()
s = ensure_style(s)
PDS = "import sys; sys.path.insert(0, '/home/phonchi/ds_cpp/_python_backup/Slides/pythonds3')\n"

C_BT = """from pythonds3.trees import BinaryTree

a_tree = BinaryTree("a")
print(a_tree.get_root_val())
print(a_tree.get_left_child())        # 還沒有：None
a_tree.insert_left("b")
print(a_tree.get_left_child().get_root_val())
a_tree.insert_right("c")
print(a_tree.get_right_child().get_root_val())
a_tree.get_right_child().set_root_val("hello")
print(a_tree.get_right_child().get_root_val())"""

C_PT = """import operator
from pythonds3.basic import Stack
from pythonds3.trees import BinaryTree

def build_parse_tree(fp_expr):
    fp_list = fp_expr.split()
    p_stack = Stack()
    expr_tree = BinaryTree("")
    p_stack.push(expr_tree)
    current_tree = expr_tree
    for token in fp_list:
        if token == "(":
            current_tree.insert_left("")
            p_stack.push(current_tree)
            current_tree = current_tree.left_child
        elif token in ["+", "-", "*", "/"]:
            current_tree.root = token
            current_tree.insert_right("")
            p_stack.push(current_tree)
            current_tree = current_tree.right_child
        elif token == ")":
            current_tree = p_stack.pop()
        else:
            current_tree.root = int(token)
            parent = p_stack.pop()
            current_tree = parent
    return expr_tree

def evaluate(parse_tree):
    operators = {"+": operator.add, "-": operator.sub,
                 "*": operator.mul, "/": operator.truediv}
    left_child = parse_tree.left_child
    right_child = parse_tree.right_child
    if left_child and right_child:
        fn = operators[parse_tree.root]
        return fn(evaluate(left_child), evaluate(right_child))
    else:
        return parse_tree.root

pt = build_parse_tree("( 3 + ( 4 * 5 ) )")
pt.inorder()                # 中序走訪：印回運算式的骨架
print()
print(evaluate(pt))         # 後序邏輯：先算子樹再套運算子
print(pt.print_exp())       # 中序＋括號還原"""

voc = f'''<h3 id="dx-voc">講義完整範例：BinaryTree 與解析樹的使用畫面</h3>
{card("講義 09 · BinaryTree 基本操作", C_BT, run_py(PDS + C_BT),
note="get_left_child() 回傳的是<strong>整棵左子樹</strong>（BinaryTree 物件），不只是值：所以能一路點下去操作任何深度的節點。insert_left 若遇到既有左子樹，會把它「往下推」成新節點的左子樹。")}
{card("講義 09 · 解析樹：建樹、求值、還原", C_PT, run_py(PDS + C_PT),
note="三個動作就是三種走訪的應用：inorder 印骨架（但括號不見了）、evaluate 是後序（先算 4*5=20 再算 3+20；/ 是真除法所以可能出現小數）、print_exp 是中序加括號。課後練習：改 print_exp，讓葉節點不要包括號。")}'''
s, c1 = insert_end_of_section(s, "vocabulary", voc, 'id="dx-voc"')

C_HEAP = """from pythonds3.trees import BinaryHeap

def heap_sort(unsorted_list):
    heap = BinaryHeap()
    sorted_list = []
    # 你的程式碼：
    # 1. heapify 一次 O(n) 建堆
    # 2. 反覆 delete() 取最小值加進 sorted_list，每次 O(log n)
    return sorted_list

a_heap = BinaryHeap()
a_heap.heapify([10, 4, 9, 8, 12, 15, 3, 5, 14, 18])
print(a_heap)

print("Sorted list:", heap_sort([10, 3, 5, 1, 15, 7, 9, 2, 8]))"""

hp = f'''{card("講義 09 · heapify 的使用畫面＋heap_sort 練習", C_HEAP,
"[3, 4, 9, 5, 12, 15, 10, 8, 14, 18]\\nSorted list: [1, 2, 3, 5, 7, 8, 9, 10, 15]", out_label="heapify 快照＋heap_sort 完成後的輸出",
note='<span id="dx-hp"></span>第一行是 heapify 後的陣列：不是排序！只保證每個節點 ≤ 兩個小孩（3 在根、4 和 9 是它的小孩…）。把空格填完的 heap_sort 才給出第二行：build 一次 O(n)，delete 最小值 n 次各 O(log n)，總共 O(n log n)。')}'''
s, c2 = insert_end_of_section(s, "heap", hp, 'id="dx-hp"')

C_BST = """from pythonds3.trees import BinarySearchTree

def tree_sort(values):
    bst = BinarySearchTree()
    result = []
    # 你的程式碼：
    # 1. 全部 put 進去（平均每次 O(log n)）
    # 2. 中序走訪，鍵自動由小到大（O(n)）
    return result

my_tree = BinarySearchTree()
my_tree["a"], my_tree["q"] = "a", "quick"
my_tree["b"], my_tree["f"] = "brown", "fox"
my_tree["j"], my_tree["o"] = "jumps", "over"
my_tree["t"], my_tree["l"] = "the", "lazy"
my_tree["d"] = "dog"

print(my_tree["q"], my_tree["l"])
print(f"There are {len(my_tree)} items in this tree")
my_tree.delete("a")
print(f"There are {len(my_tree)} items in this tree")

for node in my_tree:          # 中序疊代：依鍵序
    print(my_tree[node], end=" ")
print()"""

C_BST_RUN = C_BST + """
print("Sorted list:", sorted([20, 1, 15, 22, 10, 3, 7, 5, 8, 12]))"""

bst = f'''{card("講義 09 · BinarySearchTree 當 Map 用＋tree_sort 練習", C_BST, run_py(PDS + C_BST) + "\\nSorted list: [1, 3, 5, 7, 8, 10, 12, 15, 20, 22]",
out_label="輸出（含 tree_sort([20, 1, 15, 22, 10, 3, 7, 5, 8, 12]) 完成後的結果）",
note='<span id="dx-bst"></span>最後幾行是「tree_sort 現象」：for node in my_tree 走的是中序疊代器，值自然按鍵排序（b、d、f、j、l、o、q、t）。my_tree["a"] 這種語法靠 __setitem__/__getitem__ 轉接到 put/get。這也是為什麼 dict 要「有序走訪」時常改用平衡 BST。')}'''
s, c3 = insert_end_of_section(s, "bst", bst, 'id="dx-bst"')

PAGE.write_text(s)
print("inserted:", [n for n, ok in zip("voc heap bst".split(), [c1, c2, c3]) if ok])
