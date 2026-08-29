#!/usr/bin/env python3
"""把 head.frag + body_<stem>.html + sharedjs.frag + js_<stem>.js 組成完整頁面。"""
import sys, re
from pathlib import Path

SP = Path(__file__).resolve().parent
SITE = Path.home() / "ds-python-selfstudy"

stem, outname, title = sys.argv[1], sys.argv[2], sys.argv[3]

head = (SP / "head.frag").read_text()
head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, count=1, flags=re.S)

body = (SP / f"body_{stem}.html").read_text()
shared = (SP / "sharedjs.frag").read_text()
pagejs_path = SP / f"js_{stem}.js"
pagejs = pagejs_path.read_text() if pagejs_path.exists() else ""

out = f"""{head}<body>

{body}
<script>
{shared}
{pagejs}
</script>
</body>
</html>
"""
(SITE / outname).write_text(out)
print(f"wrote {outname}: {len(out)} bytes")
