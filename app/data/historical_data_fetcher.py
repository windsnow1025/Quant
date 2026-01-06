from app.core.models import StockHistoricalData
from app.data.eodhd_client import EODHDClient


class HistoryDataFetcher(EODHDClient):
    def fetch(self, ticker: str) -> StockHistoricalData:
        pass
