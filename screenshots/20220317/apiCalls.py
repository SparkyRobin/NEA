import alpaca_trade_api as tradeapi # trading sdk

#def instRESTapi(key, secret):

    # instantiate REST API
#api = tradeapi.REST('PK8RFJYIWKFWKHGXWQNQ', 'ijMCe84JkNIfKDTjPjEl75ytDRe2x1U7TF0rIhlV', 'https://paper-api.alpaca.markets', api_version='v2')

class conApi():

    def __init__(self, key, secret):
        self.api = tradeapi.REST(key, secret, 'https://paper-api.alpaca.markets', api_version='v2')
        self.positionsSorted = {}

    def positions(self):
        self.positions = self.api.list_positions()
        for ticker in self.positions:
            self.positionsSorted[ticker.symbol] = [ticker.current_price, ticker.market_value, ticker.qty]
            self.positionsSorted['sam'] = [ticker.current_price, ticker.market_value, ticker.qty]
        return(self.positionsSorted)

wal = conApi('PK8RFJYIWKFWKHGXWQNQ', 'ijMCe84JkNIfKDTjPjEl75ytDRe2x1U7TF0rIhlV')
print(list(wal.positions().keys()))