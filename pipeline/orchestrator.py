from scanner.bandit_runner import scn
from parser.parse_results import prs
from db.models import ins

def rn(pth):
    print(f"[START] scanning: {pth}")
    rm = scn(pth)
    print(f"[SCAN DONE] found {len(rm)} raw issues")
    cl = prs(rm)
    print(f"[PARSED] {len(cl)} filtered issues")
    for v in cl:
        ins(v["fl"], v["msg"], v["sv"], v.get("ln", 0), v.get("tid", ""))
    print(f"[STORED] {len(cl)} issues saved")
    return len(cl)
