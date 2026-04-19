from datetime import date

from app.core.models import StockDailyData, StockQuarterlyData, StockHistoricalData
from app.core.pit import compute_pit_ev_ebit
from app.data.eodhd_client import EODHDClient
from app.data.yfinance_client import YfinanceClient


class HistoryDataFetcher:
    def __init__(self):
        self.eodhd = EODHDClient()
        self.yfinance = YfinanceClient()

    def fetch(self, ticker: str) -> StockHistoricalData:
        fundamentals = self.eodhd.fetch_fundamentals(ticker)
        quarterly_history = self.eodhd.extract_quarterly_history(fundamentals)
        daily_history = self._build_daily_history(ticker, quarterly_history)

        return StockHistoricalData(
            daily=daily_history,
            quarterly=quarterly_history,
        )

    def _build_daily_history(
            self,
            ticker: str,
            quarterly_history: dict[date, StockQuarterlyData],
    ) -> dict[date, StockDailyData]:
        prices = self.yfinance.fetch_price_history(ticker)
        if not prices:
            return {}

        quarterly_records = sorted(quarterly_history.items())

        daily_data: dict[date, StockDailyData] = {}
        for day, price in prices.items():
            ev_ebit = compute_pit_ev_ebit(day, price, quarterly_records)
            daily_data[day] = StockDailyData(price=price, ev_ebit=ev_ebit)

        return daily_data
