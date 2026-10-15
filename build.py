#!/usr/bin/env python3
"""master.html 하나에서 세 벌을 생성한다.
   index.html              : 일반용 (VIP 페이지 제거)          → hareha/kw-invitation
   vip/index.html          : VIP용, 에셋 경로 절대경로         → hareha/kw-invitation 의 /vip/ 경로
   ../광운대-vip/index.html : VIP용, 에셋 경로 그대로(상대)     → hareha/kw-invitation-vip (별도 도메인)
"""
import re, os, shutil, pathlib

ROOT = pathlib.Path(__file__).parent
VIPREPO = ROOT.parent / "광운대-vip"
src = (ROOT / "master.html").read_text(encoding="utf-8")

# --- VIP 섹션 범위 찾기
m = re.search(r"\n  <!-- 2\. VIP 귀빈 초청의 글 \(VIP 전용\) -->\n.*?\n  </section>\n", src, re.S)
assert m, "VIP 섹션을 찾지 못했습니다"

# 1) 일반용: VIP 섹션 삭제
general = src[:m.start()] + "\n" + src[m.end():]
(ROOT / "index.html").write_text(general, encoding="utf-8")

# 2) VIP용(/vip/ 하위): 상대 경로 → 절대 경로
vip_abs = re.sub(r'(["\'(`])(kv/|sponsors/|gallery/|kw-logo\.png|cover\.png)', r'\1/\2', src)
os.makedirs(ROOT / "vip", exist_ok=True)
(ROOT / "vip/index.html").write_text(vip_abs, encoding="utf-8")

# 3) VIP 전용 레포(사이트 루트): 경로 손대지 않음 — 상대 경로가 그대로 맞는다
if VIPREPO.is_dir():
    (VIPREPO / "index.html").write_text(src, encoding="utf-8")
    # 에셋 동기화 (master.html 이 실제로 참조하는 것만)
    for rel in ["kv/poster.jpg", "kw-logo.png", "cover.png"]:
        dst = VIPREPO / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    if (ROOT / "gallery").is_dir():
        shutil.copytree(ROOT / "gallery", VIPREPO / "gallery", dirs_exist_ok=True)
    print("../광운대-vip/index.html", len(src), "bytes  (VIP 전용 레포)")
else:
    print("!! VIP 레포 디렉토리 없음:", VIPREPO)

print("index.html     ", len(general), "bytes  (일반용)")
print("vip/index.html ", len(vip_abs), "bytes  (VIP용 /vip/)")
