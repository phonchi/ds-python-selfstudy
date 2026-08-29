# p4m 字卡正面 -> 本站慣例「中文（English）」；順便把中國用語校成台灣慣用語
TERMS = {
 # ch1
 "演算法": "演算法（Algorithm）", "虛擬碼": "虛擬碼（Pseudocode）",
 "程式設計": "程式設計（Programming）", "程式語言": "程式語言（Programming Language）",
 "直譯式語言": "直譯式語言（Interpreted Language）", "直譯器": "直譯器（Interpreter）",
 "敘述": "敘述（Statement）", "函數": "函數（Function）", "參數": "參數（Parameter）",
 "常數": "常數（Constant）", "方法": "方法（Method）", "註解": "註解（Comment）",
 "運算式": "運算式（Expression）", "向下取整除法": "向下取整除法（Floor Division）",
 "變數": "變數（Variable）", "指派敘述": "指派敘述（Assignment Statement）",
 "關鍵字": "關鍵字（Keyword）", "型別": "型別（Type）", "除錯": "除錯（Debugging）",
 "語法錯誤": "語法錯誤（Syntax Error）", "語意錯誤": "語意錯誤（Semantic Error）",
 "執行時錯誤": "執行期錯誤（Runtime Error）",
 # ch2
 "流程控制敘述": "流程控制敘述（Control Flow Statement）",
 "布林運算式": "布林運算式（Boolean Expression）", "布林值": "布林值（Boolean Value）",
 "比較運算子": "比較運算子（Comparison Operator）", "布林運算子": "布林運算子（Boolean Operator）",
 "循序執行": "循序執行（Sequential Execution）", "選擇敘述": "選擇敘述（Selection Statement）",
 "重複敘述": "重複敘述（Iteration Statement）",
 "結構化程式設計": "結構化程式設計（Structured Programming）",
 "條件": "條件（Condition）", "子句": "子句（Clause）",
 "程式碼區塊": "程式碼區塊（Code Block）", "縮排": "縮排（Indentation）",
 "控制結構": "控制結構（Control Structure）", "if 敘述": "條件敘述（if Statement）",
 "while 敘述": "條件迴圈（while Statement）",
 "增強指派運算子": "增強指派運算子（Augmented Assignment Operator）",
 "break 敘述": "跳出迴圈（break Statement）", "無窮迴圈": "無窮迴圈（Infinite Loop）",
 "continue 敘述": "跳過本輪（continue Statement）",
 "for 迴圈敘述": "計數迴圈（for Statement）", "in 關鍵字": "成員運算子（in Operator）",
 "序列型別": "序列型別（Sequence Type）", "標準函式庫": "標準函式庫（Standard Library）",
 # ch3
 "分治法": "分而治之（Divide and Conquer）", "抽象化": "抽象化（Abstraction）",
 "呼叫函數": "函數呼叫（Function Call）", "引數": "引數（Argument）",
 "位置參數": "位置參數（Positional Parameter）", "文檔字符串": "說明字串（Docstring）",
 "返回語句": "回傳敘述（return Statement）",
 "有返回值的函數": "有回傳值的函數（Fruitful Function）",
 "無返回值的函數": "無回傳值的函數（Void Function）",
 "關鍵字參數": "關鍵字引數（Keyword Argument）", "默認參數": "預設參數（Default Parameter）",
 "局部範圍": "區域範圍（Local Scope）", "全局範圍": "全域範圍（Global Scope）",
 "局部變數": "區域變數（Local Variable）", "全局變數": "全域變數（Global Variable）",
 "模組": "模組（Module）",
 # ch4
 "容器": "容器（Container）", "序列": "序列（Sequence）", "串列": "串列（List）",
 "元組": "元組（Tuple）", "元素": "元素（Element）", "索引": "索引（Index）",
 "下標運算符": "下標運算子（Subscript Operator）", "切片": "切片（Slice）",
 "可變": "可變（Mutable）", "項目指派": "項目指派（Item Assignment）",
 "逐項迭代": "逐項走訪（Iteration）", "串列生成式": "串列生成式（List Comprehension）",
 "不可變": "不可變（Immutable）", "參照": "參照（Reference）",
 "就地修改": "就地修改（In-place Modification）",
 # ch52
 "鍵值對": "鍵值對（Key-Value Pair）", "鍵": "鍵（Key）", "值": "值（Value）",
 "字典": "字典（Dictionary）", "字典生成式": "字典生成式（Dictionary Comprehension）",
 # ch5
 "字串": "字串（String）", "跳脫字元": "跳脫字元（Escape Character）",
 "原始字串": "原始字串（Raw String）", "字串插值": "字串插值（String Interpolation）",
 "格式化字串": "格式化字串（Formatted String）",
 "格式說明子": "格式說明子（Format Specifier）", "f-字串": "f 字串（f-string）",
}

# 內文的中國用語校正（字卡背面與題目文字）
ZH_TW = [
    ("文檔字符串", "說明字串"), ("字符串", "字串"), ("返回值", "回傳值"), ("返回語句", "回傳敘述"),
    ("返回", "回傳"), ("默認", "預設"), ("局部變數", "區域變數"), ("全局變數", "全域變數"),
    ("局部範圍", "區域範圍"), ("全局範圍", "全域範圍"), ("局部", "區域"), ("全局", "全域"),
    ("運算符", "運算子"), ("創建", "建立"), ("存儲", "儲存"), ("數據", "資料"),
    ("資料類型", "資料型別"), ("類型", "型別"), ("函數式", "函式式"), ("遍歷", "走訪"),
    ("列表", "串列"), ("元素的順序", "元素的順序"), ("支持", "支援"), ("信息", "資訊"),
]
