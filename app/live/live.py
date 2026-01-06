from app.core.models import StockInfo, Stock, StockHistoricalData
from app.data.live_data_fetcher import LiveDataFetcher


def fetch_stock(stock_info: StockInfo, historical_data: dict[str, StockHistoricalData]) -> Stock:
    live_fetcher = LiveDataFetcher()

    company_name = live_fetcher.get_company_name(stock_info.ticker)
    stock_info_with_name = StockInfo(
        ticker=stock_info.ticker,
        category=stock_info.category,
        name=company_name,
    )

    live_data = live_fetcher.fetch(stock_info.ticker)

    history_data = historical_data.get(stock_info.ticker)
    if history_data is None:
        raise ValueError(f"No historical data for {stock_info.ticker}. Run save_historical_data.py first.")

    return Stock(
        info=stock_info_with_name,
        live=live_data,
        history=history_data,
    )
