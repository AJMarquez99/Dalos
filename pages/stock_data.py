import yfinance as yf

class StockPage(object):

    def __init__(self, ticker: yf.Ticker):
        info = ticker.info
        for key in info:
            setattr(self, key, info[key])

        if "currentPrice" not in ticker.info:
            hist = ticker.history(period='1d')
            hist.reset_index(inplace=True)
            print(hist)
            self.currentPrice = hist['Close'][0]
        
        try:
            self.location = ticker.info['city'] + ", " + ticker.info['state'] + ", " + ticker.info['country']
            self.hasLocation = True
        except:
            self.hasLocation = False

        try:
            self.currentPercentChange = ((ticker.info['currentPrice'] - ticker.info['open'])/ticker.info['open'])*100
        except:
            hist = ticker.history(period='1d')
            hist.reset_index(inplace=True)
            self.currentPercentChange = ((hist['Close'][0] - hist['Open'][0])/hist['Open'][0])*100
        