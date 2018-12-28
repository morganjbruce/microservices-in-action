from holdings.clients import MarketDataClient


class Holdings(object):
    holdings = [
        {'Code': 'BHP', 'Quantity': 1000},
        {'Code': 'GOOG', 'Quantity': 100},
        {'Code': 'ABC', 'Quantity': 2000}
    ]

    def __init__(self):
        self.market_data = MarketDataClient()

    def all(self):
        prices = self.market_data.all_prices()

        return [self._value(h, prices) for h in self.holdings]

    def _value(self, holding, prices):
        price = next(p for p in prices if p['Code'] == holding['Code'])

        holding['Price'] = price['Price']
        holding['Value'] = holding['Price'] * holding['Quantity']

        return holding
