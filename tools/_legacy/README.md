# `_legacy`：先備頁 P1–P9 當初的產生腳本

這些是 2026-08 建立 `p1`–`p9` 與 `00a`／`00b` 時寫的一次性腳本。
**它們原本只存在於暫存目錄，重開機就會消失**，2026-08-29 搶救進版控。

頁面本身已經是成品，平常維護不需要跑這裡的任何東西——
日常流程仍然是 `tools/inject_prereq_py.py` 與 `tools/apply_zh.py`（見 `HANDOFF.md`）。
留著它們是為了兩件事：**知道每一頁的內容是怎麼來的**，以及**下次要再移植一批頁面時有現成的範本**。

## 檔案

| 檔案 | 做什麼 |
|---|---|
| `port.py` | 把 PythonForMath 的六頁移植成 P1–P6。`PAGES` 表逐頁指定來源檔、目標檔、hero 文案與 `.ds-hook`；`convert_quiz()` 把 p4m 的 `QUIZ_DATA` 轉成本站 `questions_zh` 格式（複選改單選） |
| `terms.py` | 詞彙卡正面的對照表：p4m 的用語 → 本站慣例「中文（English）」，順便把中國用語校成台灣慣用語 |
| `extract.js` | 從 PythonForMath 的 HTML 裡把 `const QUIZ_DATA` / `const FLASHCARDS` 抽出來 |
| `gen_p7.py`／`gen_p8.py`／`gen_p9.py` | P7–P9 是新撰的，這三支用 Python 拼出 `body_p*.html` 與 `js_p*.js` |
| `add_p5_sets.py` | 在 P5 補上「集合」一節（PythonForMath 原頁沒有）。冪等 |
| `assemble.py` | `head.frag` + `body_<stem>.html` + `sharedjs.frag` + `js_<stem>.js` → 完整頁面 |
| `head.frag`／`sharedjs.frag` | 從 `recursion.html` 抽出來的 `<head>` 與共用 JS 片段 |

`gen_p*.py` 與 `add_p5_sets.py` 會 `sys.path.insert` 到 `tools/enrich/` 再
`from enrich_lib_py import hl, card`，所以要在這個 repo 底下跑。

## 素材來源

`port.py` 的輸入是 **[phonchi/PythonForMath](https://github.com/phonchi/PythonForMath)** 的六份
`.ipynb`／`.html` 與它的 `flashcards-TW/`、`questions-TW/`。
那是一個公開 repo，**沒有複製進來**（光 `Figures/` 就 2.1 MB，而且隨時能重新 clone）：

```bash
git clone https://github.com/phonchi/PythonForMath ~/PythonForMath
```

clone 完把 `port.py` 裡的來源路徑指過去即可。
