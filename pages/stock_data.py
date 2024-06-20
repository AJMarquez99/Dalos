from typing import Any, Dict, List
from yfinance import Ticker
from pandas import DataFrame

class StockPage(Ticker):

    MINUTE_DATA = ["d", "wk"]

    BREAKS_WEEKLY = [
        dict(bounds=["sat", "mon"])
    ]

    BREAKS_DAILY = [
        dict(bounds=["sat", "mon"]),
        dict(bounds=[17,9], pattern="hour")
    ]

    BREAKS_DAILY_ALT = [
        dict(bounds=["sat", "mon"]),
        dict(bounds=[16,9], pattern="hour")
    ]

    def __init__(self, ticker, session=None):
        super(StockPage, self).__init__(ticker, session=session)
        
        try:
            self.location = ticker.info['city'] + ", " + ticker.info['state'] + ", " + ticker.info['country']
            self.hasLocation = True
        except:
            self.hasLocation = False
        
    def isGrowth(self, basePrice: float) -> bool:
        return basePrice < self.currentPrice
    
    def getPercentageChange(self, startingPrice: float) -> float:
        return ((self.currentPrice - startingPrice)/startingPrice)*100
        
    def getCommonDateRange(self, range: str) -> DataFrame:
        match range:
            case "1d":
                df = self.history(period=range, interval="5m")
            case "1wk":
                df = self.history(period=range, interval="30m")
            case "1mo":
                df = self.history(period=range, interval="1h")
            case "5y":
                df = self.history(period=range, interval="1wk")
            case _:
                df = self.history(period=range, interval="1d")
        return df

    @staticmethod
    def getRangeBreaks(self, range: str) -> List:
        type = ''.join([c for c in range if c.isalpha()])
        match type:
            case "d":
                return self.BREAKS_DAILY
            case "wk":
                return self.BREAKS_DAILY_ALT
            case _:
                return self.BREAKS_WEEKLY

    def inMinutes(self, range: str) -> bool:
        type = ''.join([c for c in range if c.isalpha()])
        interval = int(''.join([c for c in range if c.isnumeric()]))
        
        if type == "mo" and interval == 1:
            return True
        elif type in self.MINUTE_DATA:
            return True
        else: 
            return False
        
    def history(self, period: str = "1mo", interval: str = "1d", start: Any | None = None, end: Any | None = None, prepost: bool = False, actions: bool = True, auto_adjust: bool = True, back_adjust: bool = False, repair: bool = False, keepna: bool = False, proxy: Any | None = None, rounding: bool = False, timeout: int = 10, debug: Any | None = None, raise_errors: bool = False) -> DataFrame:
        df = super().history(period, interval, start, end, prepost, actions, auto_adjust, back_adjust, repair, keepna, proxy, rounding, timeout, debug, raise_errors)
        df.reset_index(inplace=True)
        return df

    @property
    def currentPrice(self) -> float:
        try:
            if self.stockInfo.currentPrice:
                return self.stockInfo.currentPrice
        except:
            hist = self.history(period='1wk')
            return hist['Close'][0]
    
    @property
    def stockInfo(self):
        return StockInfo(self.info)

class StockInfo():

    def __init__(self, info: Dict):
        for key in info:
            setattr(self, key, info[key])