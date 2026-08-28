# 資料結構 × Python 互動自學網站

NSYSU 資料結構課程的互動自學配套網站（Python 版）：兩章課前準備 ＋ 九章互動教材 ＋ 九頁選讀先備知識，
每一節都能動手操作、預測、驗證，配上每節 quiz、關鍵詞彙卡（flashcards）與 REF 速查表。

- 線上閱讀：https://phonchi.github.io/ds-python-selfstudy/
- 教科書：[pythonds — Problem Solving with Algorithms and Data Structures using Python](https://github.com/RunestoneInteractive/pythonds)
- 課程講義：[nsysu-math208-2025](https://github.com/phonchi/nsysu-math208-2025)（各頁「講義 PDF」連結來源）

## 課前準備（先讀）

| # | 頁面 | 內容 |
|---|------|------|
| 00A | [AI 時代，為什麼還要學資料結構？](00a_why_code.html) | 能跑 ≠ 跑得動、AI 選錯結構的代價、學習迴圈 |
| 00B | [課前準備與環境安裝](00b_setup.html) | Colab／Anaconda／VS Code 三路線、pythonds3 安裝與驗收 |

## 章節（授課順序）

| # | 頁面 | 對應 |
|---|------|------|
| 01 | [Python 導論](introduction.html) | pythonds Ch.1 |
| 02 | [演算法分析](analysis.html) | pythonds Ch.2 |
| 03 | [陣列與稀疏矩陣](arrays.html) | 附錄 A（講義 03） |
| 04 | [鏈結串列](linked_lists.html) | pythonds §3.19–3.23 |
| 05 | [堆疊、佇列與 Deque](linear_structures.html) | pythonds Ch.3 |
| 06 | [遞迴](recursion.html) | pythonds Ch.4 |
| 07 | [搜尋與排序](searching_sorting.html) | pythonds Ch.5 |
| 08 | [圖與圖演算法](graphs.html) | pythonds Ch.7 |
| 09 | [樹與樹演算法](trees.html) | pythonds Ch.6 |

## 先備知識（選讀，不列入評分）

複習課程「預設你已經會」的基本 Python。P1–P6 的內容改寫自
[PythonForMath](https://github.com/phonchi/PythonForMath)，P7–P9 為本站新撰。

| # | 頁面 | 內容 |
|---|------|------|
| P1 | [Python 基礎](p1_python_basics.html) | 型別、變數、運算子、三種錯誤 |
| P2 | [流程控制](p2_flow_control.html) | 布林運算式、if／while／for、縮排 |
| P3 | [函數](p3_functions.html) | 定義與呼叫、引數、回傳值、範圍 |
| P4 | [串列與元組](p4_lists_tuples.html) | 索引切片、可變性、參照 vs 複製 |
| P5 | [字典與集合](p5_dicts_sets.html) | 鍵值對、get／setdefault、memoization、集合運算 |
| P6 | [字串操作](p6_strings.html) | 索引切片、跳脫字元、f-string、字串方法 |
| P7 | [檔案與例外](p7_files_exceptions.html) | pathlib、with open、JSON、try／except／else／finally |
| P8 | [物件導向（基礎）](p8_oop_basics.html) | class、`__init__`、self、封裝、`__str__`、組合 |
| P9 | [物件導向（進階）](p9_oop_advanced.html) | 繼承、多型、`__eq__`／`__hash__`、`__lt__`、容器協定 |

第 04 章之後幾乎每個資料結構都是一個 `class`，因此 **P8／P9 強烈建議不要跳過**。

每頁皆為單檔自足 HTML（互動元件為原生 JS，僅外連 MathJax 與 Google Fonts CDN）。
詞彙卡與自測題取自課程題庫並譯為繁體中文（母檔在 `data/flashcards_zh/`、`data/questions_zh/`，
詞彙卡正面採「中文（English）」格式；改內容請改母檔後跑 `tools/apply_zh.py`）。

## 維護

| 腳本 | 用途 |
|------|------|
| `tools/apply_zh.py` | 從 `data/` 重新灌入所有頁面的詞彙卡與題庫自測區（冪等） |
| `tools/inject_site_py.py` | 九章正課頁的網站化注入（導讀框、詞彙卡區、上下章導覽）；已全部注入完畢，重跑會 skip |
| `tools/inject_quiz_py.py` | 第 07–09 章的題庫自測區注入；同上 |
| `tools/inject_prereq_py.py` | 課前章 00A／00B 與先備頁 P1–P9 的同類注入（冪等） |
| `tools/check_links_py.py` | 全站錨點、頁面連結與注入前置條件檢查 |

新增一頁的流程：撰寫頁面本體 → 在 `inject_prereq_py.py` 的 `PPAGES` 登記 → 跑該腳本 →
在 `apply_zh.py` 的 `FC`／`BQ` 登記並補上 `data/` 母檔 → 跑 `apply_zh.py` → 跑 `check_links_py.py`。
