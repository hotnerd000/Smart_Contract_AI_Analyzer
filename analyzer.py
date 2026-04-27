def detect_vulnerabilities(code):
    issues = []

    if "call.value" in code:
        issues.append({"type": "Reentrancy Risk", "severity": "high"})

    if "tx.origin" in code:
        issues.append({"type": "tx.origin Usage", "severity": "medium"})

    return issues
