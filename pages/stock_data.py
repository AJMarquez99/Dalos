import yfinance as yf

class StockPage(object):

    def __init__(self, ticker: yf.Ticker):
        info = ticker.info

        
        hist = ticker.history(period='1d')
        hist.reset_index(inplace=True)
        
        for key in info:
            setattr(self, key, info[key])

        if "currentPrice" not in ticker.info:
            self.currentPrice = hist['Close'][0]
        
        try:
            self.location = ticker.info['city'] + ", " + ticker.info['state'] + ", " + ticker.info['country']
            self.hasLocation = True
        except:
            self.hasLocation = False

        try:
            self.currentPercentChange = ((ticker.info['currentPrice'] - ticker.info['open'])/ticker.info['open'])*100
        except:
            self.currentPercentChange = ((hist['Close'][0] - hist['Open'][0])/hist['Open'][0])*100
        
    def isGrowth(self, basePrice: float) -> bool:
        return basePrice < self.currentPrice
    
    def percentChange(self, startingPrice: float) -> float:
        return ((self.currentPrice - startingPrice)/startingPrice)*100