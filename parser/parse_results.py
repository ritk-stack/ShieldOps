def prs(raw):
    flt = []
    for r in raw:
        if isinstance(r, dict):
            sv = r.get("issue_severity", "LOW")
            if sv in ["HIGH", "MEDIUM", "LOW"]:
                flt.append({
                    "fl": r.get("filename", ""),
                    "msg": r.get("issue_text", ""),
                    "sv": sv,
                    "ln": r.get("line_number", 0),
                    "tid": r.get("test_id", "")
                })
    return flt
