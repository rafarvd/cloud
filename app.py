import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("URL")
wallet = os.getenv("WALLET")
tokens = json.loads(os.getenv("TOKENS_CLOUD"))

x = 0

for token in tokens:
    x += 1
    
    headers = {
        "User-Agent": "Dart/3.3 (dart:io)",
        "Accept-Encoding": "gzip",
        'buildnumber': "126",
        'platform': "android",
        'version': "1.0.126",
        'package': "crypto.bitcoin.ethereum.litecoin.cloud.mining.eth.btc.ltc.hash.pool.cloud_mining",
        "uuid": token["uuid"],
        "uuid-signature": token["uuid-signature"],
        "x-access-token": token["x-access-token"],
        'force-platform': "2",
        "other-uuid": token["other-uuid"],
    }
    
    response = requests.get(f"{url}/mining-contracts", headers=headers)

    if response.status_code == 200:

        # 24 horas
        response = requests.post(f"{url}/daily-reward", headers=headers)

        # 8 horas
        response = requests.post(
            f"{url}/free-mining-contract", headers=headers)

        # Ver Ads 24 horas 4.02 Gh/s
        payload = {
            "ecpm_tier": "FIVE",
        }
        response = requests.post(
            f"{url}/rewarded-mining-contract", data=payload, headers=headers)

        # Sacar
        response = requests.get(url, headers=headers)
        balance = response.json()["btc_balance_in_satoshi_nanos"]
        if balance >= 10000000000:
            payload = {
                'withdrawal_amount_in_nanos': balance,
                'to_address': wallet,
                'network': 'ln',
                'app_check_token': ''
            }
            response = requests.post(
                f"{url}/wallet/withdrawals/request", data=payload, headers=headers)
            print(f"ID: {x} | Sacando: {balance}")
        else:
            print(f"ID: {x} | Saldo insuficiente para saque: {balance}")

    else:
        print("Erro ao acessar a API:")
