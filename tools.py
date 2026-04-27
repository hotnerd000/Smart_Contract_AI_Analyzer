from etherscan import get_contract_source
from analyzer import detect_vulnerabilities
from config import client

def fetch_contract(address):
    return get_contract_source(address)

def static_analysis(code):
    return detect_vulnerabilities(code)

def ai_analysis(prompt):
    response = client.chat.completions.create(
        model="google/gemma-3-4b-it:free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content
