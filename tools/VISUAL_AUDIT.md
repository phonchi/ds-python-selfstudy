# Python 資料結構自學站視覺稽核

更新日期：2026-09-01。稽核範圍為 20 頁正文視覺、播放器與互動控制；hero、quiz、flashcard
只有在重複或干擾主線時才列入。

## 判準與來源

1. 黃金標準依序為 Math208 講義 notebook／PDF、pythonds／Runestone 課本、Python 官方文件。
2. 講義／課本與目前 `pythonds3` 套件不同時，正文教課堂版本，旁註套件差異與可執行名稱。
   Colab 的 restart／刪除 runtime 邊界另依 [Google Colab 官方 FAQ](https://research.google.com/colaboratory/faq.html)。
3. 不為數量精簡：真正呈現狀態、指標、演算法幾何或輸入變化者保留；固定文字輪播、重複視覺、
   假量化或錯誤模擬才移除／重做。
4. 來源界線記錄在本檔與既有 section badge，不另外增加學生頁 badge。

## 播放合約

- 文字／程式 trace：快速 900 ms、標準 1800 ms、慢速 3000 ms。
- 純比較／交換／空間移動：快速 600 ms、標準 1200 ms、慢速 2200 ms。
- Play/Pause、Previous/Next、Reset；Step 必須先 pause；初態停留完整 delay。
- 8 frames 以上有 scrubber 與 frame counter；結果／錯誤／rewire 可有較長 hold。
- frame 為 immutable snapshot；reset、seek、resize、改輸入與重播不得重複 commit 或重抽資料。
- 控制列支援 390 px、`aria-live="polite"`、鍵盤 label 與 `prefers-reduced-motion`。

2026-09-01 的實作已讓所有帶速度控制的 timeline 通過上述合約。`browser_check_py.py` 會實際
執行 Play → Step → seek → Reset，等待 1.05 秒後確認舊 timer 沒有復活；只檢查按鈕存在不算通過。
Knight 的解題 generation、AVL／heap／BST／delete snapshots 另有倒帶重播專項測試。

## 課前與先備頁

| 頁面 | 保留／重做 | 移除／靜態化 | 新增 |
|---|---|---|---|
| 00A | Big-O 改相對成長，不換算假牆鐘時間 | hero、死碼、重複習慣磚 | 靜態學習迴圈 |
| 00B | 環境選擇表 | hero、重複驗收磚、死碼 | notebook/runtime/restart 圖 |
| P1 | 運算順序、名稱綁定 | digit trace 表格化；假 identifier/type parser；雙 hello 合併 | — |
| P2 | if/elif/else、while、range、樹形練習 | 重複真值表 clicker；17-frame while 壓成語意步驟 | 縮排層級圖 |
| P3 | call stack、arguments、guess game、scope | Dragon 移選做；scope 改真 nested frames | module/import 圖 |
| P4 | slicing、methods、refs、1A2B | 固定 trace 改完整控制 | methods 索引／shift／delete ghost |
| P5 | create、nested、get、memo、sets | items iteration 表格化；Alien 移選做；`memo={}` 修正 | — |
| P6 | f-string、Mystery Island、methods | escape 限定教學子集；format 數值邊界 | — |
| P7 | exception/else/finally trace | 情境切換不得 autoplay | — |
| P8 | attribute lookup | MRO 過度宣稱修正 | class-instance-self 圖 |
| P9 | `__lt__` trace、dunder protocol | 明示 insertion sort 示意、非 Timsort | inheritance/MRO/super 圖 |

## 正課

| 頁面 | 保留／重做 | 移除／修正 | 新增 |
|---|---|---|---|
| Introduction | binding、format、functions、Fraction、logic circuit | type/list 固定輪播改表格；`[9]`/`[99]` 一致 | — |
| Analysis | growth、Anagram、ArrayList | growth log 軸；Anagram 真 26 格；移除 hash 1.2 probes | — |
| Arrays | address、compact、sparse | multidim 高速播放改並排路徑；sparse 明確 value input | ArrayList insert/erase 搬移圖 |
| Linked Lists | ULL/OLL pointer trace | Node/LinkedListNode、講義／套件 size 差異、初態與 snapshots | explicit previous/current/rewire |
| Linear Structures | ADT 操作與演算法 trace | prologue autoplay、Stack2 指標、`^`、postfix `/`、速度控制 | printer queue timeline |
| Recursion | sum、base、frames、tree、Sierpinski、Hanoi、maze、DP | spiral 改完成圖；maze 改語意 frames | — |
| Search/Sort | 搜尋、雜湊、六排序全部保留 | binary 不靜默排序；所有算法初態／速度／scrubber | — |
| Graphs | 十組圖演算法皆保留 | Knight 記憶體上限；TopSort/SCC 改可倒帶 timeline | — |
| Trees | 術語、parse、traversal、heap、BST、delete、AVL | immutable replay；BST analysis 固定 seed、resize 不換資料 | list-of-lists vs nodes/references |

## 必驗證的不變量

- Big-O 不等同實測秒數；hash 不顯示無來源平均 probes。
- Python identifier、literal、escape、format 結果不得由未標示的 JS 假 parser 冒充。
- nested scope 同時保留 caller/callee frames；memo 每次呼叫使用 fresh dict。
- Node 類名與 linked-list `size()` 複雜度明確區分講義版／套件版。
- Anagram 使用兩個 26 格計數陣列；postfix `/` 是真除法；`^` 採右結合。
- Binary search 不靜默排序輸入；Sparse value 不由未標示亂數產生。
- Knight trace 有事件上限／取消；BST/heap/delete seek 不重複 mutation；resize 不換資料。
- P9 `__lt__` 明示 insertion sort 示意，不宣稱是 `sorted()`／Timsort 內部流程。
