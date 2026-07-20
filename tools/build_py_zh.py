#!/usr/bin/env python3
"""生成 ds-python-selfstudy 的中文題庫母檔：flashcards 以 front 名重用 C++ zh、7 張差異卡新譯；questions ch7-9 拷貝後套 Python 用語修正。"""
import json, re
from pathlib import Path

PY_EN = Path.home() / "ds_cpp/_python_backup/Slides/flashcards"
CPP_EN = Path.home() / "ds_cpp/Slides/flashcards"
CPP_ZH = Path.home() / "ds-cpp-selfstudy/data/flashcards_zh"
OUT_FC = Path.home() / "ds-python-selfstudy/data/flashcards_zh"
OUT_Q = Path.home() / "ds-python-selfstudy/data/questions_zh"

# 差異卡的新譯（Python 語意）
OVERRIDE = {
    "Formatted String": {"front": "格式化字串（Formatted String）",
        "back": "內含佔位符的字串：把變數或運算式的值插進文字裡，動態組出內容。Python 最常用的是 f-string，例如 f\"{name} is {age}\"。"},
    "Format Operator": {"front": "格式化運算子（Format Operator）",
        "back": "用運算子做字串格式化的機制：Python 的 % 把變數代入字串裡定義好的佔位符，例如 \"%s is %d\" % (name, age)。是 f-string 之前的老寫法。"},
    "Syntax Error": {"front": "語法錯誤（Syntax Error）",
        "back": "程式碼文法上的錯誤：不符合語言的規則。直譯器在剖析程式碼時就會偵測出來（SyntaxError），該段程式根本不會開始執行。"},
    "Module": {"front": "模組（Module）",
        "back": "含 Python 定義與敘述的檔案：檔名就是模組名加上 .py。模組用來組織程式碼，import 之後就能重用裡面的函式與類別。"},
    "Dictionaries of Keys Matrix (DOK)": {"front": "鍵值字典矩陣（Dictionary of Keys, DOK）",
        "back": "用字典（雜湊表）表示稀疏矩陣：鍵是 (row, column) 這個 tuple、值是該位置的元素值。只有非零元素才占空間。"},
    "Tail of Linked List": {"front": "串列尾（Tail of Linked List）",
        "back": "鏈結串列的最後一個節點，其 next 參考設為 None，表示後面沒有節點了。"},
    "Circularly Linked List": {"front": "環狀鏈結串列（Circularly Linked List）",
        "back": "鏈結串列的變形：尾節點的 next 不指向 None，而是指回頭節點，適合表示循環性的資料。"},
}

total = 0
for n in range(1, 10):
    py = json.loads((PY_EN / f"ch{n}.json").read_text())
    cpp_en = json.loads((CPP_EN / f"ch{n}.json").read_text())
    cpp_zh = json.loads((CPP_ZH / f"ch{n}.json").read_text())
    # C++ 英文 front → zh 卡（同索引對齊）
    zh_by_front = {en["front"]: zh for en, zh in zip(cpp_en, cpp_zh)}
    out = []
    for c in py:
        if c["front"] in OVERRIDE and (c["front"] not in zh_by_front
                or cpp_en[[e["front"] for e in cpp_en].index(c["front"])]["back"] != c["back"]):
            out.append(OVERRIDE[c["front"]])
        elif c["front"] in zh_by_front:
            out.append(zh_by_front[c["front"]])
        else:
            out.append(OVERRIDE[c["front"]])  # 沒對映又沒新譯就會 KeyError，故意炸出來
    assert len(out) == len(py)
    for zh in out:
        assert re.search(r"[一-鿿]", zh["front"]) and re.search(r"[一-鿿]", zh["back"]), zh["front"]
        assert "（" in zh["front"], zh["front"]
    (OUT_FC / f"ch{n}.json").write_text(json.dumps(out, ensure_ascii=False, indent=0))
    total += len(out)
    print(f"ch{n}: {len(out)} 卡")
print("flashcards total:", total)

# ---- questions ch7-9：先 diff 英文原文，再把 C++ zh 拷貝＋用語修正 ----
for ch in ["ch7", "ch8", "ch9"]:
    import glob
    py_qs, cpp_qs = [], []
    for f in sorted(glob.glob(str(Path.home() / f"ds_cpp/_python_backup/Slides/questions/{ch}/*.json"))):
        py_qs += [q for q in json.load(open(f)) if q.get("type") == "multiple_choice"]
    for f in sorted(glob.glob(str(Path.home() / f"ds_cpp/Slides/questions/{ch}/*.json"))):
        cpp_qs += [q for q in json.load(open(f)) if q.get("type") == "multiple_choice"]
    diffs = []
    for i, (p, c) in enumerate(zip(py_qs, cpp_qs)):
        if p["question"] != c["question"]:
            diffs.append((i, "Q", p["question"], c["question"]))
        for j, (pa, ca) in enumerate(zip(p["answers"], c["answers"])):
            if pa["answer"] != ca["answer"]: diffs.append((i, f"A{j}", pa["answer"], ca["answer"]))
            if pa["feedback"] != ca["feedback"]: diffs.append((i, f"F{j}", pa["feedback"], ca["feedback"]))
            assert pa["correct"] == ca["correct"], (ch, i, j)
    print(f"{ch}: {len(py_qs)} 題, 英文原文差異 {len(diffs)} 處")
    for d in diffs:
        print("   ", d[0], d[1], "| py:", d[2][:90])
        print("        | cpp:", d[3][:90])
