from app.core.models import StockHistoricalData
from app.data.historical_data_fetcher import HistoryDataFetcher
from app.data.historical_data_storage import save_historical_data
from app.data.watchlist import WATCHLIST


def main():
    fetcher = HistoryDataFetcher()
    data: dict[str, StockHistoricalData] = {}

    for i, stock_info in enumerate(WATCHLIST, 1):
        ticker = stock_info.ticker
        print(f"[{i}/{len(WATCHLIST)}] Fetching {ticker}...")
        try:
            history = fetcher.fetch(ticker)
            data[ticker] = history
            print(f"  daily: {len(history.daily)}, quarterly: {len(history.quarterly)}")
        except Exception as e:
            print(f"  ERROR: {e}")

    save_historical_data(data)
    print(f"\nSaved {len(data)} tickers to historical_data.pkl")


if __name__ == "__main__":
    main()
