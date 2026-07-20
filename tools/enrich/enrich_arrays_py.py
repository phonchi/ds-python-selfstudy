#!/usr/bin/env python3
"""arrays.html（Python 版）完整自學充實。冪等。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib_py import card, ensure_style, insert_end_of_section, run_py

PAGE = Path.home() / "ds-python-selfstudy/arrays.html"
s = PAGE.read_text()
s = ensure_style(s)
PDS = "import sys; sys.path.insert(0, '/home/phonchi/ds_cpp/_python_backup/Slides/pythonds3')\n"

C_AL_SHOW = """from pythonds3.basic import ArrayList

my_array = ArrayList()
my_array.append(31)
my_array.append(77)
my_array.append(17)
my_array.append(93)

print(my_array, my_array[3])
print(my_array.size())
my_array.insert(3, 20)
print(my_array)
my_array.remove(31)
print(my_array)
my_array.erase(2)
my_array[0] = 50
print(my_array)
print(my_array.is_empty())"""

lay = f'''{card("講義 03 · ArrayList 的使用畫面", C_AL_SHOW, run_py(PDS + C_AL_SHOW),
note='<span id="dx-lay"></span>insert(3, 20) 要把索引 3 之後的元素全部往右搬一格、remove(31) 要把後面全部往左搬：中間插刪是 O(n)，只有尾端 append 是 O(1)。__getitem__ / __setitem__ 讓 my_array[3] 這種語法直接可用，越界則丟 LookupError。')}'''
s, c1 = insert_end_of_section(s, "layout", lay, 'id="dx-lay"')

C_NP = """import numpy as np
from timeit import default_timer as timer

a = list(range(10000))
start = timer()
for i in range(10000):
    a[i] = a[i] + 1        # 純 Python 迴圈：一格一格加
end = timer()
print("list  loop : %.3f ms" % (10**3 * (end - start)))

b = np.arange(10000)       # compact array：同型別、連續記憶體
start = timer()
b = b + 1                  # 向量化：一條指令全加
end = timer()
print("numpy  b+1 : %.3f ms" % (10**3 * (end - start)))

print(np.array_equal(np.array(a), b))"""

comp = f'''{card("講義 03 · compact 的威力：numpy 向量化實測", C_NP, run_py(C_NP), out_label="實跑輸出（毫秒依機器而異，看倍數）",
note='<span id="dx-comp"></span>list 是 referential：每格存指向 int 物件的參考，迴圈還得經過直譯器。numpy 的 array 是 compact：同型別資料緊排在連續記憶體，b + 1 整條在 C 層完成，快一到兩個量級。')}'''
s, c2 = insert_end_of_section(s, "compact", comp, 'id="dx-comp"')

C_MD = """from numpy import array, int32
M = array([[1, 1], [2, 2]], dtype=int32)
print(M.shape, M.dtype)
print(M[0, :])    # 第 0 列
print(M[:, 0])    # 第 0 行
print(M[1, 1])
print(M.flags['C_CONTIGUOUS'], M.flags['F_CONTIGUOUS'])

F = array([[1, 1], [2, 2]], dtype=int32, order='F')   # column-major
print(F.flags['C_CONTIGUOUS'], F.flags['F_CONTIGUOUS'])"""

C_FLAT = """import numpy as np
student = np.random.randint(0, 100, size=(100, 4))
s = student.flatten()          # 攤平成一維（row-major 順序）
# 把 ? 換成你的答案
assert student[5][3] == s[?], "Error"
print("Pass")"""

multi = f'''<h3 id="dx-multi">講義完整範例：二維陣列的每一種看法</h3>
{card("講義 03 · shape、切片、記憶體順序旗標", C_MD, run_py(C_MD),
note="order='C'（預設）是 row-major、order='F' 是 column-major：同一份資料、兩種攤法。flags 直接告訴你這個 array 在記憶體裡是哪種連續。")}
{card("講義 03 · 練習：用平面索引找 student[5][3]", C_FLAT, "Pass", out_label="填對之後的輸出",
note="row-major 公式 i*Cols + j = 5×4 + 3 = <strong>23</strong>。assert 是驗收利器：條件為假直接 AssertionError，考自己最誠實。")}'''
s, c3 = insert_end_of_section(s, "multidim", multi, 'id="dx-multi"')

C_SP_SHOW = """from pythonds3.basic import SparseMatrix

dense_matrix = [[1, 0, 0], [0, 2, 0], [0, 0, 3]]
sparse_matrix = SparseMatrix().from_dense_matrix(dense_matrix)
print(sparse_matrix)

matrix1 = SparseMatrix({(0, 1): 1, (1, 1): 2, (2, 2): 3})
matrix2 = SparseMatrix({(1, 1): 3, (2, 2): 4})

print(matrix1 + matrix2)
print(matrix1 - matrix2)
print(matrix1 * matrix2)"""

sp = f'''{card("講義 03 · SparseMatrix 使用畫面：加減乘一次看", C_SP_SHOW, run_py(PDS + C_SP_SHOW),
note='<span id="dx-sp"></span>乘法那行值得慢讀：DOK 版本的矩陣乘法只要「A 的 (i, k) 遇上 B 的 (k, j)」才產生貢獻，兩層迴圈都只走<strong>非零元素</strong>。(0,1)×(1,1) 給 (0,1)：3；(1,1)×(1,1) 給 (1,1)：6；(2,2)×(2,2) 給 (2,2)：12。')}'''
s, c4 = insert_end_of_section(s, "sparse", sp, 'id="dx-sp"')

PAGE.write_text(s)
print("inserted:", [n for n, ok in zip("lay comp multi sp".split(), [c1, c2, c3, c4]) if ok])
