from etherscan import get_contract_source
from analyzer import detect_vulnerabilities
from config import client

def fetch_contract(address):
    return get_contract_source(address)

def static_analysis(code):
    return detect_vulnerabilities(code)

import time

def ai_analysis(prompt, retries=3):
    models = [
        "nvidia/nemotron-3-super-120b-a12b:free",  # primary
        "google/gemma-3-4b-it:free",               # fallback 1
        "mistralai/mistral-7b-instruct:free",      # fallback 2
        "openai/gpt-oss-120b:free"                 # fallback 3
    ]

    for model in models:
        for i in range(retries):
            try:
                print(f"🤖 Using model: {model}")

                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2
                )

                return response.choices[0].message.content

            except Exception as e:
                print(f"⚠️ Retry {i+1} for {model}... {e}")
                time.sleep(2)

        print(f"❌ Model failed: {model}, switching...")

    raise Exception("❌ All models failed")