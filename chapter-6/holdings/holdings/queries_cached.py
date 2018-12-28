import logging

import requests
from cachetools import TTLCache, cached


class MarketDataClient(object):
    logger = logging.getLogger(__name__)
    cache = TTLCache(maxsize=10, ttl=5*60)
    base_url = 'http://market-data:8000'

    def _make_request(self, url):
        response = requests.get(
            f"{self.base_url}/{url}", headers={'content-type': 'application/json'})
        return response.json()

    @cached(cache)
    def all_prices(self):
        self.logger.debug("Making request to get all_prices")
        return self._make_request("prices")

    def price(self, code):
        return self._make_request(f"prices/{code}")
