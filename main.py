import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
import re

# Load env variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

# Setup OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# 🔍 Fetch contract source code from Etherscan
def get_contract_source(address):
    url = "https://api.etherscan.io/v2/api"

    params = {
        "chainid": "1",  # Ethereum mainnet
        "module": "contract",
        "action": "getsourcecode",
        "address": address,
        "apikey": ETHERSCAN_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "1":
        raise Exception(f"Etherscan error: {data.get('message')}")

    result = data["result"][0]
    source_code = result.get("SourceCode")

    if not source_code:
        raise Exception("No source code found (contract not verified)")

    return source_code


# 🤖 AI analysis
def analyze_contract(code):
    prompt = f"""
You are a smart contract security auditor.

Analyze this Solidity contract and return ONLY valid JSON:

{{
  "risk_score": number (0-10),
  "summary": "",
  "vulnerabilities": [],
  "severity": "low | medium | high",
  "recommendations": []
}}

Focus on:
- Reentrancy
- Access control
- Integer overflow/underflow
- Unsafe external calls

Contract Code:
{code[:12000]}
"""

    response = client.chat.completions.create(
        model="google/gemma-3-4b-it:free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content


# 🧼 Clean AI output
def clean_json_output(raw):
    raw = raw.replace("```json", "").replace("```", "").strip()
    return raw

def detect_vulnerabilities(code: str):
    issues = []

    # 🔴 Reentrancy (very important)
    if re.search(r"\.call\{value:.*\}", code):
        issues.append({
            "type": "Reentrancy Risk",
            "severity": "high",
            "detail": "Use of low-level call with value transfer"
        })

    # 🔴 Missing access control
    if "onlyOwner" not in code and "require(msg.sender" not in code:
        issues.append({
            "type": "Access Control",
            "severity": "medium",
            "detail": "No clear ownership restriction"
        })

    # 🔴 tx.origin usage (bad practice)
    if "tx.origin" in code:
        issues.append({
            "type": "Phishing Risk",
            "severity": "high",
            "detail": "Use of tx.origin is unsafe"
        })

    # 🔴 Selfdestruct
    if "selfdestruct" in code:
        issues.append({
            "type": "Self Destruct",
            "severity": "high",
            "detail": "Contract can be destroyed"
        })

    # 🟡 Integer overflow (for older Solidity)
    if "SafeMath" not in code and "pragma solidity ^0.8" not in code:
        issues.append({
            "type": "Overflow Risk",
            "severity": "medium",
            "detail": "No SafeMath or Solidity >=0.8"
        })
    #   Delegatecall
    if "delegatecall" in code:
        issues.append({
            "type": "Delegatecall Risk",
            "severity": "high",
            "detail": "delegatecall can execute external code"
        })

    return issues

def calculate_risk_score(issues):
    score = 0

    for issue in issues:
        if issue["severity"] == "high":
            score += 3
        elif issue["severity"] == "medium":
            score += 2
        else:
            score += 1

    return min(score, 10)

def build_prompt(code, detected_issues):
    return f"""
You are a professional smart contract auditor.

Known detected issues:
{detected_issues}

Analyze the contract deeper and return JSON:

{{
  "ai_additional_risks": [],
  "explanation": "",
  "recommendations": []
}}

Contract:
{code[:10000]}
"""

def analyze(code):
    static_issues = detect_vulnerabilities(code)
    score = calculate_risk_score(static_issues)

    prompt = build_prompt(code, static_issues)

    ai_response = client.chat.completions.create(
        model="google/gemma-3-4b-it:free",
        messages=[{"role": "user", "content": prompt}],
    )

    return {
        "risk_score": score,
        "static_issues": static_issues,
        "ai_analysis": ai_response.choices[0].message.content
    }

# 🖥️ Main CLI
def main():
    print("\n🔎 Smart Contract AI Analyzer\n")

    address = input("Enter contract address: ").strip()

    try:
        print("\n📡 Fetching contract source...")
        code = get_contract_source(address)

        print("🧠 Running static analysis...")
        static_issues = detect_vulnerabilities(code)

        risk_score = calculate_risk_score(static_issues)

        print("🤖 Running AI analysis...")
        prompt = build_prompt(code, static_issues)

        ai_response = client.chat.completions.create(
            model="google/gemma-3-4b-it:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        raw_ai = ai_response.choices[0].message.content
        cleaned_ai = raw_ai.replace("```json", "").replace("```", "").strip()

        # 🎨 Pretty output
        print("\n" + "="*50)

        # 🔴 Risk Score with color
        if risk_score >= 7:
            color = "\033[91m"   # red
            level = "HIGH"
        elif risk_score >= 4:
            color = "\033[93m"   # yellow
            level = "MEDIUM"
        else:
            color = "\033[92m"   # green
            level = "LOW"

        print(f"{color}🚨 Risk Score: {risk_score}/10 ({level})\033[0m\n")

        # ⚠️ Static Issues
        print("⚠️ Detected Issues:")
        if not static_issues:
            print("  ✅ No obvious issues found")
        else:
            for issue in static_issues:
                print(f"  - {issue['type']} ({issue['severity']})")
                print(f"    → {issue['detail']}")

        # 🤖 AI Analysis
        print("\n🧠 AI Insights:")
        print(cleaned_ai)

        print("="*50 + "\n")

    except Exception as e:
        print("\n❌ Error:", str(e))


if __name__ == "__main__":
    main()