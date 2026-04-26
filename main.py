import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

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


# 🖥️ Main CLI
def main():
    print("🔎 Smart Contract AI Analyzer\n")

    address = input("Enter contract address: ").strip()

    try:
        print("\n📡 Fetching contract source...")
        code = get_contract_source(address)

        print("🧠 Analyzing with AI...\n")
        result = analyze_contract(code)

        cleaned = clean_json_output(result)

        print("📊 Analysis Result:\n")
        print(cleaned)

    except Exception as e:
        print("❌ Error:", str(e))


if __name__ == "__main__":
    main()