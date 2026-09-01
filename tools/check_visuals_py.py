#!/usr/bin/env python3
"""Audit the 20 curriculum pages for visual and playback regressions.

This is deliberately a dependency-free structural check.  Browser behaviour and
390 px layout are covered by ``browser_check_py.py``.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    "00a_why_code.html",
    "00b_setup.html",
    "introduction.html",
    "analysis.html",
    "arrays.html",
    "linked_lists.html",
    "linear_structures.html",
    "recursion.html",
    "searching_sorting.html",
    "graphs.html",
    "trees.html",
    *[f"p{i}_{name}.html" for i, name in enumerate(
        [
            "python_basics",
            "flow_control",
            "functions",
            "lists_tuples",
            "dicts_sets",
            "strings",
            "files_exceptions",
            "oop_basics",
            "oop_advanced",
        ],
        1,
    )],
]

TRACE_SPEEDS = {"900", "1800", "3000"}
SPATIAL_SPEEDS = {"600", "1200", "2200"}
VALID_SPEEDS = (TRACE_SPEEDS, SPATIAL_SPEEDS)


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.speed_ranges: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.append(data["id"] or "")
        if (
            tag == "input"
            and data.get("type") == "range"
            and "speed" in (data.get("id") or "").lower()
        ):
            self.speed_ranges.append(data.get("id") or "(unnamed)")


def inline_scripts(source: str) -> list[str]:
    scripts = []
    for attrs, body in re.findall(r"<script\b([^>]*)>(.*?)</script>", source, re.S | re.I):
        if re.search(r"\bsrc\s*=", attrs, re.I):
            continue
        kind = re.search(r'\btype\s*=\s*["\']([^"\']+)', attrs, re.I)
        if kind and kind.group(1).lower() not in {
            "text/javascript",
            "application/javascript",
            "module",
        }:
            continue
        scripts.append(body)
    return scripts


def speed_selects(source: str) -> list[tuple[str, set[str]]]:
    found = []
    pattern = r'<select\b([^>]*\bid="[^"]*[Ss]peed[^"]*"[^>]*)>(.*?)</select>'
    for attrs, body in re.findall(pattern, source, re.S):
        ident = re.search(r'\bid="([^"]+)"', attrs).group(1)
        values = set(re.findall(r'<option\b[^>]*\bvalue="([^"]+)"', body))
        found.append((ident, values))
    return found


def require(page: str, source: str, patterns: list[tuple[str, str]]) -> list[str]:
    return [f"{page}: missing {label}" for label, pattern in patterns if not re.search(pattern, source, re.I | re.S)]


def forbid(page: str, source: str, patterns: list[tuple[str, str]]) -> list[str]:
    return [f"{page}: retained {label}" for label, pattern in patterns if re.search(pattern, source, re.I | re.S)]


def main() -> int:
    errors: list[str] = []
    missing = [name for name in PAGES if not (ROOT / name).exists()]
    if missing:
        errors.extend(f"missing page: {name}" for name in missing)

    sources: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="ds-visual-js-") as temp_dir:
        temp = Path(temp_dir)
        for page in PAGES:
            path = ROOT / page
            if not path.exists():
                continue
            source = path.read_text(encoding="utf-8")
            sources[page] = source

            parser = StructureParser()
            parser.feed(source)
            duplicates = sorted(ident for ident, count in Counter(parser.ids).items() if count > 1)
            if duplicates:
                errors.append(f"{page}: duplicate ids: {', '.join(duplicates)}")
            if parser.speed_ranges:
                errors.append(f"{page}: playback speed still uses range input: {', '.join(parser.speed_ranges)}")

            for ident, values in speed_selects(source):
                if values not in VALID_SPEEDS:
                    errors.append(f"{page}: {ident} has non-standard speed choices {sorted(values)}")

            for index, script in enumerate(inline_scripts(source), 1):
                js_path = temp / f"{path.stem}-{index}.js"
                js_path.write_text(script, encoding="utf-8")
                checked = subprocess.run(
                    ["node", "--check", str(js_path)],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if checked.returncode:
                    detail = (checked.stderr or checked.stdout).strip().splitlines()[-1]
                    errors.append(f"{page}: inline script {index} does not parse ({detail})")

    if len(sources) != 20:
        errors.append(f"expected 20 curriculum pages, found {len(sources)}")

    # Source-backed additions and intentional replacements.
    required: dict[str, list[tuple[str, str]]] = {
        "00a_why_code.html": [("learning loop", r"學習迴圈")],
        "00b_setup.html": [
            ("runtime lifecycle", r"runtime|執行階段|核心.*重啟|重新啟動.*核心"),
            ("new-VM/delete-runtime distinction", r"Disconnect and delete runtime|中斷連線並刪除|刪除\s*runtime|全新\s*runtime"),
        ],
        "p2_flow_control.html": [("indentation model", r'class="indent-map"')],
        "p3_functions.html": [("module boundary", r"模組.*邊界|import.*模組")],
        "p8_oop_basics.html": [("class-instance-self model", r"class.*instance.*self|類別.*實例.*self")],
        "p9_oop_advanced.html": [
            ("inheritance/MRO model", r"繼承.*MRO|MRO.*繼承"),
            ("pythonds3 LinkedList hierarchy", r"LinkedList"),
        ],
        "arrays.html": [("ArrayList shift visual", r"ArrayList.*(?:搬移|shift)|(?:搬移|shift).*ArrayList")],
        "linked_lists.html": [("previous/current rewiring", r"previous\s*/\s*current|previous.*current")],
        "linear_structures.html": [("printer queue timeline", r"印表機.*timeline|printer.*timeline|印表機.*時間軸")],
        "trees.html": [("list-of-lists comparison", r"list-of-lists|列表的列表|串列的串列")],
    }
    for page, patterns in required.items():
        errors.extend(require(page, sources.get(page, ""), patterns))

    forbidden: dict[str, list[tuple[str, str]]] = {
        "00a_why_code.html": [("decorative hero markup", r'<div\s+class="hero"')],
        "00b_setup.html": [("decorative hero markup", r'<div\s+class="hero"')],
        "analysis.html": [("invented 1.2-probe hash estimate", r"1\.2\s*(?:次)?探查|1\.2\s*\*\s*q")],
        "linked_lists.html": [("non-existent Node import", r"from\s+pythonds3\.basic\.linked_list\s+import\s+Node\b")],
        "linear_structures.html": [("floored postfix division", r"Math\.floor\s*\(\s*l\s*/\s*r\s*\)")],
        "p5_dicts_sets.html": [("shared mutable memo default", r"def\s+\w+\s*\([^)]*memo\s*=\s*\{\}")],
        "p9_oop_advanced.html": [
            ("claim that the trace is Timsort", r"(?:逐步器|動畫).{0,80}(?:拆開|模擬).{0,30}(?:sorted\(\)|Timsort)"),
            ("false OrderedList-to-UnorderedList inheritance", r"OrderedList\s*繼承\s*UnorderedList"),
        ],
        "00b_setup.html": [
            ("claim that restart deletes installed packages", r"(?:重新啟動|重開).{0,50}(?:套件|pip).{0,20}(?:消失|清掉)"),
        ],
        "searching_sorting.html": [("silent binary-search sorting", r"function\s+buildBinaryFrames[^}]*\.sort\(")],
        "graphs.html": [("unbounded knight trace", r"800000|800_000")],
    }
    for page, patterns in forbidden.items():
        errors.extend(forbid(page, sources.get(page, ""), patterns))

    errors.extend(require(
        "searching_sorting.html",
        sources.get("searching_sorting.html", ""),
        [("explicit unsorted-input rejection", r"不會替你偷偷排序")],
    ))
    errors.extend(require(
        "trees.html",
        sources.get("trees.html", ""),
        [("seeded BST analysis sample", r"sampleSeed.*rngForSeed")],
    ))

    # These long late-chapter traces must remain directly seekable.
    for page, ids in {
        "graphs.html": ["tsScrubber", "sccScrubber"],
        "trees.html": ["heapScrubber", "bstScrubber", "delScrubber"],
        "p9_oop_advanced.html": ["ltSeek"],
        "p5_dicts_sets.html": ["nestedSeek"],
    }.items():
        source = sources.get(page, "")
        for ident in ids:
            if not re.search(rf'\bid="{re.escape(ident)}"', source):
                errors.append(f"{page}: missing scrubber #{ident}")

    print(f"checked {len(sources)} curriculum pages")
    for error in errors:
        print("FAIL", error)
    print(f"\n{len(errors)} visual audit error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
