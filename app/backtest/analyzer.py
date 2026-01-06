from app.backtest.metrics import (
    calc_total_return,
    calc_annual_return,
    calc_max_drawdown,
    calc_sharpe_ratio,
)
from app.backtest.models import BacktestMetrics, DailySnapshot


def analyze_backtest(snapshots: list[DailySnapshot]) -> BacktestMetrics:
    equity_curve = [snapshot.equity for snapshot in snapshots]
    total_return = calc_total_return(equity_curve)
    return BacktestMetrics(
        total_return=total_return,
        annual_return=calc_annual_return(total_return, len(snapshots)),
        max_drawdown=calc_max_drawdown(equity_curve),
        sharpe_ratio=calc_sharpe_ratio(equity_curve),
    )
