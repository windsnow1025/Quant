from datetime import date

from app.backtest.models import DailySnapshot
from app.backtest.portfolio import Portfolio
from app.core.analyzer import analyze_stock
from app.core.models import Stock


class BacktestEngine:
    def __init__(
            self,
            stocks: list[Stock],
            start_date: date,
            end_date: date,
            verbose: bool = False,
    ):
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date
        self.verbose = verbose
        self.strategy_portfolio = Portfolio()
        self.benchmark_portfolio = Portfolio()

    def run(self) -> tuple[list[DailySnapshot], list[DailySnapshot]]:
        """
        Run backtest and return (strategy_snapshots, benchmark_snapshots).
        """
        trading_days = self._get_trading_days()
        all_tickers = {stock.info.ticker for stock in self.stocks}

        total_days = len(trading_days)
        for i, current_date in enumerate(trading_days):
            if self.verbose and i % 50 == 0:
                print(f"  [{i}/{total_days}] {current_date}")

            prices = self._get_prices(current_date)

            # Strategy: rebalance to stocks passing all signals
            target_tickers = self._get_target_tickers(current_date)
            self.strategy_portfolio.rebalance(target_tickers, prices, current_date)

            # Benchmark: buy on day 1, then just hold
            if i == 0:
                self.benchmark_portfolio.rebalance(all_tickers, prices, current_date)
            else:
                self.benchmark_portfolio.update_snapshot(prices, current_date)

        if self.verbose:
            print(f"  [{total_days}/{total_days}] Done")

        return (
            self.strategy_portfolio.snapshots,
            self.benchmark_portfolio.snapshots,
        )

    def _get_trading_days(self) -> list[date]:
        """Get all trading days in the backtest period."""
        all_dates: set[date] = set()
        for stock in self.stocks:
            for day in stock.history.daily.keys():
                if self.start_date <= day <= self.end_date:
                    all_dates.add(day)
        return sorted(all_dates)

    def _get_prices(self, current_date: date) -> dict[str, float | None]:
        """Get prices for all stocks on a given date."""
        prices: dict[str, float | None] = {}
        for stock in self.stocks:
            daily = stock.history.daily.get(current_date)
            prices[stock.info.ticker] = daily.price if daily else None
        return prices

    def _get_target_tickers(self, current_date: date) -> set[str]:
        """Get tickers that pass all signals on a given date."""
        target_tickers: set[str] = set()
        for stock in self.stocks:
            analysis = analyze_stock(stock, target_date=current_date)
            if analysis.signals.all_signals_pass:
                target_tickers.add(stock.info.ticker)
        return target_tickers
