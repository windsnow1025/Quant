from datetime import date

from app.backtest.models import DailySnapshot


class Portfolio:
    def __init__(self):
        self.equity: float = 1.0
        self.positions: dict[str, float] = {}  # ticker -> shares
        self.snapshots: list[DailySnapshot] = []

    def rebalance(
            self,
            target_tickers: set[str],
            prices: dict[str, float | None],
            current_date: date,
    ) -> None:
        self._update_equity(prices)
        self.positions.clear()

        valid_tickers = [
            ticker for ticker in target_tickers
            if prices.get(ticker) is not None and prices[ticker] > 0
        ]

        if valid_tickers:
            weight_per_stock = self.equity / len(valid_tickers)
            for ticker in valid_tickers:
                self.positions[ticker] = weight_per_stock / prices[ticker]

        self._append_snapshot(current_date)

    def update_snapshot(self, prices: dict[str, float | None], current_date: date) -> None:
        self._update_equity(prices)
        self._append_snapshot(current_date)

    def _update_equity(self, prices: dict[str, float | None]) -> None:
        if not self.positions:
            return
        total = 0.0
        for ticker, shares in self.positions.items():
            price = prices.get(ticker)
            if price is not None and price > 0:
                total += shares * price
        self.equity = total

    def _append_snapshot(self, current_date: date) -> None:
        self.snapshots.append(DailySnapshot(
            date=current_date,
            equity=self.equity,
            positions=dict(self.positions),
        ))
