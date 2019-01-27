import logging

import requests


class MarketDataClient(object):

    base_url = 'http://market-data:8000'

    def _make_request(self, url):
        response = requests.get(
            f"{self.base_url}/{url}", headers={'content-type': 'application/json'}, timeout=5)
        return response.json()

    def all_prices(self):
        return self._make_request("prices")

    def price(self, code):
        return self._make_request(f"prices/{code}")
