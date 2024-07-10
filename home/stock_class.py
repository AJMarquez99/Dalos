from typing import Any, List
from yfinance import Ticker
from pandas import DataFrame

class StockPage(Ticker):

    MINUTES_DATA = ["d", "wk"]

    BREAKS_WEEKLY = [
        dict(bounds=["sat", "mon"])
    ]

    BREAKS_DAILY = [
        dict(bounds=["sat", "mon"]),
        dict(bounds=[17, 9], pattern="hour")
    ]

    BREAKS_DAILY_ALT = [
        dict(bounds=["sat", "mon"]),
        dict(bounds=[16, 9], pattern="hour")
    ]

    def __init__(self, ticker: str, session=None):
        super(StockPage, self).__init__(ticker, session=session)

        try:
            self.location = self.info['city'] + ", " + self.info['state'] + ", " + self.info['country']
            self.hasLocation = True
        except:
            self.hasLocation = False
        
    def isGrowth(self, basePrice: float) -> bool:
        return basePrice < self.currentPrice
    
    def percentChange(self, startingPrice: float) -> float:
        return ((self.currentPrice - startingPrice)/startingPrice)*100
    
    def getCommonDateRange(self, period: str) -> DataFrame:
        match period:
            case "1d":
                interval = "5m"
            case "1wk":
                interval = "30m"
            case "1mo":
                interval = "1h"
            case "5y":
                interval = "1wk"
            case "max":
                interval = "1wk"
            case _:
                interval = "1d"
        return self.history(period=period, interval=interval)
    
    @staticmethod
    def getRangeBreaks(period: str) -> List:
        type = ''.join(filter(str.isalpha, period))

        if period == "1mo":
            return StockPage.BREAKS_DAILY_ALT
        
        match type:
            case "d":
                return StockPage.BREAKS_DAILY
            case "wk":
                return StockPage.BREAKS_DAILY_ALT
            case _:
                return StockPage.BREAKS_WEEKLY

    @staticmethod        
    def inMinutes(period: str) -> bool:
        type = ''.join(filter(str.isalpha, period))
        interval = int(''.join(filter(str.isdigit, period)))

        if type == "mo" and interval == 1:
            return True
        elif type in StockPage.MINUTES_DATA:
            return True
        else:
            return False
        
    def history(self, period: str = "1mo", interval: str = "1d", start: Any | None = None, end: Any | None = None) -> DataFrame:
        df = super().history(period, interval, start, end)
        df.reset_index(inplace=True)
        return df
    
    @property
    def currentPrice(self) -> float:
        try:
            return self.stockInfo.currentPrice
        except:
            return self.history(period='1wk')['Close'][0]
        
    @property
    def stockInfo(self) -> dict:
        return StockInfo(self.info)
    
class StockInfo():

    def __init__(self, info: dict):
        for key in info:
            setattr(self, key, info[key])