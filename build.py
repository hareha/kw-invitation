#!/usr/bin/env python3
"""master.html 하나에서 두 벌을 생성한다.
   index.html      : 일반용 (VIP 페이지 제거)
   vip/index.html  : VIP용  (VIP 페이지 포함, 에셋 경로를 절대경로로)
"""
import re, os, pathlib
src = pathlib.Path("master.html").read_text(encoding="utf-8")

# --- VIP 섹션 범위 찾기
m = re.search(r"\n  <!-- 2\. VIP 귀빈 초청의 글 \(VIP 전용\) -->\n.*?\n  </section>\n", src, re.S)
assert m, "VIP 섹션을 찾지 못했습니다"

# 1) 일반용: VIP 섹션 삭제
general = src[:m.start()] + "\n" + src[m.end():]
pathlib.Path("index.html").write_text(general, encoding="utf-8")

# 2) VIP용: 상대 경로 → 절대 경로 (/vip/ 하위에서도 에셋이 깨지지 않게)
vip = re.sub(r'(["\'(`])(kv/|sponsors/|gallery/|kw-logo\.png|cover\.png)', r'\1/\2', src)
os.makedirs("vip", exist_ok=True)
pathlib.Path("vip/index.html").write_text(vip, encoding="utf-8")

print("index.html     ", len(general), "bytes  (일반용)")
print("vip/index.html ", len(vip), "bytes  (VIP용)")
