from datetime import date

from app.core.models import StockLiveData
from app.core.pit import compute_pit_ev_ebit
from app.data.eodhd_client import EODHDClient
from app.data.yfinance_client import YfinanceClient


class LiveDataFetcher:
    def __init__(self):
        self.eodhd = EODHDClient()
        self.yfinance = YfinanceClient()

    def fetch(self, ticker: str) -> StockLiveData:
        price = self.yfinance.fetch_current_price(ticker)
        fundamentals = self.eodhd.fetch_fundamentals(ticker)
        quarterly_history = self.eodhd.extract_quarterly_history(fundamentals)
        quarterly_records = sorted(quarterly_history.items())
        ev_ebit = (
            compute_pit_ev_ebit(date.today(), price, quarterly_records)
            if price is not None else None
        )
        return StockLiveData(price=price, ev_ebit=ev_ebit)

    def fetch_company_name(self, ticker: str) -> str:
        return self.eodhd.fetch_company_name(ticker)
