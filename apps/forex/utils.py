from typing import Dict

import requests


def fetch_latest_price(url: str) -> Dict:
    price_response = requests.get(url, timeout=(5, 10))

    return price_response.json()
