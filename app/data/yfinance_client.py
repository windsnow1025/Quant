from datetime import date

import yfinance as yf


class YfinanceClient:
    def fetch_price_history(self, ticker: str) -> dict[date, float]:
        ticker_obj = yf.Ticker(ticker)
        hist = ticker_obj.history(period="max")
        if hist.empty:
            return {}
        return {ts.date(): float(hist.loc[ts, 'Close']) for ts in hist.index}

    def fetch_current_price(self, ticker: str) -> float | None:
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info
        for key in ('currentPrice', 'regularMarketPrice'):
            value = info.get(key)
            if isinstance(value, (int, float)):
                return float(value)
        return None
