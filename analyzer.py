def detect_vulnerabilities(code):
    issues = []

    code_lower = code.lower()

    # 🔥 Reentrancy (modern pattern)
    if ".call{" in code_lower:
        issues.append({
            "type": "Reentrancy Risk",
            "severity": "high"
        })

    # 🔥 tx.origin usage
    if "tx.origin" in code_lower:
        issues.append({
            "type": "tx.origin Usage",
            "severity": "medium"
        })

    # 🔥 selfdestruct
    if "selfdestruct" in code_lower:
        issues.append({
            "type": "Selfdestruct Usage",
            "severity": "high"
        })

    # 🔥 delegatecall
    if "delegatecall" in code_lower:
        issues.append({
            "type": "Delegatecall Risk",
            "severity": "high"
        })

    return issues