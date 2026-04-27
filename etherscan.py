import os
import requests
from dotenv import load_dotenv

load_dotenv()
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

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
        raise Exception("No source code found (contract may not be verified)")

    return source_code