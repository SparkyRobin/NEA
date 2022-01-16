import alpaca_trade_api as tradeapi # trading sdk

def instRESTapi(key, secret):

    # instantiate REST API
    api = tradeapi.REST(key, secret, 'https://paper-api.alpaca.markets', api_version='v2')



#def makeTrade(ticker, value):
#def

instRESTapi('PK8RFJYIWKFWKHGXWQNQ', 'ijMCe84JkNIfKDTjPjEl75ytDRe2x1U7TF0rIhlV')