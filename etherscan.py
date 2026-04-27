import os
import requests

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

def get_contract_source(address):
    url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url).json()

    if response["status"] != "1":
        raise Exception("Failed to fetch contract")

    return response["result"][0]["SourceCode"]
