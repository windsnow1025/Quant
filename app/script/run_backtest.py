from datetime import date, timedelta

from app.backtest.analyzer import analyze_backtest
from app.backtest.engine import BacktestEngine
from app.backtest.report import print_backtest_report, plot_equity_curve
from app.core.models import Stock
from app.data.historical_data_storage import load_historical_data
from app.data.watchlist import WATCHLIST


def main():
    historical_data = load_historical_data()

    # Build Stock objects for backtest
    stocks: list[Stock] = []
    for stock_info in WATCHLIST:
        history = historical_data.get(stock_info.ticker)
        if history is None:
            print(f"  Skipping {stock_info.ticker}: no historical data")
            continue
        stocks.append(
            Stock(
                info=stock_info,
                history=history
            )
        )

    print(f"Loaded {len(stocks)} stocks for backtest")

    # Backtest period: last 5 years
    end_date = date.today()
    start_date = end_date - timedelta(days=5 * 365)

    print(f"Backtest period: {start_date} to {end_date}")
    print("Running backtest...")

    engine = BacktestEngine(stocks, start_date, end_date, verbose=True)
    strategy_snapshots, benchmark_snapshots = engine.run()

    print(f"Backtest complete: {len(strategy_snapshots)} trading days")

    # Analyze results
    strategy_metrics = analyze_backtest(strategy_snapshots)
    benchmark_metrics = analyze_backtest(benchmark_snapshots)

    # Print report and plot
    print_backtest_report(strategy_metrics, benchmark_metrics)
    plot_equity_curve(strategy_snapshots, benchmark_snapshots)


if __name__ == "__main__":
    main()
