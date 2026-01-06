from app.core.models import StockLiveData
from app.data.eodhd_client import EODHDClient


class LiveDataFetcher(EODHDClient):
    def fetch(self, ticker: str) -> StockLiveData:
        pass

    def get_company_name(self, ticker: str) -> str:
        pass
