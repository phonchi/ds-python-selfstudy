# 接力文件（ds-python-selfstudy）

姊妹站是 [`ds-cpp-selfstudy`](https://github.com/phonchi/ds-cpp-selfstudy)，兩站結構完全相同，
`recursion.html` 的整個 `<head>`（1–332 行）除了 `<title>` 之外逐位元組一致。
**改動任一站之前，先看另一站有沒有已經解過同一個問題** —— 那邊的 `HANDOFF.md` 記了八個坑，
其中大半在這邊也成立。

## 現況（2026-08-28 已上線）

站上共 20 頁：**兩章課前準備 ＋ 九章正課 ＋ 九頁選讀先備知識**。

| 區塊 | 頁面 |
|---|---|
| 課前準備 | `00a_why_code`（為什麼還要學）、`00b_setup`（環境安裝） |
| 正課 | `introduction` → `trees` 九章 |
| 先備知識 | `p1_python_basics` … `p9_oop_advanced` |

P1–P6 的內容改寫自 [PythonForMath](https://github.com/phonchi/PythonForMath)（兩站共用同一套
設計系統，移植成本很低）；P7–P9 與 00A／00B 為新撰。

## 工具鏈與它們的契約

| 腳本 | 做什麼 | 冪等靠什麼 |
|---|---|---|
| `tools/apply_zh.py` | 從 `data/` 重生各頁的 `const FLASHCARDS` 與 `<section id="bankquiz">` | 整段以邊界重生 |
| `tools/inject_prereq_py.py` | 課前章與先備頁的尾段注入（導讀框、bankquiz 錨點、詞彙卡區、上下頁導覽、CSS/JS、補 MathJax） | `<!-- prereq-injected -->` 標記 |
| `tools/check_links_py.py` | 錨點、站內連結、注入前置條件、C++ 殘留 | — |
| `tools/inject_site_py.py`／`inject_quiz_py.py` | 九章正課頁的網站化注入，已全部注入完畢，重跑會 skip | `id="cards"`／`id="bankquiz"` |
| `tools/enrich/enrich_lib_py.py` | `hl()` Python 上色、`card()` 範例卡、`run_py()` 實跑 | — |
| `tools/build_py_zh.py` | 詞彙卡母檔的產生器，依賴 repo 外路徑，本機跑不動 | — |

## 新增一頁的流程

```bash
# 撰寫頁面本體（head 從 recursion.html 1–332 行複製，改 <title>）
# 在 tools/inject_prereq_py.py 的 PPAGES 登記
python3 tools/inject_prereq_py.py
# 在 tools/apply_zh.py 的 FC／BQ 登記並補上 data/ 母檔
python3 tools/apply_zh.py
python3 tools/check_links_py.py
```

## 踩過的坑

1. **`FC`／`BQ` 的條目必須跟頁面同批進 commit。** `apply_zh.py` 對每個 `FC` key 無條件讀檔並
   assert，先加會讓腳本一路中斷。
2. **`apply_zh.py` 的 `re.subn` 不能用 f-string 當替換字串。** 資料裡 `sanitize_js` 產生的
   `\uXXXX` 會被 `re` 當成模板跳脫，Python 3.13 直接拋 `bad escape \u`。已改用 `lambda`。
   （這支腳本在修好之前，從來沒有在 Python 3.13 上執行完成過。）
3. **移植進來的頁面要補 MathJax。** PythonForMath 的 `<head>` 沒有 MathJax，而 P4／P5 有
   `$…$` 數學式。`inject_prereq_py.py` 已加入冪等的補齊步驟。
4. **`Player` 動態更新的文字不能用 `$…$`**，MathJax 不會重新排版，要寫成 `<code>O(n)</code>`。
5. **`inject_site_py.py` 的守衛是 `id="cards"`**，而 PythonForMath 的頁面本來就有這個 id。
   移植時要先把來源頁的 `#cards` 區與舊 `chapter-nav` 整段刪掉，否則注入器會整頁跳過而且不報錯。
6. **姊妹站的 `hl()` 缺 `data-l` 導致 `hlLine` 靜默失效**（C++ 站已修）。這邊的
   `enrich_lib_py.py` 有同樣的問題，但這邊的頁面沒有「`hl()` 產生的程式碼 ＋ `hlLine` 高亮」
   這種組合，所以沒有實際影響。**之後若要新增這種頁面，記得先修 `hl()`。**

## 文字風格

2026-08 對 11 個新頁做過一次校對（commit `11675be`），判準是**跟既有九章的用字習慣走**，
不另立一套：走訪不是遍歷（九章 56:0）、運算子不是運算符（33:0）、串列不是列表、
呼叫不是調用、型別不是類型、回傳不是返回。另外砍掉了贅語（「進行四捨五入」→「四捨五入」）、
重複的修辭框架（`00a` 一頁用了六次「不是 A，而是 B」，降到兩次）與解說導引句。

粗體與 emoji 密度本來就低於既有九章（粗體每 107 字一個 vs 九章 70），維持原樣沒動。

## 已知待辦

- `data/flashcards_zh/ch7.json` 等正課母檔仍有少量贅語，改了會動到既有頁面，沒做。
- `searching_sorting.html` 表頭裡的 `<code>put</code>` 在深藍底上看不見
  （`.cmp-table th` 是深藍底白字，而 `code` 預設也是深藍字）。C++ 站的先備頁 CSS 已補覆寫規則，
  這邊的既有頁面沒補。
- 全站在 375px 寬會橫向溢位 —— 既有特性，九章正課頁本來就這樣。
