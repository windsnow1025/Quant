import matplotlib.pyplot as plt

from app.backtest.models import BacktestMetrics, DailySnapshot


def print_backtest_report(
        strategy_metrics: BacktestMetrics,
        benchmark_metrics: BacktestMetrics,
) -> None:
    print(f"\n{'Metric':<13} | {'Strategy':>8} | {'Benchmark':>8}")
    print(f"{'-' * 13}-+-{'-' * 8}-+-{'-' * 8}")

    _print_metric_row("Total Return", strategy_metrics.total_return, benchmark_metrics.total_return, is_pct=True)
    _print_metric_row("Annual Return", strategy_metrics.annual_return, benchmark_metrics.annual_return, is_pct=True)
    _print_metric_row("Max Drawdown", strategy_metrics.max_drawdown, benchmark_metrics.max_drawdown, is_pct=True)
    _print_metric_row("Sharpe Ratio", strategy_metrics.sharpe_ratio, benchmark_metrics.sharpe_ratio, is_pct=False)

    excess_return = strategy_metrics.total_return - benchmark_metrics.total_return
    if excess_return > 0:
        print(f"\n📈 Strategy outperformed by {excess_return:+.2%}")
    elif excess_return < 0:
        print(f"\n📉 Strategy underperformed by {excess_return:+.2%}")


def _print_metric_row(label: str, strategy_val: float, benchmark_val: float, is_pct: bool) -> None:
    if is_pct:
        s_str = f"{strategy_val:+.2%}"
        b_str = f"{benchmark_val:+.2%}"
    else:
        s_str = f"{strategy_val:.2f}"
        b_str = f"{benchmark_val:.2f}"
    print(f"{label:<13} | {s_str:>8} | {b_str:>8}")


def plot_equity_curve(
        strategy_snapshots: list[DailySnapshot],
        benchmark_snapshots: list[DailySnapshot],
) -> None:
    dates = [s.date for s in strategy_snapshots]
    strategy_equity = [s.equity for s in strategy_snapshots]
    benchmark_equity = [b.equity for b in benchmark_snapshots]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, strategy_equity, label="Strategy", linewidth=1.5)
    plt.plot(dates, benchmark_equity, label="Benchmark", linewidth=1.5, alpha=0.7)
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.yscale("log")
    plt.title("Backtest: Strategy vs Benchmark")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
